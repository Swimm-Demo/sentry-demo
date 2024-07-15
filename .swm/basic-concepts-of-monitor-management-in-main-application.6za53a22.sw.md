---
title: Basic Concepts of Monitor Management in Main Application
---
Monitors in Sentry are a way to keep track of and respond to specific conditions or errors that occur in your application. They are associated with specific projects and can be configured with various parameters to define their behavior. Monitors can be created, updated, and managed through various functions in the codebase.

The function `_ensure_monitor_with_config` is used to ensure that a monitor with a specific configuration exists. If the monitor does not exist, it is created. The function also validates the configuration of the monitor and updates it if necessary.

The `update_monitor` function is used to update the properties of a monitor. This includes the monitor's name, slug, status, type, and configuration. The function also handles the assignment and unassignment of monitor seats.

The `update_monitor_environment` function is used to update the environment of a monitor. This function is primarily used to mute or unmute monitor environments.

The `post` function in `organization_monitor_index.py` is used to create a new monitor. It validates the data provided in the request, assigns a seat to the monitor, and creates an audit entry for the creation of the monitor.

<SwmSnippet path="/src/sentry/monitors/consumers/monitor_consumer.py" line="89">

---

# Creating and Updating Monitors

The function `_ensure_monitor_with_config` is used to ensure that a monitor with a specific configuration exists. If the monitor does not exist, it is created. The function also validates the configuration of the monitor and updates it if necessary.

```python
def _ensure_monitor_with_config(
    project: Project,
    monitor_slug: str,
    config: Mapping | None,
):
    try:
        monitor = Monitor.objects.get(
            slug=monitor_slug,
            project_id=project.id,
            organization_id=project.organization_id,
        )
    except Monitor.DoesNotExist:
        monitor = None

    if not config:
        return monitor

    # The upsert payload doesn't quite match the api one. Pop out the owner here since
    # it's not part of the monitor config
    owner = config.pop("owner", None)
    owner_user_id = None
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/monitors/endpoints/base_monitor_details.py" line="54">

---

# Updating Monitor Properties

The `update_monitor` function is used to update the properties of a monitor. This includes the monitor's name, slug, status, type, and configuration. The function also handles the assignment and unassignment of monitor seats.

```python
    def update_monitor(
        self, request: AuthenticatedHttpRequest, project: Project, monitor: Monitor
    ) -> Response:
        """
        Update a monitor.
        """
        # set existing values as validator will overwrite
        existing_config = monitor.config
        existing_margin = existing_config.get("checkin_margin")
        existing_max_runtime = existing_config.get("max_runtime")

        validator = MonitorValidator(
            data=request.data,
            partial=True,
            instance={
                "name": monitor.name,
                "slug": monitor.slug,
                "status": monitor.status,
                "type": monitor.type,
                "config": monitor.config,
                "project": project,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/monitors/endpoints/organization_monitor_details.py" line="71">

---

# Creating a New Monitor

The `put` function in `organization_monitor_details.py` is used to create a new monitor. It validates the data provided in the request, assigns a seat to the monitor, and creates an audit entry for the creation of the monitor.

```python
    def put(self, request: AuthenticatedHttpRequest, organization, project, monitor) -> Response:
        """
        Update a monitor.
        """
        return self.update_monitor(request, project, monitor)
```

---

</SwmSnippet>

# Monitor Management Endpoints

Monitor Management in Sentry

<SwmSnippet path="/src/sentry/monitors/consumers/monitor_consumer.py" line="89">

---

## \_ensure_monitor_with_config

The `_ensure_monitor_with_config` function is used to ensure that a monitor with a specific configuration exists. If the monitor does not exist, it is created. The function also validates the configuration of the monitor and updates it if necessary.

```python
def _ensure_monitor_with_config(
    project: Project,
    monitor_slug: str,
    config: Mapping | None,
):
    try:
        monitor = Monitor.objects.get(
            slug=monitor_slug,
            project_id=project.id,
            organization_id=project.organization_id,
        )
    except Monitor.DoesNotExist:
        monitor = None

    if not config:
        return monitor

    # The upsert payload doesn't quite match the api one. Pop out the owner here since
    # it's not part of the monitor config
    owner = config.pop("owner", None)
    owner_user_id = None
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/monitors/endpoints/base_monitor_details.py" line="54">

---

## update_monitor

The `update_monitor` function is used to update the properties of a monitor. This includes the monitor's name, slug, status, type, and configuration. The function also handles the assignment and unassignment of monitor seats.

```python
    def update_monitor(
        self, request: AuthenticatedHttpRequest, project: Project, monitor: Monitor
    ) -> Response:
        """
        Update a monitor.
        """
        # set existing values as validator will overwrite
        existing_config = monitor.config
        existing_margin = existing_config.get("checkin_margin")
        existing_max_runtime = existing_config.get("max_runtime")

        validator = MonitorValidator(
            data=request.data,
            partial=True,
            instance={
                "name": monitor.name,
                "slug": monitor.slug,
                "status": monitor.status,
                "type": monitor.type,
                "config": monitor.config,
                "project": project,
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
