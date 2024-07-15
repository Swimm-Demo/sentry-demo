---
title: Webhook Flow in Sentry
---
## Overview

The `send_resource_change_webhook` function is a key part of the webhook flow in Sentry. It is responsible for notifying external services about changes in resources. The function initiates a series of actions that involve sending the webhook, recording the response, and handling any errors or timeouts that may occur during the process.

<SwmSnippet path="/src/sentry/tasks/sentry_apps.py" line="318">

---

## Sending Webhooks

The `send_resource_change_webhook` function is the entry point for the webhook flow. It retrieves the installation by its ID and if it exists, it triggers the `send_webhooks` function with the installation, event, and data as parameters.

```python
def send_resource_change_webhook(installation_id, event, data, *args, **kwargs):
    installation = app_service.installation_by_id(id=installation_id)
    if not installation:
        logger.info(
            "send_process_resource_change_webhook.missing_installation",
            extra={"installation_id": installation_id, "event": event},
        )
        return

    send_webhooks(installation, event, data=data)

    metrics.incr("resource_change.processed", sample_rate=1.0, tags={"change_event": event})
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/sentry_apps.py" line="360">

---

The `send_webhooks` function retrieves the service hook associated with the installation. If the service hook exists and the event is within the allowed events, it prepares the request data and calls the `send_and_save_webhook_request` function.

```python
def send_webhooks(installation, event, **kwargs):
    try:
        servicehook = ServiceHook.objects.get(
            organization_id=installation.organization_id, actor_id=installation.id
        )
    except ServiceHook.DoesNotExist:
        logger.info(
            "send_webhooks.missing_servicehook",
            extra={"installation_id": installation.id, "event": event},
        )
        return

    if event not in servicehook.events:
        return

    # The service hook applies to all projects if there are no
    # ServiceHookProject records. Otherwise we want check if
    # the event is within the allowed projects.
    project_limited = ServiceHookProject.objects.filter(service_hook_id=servicehook.id).exists()

    # TODO(nola): This is disabled for now, because it could potentially affect internal integrations w/ error.created
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/sentry_apps/webhooks.py" line="116">

---

## Recording Responses and Handling Errors

The `send_and_save_webhook_request` function sends the webhook request and logs the response. In case of a timeout or connection error, it records the timeout and re-raises the exception. If the response status code indicates an error, it raises the corresponding error. If the action is not 'event.alert', it records the response for disabling integration.

```python
def send_and_save_webhook_request(
    sentry_app: SentryApp | RpcSentryApp,
    app_platform_event: AppPlatformEvent,
    url: str | None = None,
) -> Response:
    """
    Notify a SentryApp's webhook about an incident and log response on redis.

    :param sentry_app: The SentryApp to notify via a webhook.
    :param app_platform_event: Incident data. See AppPlatformEvent.
    :param url: The URL to hit for this webhook if it is different from `sentry_app.webhook_url`.
    :return: Webhook response
    """
    buffer = SentryAppWebhookRequestsBuffer(sentry_app)

    org_id = app_platform_event.install.organization_id
    event = f"{app_platform_event.resource}.{app_platform_event.action}"
    slug = sentry_app.slug_for_metrics
    url = url or sentry_app.webhook_url
    assert url is not None

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/sentry_apps/webhooks.py" line="82">

---

The `record_timeout` function records the timeout or connection error in the integration buffer to check if the integration is broken and should be disabled.

```python
def record_timeout(
    sentryapp: SentryApp | RpcSentryApp, org_id: str, e: ConnectionError | Timeout
) -> None:
    """
    Record Unpublished Sentry App timeout or connection error in integration buffer to check if it is broken and should be disabled
    """
    if not sentryapp.is_internal:
        return
    redis_key = get_redis_key(sentryapp, org_id)
    if not len(redis_key):
        return
    buffer = IntegrationRequestBuffer(redis_key)
    buffer.record_timeout()
    check_broken(sentryapp, org_id)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/sentry_apps/webhooks.py" line="98">

---

The `record_response_for_disabling_integration` function is used to record the response of a webhook request. If the response indicates an error, it records the error and calls the `check_broken` function to check if the integration is broken.

```python
def record_response_for_disabling_integration(
    sentryapp: SentryApp | RpcSentryApp, org_id: str, response: Response
) -> None:
    if not sentryapp.is_internal:
        return
    redis_key = get_redis_key(sentryapp, org_id)
    if not len(redis_key):
        return
    buffer = IntegrationRequestBuffer(redis_key)
    if is_response_success(response):
        buffer.record_success()
        return
    if is_response_error(response):
        buffer.record_error()
        check_broken(sentryapp, org_id)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/sentry_apps/webhooks.py" line="53">

---

The `check_broken` function checks if the integration is broken by using the `IntegrationRequestBuffer`. If the integration is broken, it disables the Sentry app and notifies about the disabling by calling the `notify_disable` function.

```python
def check_broken(sentryapp: SentryApp | RpcSentryApp, org_id: str) -> None:
    from sentry.sentry_apps.services.app.service import app_service

    redis_key = get_redis_key(sentryapp, org_id)
    buffer = IntegrationRequestBuffer(redis_key)
    if buffer.is_integration_broken():
        org = Organization.objects.get(id=org_id)
        app_service.disable_sentryapp(id=sentryapp.id)
        notify_disable(org, sentryapp.name, redis_key, sentryapp.slug, sentryapp.webhook_url)
        buffer.clear()
        create_system_audit_entry(
            organization=org,
            target_object=org.id,
            event=audit_log.get_event_id("INTERNAL_INTEGRATION_DISABLED"),
            data={"name": sentryapp.name},
        )
        extra = {
            "sentryapp_webhook": sentryapp.webhook_url,
            "sentryapp_slug": sentryapp.slug,
            "sentryapp_uuid": sentryapp.uuid,
            "org_id": org_id,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/integrations/notify_disable.py" line="42">

---

## Notifying about Disabled Integration

The `notify_disable` function is used to notify the owners of the organization about the disabled integration. It creates a message with the necessary context and sends it asynchronously.

```python
def notify_disable(
    organization: RpcOrganization | Organization,
    integration_name: str,
    redis_key: str,
    integration_slug: str | None = None,
    webhook_url: str | None = None,
    project: str | None = None,
):

    integration_link = get_url(
        organization,
        get_provider_type(redis_key),
        integration_slug if "sentry-app" in redis_key and integration_slug else integration_name,
    )

    referrer = (
        "?referrer=disabled-sentry-app"
        if "sentry-app" in redis_key
        else "?referrer=disabled-integration"
    )

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/email/message_builder.py" line="232">

---

The `send_async` function is used to send the email notification asynchronously. It builds the messages and sends them using the `send_email` task.

```python
    def send_async(
        self,
        to: Iterable[str] | None = None,
        cc: Sequence[str] | None = None,
        bcc: Sequence[str] | None = None,
    ) -> None:
        from sentry.tasks.email import send_email, send_email_control

        fmt = options.get("system.logging-format")
        messages = self.get_built_messages(to, cc=cc, bcc=bcc)
        extra: MutableMapping[str, str | tuple[str]] = {"message_type": self.type}
        loggable = [v for k, v in self.context.items() if hasattr(v, "id")]
        for context in loggable:
            extra[f"{type(context).__name__.lower()}_id"] = context.id

        log_mail_queued = partial(logger.info, "mail.queued", extra=extra)
        for message in messages:
            send_email_task = send_email.delay
            if SiloMode.get_current_mode() == SiloMode.CONTROL:
                send_email_task = send_email_control.delay
            safe_execute(send_email_task, message=message)
```

---

</SwmSnippet>

```mermaid
graph TD;
subgraph src/sentry
  send_resource_change_webhook:::mainFlowStyle --> send_webhooks:::mainFlowStyle
end
subgraph src/sentry/utils
  send_webhooks:::mainFlowStyle --> send_and_save_webhook_request:::mainFlowStyle
end
subgraph src/sentry/utils
  send_and_save_webhook_request:::mainFlowStyle --> record_timeout
end
subgraph src/sentry/utils
  send_and_save_webhook_request:::mainFlowStyle --> record_response_for_disabling_integration:::mainFlowStyle
end
subgraph src/sentry/utils
  record_response_for_disabling_integration:::mainFlowStyle --> check_broken:::mainFlowStyle
end
subgraph src/sentry
  check_broken:::mainFlowStyle --> notify_disable:::mainFlowStyle
end
subgraph src/sentry/utils
  notify_disable:::mainFlowStyle --> send_async:::mainFlowStyle
end
subgraph src/sentry/utils
  send_async:::mainFlowStyle --> incr
end

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

# Flow drill down

First, we'll zoom into this section of the flow:

```mermaid
graph TD;
subgraph src/sentry
  send_resource_change_webhook:::mainFlowStyle --> send_webhooks:::mainFlowStyle
end
subgraph src/sentry
  send_webhooks:::mainFlowStyle --> send_and_save_webhook_request:::mainFlowStyle
end
subgraph src/sentry
  send_and_save_webhook_request:::mainFlowStyle --> record_timeout
end
subgraph src/sentry
  send_and_save_webhook_request:::mainFlowStyle --> record_response_for_disabling_integration:::mainFlowStyle
end
subgraph src/sentry
  record_response_for_disabling_integration:::mainFlowStyle --> zgdaj[...]
end

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

<SwmSnippet path="/src/sentry/tasks/sentry_apps.py" line="318">

---

# send_resource_change_webhook

The `send_resource_change_webhook` function is the entry point for the webhook flow. It retrieves the installation by its ID and if it exists, it triggers the `send_webhooks` function with the installation, event, and data as parameters.

```python
def send_resource_change_webhook(installation_id, event, data, *args, **kwargs):
    installation = app_service.installation_by_id(id=installation_id)
    if not installation:
        logger.info(
            "send_process_resource_change_webhook.missing_installation",
            extra={"installation_id": installation_id, "event": event},
        )
        return

    send_webhooks(installation, event, data=data)

    metrics.incr("resource_change.processed", sample_rate=1.0, tags={"change_event": event})
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/sentry_apps.py" line="360">

---

# send_webhooks

The `send_webhooks` function retrieves the service hook associated with the installation. If the service hook exists and the event is within the allowed events, it prepares the request data and calls the `send_and_save_webhook_request` function.

```python
def send_webhooks(installation, event, **kwargs):
    try:
        servicehook = ServiceHook.objects.get(
            organization_id=installation.organization_id, actor_id=installation.id
        )
    except ServiceHook.DoesNotExist:
        logger.info(
            "send_webhooks.missing_servicehook",
            extra={"installation_id": installation.id, "event": event},
        )
        return

    if event not in servicehook.events:
        return

    # The service hook applies to all projects if there are no
    # ServiceHookProject records. Otherwise we want check if
    # the event is within the allowed projects.
    project_limited = ServiceHookProject.objects.filter(service_hook_id=servicehook.id).exists()

    # TODO(nola): This is disabled for now, because it could potentially affect internal integrations w/ error.created
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/sentry_apps/webhooks.py" line="116">

---

# send_and_save_webhook_request

The `send_and_save_webhook_request` function sends the webhook request and logs the response. In case of a timeout or connection error, it records the timeout and re-raises the exception. If the response status code indicates an error, it raises the corresponding error. If the action is not 'event.alert', it records the response for disabling integration.

```python
def send_and_save_webhook_request(
    sentry_app: SentryApp | RpcSentryApp,
    app_platform_event: AppPlatformEvent,
    url: str | None = None,
) -> Response:
    """
    Notify a SentryApp's webhook about an incident and log response on redis.

    :param sentry_app: The SentryApp to notify via a webhook.
    :param app_platform_event: Incident data. See AppPlatformEvent.
    :param url: The URL to hit for this webhook if it is different from `sentry_app.webhook_url`.
    :return: Webhook response
    """
    buffer = SentryAppWebhookRequestsBuffer(sentry_app)

    org_id = app_platform_event.install.organization_id
    event = f"{app_platform_event.resource}.{app_platform_event.action}"
    slug = sentry_app.slug_for_metrics
    url = url or sentry_app.webhook_url
    assert url is not None

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/sentry_apps/webhooks.py" line="82">

---

# record_timeout

The `record_timeout` function records the timeout or connection error in the integration buffer to check if the integration is broken and should be disabled.

```python
def record_timeout(
    sentryapp: SentryApp | RpcSentryApp, org_id: str, e: ConnectionError | Timeout
) -> None:
    """
    Record Unpublished Sentry App timeout or connection error in integration buffer to check if it is broken and should be disabled
    """
    if not sentryapp.is_internal:
        return
    redis_key = get_redis_key(sentryapp, org_id)
    if not len(redis_key):
        return
    buffer = IntegrationRequestBuffer(redis_key)
    buffer.record_timeout()
    check_broken(sentryapp, org_id)
```

---

</SwmSnippet>

Now, lets zoom into this section of the flow:

```mermaid
graph TD;
subgraph src/sentry/utils
  record_response_for_disabling_integration:::mainFlowStyle --> check_broken:::mainFlowStyle
end
subgraph src/sentry/integrations/notify_disable.py
  check_broken:::mainFlowStyle --> notify_disable:::mainFlowStyle
end
subgraph src/sentry/utils
  notify_disable:::mainFlowStyle --> send_async:::mainFlowStyle
end

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

<SwmSnippet path="/src/sentry/utils/sentry_apps/webhooks.py" line="98">

---

## Recording Response for Disabling Integration

The `record_response_for_disabling_integration` function is used to record the response of a webhook request. If the response indicates an error, it records the error and calls the `check_broken` function to check if the integration is broken.

```python
def record_response_for_disabling_integration(
    sentryapp: SentryApp | RpcSentryApp, org_id: str, response: Response
) -> None:
    if not sentryapp.is_internal:
        return
    redis_key = get_redis_key(sentryapp, org_id)
    if not len(redis_key):
        return
    buffer = IntegrationRequestBuffer(redis_key)
    if is_response_success(response):
        buffer.record_success()
        return
    if is_response_error(response):
        buffer.record_error()
        check_broken(sentryapp, org_id)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/sentry_apps/webhooks.py" line="53">

---

## Checking if Integration is Broken

The `check_broken` function checks if the integration is broken by using the `IntegrationRequestBuffer`. If the integration is broken, it disables the Sentry app and notifies about the disabling by calling the `notify_disable` function.

```python
def check_broken(sentryapp: SentryApp | RpcSentryApp, org_id: str) -> None:
    from sentry.sentry_apps.services.app.service import app_service

    redis_key = get_redis_key(sentryapp, org_id)
    buffer = IntegrationRequestBuffer(redis_key)
    if buffer.is_integration_broken():
        org = Organization.objects.get(id=org_id)
        app_service.disable_sentryapp(id=sentryapp.id)
        notify_disable(org, sentryapp.name, redis_key, sentryapp.slug, sentryapp.webhook_url)
        buffer.clear()
        create_system_audit_entry(
            organization=org,
            target_object=org.id,
            event=audit_log.get_event_id("INTERNAL_INTEGRATION_DISABLED"),
            data={"name": sentryapp.name},
        )
        extra = {
            "sentryapp_webhook": sentryapp.webhook_url,
            "sentryapp_slug": sentryapp.slug,
            "sentryapp_uuid": sentryapp.uuid,
            "org_id": org_id,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/integrations/notify_disable.py" line="42">

---

## Notifying about Disabled Integration

The `notify_disable` function is used to notify the owners of the organization about the disabled integration. It creates a message with the necessary context and sends it asynchronously.

```python
def notify_disable(
    organization: RpcOrganization | Organization,
    integration_name: str,
    redis_key: str,
    integration_slug: str | None = None,
    webhook_url: str | None = None,
    project: str | None = None,
):

    integration_link = get_url(
        organization,
        get_provider_type(redis_key),
        integration_slug if "sentry-app" in redis_key and integration_slug else integration_name,
    )

    referrer = (
        "?referrer=disabled-sentry-app"
        if "sentry-app" in redis_key
        else "?referrer=disabled-integration"
    )

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/email/message_builder.py" line="232">

---

## Sending Email Asynchronously

The `send_async` function is used to send the email notification asynchronously. It builds the messages and sends them using the `send_email` task.

```python
    def send_async(
        self,
        to: Iterable[str] | None = None,
        cc: Sequence[str] | None = None,
        bcc: Sequence[str] | None = None,
    ) -> None:
        from sentry.tasks.email import send_email, send_email_control

        fmt = options.get("system.logging-format")
        messages = self.get_built_messages(to, cc=cc, bcc=bcc)
        extra: MutableMapping[str, str | tuple[str]] = {"message_type": self.type}
        loggable = [v for k, v in self.context.items() if hasattr(v, "id")]
        for context in loggable:
            extra[f"{type(context).__name__.lower()}_id"] = context.id

        log_mail_queued = partial(logger.info, "mail.queued", extra=extra)
        for message in messages:
            send_email_task = send_email.delay
            if SiloMode.get_current_mode() == SiloMode.CONTROL:
                send_email_task = send_email_control.delay
            safe_execute(send_email_task, message=message)
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
