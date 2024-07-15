---
title: Exploring the Notification System
---
Notifications in Sentry are a way to inform users about different activities and events happening within the application. They are implemented as a series of classes, each representing a different type of notification.

These classes are organized in the 'notifications' directory, with each subdirectory and file representing a different type of notification. For example, 'activity' notifications are related to user activities, while 'rules' notifications are triggered by specific rules set within the application.

Each notification class, such as 'ActivityNotification' or 'UserReportNotification', represents a specific type of notification and contains the logic for how that notification should be handled.

The 'EMAIL_CLASSES_BY_TYPE' dictionary in the 'activity' module maps different activity types to their corresponding notification classes. This allows the application to easily determine which class to use for a given activity type.

In addition to these specific notification classes, there are also base classes like 'BaseNotification' and 'ProjectNotification' that provide common functionality for all notifications.

# Notification Classes

Each notification class, such as 'ActivityNotification' or 'UserReportNotification', represents a specific type of notification and contains the logic for how that notification should be handled.

<SwmSnippet path="/src/sentry/notifications/notifications/base.py" line="275">

---

# Sending Notifications

Notifications are sent by calling the 'send' method of the relevant notification class. This method gathers the necessary context, determines the recipients, and then sends the notification.

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

<SwmSnippet path="/src/sentry/notifications/notifications/base.py" line="238">

---

# Notification Providers

The 'get_notification_providers' method is used to determine which providers should be used to send the notification. This could include things like email, SMS, or other notification services.

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
