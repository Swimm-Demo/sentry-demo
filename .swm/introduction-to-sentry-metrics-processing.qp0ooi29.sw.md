---
title: Introduction to Sentry Metrics Processing
---
Sentry metrics in the main application are a part of the Sentry's error tracking and performance monitoring platform. They are used to collect, process, and analyze data about the application's performance and errors. This data is then used to provide insights and help developers understand the behavior of their application.

The metrics are collected and processed by various components in the `sentry_metrics` module. This includes the `indexer` which is responsible for indexing the metrics data, and the `MetricsIngestConfiguration` which is used to configure how the metrics data is ingested into the system.

The `UseCaseKey` is a part of the configuration that is used to identify specific use cases for the metrics data. The `OperationsConfiguration` is used to configure the operations that can be performed on the metrics data.

The `metrics` module from `sentry.utils` is used across the `sentry_metrics` module for various utility functions related to metrics.

<SwmSnippet path="/src/sentry/sentry_metrics/utils.py" line="5">

---

# Metrics Indexer

The `indexer` from `sentry.sentry_metrics` is used for indexing the metrics data. It is imported in various files across the `sentry_metrics` module.

```python
from sentry.sentry_metrics import indexer
from sentry.sentry_metrics.configuration import UseCaseKey
from sentry.sentry_metrics.indexer.base import to_use_case_id
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_metrics/indexer/limiters/writes.py" line="15">

---

# Metrics Configuration

`MetricsIngestConfiguration` from `sentry.sentry_metrics.configuration` is used to configure how the metrics data is ingested into the system.

```python
from sentry.sentry_metrics.configuration import MetricsIngestConfiguration, UseCaseKey
from sentry.sentry_metrics.indexer.base import (
    FetchType,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_metrics/indexer/base.py" line="9">

---

# Use Case Key

`UseCaseKey` is a part of the configuration that is used to identify specific use cases for the metrics data.

```python
from sentry.sentry_metrics.configuration import UseCaseKey
from sentry.sentry_metrics.use_case_id_registry import REVERSE_METRIC_PATH_MAPPING, UseCaseID
from sentry.utils import metrics
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_metrics/querying/metadata/metrics.py" line="15">

---

# Operations Configuration

`OperationsConfiguration` is used to configure the operations that can be performed on the metrics data.

```python
)
from sentry.sentry_metrics.use_case_id_registry import UseCaseID
from sentry.snuba.metrics import parse_mri
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_metrics/utils.py" line="4">

---

# Metrics Utility Functions

The `metrics` module from `sentry.utils` is used across the `sentry_metrics` module for various utility functions related to metrics.

```python
from sentry.exceptions import InvalidParams
from sentry.sentry_metrics import indexer
from sentry.sentry_metrics.configuration import UseCaseKey
from sentry.sentry_metrics.indexer.base import to_use_case_id
from sentry.sentry_metrics.use_case_id_registry import METRIC_PATH_MAPPING, UseCaseID
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
