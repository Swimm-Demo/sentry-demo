---
title: Understanding the Reprocessing Group Function
---
# Introduction to reprocess_group

The `reprocess_group` function is a task that handles the reprocessing of a group of events. It takes in parameters such as the project id, group id, and other optional parameters like the remaining events, new group id, query state, start time, max events, and acting user id. The function sets tags for the project and group id using the `sentry_sdk.set_tag` method.

# Starting Group Reprocessing

If the `start_time` is None, it means that this is the first time the function is being called for this group. In this case, the function sets the start time to the current time and calls the `start_group_reprocessing` function, which initiates the reprocessing of the group.

# Running Batch Query

The function then runs a batch query using the `celery_run_batch_query` function. This function retrieves a batch of events from the group that needs to be reprocessed.

# Handling Remaining Events

If there are no events returned from the batch query, the function calls `buffered_handle_remaining_events` to handle any remaining events that belong to the new group generated after reprocessing.

# Reprocessing Events

For each event in the batch, the function checks if the max events limit has been reached. If not, it calls the `reprocess_event` function to reprocess the event. If there are any errors during reprocessing or if the max events limit has been reached, the function adds the event to the `remaining_event_ids` list.

# Recursion

Finally, the function calls itself recursively with the updated parameters to continue the reprocessing of the remaining events in the group.

# Flow drill down

```mermaid
graph TD;

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

<SwmSnippet path="/src/sentry/tasks/reprocessing2.py" line="29">

---

# reprocess_group Function

The `reprocess_group` function is a task that handles the reprocessing of a group of events. It takes in parameters such as the project id, group id, and other optional parameters like the remaining events, new group id, query state, start time, max events, and acting user id. The function sets tags for the project and group id using the `sentry_sdk.set_tag` method.

```python
def reprocess_group(
    project_id: int,
    group_id: int,
    remaining_events: str = "delete",
    new_group_id: int | None = None,
    query_state: str | None = None,
    start_time: float | None = None,
    max_events: int | None = None,
    acting_user_id: int | None = None,
) -> None:
    sentry_sdk.set_tag("project", project_id)
    sentry_sdk.set_tag("group_id", group_id)

    from sentry.reprocessing2 import (
        CannotReprocess,
        buffered_handle_remaining_events,
        logger,
        reprocess_event,
        start_group_reprocessing,
    )

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/reprocessing2.py" line="54">

---

## Starting Group Reprocessing

If the `start_time` is None, it means that this is the first time the function is being called for this group. In this case, the function sets the start time to the current time and calls the `start_group_reprocessing` function, which initiates the reprocessing of the group.

```python
        assert new_group_id is None
        start_time = time.time()
        metrics.incr("events.reprocessing.start_group_reprocessing", sample_rate=1.0)
        sentry_sdk.set_tag("is_start", "true")
        new_group_id = start_group_reprocessing(
            project_id,
            group_id,
            max_events=max_events,
            acting_user_id=acting_user_id,
            remaining_events=remaining_events,
        )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/reprocessing2.py" line="68">

---

## Running Batch Query

The function then runs a batch query using the `celery_run_batch_query` function. This function retrieves a batch of events from the group that needs to be reprocessed.

```python
    query_state, events = celery_run_batch_query(
        filter=eventstore.Filter(project_ids=[project_id], group_ids=[group_id]),
        batch_size=settings.SENTRY_REPROCESSING_PAGE_SIZE,
        state=query_state,
        referrer="reprocessing2.reprocess_group",
        tenant_ids={
            "organization_id": Project.objects.get_from_cache(id=project_id).organization_id
        },
    )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/reprocessing2.py" line="78">

---

## Handling Remaining Events

If there are no events returned from the batch query, the function calls `buffered_handle_remaining_events` to handle any remaining events that belong to the new group generated after reprocessing.

```python
    if not events:
        # Migrate events that belong to new group generated after reprocessing
        buffered_handle_remaining_events(
            project_id=project_id,
            old_group_id=group_id,
            new_group_id=new_group_id,
            datetime_to_event=[],
            remaining_events=remaining_events,
            force_flush_batch=True,
        )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/reprocessing2.py" line="93">

---

## Reprocessing Events

For each event in the batch, the function checks if the max events limit has been reached. If not, it calls the `reprocess_event` function to reprocess the event. If there are any errors during reprocessing or if the max events limit has been reached, the function adds the event to the `remaining_event_ids` list.

```python
    for event in events:
        if max_events is None or max_events > 0:
            with sentry_sdk.start_span(op="reprocess_event"):
                try:
                    reprocess_event(
                        project_id=project_id,
                        event_id=event.event_id,
                        start_time=start_time,
                    )
                except CannotReprocess as e:
                    logger.error("reprocessing2.%s", str(e))
                except Exception:
                    sentry_sdk.capture_exception()
                else:
                    if max_events is not None:
                        max_events -= 1

                    continue

        # In case of errors while kicking off reprocessing or if max_events has
        # been exceeded, do the default action.
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/reprocessing2.py" line="127">

---

## Recursion

Finally, the function calls itself recursively with the updated parameters to continue the reprocessing of the remaining events in the group.

```python
    reprocess_group.delay(
        project_id=project_id,
        group_id=group_id,
        new_group_id=new_group_id,
        query_state=query_state,
        start_time=start_time,
        max_events=max_events,
        remaining_events=remaining_events,
    )
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
