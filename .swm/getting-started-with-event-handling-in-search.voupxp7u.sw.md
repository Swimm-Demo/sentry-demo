---
title: Getting Started with Event Handling in Search
---
Events in the context of the sentry-demo repository refer to the data points or occurrences that are tracked and monitored in an application. They are represented and manipulated through various modules and functions within the 'sentry.search.events' directory. These modules provide functionalities for filtering, building, and handling events.

The 'events' directory contains several Python files that define classes, functions, and constants used for event data manipulation. For instance, '[fields.py](http://fields.py)' contains definitions for various classes and functions that handle event fields. Similarly, '[constants.py](http://constants.py)' defines various constants used across the 'events' modules.

The 'events' data is used in the 'Search' functionality of the application. The 'Search' feature allows users to filter and search through the events based on various parameters. This is facilitated by functions such as 'format_search_filter' and 'convert_search_filter_to_condition' which are used to format and convert search filters to conditions respectively.

<SwmSnippet path="/src/sentry/search/events/builder/discover.py" line="326">

---

# Event Handling in [Discover.py](http://Discover.py)

The `resolve_top_event_conditions` function in `discover.py` is used to construct conditions for a list of top events. It iterates through the fields of the events and applies various conditions based on the field type. This function is a key part of how events are filtered and handled in the application.

```python
    def resolve_top_event_conditions(
        self, top_events: list[dict[str, Any]], other: bool
    ) -> WhereType | None:
        """Given a list of top events construct the conditions"""
        conditions = []
        for field in self.fields:
            # If we have a project field, we need to limit results by project so we don't hit the result limit
            if field in ["project", "project.id"] and top_events:
                # Iterate through the existing conditions to find the project one
                # the project condition is a requirement of queries so there should always be one
                project_condition = [
                    condition
                    for condition in self.where
                    if isinstance(condition, Condition)
                    and condition.lhs == self.column("project_id")
                ][0]
                self.where.remove(project_condition)
                if field == "project":
                    projects = list(
                        {self.params.project_slug_map[event["project"]] for event in top_events}
                    )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/search/events/builder/metrics.py" line="1910">

---

# Event Handling in [Metrics.py](http://Metrics.py)

Similarly, the `resolve_top_event_conditions` function in `metrics.py` is used to construct conditions for a list of top events. It also iterates through the fields of the events and applies various conditions based on the field type. This function is another key part of how events are filtered and handled in the application.

```python
    def resolve_top_event_conditions(
        self, top_events: list[dict[str, Any]], other: bool
    ) -> WhereType | None:
        """Given a list of top events construct the conditions"""
        conditions = []

        for field in self.fields:
            if fields.is_function(field):
                # A function will never be in a top_events dict.
                continue
            resolved_field = self.resolve_column(field)

            values: set[Any] = set()
            for event in top_events:
                if field not in event:
                    continue

                value = event.get(field)
                # Ensure the project id fields stay as numbers, clickhouse 20 can't handle it, but 21 can
                if field in {"project_id", "project.id"}:
                    value = int(value)
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
