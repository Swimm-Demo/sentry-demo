---
title: Issue Tracking Integration in the Sentry Platform
---
This document will cover how issue tracking integrates with the rest of the Sentry platform. We'll cover:

1. The role of the IssueTrackingPlugin and IssueTrackingPlugin2 classes
2. The use of the issue_tracker_used signal
3. The role of analytics events in issue tracking
4. The integration of issue tracking with other parts of the Sentry platform.

<SwmSnippet path="/src/sentry/plugins/examples/issue_tracking.py" line="1">

---

# IssueTrackingPlugin and IssueTrackingPlugin2

The `IssueTrackingPlugin` and `IssueTrackingPlugin2` classes are the base classes for issue tracking plugins. They define the basic structure and functionality of an issue tracking plugin.

```python
from rest_framework.request import Request

from sentry.plugins.bases.issue2 import IssuePlugin2


class ExampleIssueTrackingPlugin(IssuePlugin2):
    author = "Sentry Team"
    author_url = "https://github.com/getsentry/sentry"
    version = "0.0.0"
    description = "An example issue tracking plugin"
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/receivers/onboarding.py" line="18">

---

# issue_tracker_used signal

The `issue_tracker_used` signal is used to track when an issue tracking plugin is used. This helps in analytics and can trigger other actions in the Sentry platform.

```python
from sentry.models.project import Project
from sentry.onboarding_tasks import try_mark_onboarding_complete
from sentry.plugins.bases.issue import IssueTrackingPlugin
from sentry.plugins.bases.issue2 import IssueTrackingPlugin2
from sentry.signals import (
    alert_rule_created,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/analytics/events/issue_tracker_used.py" line="1">

---

# Analytics events in issue tracking

Analytics events like `IssueTrackerUsedEvent` are used to track usage of issue tracking features. These events can be used for reporting and analysis.

```python
from sentry import analytics


class IssueTrackerUsedEvent(analytics.Event):
    type = "issue_tracker.used"
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/web/frontend/organization_integration_setup.py" line="5">

---

# Integration with other parts of the Sentry platform

Issue tracking is integrated with other parts of the Sentry platform. For example, the `TRANSACTION_SOURCE_VIEW` in `organization_integration_setup.py` can be used to track the source of transactions related to issue tracking.

```python
from django.http.response import HttpResponseBase
from rest_framework.request import Request
from sentry_sdk.tracing import TRANSACTION_SOURCE_VIEW

from sentry import features
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="follow-up"><sup>Powered by [Swimm](/)</sup></SwmMeta>
