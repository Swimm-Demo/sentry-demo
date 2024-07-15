---
title: Getting started with Incident Endpoints
---
Endpoints in the Incidents module of the Sentry application are the interfaces through which the application communicates with the outside world. They are used to handle various operations related to incidents such as fetching incident details, listing incidents, marking an incident as seen, and managing comments on incidents.

For instance, the `OrganizationIncidentIndexEndpoint` is used to list incidents that a user can access within an organization. It returns a paginated list of incidents that a user can access. The `OrganizationIncidentDetailsEndpoint` is used to fetch and update the details of a specific incident.

The `OrganizationIncidentSeenEndpoint` is used to mark an incident as seen by the user. The `OrganizationIncidentCommentIndexEndpoint` and `OrganizationIncidentCommentDetailsEndpoint` are used to manage comments on incidents.

<SwmSnippet path="/src/sentry/incidents/endpoints/bases.py" line="12">

---

# ProjectAlertRuleEndpoint

The `ProjectAlertRuleEndpoint` class is an example of an endpoint in the Sentry application. It inherits from the `ProjectEndpoint` base class and defines a `convert_args` method that handles requests to the endpoint.

```python
class ProjectAlertRuleEndpoint(ProjectEndpoint):
    owner = ApiOwner.ISSUES
    permission_classes = (ProjectAlertRulePermission,)

    def convert_args(self, request: Request, alert_rule_id, *args, **kwargs):
        args, kwargs = super().convert_args(request, *args, **kwargs)
        project = kwargs["project"]

        # Allow orgs that have downgraded plans to delete metric alerts
        if request.method != "DELETE" and not features.has(
            "organizations:incidents", project.organization, actor=request.user
        ):
            raise ResourceDoesNotExist

        if not request.access.has_project_access(project):
            raise PermissionDenied

        try:
            kwargs["alert_rule"] = AlertRule.objects.get(projects=project, id=alert_rule_id)
        except AlertRule.DoesNotExist:
            raise ResourceDoesNotExist
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/incidents/endpoints/bases.py" line="37">

---

# OrganizationAlertRuleEndpoint

The `OrganizationAlertRuleEndpoint` class is another example of an endpoint. It inherits from the `OrganizationEndpoint` base class and also defines a `convert_args` method that handles requests to the endpoint.

```python
class OrganizationAlertRuleEndpoint(OrganizationEndpoint):
    permission_classes = (OrganizationAlertRulePermission,)

    def convert_args(self, request: Request, alert_rule_id, *args, **kwargs):
        args, kwargs = super().convert_args(request, *args, **kwargs)
        organization = kwargs["organization"]

        # Allow orgs that have downgraded plans to delete metric alerts
        if request.method != "DELETE" and not features.has(
            "organizations:incidents", organization, actor=request.user
        ):
            raise ResourceDoesNotExist

        try:
            kwargs["alert_rule"] = AlertRule.objects.get(
                organization=organization, id=alert_rule_id
            )
        except AlertRule.DoesNotExist:
            raise ResourceDoesNotExist

        return args, kwargs
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/incidents/endpoints/bases.py" line="60">

---

# OrganizationAlertRuleTriggerEndpoint

The `OrganizationAlertRuleTriggerEndpoint` class is an example of an endpoint that inherits from another endpoint (`OrganizationAlertRuleEndpoint`). This shows how endpoints can be organized in a hierarchical manner, with more specific endpoints inheriting from more general ones.

```python
class OrganizationAlertRuleTriggerEndpoint(OrganizationAlertRuleEndpoint):
    def convert_args(self, request: Request, alert_rule_trigger_id, *args, **kwargs):
```

---

</SwmSnippet>

# Endpoint Functions

This section provides an overview of the main functions related to endpoints in the Sentry application.

<SwmSnippet path="/src/sentry/incidents/endpoints/organization_incident_index.py" line="27">

---

## OrganizationIncidentIndexEndpoint

The `OrganizationIncidentIndexEndpoint` is used to list incidents that a user can access within an organization. It returns a paginated list of incidents that a user can access.

`````````````````````````````````````````````````````````````python
class OrganizationIncidentIndexEndpoint(OrganizationEndpoint):
    owner = ApiOwner.ISSUES
    publish_status = {
        "GET": ApiPublishStatus.UNKNOWN,
    }
    permission_classes = (IncidentPermission,)

    def get(self, request: Request, organization) -> Response:
        """
        List Incidents that a User can access within an Organization
        ````````````````````````````````````````````````````````````
        Returns a paginated list of Incidents that a user can access.

        :auth: required
        """
        if not features.has("organizations:incidents", organization, actor=request.user):
            raise ResourceDoesNotExist

        incidents = Incident.objects.fetch_for_organization(
            organization, self.get_projects(request, organization)
        )
`````````````````````````````````````````````````````````````

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/incidents/endpoints/organization_incident_details.py" line="8">

---

## OrganizationIncidentDetailsEndpoint

The `OrganizationIncidentDetailsEndpoint` is used to fetch and update the details of a specific incident.

```python
from sentry.api.bases.incident import IncidentEndpoint, IncidentPermission
from sentry.api.serializers import serialize
from sentry.incidents.endpoints.serializers.incident import DetailedIncidentSerializer
from sentry.incidents.logic import update_incident_status
from sentry.incidents.models.incident import IncidentStatus, IncidentStatusMethod
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/incidents/endpoints/organization_incident_seen.py" line="12">

---

## OrganizationIncidentSeenEndpoint

The `OrganizationIncidentSeenEndpoint` is used to mark an incident as seen by the user.

`````````````````````````````````````python
class OrganizationIncidentSeenEndpoint(IncidentEndpoint):
    owner = ApiOwner.ISSUES
    publish_status = {
        "POST": ApiPublishStatus.UNKNOWN,
    }
    permission_classes = (IncidentPermission,)

    def post(self, request: Request, organization, incident) -> Response:
        """
        Mark an incident as seen by the user
        ````````````````````````````````````

        :auth: required
        """

        set_incident_seen(incident=incident, user=request.user)
        return Response({}, status=201)
`````````````````````````````````````

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/incidents/endpoints/organization_incident_comment_index.py" line="26">

---

## OrganizationIncidentCommentIndexEndpoint

The `OrganizationIncidentCommentIndexEndpoint` is used to manage comments on incidents. It allows users to post comments on incidents.

```python
class OrganizationIncidentCommentIndexEndpoint(IncidentEndpoint):
    owner = ApiOwner.ISSUES
    publish_status = {
        "POST": ApiPublishStatus.UNKNOWN,
    }
    permission_classes = (IncidentPermission,)

    def post(self, request: Request, organization, incident) -> Response:
        serializer = CommentSerializer(
            data=request.data,
            context={
                "projects": incident.projects.all(),
                "organization": organization,
                "organization_id": organization.id,
            },
        )
        if serializer.is_valid():
            mentions = extract_user_ids_from_mentions(
                organization.id, serializer.validated_data.get("mentions", [])
            )
            mentioned_user_ids = mentions["users"] | mentions["team_users"]
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/incidents/endpoints/organization_incident_comment_details.py" line="50">

---

## OrganizationIncidentCommentDetailsEndpoint

The `OrganizationIncidentCommentDetailsEndpoint` is used to manage specific comments on incidents. It allows users to update or delete their comments on incidents.

`````````````````python
class OrganizationIncidentCommentDetailsEndpoint(CommentDetailsEndpoint):
    owner = ApiOwner.ISSUES
    publish_status = {
        "DELETE": ApiPublishStatus.UNKNOWN,
        "PUT": ApiPublishStatus.UNKNOWN,
    }
    permission_classes = (IncidentPermission,)

    def delete(self, request: Request, organization, incident, activity) -> Response:
        """
        Delete a comment
        ````````````````
        :auth: required
        """

        try:
            delete_comment(activity)
        except IncidentActivity.DoesNotExist:
            raise ResourceDoesNotExist

        return Response(status=204)
`````````````````

---

</SwmSnippet>

# Incident Endpoints Overview

Incident Endpoints

<SwmSnippet path="/src/sentry/incidents/endpoints/organization_incident_index.py" line="28">

---

## OrganizationIncidentIndexEndpoint

The `OrganizationIncidentIndexEndpoint` is used to list incidents that a user can access within an organization. It returns a paginated list of incidents that a user can access. The endpoint supports filtering by status, team, and event types. It also supports sorting the results.

`````````````````````````````````````````````````````````````python
    owner = ApiOwner.ISSUES
    publish_status = {
        "GET": ApiPublishStatus.UNKNOWN,
    }
    permission_classes = (IncidentPermission,)

    def get(self, request: Request, organization) -> Response:
        """
        List Incidents that a User can access within an Organization
        ````````````````````````````````````````````````````````````
        Returns a paginated list of Incidents that a user can access.

        :auth: required
        """
        if not features.has("organizations:incidents", organization, actor=request.user):
            raise ResourceDoesNotExist

        incidents = Incident.objects.fetch_for_organization(
            organization, self.get_projects(request, organization)
        )

`````````````````````````````````````````````````````````````

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/incidents/endpoints/organization_incident_details.py" line="32">

---

## OrganizationIncidentDetailsEndpoint

The `OrganizationIncidentDetailsEndpoint` is used to fetch and update the details of a specific incident. The `get` method fetches the details of the incident, while the `put` method updates the status of the incident.

```````````````````python
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
        if serializer.is_valid():
```````````````````

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
