---
title: Basic Concepts of Asynchronous Tasks in Main Application
---
Tasks in the Main Application of sentry-demo are functions decorated with the `instrumented_task` decorator. These tasks are designed to perform specific operations asynchronously and independently from the main application flow. They are used to handle heavy or time-consuming operations such as sending notifications, processing data, or scheduling reports.

Tasks are defined in various modules within the `sentry/tasks` directory. Each task is typically associated with a specific feature or functionality of the application. For example, the `send_activity_notifications` task in `sentry/tasks/activity.py` is responsible for sending notifications related to activities.

Tasks are scheduled and managed using Celery, a distributed task queue system. The `instrumented_task` decorator, defined in `sentry/tasks/base.py`, is used to wrap these tasks. This decorator provides additional functionalities such as statsd metrics for duration and memory usage, Sentry SDK tagging, hybrid cloud silo restrictions, and disabling of result collection.

Tasks can be scheduled to run at specific times or triggered by certain events. For example, the `schedule_organizations` function in `sentry/tasks/summaries/weekly_reports.py` schedules tasks for generating weekly reports for each active organization.

<SwmSnippet path="/src/sentry/tasks/base.py" line="43">

---

# Task Definition

This is where the `instrumented_task` decorator is defined. This decorator is used to wrap tasks and provides additional functionalities such as statsd metrics for duration and memory usage, Sentry SDK tagging, hybrid cloud silo restrictions, and disabling of result collection.

```python
    def __call__(self, decorated_task: Any) -> Any:
        # Replace the celery.Task interface we use.
        replacements = {"delay", "apply_async", "s", "signature", "retry", "apply", "run"}
        for attr_name in replacements:
            task_attr = getattr(decorated_task, attr_name)
            if callable(task_attr):
                limited_attr = self.create_override(task_attr)
                setattr(decorated_task, attr_name, limited_attr)

        limited_func = self.create_override(decorated_task)
        if hasattr(decorated_task, "name"):
            limited_func.name = decorated_task.name
        return limited_func
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="671">

---

# Task Scheduling

This is an example of how tasks are scheduled in the application. The `NextTask` class is used to encapsulate a task along with its parameters, allowing it to be scheduled at a later point in the execution.

```python
    status: ValidationStatus,
) -> NextTask | None:
    """
    After a `RelocationValidationAttempt` resolves, make sure to update the owning
    `RelocationValidation` and `Relocation` as well.

    Returns the subsequent task that should be executed as soon as the wrapping
    `retry_task_or_fail_relocation` exits, as the last action in the currently running task.
    """

    with atomic_transaction(
        using=(
            router.db_for_write(Relocation),
            router.db_for_write(RelocationValidation),
            router.db_for_write(RelocationValidationAttempt),
        )
    ):
        # If no interesting status updates occurred, check again in a minute.
        if status == ValidationStatus.IN_PROGRESS:
            logger.info(
                "Validation polling: scheduled",
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/sentry_apps.py" line="156">

---

# Task Execution

This is an example of a task function, `_process_resource_change`. This function is responsible for processing resource changes. It demonstrates how tasks handle complex operations, manage exceptions, and interact with other parts of the application.

```python
def _process_resource_change(action, sender, instance_id, retryer=None, *args, **kwargs):
    # The class is serialized as a string when enqueueing the class.
    model = TYPES[sender]
    # The Event model has different hooks for the different event types. The sender
    # determines which type eg. Error and therefore the 'name' eg. error
    if issubclass(model, Event):
        if not kwargs.get("instance"):
            extra = {"sender": sender, "action": action, "event_id": instance_id}
            logger.info("process_resource_change.event_missing_event", extra=extra)
            return
        name = sender.lower()
    else:
        # Some resources are named differently than their model. eg. Group vs Issue.
        # Looks up the human name for the model. Defaults to the model name.
        name = RESOURCE_RENAMES.get(model.__name__, model.__name__.lower())

    # By default, use Celery's `current_task` but allow a value to be passed for the
    # bound Task.
    retryer = retryer or current_task

    # We may run into a race condition where this task executes before the
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
