---
title: Flow of Sending Notifications in Sentry
---
This document will cover the flow of sending a notification in the Sentry system. We'll cover:

1. How notifications are defined and handled
2. The role of different services and modules in the notification process
3. The flow of sending a notification through different integrations like Slack, PagerDuty, and MS Teams.

<SwmSnippet path="/src/sentry/integrations/slack/service.py" line="57">

---

# Notification Definition and Handling

This section of the code defines the different types of notifications that can be sent based on various activity types. Each activity type is associated with a specific notification handler.

```python
_default_logger = getLogger(__name__)


DEFAULT_SUPPORTED_ACTIVITY_THREAD_NOTIFICATION_HANDLERS: dict[
    ActivityType, type[ActivityNotification]
] = {
    ActivityType.ASSIGNED: AssignedActivityNotification,
    ActivityType.DEPLOY: ReleaseActivityNotification,
    ActivityType.SET_REGRESSION: RegressionActivityNotification,
    ActivityType.SET_RESOLVED: ResolvedActivityNotification,
    ActivityType.SET_RESOLVED_BY_AGE: ResolvedActivityNotification,
    ActivityType.SET_RESOLVED_IN_COMMIT: ResolvedActivityNotification,
    ActivityType.SET_RESOLVED_IN_PULL_REQUEST: ResolvedActivityNotification,
    ActivityType.SET_RESOLVED_IN_RELEASE: ResolvedInReleaseActivityNotification,
    ActivityType.UNASSIGNED: UnassignedActivityNotification,
    ActivityType.SET_ESCALATING: EscalatingActivityNotification,
    ActivityType.SET_IGNORED: ArchiveActivityNotification,
    ActivityType.SET_UNRESOLVED: UnresolvedActivityNotification,
    ActivityType.CREATE_ISSUE: ExternalIssueCreatedActivityNotification,
}
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/notifications/utils/participants.py" line="45">

---

# Role of Different Services and Modules

This file defines the available providers for notifications and a limit for fallthrough notifications. It also imports the `notifications_service` from `sentry.notifications.services` which is used to manage notifications.

```python
logger = logging.getLogger(__name__)


AVAILABLE_PROVIDERS = {
    ExternalProviders.EMAIL,
    ExternalProviders.SLACK,
}

FALLTHROUGH_NOTIFICATION_LIMIT = 20
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/integrations/slack/webhooks/action.py" line="51">

---

# Sending Notifications Through Different Integrations

This file contains the definitions for various actions and options related to notifications in the Slack integration. It also imports the `notifications_service` for managing notifications.

```python
UNFURL_ACTION_OPTIONS = ["link", "ignore"]
NOTIFICATION_SETTINGS_ACTION_OPTIONS = ["all_slack"]

LINK_IDENTITY_MESSAGE = (
    "Looks like you haven't linked your Sentry account with your Slack identity yet! "
    "<{associate_url}|Link your identity now> to perform actions in Sentry through Slack. "
)
UNLINK_IDENTITY_MESSAGE = (
    "Looks like this Slack identity is linked to the Sentry user *{user_email}* "
    "who is not a member of organization *{org_name}* used with this Slack integration. "
    "<{associate_url}|Unlink your identity now>. "
)

NO_ACCESS_MESSAGE = "You do not have access to the organization for the invitation."
NO_PERMISSION_MESSAGE = "You do not have permission to approve member invitations."
NO_IDENTITY_MESSAGE = "Identity not linked for user."
ENABLE_SLACK_SUCCESS_MESSAGE = "Slack notifications have been enabled."

DEFAULT_ERROR_MESSAGE = "Sentry can't perform that action right now on your behalf!"
SUCCESS_MESSAGE = (
    "{invite_type} request for {email} has been {verb}. <{url}|See Members and Requests>."
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="follow-up"><sup>Powered by [Swimm](/)</sup></SwmMeta>
