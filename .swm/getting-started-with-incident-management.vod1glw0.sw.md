---
title: Getting started with Incident Management
---
Incidents in the Sentry application refer to events that signify a significant change or anomaly in your system's behavior. They are primarily used for tracking and managing issues that affect the performance and reliability of your applications.

Incidents are represented in the codebase by the `Incident` class, which is defined in the `sentry.incidents.models.incident` module. This class contains various attributes and methods that allow for the manipulation and management of incident data.

Associated with the `Incident` class is the `IncidentActivity` class. This class records changes that occur in an incident, such as a status change. It provides a historical record of the incident's lifecycle.

The `IncidentSeen` class is used to track which incidents have been viewed by users. This helps in managing the workflow of incident resolution by keeping track of which incidents are still pending review.

The `IncidentProject` class is used to associate incidents with specific projects. This allows for better organization and filtering of incidents based on the projects they affect.

<SwmSnippet path="/src/sentry/incidents/models/incident.py" line="8">

---

# Incident Class

The `Incident` class is the main class representing an incident. It contains various attributes and methods for managing incident data.

```python
from django.conf import settings
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/incidents/models/incident.py" line="9">

---

# IncidentActivity Class

The `IncidentActivity` class is used to record changes in an incident, providing a historical record of the incident's lifecycle.

```python
from django.core.cache import cache
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/incidents/models/incident.py" line="11">

---

# IncidentSeen Class

The `IncidentSeen` class is used to track which incidents have been viewed by users, aiding in the management of incident resolution workflow.

```python
from django.db.models.signals import post_delete, post_save
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/incidents/models/incident.py" line="10">

---

# IncidentProject Class

The `IncidentProject` class is used to associate incidents with specific projects, allowing for better organization and filtering of incidents.

```python
from django.db import IntegrityError, models, router, transaction
```

---

</SwmSnippet>

# Incident and Alert Rule Endpoints

Incident and Alert Rule Endpoints

<SwmSnippet path="/src/sentry/incidents/endpoints/organization_incident_details.py" line="31">

---

## OrganizationIncidentDetailsEndpoint

The `OrganizationIncidentDetailsEndpoint` class is a Django Rest Framework endpoint that handles HTTP requests to the `/organizations/{organization}/incidents/{incident}` URL. It supports GET, PUT, and DELETE methods. The GET method fetches details of a specific incident. The PUT method updates the status of an incident. The DELETE method is not currently implemented.

```````````````````python
@region_silo_endpoint
class OrganizationIncidentDetailsEndpoint(IncidentEndpoint):
    owner = ApiOwner.ISSUES
    publish_status = {
        "GET": ApiPublishStatus.UNKNOWN,
        "PUT": ApiPublishStatus.UNKNOWN,
    }
    permission_classes = (IncidentPermission,)

    def get(self, request: Request, organization, incident) -> Response:
        """
        Fetch an Incident.
        ``````````````````
        :auth: required
        """
        data = serialize(incident, request.user, DetailedIncidentSerializer())

        return Response(data)

    def put(self, request: Request, organization, incident) -> Response:
        serializer = IncidentSerializer(data=request.data)
```````````````````

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/incidents/endpoints/organization_alert_rule_details.py" line="31">

---

## OrganizationAlertRuleDetailsEndpoint

The `OrganizationAlertRuleDetailsEndpoint` class is a Django Rest Framework endpoint that handles HTTP requests to the `/organizations/{organization}/alert-rules/{alert_rule}` URL. It supports GET, PUT, and DELETE methods. The GET method fetches details of a specific alert rule. The PUT method updates an alert rule. The DELETE method deletes an alert rule.

```python
from sentry.incidents.serializers import AlertRuleSerializer as DrfAlertRuleSerializer
from sentry.incidents.utils.sentry_apps import trigger_sentry_app_action_creators_for_incidents
from sentry.integrations.slack.utils import RedisRuleStatus
from sentry.models.rulesnooze import RuleSnooze
from sentry.sentry_apps.services.app import app_service
from sentry.tasks.integrations.slack import find_channel_id_for_alert_rule
from sentry.users.services.user.service import user_service


def fetch_alert_rule(request: Request, organization, alert_rule):
    # Serialize Alert Rule
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
