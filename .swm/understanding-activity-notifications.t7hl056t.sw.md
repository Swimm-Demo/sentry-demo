---
title: Understanding Activity Notifications
---
Activity in the Notifications section of the sentry-demo repository refers to different types of notifications that are triggered based on certain events or actions in the system. These activities are represented by different classes such as `NoteActivityNotification`, `ReleaseActivityNotification`, `AssignedActivityNotification`, and others. Each of these classes represents a specific type of activity and contains the logic for handling the corresponding notifications.

For instance, `NoteActivityNotification` handles the notifications related to notes. It includes the logic for generating the notification title and message description. Similarly, `ReleaseActivityNotification` deals with notifications related to releases. It contains the logic for initializing the notification, getting the participants for the release, and generating the context for the notification.

These activity classes are derived from the `ActivityNotification` base class, which provides the basic structure and common functionalities for all types of activity notifications. The `ActivityNotification` class is an abstract base class and it defines some abstract methods like `get_context` and `get_participants_with_group_subscription_reason` that must be implemented by the derived classes.

The `ActivityNotification` class also includes some common properties and methods that are used across all types of activity notifications. For example, it includes a `send` method for sending the notification and a `get_log_params` method for getting the log parameters.

<SwmSnippet path="/src/sentry/notifications/notifications/activity/base.py" line="28">

---

# Activity Classes

This is the `ActivityNotification` base class. It provides the basic structure and common functionalities for all types of activity notifications. It defines some abstract methods like `get_context` and `get_participants_with_group_subscription_reason` that must be implemented by the derived classes.

```python
class ActivityNotification(ProjectNotification, abc.ABC):
    metrics_key = "activity"
    notification_setting_type_enum = NotificationSettingEnum.WORKFLOW
    template_path = "sentry/emails/activity/generic"

    def __init__(self, activity: Activity) -> None:
        super().__init__(activity.project)
        self.activity = activity

    @property
    @abc.abstractmethod
    def title(self) -> str:
        """The header for Workflow notifications."""

    def get_base_context(self) -> MutableMapping[str, Any]:
        """The most basic context shared by every notification type."""
        return {
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/notifications/notifications/activity/assigned.py" line="55">

---

# Derived Activity Classes

This is an example of a derived activity class, `AssignedActivityNotification`. It represents the activity of assigning a task and contains the logic for handling the corresponding notifications.

```python
class AssignedActivityNotification(GroupActivityNotification):
    metrics_key = "assigned_activity"
    title = "Assigned"
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/notifications/notifications/activity/base.py" line="33">

---

# Activity Data

The `Activity` data is passed to the activity class during initialization. This data contains the details of the event or action that triggered the notification.

```python
    def __init__(self, activity: Activity) -> None:
        super().__init__(activity.project)
        self.activity = activity
```

---

</SwmSnippet>

# Activity Notifications

This section will cover the main functions related to 'Activity' in the sentry-demo repository.

<SwmSnippet path="/src/sentry/notifications/notifications/activity/note.py" line="16">

---

## NoteActivityNotification

The `NoteActivityNotification` class handles the notifications related to notes. It includes the logic for generating the notification title and message description.

```python
class NoteActivityNotification(GroupActivityNotification):
    message_builder = "SlackNotificationsMessageBuilder"
    metrics_key = "note_activity"
    template_path = "sentry/emails/activity/note"

    def get_description(self) -> tuple[str, str | None, Mapping[str, Any]]:
        # Notes may contain {} characters so we should escape them.
        text = str(self.activity.data["text"]).replace("{", "{{").replace("}", "}}")
        return text, None, {}

    @property
    def title(self) -> str:
        if self.user:
            author = self.user.get_display_name()
        else:
            author = "Unknown"
        return f"New comment by {author}"

    def get_notification_title(
        self, provider: ExternalProviders, context: Mapping[str, Any] | None = None
    ) -> str:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/notifications/notifications/activity/release.py" line="32">

---

## ReleaseActivityNotification

The `ReleaseActivityNotification` class deals with notifications related to releases. It contains the logic for initializing the notification, getting the participants for the release, and generating the context for the notification.

```python
class ReleaseActivityNotification(ActivityNotification):
    metrics_key = "release_activity"
    notification_setting_type_enum = NotificationSettingEnum.DEPLOY
    template_path = "sentry/emails/activity/release"

    def __init__(self, activity: Activity) -> None:
        super().__init__(activity)
        self.group = None
        self.user_id_team_lookup: Mapping[int, list[int]] | None = None
        self.deploy = get_deploy(activity)
        self.release = get_release(activity, self.organization)

        if not self.release:
            self.email_list: set[str] = set()
            self.repos: Iterable[Mapping[str, Any]] = set()
            self.projects: set[Project] = set()
            self.version = "unknown"
            self.version_parsed = self.version
            self.user_ids = set()
            return

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/notifications/notifications/activity/assigned.py" line="55">

---

## AssignedActivityNotification

The `AssignedActivityNotification` class handles the notifications when an issue is assigned. It includes the logic for generating the notification title and getting the assignee.

```python
class AssignedActivityNotification(GroupActivityNotification):
    metrics_key = "assigned_activity"
    title = "Assigned"

    def get_assignee(self) -> str:
        return get_assignee_str(self.activity, self.organization)

    def get_description(self) -> tuple[str, str | None, Mapping[str, Any]]:
        return "{author} assigned {an issue} to {assignee}", None, {"assignee": self.get_assignee()}

    def get_notification_title(
        self, provider: ExternalProviders, context: Mapping[str, Any] | None = None
    ) -> str:
        assignee = self.get_assignee()

```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
