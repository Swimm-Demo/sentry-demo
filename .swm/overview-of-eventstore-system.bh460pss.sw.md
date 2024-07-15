---
title: Overview of Eventstore System
---
Eventstore in the Main Application refers to a system that stores events, which are immutable records of actions within the application. It is primarily used for event sourcing, a design pattern that derives the current state of an application from the sequence of events that have happened in the past.

The Eventstore is implemented using Snuba, a column-oriented data storage system. This is evident from the `SnubaEventStorage` class in the `sentry.eventstore.snuba.backend.py` file. This class provides methods for querying and retrieving events from the Snuba storage.

The Eventstore also includes a processing component, as seen in the `sentry.eventstore.processing` directory. This component is responsible for processing events before they are stored. The `store` function in `sentry.eventstore.processing.base.py` is an example of this, where it prepares an event for storage and assigns it a cache key.

Additionally, the Eventstore includes a reprocessing component, as seen in the `sentry.eventstore.reprocessing` directory. This component is used when events need to be reprocessed, for example, when an error occurs during processing.

<SwmSnippet path="/src/sentry/eventstore/snuba/backend.py" line="61">

---

# SnubaEventStorage

The `SnubaEventStorage` class in the `sentry.eventstore.snuba.backend.py` file provides methods for querying and retrieving events from the Snuba storage. It is an implementation of the EventStorage interface.

```python
class SnubaEventStorage(EventStorage):
    """
    Eventstore backend backed by Snuba
    """

    def get_events_snql(
        self,
        organization_id: int,
        group_id: int,
        start: datetime | None,
        end: datetime | None,
        conditions: Sequence[Condition],
        orderby: Sequence[str],
        limit=DEFAULT_LIMIT,
        offset=DEFAULT_OFFSET,
        referrer="eventstore.get_events_snql",
        dataset=Dataset.Events,
        tenant_ids=None,
    ):
        cols = self.__get_columns(dataset)

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/eventstore/processing/base.py" line="41">

---

# Event Processing

The `store` function in `sentry.eventstore.processing.base.py` prepares an event for storage and assigns it a cache key. This is part of the event processing component of the Eventstore.

```python
    def store(self, event: Event, unprocessed: bool = False) -> str:
        key = cache_key_for_event(event)
        if unprocessed:
            key = self.__get_unprocessed_key(key)
        self.inner.set(key, event, self.timeout)
        return key
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/eventstore/snuba/backend.py" line="161">

---

# Event Retrieval

The `get_events` function in `sentry.eventstore.snuba.backend.py` retrieves events from the Snuba storage. It uses the `__get_events` helper function to perform the actual retrieval.

```python
    def get_events(
        self,
        filter,
        orderby=None,
        limit=DEFAULT_LIMIT,
        offset=DEFAULT_OFFSET,
        referrer="eventstore.get_events",
        dataset=Dataset.Events,
        tenant_ids=None,
    ):
        """
        Get events from Snuba, with node data loaded.
        """
        with sentry_sdk.start_span(op="eventstore.snuba.get_events"):
            return self.__get_events(
                filter,
                orderby=orderby,
                limit=limit,
                offset=offset,
                referrer=referrer,
```

---

</SwmSnippet>

# Eventstore Functions

This section will cover the main functions of the Eventstore, including retrieving events, binding nodes, and storing events.

<SwmSnippet path="/src/sentry/eventstore/base.py" line="157">

---

## get_events

The `get_events` function is used to fetch a list of events based on a set of criteria. It is an abstract method that must be implemented by the specific backend used by the Eventstore.

```python
    def get_events(
        self,
        filter,
        orderby=None,
        limit=100,
        offset=0,
        referrer="eventstore.get_events",
        dataset=Dataset.Events,
        tenant_ids=None,
    ):
        """
        Fetches a list of events given a set of criteria.

        Searches for error events, including security and default messages, but not for
        transaction events. Returns an empty list if no events match the filter.

        Arguments:
        snuba_filter (Filter): Filter
        orderby (Sequence[str]): List of fields to order by - default ['-time', '-event_id']
        limit (int): Query limit - default 100
        offset (int): Query offset - default 0
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/eventstore/base.py" line="226">

---

## get_event_by_id

The `get_event_by_id` function retrieves a single event given a project ID and event ID. It returns None if an event cannot be found.

```python
    def get_event_by_id(
        self,
        project_id: int,
        event_id: str,
        group_id: int | None = None,
        skip_transaction_groupevent=False,
        tenant_ids=None,
        occurrence_id: str | None = None,
    ):
        """
        Gets a single event of any event type given a project_id and event_id.
        Returns None if an event cannot be found.

        Arguments:
        project_id (int): Project ID
        event_id (str): Event ID
        group_id (Optional[int]): If the group ID for this event is already known, pass
            it here to save one Snuba query.
        """
        raise NotImplementedError
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/eventstore/base.py" line="264">

---

## bind_nodes

The `bind_nodes` function fetches all the data blobs for a list of Event objects with a single multi-get command to nodestore, and binds the returned blobs to the NodeDatas of the events.

```python
    def bind_nodes(self, object_list: Sequence[Event]) -> None:
        """
        For a list of Event objects, and a property name where we might find an
        (unfetched) NodeData on those objects, fetch all the data blobs for
        those NodeDatas with a single multi-get command to nodestore, and bind
        the returned blobs to the NodeDatas.

        It's not necessary to bind a single Event object since data will be lazily
        fetched on any attempt to access a property.
        """
        sentry_sdk.set_tag("eventstore.backend", "nodestore")

        with sentry_sdk.start_span(op="eventstore.base.bind_nodes"):
            object_node_list = [(i, i.data) for i in object_list if i.data.id]

            # Remove duplicates from the list of nodes to be fetched
            node_ids = list({n.id for _, n in object_node_list})
            if not node_ids:
                return

            node_results = nodestore.backend.get_multi(node_ids)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/eventstore/processing/base.py" line="41">

---

## store

The `store` function prepares an event for storage and assigns it a cache key. It is part of the processing component of the Eventstore.

```python
    def store(self, event: Event, unprocessed: bool = False) -> str:
        key = cache_key_for_event(event)
        if unprocessed:
            key = self.__get_unprocessed_key(key)
        self.inner.set(key, event, self.timeout)
        return key
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
