---
title: Basic Concepts of Relocations Management in Endpoints
---
Relocations in the Endpoints directory refer to the process of moving data from one state or location to another within the Sentry application. This is handled through various API endpoints that allow for pausing, unpausing, cancelling, and recovering relocations. These operations are crucial for managing data flow and ensuring data integrity within the application.

The RelocationUnpauseEndpoint, for instance, is an API endpoint that allows for the unpausing of a paused relocation. It contains a helper function '\_unpause' that performs the actual unpausing in a transaction-safe manner. If the unpausing fails, it returns a Response with an error message. Otherwise, it returns None and lets the calling function perform the serialization for the return payload.

There are also various error messages defined, such as ERR_UNKNOWN_RELOCATION_STEP and ERR_COULD_NOT_PAUSE_RELOCATION_AT_STEP, which are used to handle and communicate errors during the relocation process. These error messages are used across multiple files in the relocations directory, indicating their shared role in managing relocations.

In summary, relocations in the Endpoints directory are a critical part of managing data within the Sentry application, with various endpoints and error messages defined to handle the process.

<SwmSnippet path="/src/sentry/api/endpoints/relocations/unpause.py" line="16">

---

# RelocationUnpauseEndpoint

This is where the Relocation model is imported from sentry.models.relocation. It's used in the endpoint to handle the unpausing of relocations.

```python
from sentry.api.permissions import SuperuserOrStaffFeatureFlaggedPermission
from sentry.api.serializers import serialize
from sentry.models.relocation import Relocation
from sentry.tasks.relocation import get_first_task_for_step
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/relocations/unpause.py" line="11">

---

# Error Messages

These are the error messages used to handle and communicate errors during the relocation process. They are defined in the relocations module and used across multiple files in the relocations directory.

```python
from sentry.api.endpoints.relocations import (
    ERR_COULD_NOT_PAUSE_RELOCATION_AT_STEP,
    ERR_UNKNOWN_RELOCATION_STEP,
)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/relocations/artifacts/index.py" line="52">

---

# Permission Check

This is an example of a permission check for relocation admin. If the user does not have the required permissions, a PermissionDenied error is raised with the ERR_NEED_RELOCATION_ADMIN message.

```python
        if not request.access.has_permission("relocation.admin"):
            raise PermissionDenied(ERR_NEED_RELOCATION_ADMIN)
```

---

</SwmSnippet>

# Relocation Functions Overview

This section provides an overview of the main functions involved in handling data relocations in the Sentry application.

<SwmSnippet path="/src/sentry/api/endpoints/relocations/unpause.py" line="33">

---

## RelocationUnpauseEndpoint and \_unpause function

The 'RelocationUnpauseEndpoint' class is an API endpoint that allows for the unpausing of a paused relocation. It contains a helper function '\_unpause' that performs the actual unpausing in a transaction-safe manner. If the unpausing fails, it returns a 'Response' with an error message. Otherwise, it returns 'None' and lets the calling function perform the serialization for the return payload.

```python
class RelocationUnpauseEndpoint(Endpoint):
    owner = ApiOwner.OPEN_SOURCE
    publish_status = {
        # TODO(getsentry/team-ospo#214): Stabilize before GA.
        "PUT": ApiPublishStatus.EXPERIMENTAL,
    }
    permission_classes = (SuperuserOrStaffFeatureFlaggedPermission,)

    def _unpause(self, request: Request, relocation: Relocation) -> Response | None:
        """
        Helper function to do the actual unpausing in a transaction-safe manner. It will only return
        a `Response` if the relocation failed - otherwise, it will return `None` and let the calling
        function perform the serialization for the return payload.
        """
        existing_scheduled_pause_at_step = relocation.scheduled_pause_at_step
        until_step = request.data.get("untilStep", None)
        if until_step is None:
            relocation.scheduled_pause_at_step = None
        else:
            try:
                step = Relocation.Step[until_step.upper()]
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/relocations/unpause.py" line="117">

---

## put function

The 'put' function in the 'RelocationUnpauseEndpoint' class is used to unpause an in-progress relocation. It uses a 'select_for_update' transaction to prevent duplicate tasks from being started by racing unpause calls.

```````````````````````````````````````````````````python
    def put(self, request: Request, relocation_uuid: str) -> Response:
        """
        Unpause an in-progress relocation.
        ``````````````````````````````````````````````````

        This command accepts a single optional parameter, which specifies the step BEFORE which the
        next pause should occur. If no such parameter is specified, no future pauses are scheduled.

        :pparam string relocation_uuid: a UUID identifying the relocation.
        :param string untilStep: an optional string identifying the next step to pause before; must
                                 be greater than the currently active step, and one of:
                                 `PREPROCESSING`, `VALIDATING`, `IMPORTING`, `POSTPROCESSING`,
                                 `NOTIFYING`.

        :auth: required
        """

        logger.info("relocations.unpause.put.start", extra={"caller": request.user.id})

        # Use a `select_for_update` transaction to prevent duplicate tasks from being started by
        # racing unpause calls.
```````````````````````````````````````````````````

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/relocations/unpause.py" line="21">

---

## Error Messages

Various error messages are defined, such as 'ERR_UNKNOWN_RELOCATION_STEP' and 'ERR_COULD_NOT_PAUSE_RELOCATION_AT_STEP', which are used to handle and communicate errors during the relocation process. These error messages are used across multiple files in the relocations directory, indicating their shared role in managing relocations.

```python
ERR_NOT_UNPAUSABLE_STATUS = Template(
    """Relocations can only be unpaused if they are already paused; this relocation is
    `$status`."""
)
ERR_COULD_NOT_UNPAUSE_RELOCATION = (
    "Could not unpause relocation, perhaps because it is no longer in-progress."
)
```

---

</SwmSnippet>

# Relocation Endpoints

Relocation API Endpoints

<SwmSnippet path="/src/sentry/api/endpoints/relocations/recover.py" line="34">

---

## RelocationRecoverEndpoint

The RelocationRecoverEndpoint is used to recover a failed relocation. It includes a helper function '\_recover' that attempts to recover a failed relocation. If the recovery fails, it returns an error response. If successful, it returns None and the calling function handles the serialization of the return payload.

```python
@region_silo_endpoint
class RelocationRecoverEndpoint(Endpoint):
    owner = ApiOwner.OPEN_SOURCE
    publish_status = {
        # TODO(getsentry/team-ospo#214): Stabilize before GA.
        "PUT": ApiPublishStatus.EXPERIMENTAL,
    }
    permission_classes = (SuperuserOrStaffFeatureFlaggedPermission,)

    def _recover(self, request: Request, relocation: Relocation) -> Response | None:
        """
        Helper function to do just... one... more... attempt of a the last task that the relocation
        failed at. Useful to try to recover a relocation after a fix has been pushed.
        """

        until_step = request.data.get("untilStep", None)
        if until_step is not None:
            try:
                step = Relocation.Step[until_step.upper()]
            except KeyError:
                return Response(
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/relocations/pause.py" line="32">

---

## RelocationPauseEndpoint

The RelocationPauseEndpoint is used to pause an in-progress relocation. It includes logic to handle various conditions such as the current status of the relocation and the step at which the pause should occur. If the pause operation fails, it returns an error response.

```````````````````````````````````````````````````python
@region_silo_endpoint
class RelocationPauseEndpoint(Endpoint):
    owner = ApiOwner.OPEN_SOURCE
    publish_status = {
        # TODO(getsentry/team-ospo#214): Stabilize before GA.
        "PUT": ApiPublishStatus.EXPERIMENTAL,
    }
    permission_classes = (SuperuserOrStaffFeatureFlaggedPermission,)

    def put(self, request: Request, relocation_uuid: str) -> Response:
        """
        Pause an in-progress relocation.
        ``````````````````````````````````````````````````

        This command accepts a single optional parameter, which specifies the step BEFORE which the
        pause should occur. If no such parameter is specified, the pause is scheduled for the step
        immediately following the currently active one, if possible.

        :pparam string relocation_uuid: a UUID identifying the relocation.
        :param string atStep: an optional string identifying the step to pause at; must be greater
                               than the currently active step, and one of: `PREPROCESSING`,
```````````````````````````````````````````````````

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
