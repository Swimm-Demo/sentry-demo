---
title: Basic Concepts of Metrics Indexer
---
The Indexer in Sentry metrics is a service that provides integer IDs for metric names, tag keys, and tag values, and the corresponding reverse lookup. It is a crucial part of the Sentry metrics system, allowing efficient storage and retrieval of metrics data.

The Indexer is implemented as a StringIndexer class, which is part of the sentry.sentry_metrics.indexer.base module. This class provides methods for recording and resolving metrics data.

The Indexer uses a caching mechanism to improve performance. This is implemented in the CachingIndexer class, which is part of the sentry.sentry_metrics.indexer.cache module.

The Indexer also uses a Postgres database for persistent storage of the indexed data. This is implemented in the PostgresIndexer class, which is part of the sentry.sentry_metrics.indexer.postgres.postgres_v2 module.

<SwmSnippet path="/src/sentry/sentry_metrics/indexer/base.py" line="64">

---

# StringIndexer Class

The `StringIndexer` class is the base class for the Indexer. It provides the basic structure and methods for the Indexer.

```python

class KeyCollection:
    """
    A KeyCollection is a way of keeping track of a group of keys
    used to fetch ids, whose results are stored in KeyResults.

    A key is a org_id, string pair, either represented as a
    tuple e.g (1, "a"), or a string "1:a".

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_metrics/indexer/cache.py" line="208">

---

# CachingIndexer Class

The `CachingIndexer` class is a wrapper around the `StringIndexer` that adds caching functionality. This improves the performance of the Indexer by storing frequently accessed data in memory.

```python
class CachingIndexer(StringIndexer):
    def __init__(self, cache: StringIndexerCache, indexer: StringIndexer) -> None:
        self.cache = cache
        self.indexer = indexer

    def bulk_record(
        self, strings: Mapping[UseCaseID, Mapping[OrgId, set[str]]]
    ) -> UseCaseKeyResults:
        cache_keys = UseCaseKeyCollection(strings)
        metrics.gauge("sentry_metrics.indexer.lookups_per_batch", value=cache_keys.size)
        cache_key_strs = cache_keys.as_strings()
        cache_results = self.cache.get_many(BULK_RECORD_CACHE_NAMESPACE, cache_key_strs)

        hits = [k for k, v in cache_results.items() if v is not None]

        # record all the cache hits we had
        metrics.incr(
            _INDEXER_CACHE_BULK_RECORD_METRIC,
            tags={"cache_hit": "true", "caller": "get_many_ids"},
            amount=len(hits),
        )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_metrics/indexer/postgres/postgres_v2.py" line="325">

---

# PostgresIndexer Class

The `PostgresIndexer` class is a wrapper around the `CachingIndexer` that adds persistent storage functionality. This allows the Indexer to store data in a Postgres database.

```python
class PostgresIndexer(StaticStringIndexer):
    def __init__(self) -> None:
        super().__init__(CachingIndexer(indexer_cache, PGStringIndexerV2()))
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
