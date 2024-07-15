---
title: Overview of Notification System
---
Notifications in Sentry-demo refer to the system's way of alerting users about different activities or events within the application. They are implemented through various classes, each representing a specific type of notification.

These classes include `ActivityNotification`, `NoteActivityNotification`, `EscalatingActivityNotification`, `RegressionActivityNotification`, `ReleaseActivityNotification`, and others. Each class represents a specific type of activity that triggers a notification.

The `get_notification_title` function is used to generate the title for the notification. This function is used in different parts of the application, such as in the Slack and MS Teams integrations, to provide the subject line for chat notifications.

The `BaseNotification` class serves as the base for all notification types. It defines the basic structure and common methods for all notifications. Other notification classes extend this base class to provide specific functionality.

The `notification_providers` function is used to limit notifications to specific providers. This allows the system to control where notifications are sent.

<SwmSnippet path="/src/sentry/notifications/notifications/activity/__init__.py" line="16">

---

# Notification Classes

Here we define different types of notifications. Each type is represented by a class, such as `ResolvedActivityNotification`, `RegressionActivityNotification`, `NoteActivityNotification`, etc. These classes are used to generate specific types of notifications.

```python
EMAIL_CLASSES_BY_TYPE: dict[int, type[ActivityNotification]] = {
    ActivityType.SET_RESOLVED.value: ResolvedActivityNotification,
    ActivityType.SET_REGRESSION.value: RegressionActivityNotification,
    ActivityType.NOTE.value: NoteActivityNotification,
    ActivityType.ASSIGNED.value: AssignedActivityNotification,
    ActivityType.UNASSIGNED.value: UnassignedActivityNotification,
    ActivityType.SET_RESOLVED_IN_RELEASE.value: ResolvedInReleaseActivityNotification,
    ActivityType.DEPLOY.value: ReleaseActivityNotification,
    ActivityType.SET_ESCALATING.value: EscalatingActivityNotification,
}
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/notifications/notifications/base.py" line="275">

---

# Sending Notifications

The `send` function is the main function responsible for sending notifications. It first gets the participants who should receive the notification, then it gets the context for the notification, and finally, it sends the notification to each provider (like email, slack, etc.) for each recipient.

```python
    def send(self) -> None:
        """The default way to send notifications that respects Notification Settings."""
        from sentry.notifications.notify import notify

        with sentry_sdk.start_span(op="notification.send", description="get_participants"):
            participants_by_provider = self.get_participants()
            if not participants_by_provider:
                return

        context = self.get_context()
        for provider, recipients in participants_by_provider.items():
            with sentry_sdk.start_span(op="notification.send", description=f"send_for_{provider}"):
                safe_execute(notify, provider, self, recipients, context)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/notifications/notifications/base.py" line="106">

---

# Notification Title

The `get_notification_title` function is used to generate the title for the notification. This function is used in different parts of the application, such as in the Slack and MS Teams integrations, to provide the subject line for chat notifications.

```python
    def get_notification_title(
        self, provider: ExternalProviders, context: Mapping[str, Any] | None = None
    ) -> str:
        """The subject line when sending this notifications as a chat notification."""
        raise NotImplementedError
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/notifications/notifications/base.py" line="238">

---

# Notification Providers

The `get_notification_providers` function is used to limit notifications to specific providers. This allows the system to control where notifications are sent.

```python
    def get_notification_providers(self) -> Iterable[ExternalProviders]:
        # subclass this method to limit notifications to specific providers
        from sentry.notifications.notify import notification_providers

        return notification_providers()
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
