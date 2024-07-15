---
title: Introduction to Monitor Endpoints
---
Endpoints in the Monitors module of the sentry-demo repository are defined as classes that inherit from base classes like Endpoint, ProjectEndpoint, and others. These classes define the HTTP methods (GET, POST, etc.) that the endpoint responds to and the actions to be performed when these methods are called. They are used to handle requests and responses for different operations related to monitors, such as retrieving monitor stats, updating a monitor, deleting a monitor, and more.

The MonitorEndpoint class, for example, is a base endpoint class for monitors. It contains methods to convert arguments from the request into a Monitor object. It also checks permissions and handles exceptions if the monitor does not exist.

There are also more specific endpoint classes like ProjectMonitorEndpoint and ProjectMonitorCheckinEndpoint. These classes inherit from MonitorEndpoint and add more specific functionality. For example, ProjectMonitorCheckinEndpoint looks up a checkin and converts it to a MonitorCheckin object.

Each endpoint class defines a convert_args method that takes the request and other arguments, and converts them into the required format. This method also handles exceptions if the required objects do not exist.

In addition to these, there are mixin classes like MonitorStatsMixin and MonitorCheckInMixin that provide additional methods to retrieve monitor stats and check-ins. These mixins can be used in combination with the endpoint classes to add more functionality.

<SwmSnippet path="/src/sentry/monitors/endpoints/base.py" line="40">

---

# MonitorEndpoint

The MonitorEndpoint class is a base endpoint class for monitors. It contains methods to convert arguments from the request into a Monitor object. It also checks permissions and handles exceptions if the monitor does not exist.

```python
class MonitorEndpoint(Endpoint):
    """
    Base endpoint class for monitors which will look up the monitor and
    convert it to a Monitor object.
    """

    permission_classes: tuple[type[BasePermission], ...] = (ProjectMonitorPermission,)

    def convert_args(
        self,
        request: Request,
        organization_id_or_slug: int | str,
        monitor_id_or_slug: str,
        environment: str | None = None,
        checkin_id: str | None = None,
        *args,
        **kwargs,
    ):
        try:
            if str(organization_id_or_slug).isdigit():
                organization = Organization.objects.get_from_cache(id=organization_id_or_slug)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/monitors/endpoints/base.py" line="105">

---

# ProjectMonitorEndpoint

The ProjectMonitorEndpoint class inherits from MonitorEndpoint and adds more specific functionality. It also converts arguments from the request into a Monitor object and handles exceptions if the monitor does not exist.

```python
class ProjectMonitorEndpoint(ProjectEndpoint):
    """
    Base endpoint class for monitors which will look up the monitor and
    convert it to a Monitor object.
    """

    permission_classes: tuple[type[BasePermission], ...] = (ProjectMonitorPermission,)

    def convert_args(
        self,
        request: Request,
        monitor_id_or_slug: str,
        *args,
        **kwargs,
    ):
        args, kwargs = super().convert_args(request, *args, **kwargs)

        # Try lookup by slug
        try:
            kwargs["monitor"] = Monitor.objects.get(
                project_id=kwargs["project"].id, slug=monitor_id_or_slug
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/monitors/endpoints/base.py" line="145">

---

# ProjectMonitorCheckinEndpoint

The ProjectMonitorCheckinEndpoint class inherits from ProjectMonitorEndpoint and adds functionality to look up a checkin and convert it to a MonitorCheckin object.

```python
class ProjectMonitorCheckinEndpoint(ProjectMonitorEndpoint):
    """
    Base endpoint class for monitors which will look up a checkin
    and convert it to a MonitorCheckin object.
    """

    def convert_args(
        self,
        request: Request,
        checkin_id: str,
        *args,
        **kwargs,
    ):
        args, kwargs = super().convert_args(request, *args, **kwargs)
        try:
            kwargs["checkin"] = MonitorCheckIn.objects.get(
                project_id=kwargs["project"].id,
                guid=checkin_id,
            )
        except MonitorCheckIn.DoesNotExist:
            raise ResourceDoesNotExist
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/monitors/endpoints/monitor_ingest_checkin_attachment.py" line="57">

---

# convert_args method

The convert_args method is defined in each endpoint class. It takes the request and other arguments, and converts them into the required format. This method also handles exceptions if the required objects do not exist.

```python
    def convert_args(
        self,
        request: Request,
        monitor_id_or_slug: int | str,
        checkin_id: str,
        organization_id_or_slug: int | str | None = None,
        *args,
        **kwargs,
    ):
        monitor = None

        using_dsn_auth = isinstance(request.auth, ProjectKey)
        if checkin_id != "latest":
            # We require a checkin for this endpoint. If one doesn't exist then error. If the
            # checkin_id is `latest` we'll need to resolve the monitor before we can get it.
            try:
                UUID(checkin_id)
            except ValueError:
                raise ParameterValidationError("Invalid check-in UUID")

            try:
```

---

</SwmSnippet>

# Endpoint Classes

This section covers the main endpoint classes in the Monitors module of the sentry-demo repository.

<SwmSnippet path="/src/sentry/monitors/endpoints/base.py" line="40">

---

## MonitorEndpoint

The MonitorEndpoint class is a base endpoint class for monitors. It contains methods to convert arguments from the request into a Monitor object. It also checks permissions and handles exceptions if the monitor does not exist.

```python
class MonitorEndpoint(Endpoint):
    """
    Base endpoint class for monitors which will look up the monitor and
    convert it to a Monitor object.
    """

    permission_classes: tuple[type[BasePermission], ...] = (ProjectMonitorPermission,)

    def convert_args(
        self,
        request: Request,
        organization_id_or_slug: int | str,
        monitor_id_or_slug: str,
        environment: str | None = None,
        checkin_id: str | None = None,
        *args,
        **kwargs,
    ):
        try:
            if str(organization_id_or_slug).isdigit():
                organization = Organization.objects.get_from_cache(id=organization_id_or_slug)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/monitors/endpoints/base.py" line="105">

---

## ProjectMonitorEndpoint

The ProjectMonitorEndpoint class inherits from MonitorEndpoint and adds more specific functionality. It looks up the monitor and converts it to a Monitor object.

```python
class ProjectMonitorEndpoint(ProjectEndpoint):
    """
    Base endpoint class for monitors which will look up the monitor and
    convert it to a Monitor object.
    """

    permission_classes: tuple[type[BasePermission], ...] = (ProjectMonitorPermission,)

    def convert_args(
        self,
        request: Request,
        monitor_id_or_slug: str,
        *args,
        **kwargs,
    ):
        args, kwargs = super().convert_args(request, *args, **kwargs)

        # Try lookup by slug
        try:
            kwargs["monitor"] = Monitor.objects.get(
                project_id=kwargs["project"].id, slug=monitor_id_or_slug
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/monitors/endpoints/base.py" line="145">

---

## ProjectMonitorCheckinEndpoint

The ProjectMonitorCheckinEndpoint class inherits from ProjectMonitorEndpoint. It looks up a checkin and converts it to a MonitorCheckin object.

```python
class ProjectMonitorCheckinEndpoint(ProjectMonitorEndpoint):
    """
    Base endpoint class for monitors which will look up a checkin
    and convert it to a MonitorCheckin object.
    """

    def convert_args(
        self,
        request: Request,
        checkin_id: str,
        *args,
        **kwargs,
    ):
        args, kwargs = super().convert_args(request, *args, **kwargs)
        try:
            kwargs["checkin"] = MonitorCheckIn.objects.get(
                project_id=kwargs["project"].id,
                guid=checkin_id,
            )
        except MonitorCheckIn.DoesNotExist:
            raise ResourceDoesNotExist
```

---

</SwmSnippet>

# Monitor Endpoints

Monitor Endpoints

<SwmSnippet path="/src/sentry/monitors/endpoints/organization_monitor_environment_details.py" line="1">

---

## OrganizationMonitorEnvironmentDetailsEndpoint

The `OrganizationMonitorEnvironmentDetailsEndpoint` class defines endpoints for handling operations related to monitor environments at the organization level. It inherits from the `MonitorEndpoint` and `MonitorEnvironmentDetailsMixin` classes. It defines HTTP methods like PUT and DELETE for updating and deleting a monitor environment respectively.

```python
from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response

from sentry.api.api_owners import ApiOwner
from sentry.api.api_publish_status import ApiPublishStatus
from sentry.api.base import region_silo_endpoint
from sentry.apidocs.constants import (
    RESPONSE_ACCEPTED,
    RESPONSE_BAD_REQUEST,
    RESPONSE_FORBIDDEN,
    RESPONSE_NOT_FOUND,
    RESPONSE_UNAUTHORIZED,
)
from sentry.apidocs.parameters import GlobalParams, MonitorParams
from sentry.monitors.serializers import MonitorSerializer

from .base import MonitorEndpoint
from .base_monitor_environment_details import MonitorEnvironmentDetailsMixin
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/monitors/endpoints/project_monitor_checkin_attachment.py" line="1">

---

## ProjectMonitorCheckInAttachmentEndpoint

The `ProjectMonitorCheckInAttachmentEndpoint` class defines endpoints for handling operations related to monitor check-in attachments at the project level. It inherits from the `ProjectMonitorCheckinEndpoint` and `BaseMonitorCheckInAttachmentEndpoint` classes. It defines the HTTP GET method for retrieving a monitor check-in attachment.

```python
from __future__ import annotations

from rest_framework.request import Request
from rest_framework.response import Response

from sentry.api.api_owners import ApiOwner
from sentry.api.api_publish_status import ApiPublishStatus
from sentry.api.base import region_silo_endpoint

from .base import ProjectMonitorCheckinEndpoint
from .base_monitor_checkin_attachment import (
    BaseMonitorCheckInAttachmentEndpoint,
    MonitorCheckInAttachmentPermission,
)


@region_silo_endpoint
class ProjectMonitorCheckInAttachmentEndpoint(
    ProjectMonitorCheckinEndpoint, BaseMonitorCheckInAttachmentEndpoint
):
    publish_status = {
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
