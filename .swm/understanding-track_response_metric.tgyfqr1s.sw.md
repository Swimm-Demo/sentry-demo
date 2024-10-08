---
title: Understanding track_response_metric
---
<SwmSnippet path="/src/sentry_plugins/amazon_sqs/plugin.py" line="29">

---

# track_response_metric

The `track_response_metric` function is a decorator that wraps around another function (referred to as `fn` in the parameters). It is designed to track the success or failure of the HTTP response from the Amazon SQS service. The success is determined based on whether an exception was raised during the execution of the wrapped function.

```python
def track_response_metric(fn):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.send_message
    # boto3's send_message doesn't return success/fail or http codes
    # success is a boolean based on whether there was an exception or not
    def wrapper(*args, **kwargs):
        try:
            success = fn(*args, **kwargs)
            metrics.incr(
                "data-forwarding.http_response", tags={"plugin": "amazon-sqs", "success": success}
            )
        except Exception:
            metrics.incr(
                "data-forwarding.http_response", tags={"plugin": "amazon-sqs", "success": False}
            )
            raise
        return success

    return wrapper
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/organization_events_stats.py" line="316">

---

# fn

The `fn` function is a complex function that performs a series of operations to fetch event statistics. It first checks if the metrics are enhanced and if a dashboard widget ID is provided. If not, it calls the `_get_event_stats` function. If these conditions are met, it retrieves the widget, checks if it has a split, and performs a series of operations based on the widget's split type.

```python
            def fn(
                query_columns: Sequence[str],
                query: str,
                params: dict[str, str],
                rollup: int,
                zerofill_results: bool,
                comparison_delta: datetime | None,
            ) -> SnubaTSResult | dict[str, SnubaTSResult]:

                if not (metrics_enhanced and dashboard_widget_id):
                    return _get_event_stats(
                        scoped_dataset,
                        query_columns,
                        query,
                        params,
                        rollup,
                        zerofill_results,
                        comparison_delta,
                    )

                try:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/organization_events_stats.py" line="254">

---

# \_get_event_stats

The `_get_event_stats` function is responsible for fetching event statistics. It checks if the `top_events` parameter is greater than 0. If it is, it calls the `top_events_timeseries` function from the `scoped_dataset` object. If not, it calls the `timeseries_query` function from the `scoped_dataset` object.

```python
        def _get_event_stats(
            scoped_dataset: Any,
            query_columns: Sequence[str],
            query: str,
            params: dict[str, str],
            rollup: int,
            zerofill_results: bool,
            comparison_delta: datetime | None,
        ) -> SnubaTSResult | dict[str, SnubaTSResult]:
            if top_events > 0:
                return scoped_dataset.top_events_timeseries(
                    timeseries_columns=query_columns,
                    selected_columns=self.get_field_list(organization, request),
                    equations=self.get_equation_list(organization, request),
                    user_query=query,
                    params=params,
                    orderby=self.get_orderby(request),
                    rollup=rollup,
                    limit=top_events,
                    organization=organization,
                    referrer=referrer + ".find-topn",
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/snuba/spans_metrics.py" line="138">

---

# top_events_timeseries

The `top_events_timeseries` function performs a timeseries query for a limited number of top events. It first checks if the `top_events` parameter is `None`. If it is, it calls the `query` function to fetch the top events. It then creates a `TopSpansMetricsQueryBuilder` object and runs the query. If the number of top events equals the limit and `include_other` is `True`, it also runs a query for other events.

```python
def top_events_timeseries(
    timeseries_columns,
    selected_columns,
    user_query,
    params,
    orderby,
    rollup,
    limit,
    organization,
    equations=None,
    referrer=None,
    top_events=None,
    allow_empty=True,
    zerofill_results=True,
    include_other=False,
    functions_acl=None,
    on_demand_metrics_enabled=False,
    on_demand_metrics_type: MetricSpecType | None = None,
):
    """
    High-level API for doing arbitrary user timeseries queries for a limited number of top events
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/snuba/spans_metrics.py" line="76">

---

# timeseries_query

The `timeseries_query` function performs a timeseries query against events. It creates a `TimeseriesSpansMetricsQueryBuilder` object and runs the query. The results are then processed and returned as a `SnubaTSResult` object.

```python
def timeseries_query(
    selected_columns: Sequence[str],
    query: str,
    params: dict[str, str],
    rollup: int,
    referrer: str,
    zerofill_results: bool = True,
    allow_metric_aggregates=True,
    comparison_delta: timedelta | None = None,
    functions_acl: list[str] | None = None,
    has_metrics: bool = True,
    use_metrics_layer: bool = False,
    on_demand_metrics_enabled: bool = False,
    on_demand_metrics_type: MetricSpecType | None = None,
    groupby: Column | None = None,
) -> SnubaTSResult:
    """
    High-level API for doing arbitrary user timeseries queries against events.
    this API should match that of sentry.snuba.discover.timeseries_query
    """
    metrics_query = TimeseriesSpansMetricsQueryBuilder(
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/organization_events_stats.py" line="167">

---

# get

The flow begins with the `get` function in the `organization_events_stats.py` file. This function is responsible for handling the request and organization parameters and returning a response.

```python
    def get(self, request: Request, organization: Organization) -> Response:
        with sentry_sdk.start_span(op="discover.endpoint", description="filter_params") as span:
            span.set_data("organization", organization)

            top_events = 0

            if "topEvents" in request.GET:
                try:
                    top_events = int(request.GET.get("topEvents", 0))
                except ValueError:
                    return Response({"detail": "topEvents must be an integer"}, status=400)
                if top_events > MAX_TOP_EVENTS:
                    return Response(
                        {"detail": f"Can only get up to {MAX_TOP_EVENTS} top events"},
                        status=400,
                    )
                elif top_events <= 0:
                    return Response({"detail": "If topEvents needs to be at least 1"}, status=400)

            comparison_delta = None
            if "comparisonDelta" in request.GET:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/bases/organization_events.py" line="421">

---

# get_event_stats_data

The `get_event_stats_data` function is called within the `get` function. It takes several parameters including the request, organization, get_event_stats function, and others. It handles query errors, creates stats query, and serializes the result.

```python
    def get_event_stats_data(
        self,
        request: Request,
        organization: Organization,
        get_event_stats: Callable[
            [Sequence[str], str, dict[str, str], int, bool, timedelta | None], SnubaTSResult
        ],
        top_events: int = 0,
        query_column: str = "count()",
        params: ParamsType | None = None,
        query: str | None = None,
        allow_partial_buckets: bool = False,
        zerofill_results: bool = True,
        comparison_delta: timedelta | None = None,
        additional_query_column: str | None = None,
        dataset: Any | None = None,
    ) -> dict[str, Any]:
        with handle_query_errors():
            with sentry_sdk.start_span(
                op="discover.endpoint", description="base.stats_query_creation"
            ):
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/organization_profiling_functions.py" line="115">

---

# get_event_stats

The `get_event_stats` function is used within the `get_event_stats_data` function. It takes several parameters including columns, query, params, rollup, zerofill results, and comparison delta. It performs a query for each chunk of top functions and returns the results.

```python
        def get_event_stats(_columns, query, params, _rollup, zerofill_results, _comparison_delta):
            rollup = get_rollup_from_range(params["end"] - params["start"])

            chunks = [
                top_functions["data"][i : i + FUNCTIONS_PER_QUERY]
                for i in range(0, len(top_functions["data"]), FUNCTIONS_PER_QUERY)
            ]

            builders = [
                ProfileTopFunctionsTimeseriesQueryBuilder(
                    dataset=Dataset.Functions,
                    params=params,
                    interval=rollup,
                    top_events=chunk,
                    other=False,
                    query=query,
                    selected_columns=["project.id", "fingerprint"],
                    # It's possible to override the columns via
                    # the `yAxis` qs. So we explicitly ignore the
                    # columns, and hard code in the columns we want.
                    timeseries_columns=[data["function"], "examples()"],
```

---

</SwmSnippet>

```mermaid
graph TD;
subgraph src/sentry/api/endpoints
  track_response_metric:::mainFlowStyle --> fn:::mainFlowStyle
end
subgraph src/sentry/api/endpoints
  fn:::mainFlowStyle --> _get_event_stats
end
subgraph src/sentry/api/endpoints
  fn:::mainFlowStyle --> get:::mainFlowStyle
end
subgraph src/sentry/api/endpoints
  get:::mainFlowStyle --> _get_event_stats
end
subgraph src/sentry/snuba/spans_metrics.py
  get:::mainFlowStyle --> top_events_timeseries
end
subgraph src/sentry/snuba/spans_metrics.py
  get:::mainFlowStyle --> timeseries_query
end
subgraph src/sentry/api/bases/organization_events.py
  get:::mainFlowStyle --> get_event_stats_data:::mainFlowStyle
end
subgraph src/sentry/api/endpoints
  get_event_stats_data:::mainFlowStyle --> get_event_stats:::mainFlowStyle
end

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

# Flow drill down

First, we'll zoom into this section of the flow:

```mermaid
graph TD;
subgraph src/sentry
  track_response_metric:::mainFlowStyle --> fn:::mainFlowStyle
end
subgraph src/sentry
  fn:::mainFlowStyle --> _get_event_stats
end
subgraph src/sentry
  fn:::mainFlowStyle --> get:::mainFlowStyle
end
subgraph src/sentry
  get:::mainFlowStyle --> ociq7[...]
end
subgraph src/sentry
  _get_event_stats --> top_events_timeseries
end
subgraph src/sentry
  _get_event_stats --> timeseries_query
end
subgraph src/sentry
  top_events_timeseries --> query
end

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

<SwmSnippet path="/src/sentry_plugins/amazon_sqs/plugin.py" line="29">

---

# track_response_metric

The `track_response_metric` function is a decorator that wraps around another function (referred to as `fn` in the parameters). It is designed to track the success or failure of the HTTP response from the Amazon SQS service. The success is determined based on whether an exception was raised during the execution of the wrapped function.

```python
def track_response_metric(fn):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.send_message
    # boto3's send_message doesn't return success/fail or http codes
    # success is a boolean based on whether there was an exception or not
    def wrapper(*args, **kwargs):
        try:
            success = fn(*args, **kwargs)
            metrics.incr(
                "data-forwarding.http_response", tags={"plugin": "amazon-sqs", "success": success}
            )
        except Exception:
            metrics.incr(
                "data-forwarding.http_response", tags={"plugin": "amazon-sqs", "success": False}
            )
            raise
        return success

    return wrapper
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/organization_events_stats.py" line="316">

---

# fn

The `fn` function is a complex function that performs a series of operations to fetch event statistics. It first checks if the metrics are enhanced and if a dashboard widget ID is provided. If not, it calls the `_get_event_stats` function. If these conditions are met, it retrieves the widget, checks if it has a split, and performs a series of operations based on the widget's split type.

```python
            def fn(
                query_columns: Sequence[str],
                query: str,
                params: dict[str, str],
                rollup: int,
                zerofill_results: bool,
                comparison_delta: datetime | None,
            ) -> SnubaTSResult | dict[str, SnubaTSResult]:

                if not (metrics_enhanced and dashboard_widget_id):
                    return _get_event_stats(
                        scoped_dataset,
                        query_columns,
                        query,
                        params,
                        rollup,
                        zerofill_results,
                        comparison_delta,
                    )

                try:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/organization_events_stats.py" line="254">

---

# \_get_event_stats

The `_get_event_stats` function is responsible for fetching event statistics. It checks if the `top_events` parameter is greater than 0. If it is, it calls the `top_events_timeseries` function from the `scoped_dataset` object. If not, it calls the `timeseries_query` function from the `scoped_dataset` object.

```python
        def _get_event_stats(
            scoped_dataset: Any,
            query_columns: Sequence[str],
            query: str,
            params: dict[str, str],
            rollup: int,
            zerofill_results: bool,
            comparison_delta: datetime | None,
        ) -> SnubaTSResult | dict[str, SnubaTSResult]:
            if top_events > 0:
                return scoped_dataset.top_events_timeseries(
                    timeseries_columns=query_columns,
                    selected_columns=self.get_field_list(organization, request),
                    equations=self.get_equation_list(organization, request),
                    user_query=query,
                    params=params,
                    orderby=self.get_orderby(request),
                    rollup=rollup,
                    limit=top_events,
                    organization=organization,
                    referrer=referrer + ".find-topn",
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/snuba/spans_metrics.py" line="138">

---

# top_events_timeseries

The `top_events_timeseries` function performs a timeseries query for a limited number of top events. It first checks if the `top_events` parameter is `None`. If it is, it calls the `query` function to fetch the top events. It then creates a `TopSpansMetricsQueryBuilder` object and runs the query. If the number of top events equals the limit and `include_other` is `True`, it also runs a query for other events.

```python
def top_events_timeseries(
    timeseries_columns,
    selected_columns,
    user_query,
    params,
    orderby,
    rollup,
    limit,
    organization,
    equations=None,
    referrer=None,
    top_events=None,
    allow_empty=True,
    zerofill_results=True,
    include_other=False,
    functions_acl=None,
    on_demand_metrics_enabled=False,
    on_demand_metrics_type: MetricSpecType | None = None,
):
    """
    High-level API for doing arbitrary user timeseries queries for a limited number of top events
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/snuba/spans_metrics.py" line="76">

---

# timeseries_query

The `timeseries_query` function performs a timeseries query against events. It creates a `TimeseriesSpansMetricsQueryBuilder` object and runs the query. The results are then processed and returned as a `SnubaTSResult` object.

```python
def timeseries_query(
    selected_columns: Sequence[str],
    query: str,
    params: dict[str, str],
    rollup: int,
    referrer: str,
    zerofill_results: bool = True,
    allow_metric_aggregates=True,
    comparison_delta: timedelta | None = None,
    functions_acl: list[str] | None = None,
    has_metrics: bool = True,
    use_metrics_layer: bool = False,
    on_demand_metrics_enabled: bool = False,
    on_demand_metrics_type: MetricSpecType | None = None,
    groupby: Column | None = None,
) -> SnubaTSResult:
    """
    High-level API for doing arbitrary user timeseries queries against events.
    this API should match that of sentry.snuba.discover.timeseries_query
    """
    metrics_query = TimeseriesSpansMetricsQueryBuilder(
```

---

</SwmSnippet>

Now, lets zoom into this section of the flow:

```mermaid
graph TD;
subgraph src/sentry/api/endpoints
  get:::mainFlowStyle --> _get_event_stats
end
subgraph src/sentry/snuba/spans_metrics.py
  get:::mainFlowStyle --> top_events_timeseries
end
subgraph src/sentry/snuba/spans_metrics.py
  get:::mainFlowStyle --> timeseries_query
end
subgraph src/sentry/api/bases/organization_events.py
  get:::mainFlowStyle --> get_event_stats_data:::mainFlowStyle
end
subgraph src/sentry/api/endpoints
  get_event_stats_data:::mainFlowStyle --> get_event_stats:::mainFlowStyle
end
subgraph src/sentry/snuba/spans_metrics.py
  top_events_timeseries --> query
end
subgraph src/sentry/snuba/spans_metrics.py
  _get_event_stats --> top_events_timeseries
end
subgraph src/sentry/snuba/spans_metrics.py
  _get_event_stats --> timeseries_query
end

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

<SwmSnippet path="/src/sentry/api/endpoints/organization_events_stats.py" line="167">

---

# track_response_metric Flow

The flow begins with the `get` function in the `organization_events_stats.py` file. This function is responsible for handling the request and organization parameters and returning a response.

```python
    def get(self, request: Request, organization: Organization) -> Response:
        with sentry_sdk.start_span(op="discover.endpoint", description="filter_params") as span:
            span.set_data("organization", organization)

            top_events = 0

            if "topEvents" in request.GET:
                try:
                    top_events = int(request.GET.get("topEvents", 0))
                except ValueError:
                    return Response({"detail": "topEvents must be an integer"}, status=400)
                if top_events > MAX_TOP_EVENTS:
                    return Response(
                        {"detail": f"Can only get up to {MAX_TOP_EVENTS} top events"},
                        status=400,
                    )
                elif top_events <= 0:
                    return Response({"detail": "If topEvents needs to be at least 1"}, status=400)

            comparison_delta = None
            if "comparisonDelta" in request.GET:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/organization_events_stats.py" line="254">

---

The `get` function calls `_get_event_stats` function. This function takes several parameters including the dataset, query columns, query, parameters, rollup, zerofill results, and comparison delta. Depending on the number of top events, it either calls `top_events_timeseries` or `timeseries_query`.

```python
        def _get_event_stats(
            scoped_dataset: Any,
            query_columns: Sequence[str],
            query: str,
            params: dict[str, str],
            rollup: int,
            zerofill_results: bool,
            comparison_delta: datetime | None,
        ) -> SnubaTSResult | dict[str, SnubaTSResult]:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/snuba/spans_metrics.py" line="138">

---

`top_events_timeseries` function is used when there are top events. It performs a timeseries query for a limited number of top events and returns a dictionary of SnubaTSResult objects.

```python
def top_events_timeseries(
    timeseries_columns,
    selected_columns,
    user_query,
    params,
    orderby,
    rollup,
    limit,
    organization,
    equations=None,
    referrer=None,
    top_events=None,
    allow_empty=True,
    zerofill_results=True,
    include_other=False,
    functions_acl=None,
    on_demand_metrics_enabled=False,
    on_demand_metrics_type: MetricSpecType | None = None,
):
    """
    High-level API for doing arbitrary user timeseries queries for a limited number of top events
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/snuba/spans_metrics.py" line="76">

---

`timeseries_query` function is used when there are no top events. It performs an arbitrary user timeseries query against events.

```python
def timeseries_query(
    selected_columns: Sequence[str],
    query: str,
    params: dict[str, str],
    rollup: int,
    referrer: str,
    zerofill_results: bool = True,
    allow_metric_aggregates=True,
    comparison_delta: timedelta | None = None,
    functions_acl: list[str] | None = None,
    has_metrics: bool = True,
    use_metrics_layer: bool = False,
    on_demand_metrics_enabled: bool = False,
    on_demand_metrics_type: MetricSpecType | None = None,
    groupby: Column | None = None,
) -> SnubaTSResult:
    """
    High-level API for doing arbitrary user timeseries queries against events.
    this API should match that of sentry.snuba.discover.timeseries_query
    """
    metrics_query = TimeseriesSpansMetricsQueryBuilder(
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/bases/organization_events.py" line="421">

---

The `get_event_stats_data` function is called within the `get` function. It takes several parameters including the request, organization, get_event_stats function, and others. It handles query errors, creates stats query, and serializes the result.

```python
    def get_event_stats_data(
        self,
        request: Request,
        organization: Organization,
        get_event_stats: Callable[
            [Sequence[str], str, dict[str, str], int, bool, timedelta | None], SnubaTSResult
        ],
        top_events: int = 0,
        query_column: str = "count()",
        params: ParamsType | None = None,
        query: str | None = None,
        allow_partial_buckets: bool = False,
        zerofill_results: bool = True,
        comparison_delta: timedelta | None = None,
        additional_query_column: str | None = None,
        dataset: Any | None = None,
    ) -> dict[str, Any]:
        with handle_query_errors():
            with sentry_sdk.start_span(
                op="discover.endpoint", description="base.stats_query_creation"
            ):
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/organization_profiling_functions.py" line="115">

---

The `get_event_stats` function is used within the `get_event_stats_data` function. It takes several parameters including columns, query, params, rollup, zerofill results, and comparison delta. It performs a query for each chunk of top functions and returns the results.

```python
        def get_event_stats(_columns, query, params, _rollup, zerofill_results, _comparison_delta):
            rollup = get_rollup_from_range(params["end"] - params["start"])

            chunks = [
                top_functions["data"][i : i + FUNCTIONS_PER_QUERY]
                for i in range(0, len(top_functions["data"]), FUNCTIONS_PER_QUERY)
            ]

            builders = [
                ProfileTopFunctionsTimeseriesQueryBuilder(
                    dataset=Dataset.Functions,
                    params=params,
                    interval=rollup,
                    top_events=chunk,
                    other=False,
                    query=query,
                    selected_columns=["project.id", "fingerprint"],
                    # It's possible to override the columns via
                    # the `yAxis` qs. So we explicitly ignore the
                    # columns, and hard code in the columns we want.
                    timeseries_columns=[data["function"], "examples()"],
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
