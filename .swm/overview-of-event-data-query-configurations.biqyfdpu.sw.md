---
title: Overview of Event Data Query Configurations
---
Datasets in Sentry's event search are configurations that define how event data is queried. They are represented by the `DatasetConfig` class, which is imported from the `sentry.search.events.datasets.base` module in various files within the `sentry.search.events.datasets` directory.

Each dataset configuration is specific to a certain type of event data. For example, there are separate dataset configurations for metrics, sessions, profiles, and other types of event data. These configurations are used when querying event data to ensure that the correct fields, filters, and functions are applied.

The `DatasetConfig` class is not defined within the `sentry.search.events.datasets` directory itself, but is imported from the `sentry.search.events.datasets.base` module. This suggests that the `DatasetConfig` class is a base class that provides common functionality for all dataset configurations.

<SwmSnippet path="/src/sentry/search/events/datasets/base.py" line="21">

---

# DatasetConfig Class

The `DatasetConfig` class is a base class that provides common functionality for all dataset configurations. It has a `subscriptables_with_index` attribute which is a set of strings.

```python
    missing_function_error: ClassVar[type[Exception]] = InvalidSearchQuery
    optimize_wildcard_searches = False
    subscriptables_with_index: set[str] = set()

    def __init__(self, builder: BaseQueryBuilder):
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/search/events/datasets/profiles.py" line="195">

---

# Function Converter

The `function_converter` method in the `DatasetConfig` class is used to map function names to their corresponding `SnQLFunction` instances. This is used when constructing a query to ensure that the correct functions are applied to the data.

```python
    def function_converter(self) -> Mapping[str, SnQLFunction]:
        return {
            function.name: function
            for function in [
                # TODO: A lot of this is duplicated from the discover dataset.
                # Ideally, we refactor it to be shared across datasets.
                SnQLFunction(
                    "last_seen",
                    snql_aggregate=lambda _, alias: Function(
                        "max",
                        [self.builder.column("timestamp")],
                        alias,
                    ),
                    default_result_type="date",
                    redundant_grouping=True,
                ),
                SnQLFunction(
                    "latest_event",
                    snql_aggregate=lambda _, alias: Function(
                        "argMax",
                        [self.builder.column("id"), self.builder.column("timestamp")],
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/search/events/datasets/base.py" line="50">

---

# Reflective Result Type

The `reflective_result_type` method in the `DatasetConfig` class is used to determine the type of the metric based on the function arguments and parameter values. It defaults to 'duration' if the field type is not found.

```python
    def reflective_result_type(
        self, index: int = 0
    ) -> Callable[[list[fields.FunctionArg], dict[str, Any]], str]:
        """Return the type of the metric, default to duration

        based on fields.reflective_result_type, but in this config since we need the _custom_measurement_cache
        """

        def result_type_fn(
            function_arguments: list[fields.FunctionArg], parameter_values: dict[str, Any]
        ) -> str:
            argument = function_arguments[index]
            value = parameter_values[argument.name]
            if (field_type := self.builder.get_field_type(value)) is not None:  # type: ignore[attr-defined]
                return field_type
            else:
                return argument.get_type(value)

        return result_type_fn
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/search/events/datasets/profiles.py" line="377">

---

# Resolve Percentile

The `_resolve_percentile` method in the `DatasetConfig` class is used to construct a `Function` instance for calculating percentiles. It takes in arguments, an alias, and an optional fixed percentile value.

```python
    def _resolve_percentile(
        self,
        args: Mapping[str, str | Column | SelectType | int | float],
        alias: str,
        fixed_percentile: float | None = None,
    ) -> SelectType:
        return (
            Function(
                "max",
                [args["column"]],
                alias,
            )
            if fixed_percentile == 1
            else Function(
                f'quantile({fixed_percentile if fixed_percentile is not None else args["percentile"]})',
                [args["column"]],
                alias,
            )
        )
```

---

</SwmSnippet>

# Dataset Functions

The functions in the datasets are used to manipulate and query event data. They include functions for resolving project threshold configurations, calculating percentiles, comparing averages, and more. These functions are essential for querying and analyzing event data in Sentry.

<SwmSnippet path="/src/sentry/search/events/datasets/function_aliases.py" line="19">

---

## resolve_project_threshold_config

The `resolve_project_threshold_config` function is used to resolve the project threshold configuration. It takes in a tag value resolver, a column name resolver, a list of project IDs, and an organization ID. It returns a `SelectType` object that represents the project threshold configuration.

```python
def resolve_project_threshold_config(
    # See resolve_tag_value signature
    tag_value_resolver: Callable[[UseCaseID | UseCaseKey, int, str], int | str | None],
    # See resolve_tag_key signature
    column_name_resolver: Callable[[UseCaseID | UseCaseKey, int, str], str],
    project_ids: Sequence[int],
    org_id: int,
    use_case_id: UseCaseID | None = None,
) -> SelectType:
    """
    Shared function that resolves the project threshold configuration used by both snuba/metrics
    and search/events/datasets.
    """

    project_threshold_configs = ProjectTransactionThreshold.filter(
        organization_id=org_id,
        project_ids=project_ids,
        order_by=["project_id"],
        value_list=["project_id", "metric"],
    )

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/search/events/datasets/function_aliases.py" line="179">

---

## resolve_metrics_percentile

The `resolve_metrics_percentile` function is used to calculate the percentile of a metric. It takes in a mapping of arguments and an alias, and optionally a fixed percentile. It returns a `SelectType` object that represents the calculated percentile.

```python
def resolve_metrics_percentile(
    args: Mapping[str, str | Column | SelectType | int | float],
    alias: str | None,
    fixed_percentile: float | None = None,
    extra_conditions: list[Function] | None = None,
) -> SelectType:
    if fixed_percentile is None:
        fixed_percentile = args["percentile"]
    if fixed_percentile not in constants.METRIC_PERCENTILES:
        raise IncompatibleMetricsQuery("Custom quantile incompatible with metrics")

    conditions = [Function("equals", [Column("metric_id"), args["metric_id"]])]
    if extra_conditions is not None:
        conditions.extend(extra_conditions)

    if len(conditions) == 2:
        condition = Function("and", conditions)
    elif len(conditions) != 1:
        # Need to chain multiple and functions here to allow more than 2 conditions (ie. and(and(a, b), c))
        raise InvalidSearchQuery("Only 1 additional condition is currently available")
    else:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/search/events/datasets/function_aliases.py" line="263">

---

## resolve_avg_compare

The `resolve_avg_compare` function is used to calculate the percent change between two averages. It takes in a column resolver, a mapping of arguments, and an alias. It returns a `SelectType` object that represents the percent change.

```python
def resolve_avg_compare(
    column_resolver: Callable[[str], Column],
    args: Mapping[str, str | Column | SelectType | int | float],
    alias: str | None = None,
) -> SelectType:
    return resolve_percent_change(
        resolve_avg_compare_if(column_resolver, args, "first_value", alias),
        resolve_avg_compare_if(column_resolver, args, "second_value", alias),
        alias,
    )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/search/events/datasets/function_aliases.py" line="275">

---

## resolve_metrics_layer_percentile

The `resolve_metrics_layer_percentile` function is used to calculate the percentile of a metric in the metrics layer. It takes in a mapping of arguments, an alias, a function to resolve the MRI, and optionally a fixed percentile. It returns a `SelectType` object that represents the calculated percentile.

```python
def resolve_metrics_layer_percentile(
    args: Mapping[str, str | Column | SelectType | int | float],
    alias: str,
    resolve_mri: Callable[[str], Column],
    fixed_percentile: float | None = None,
) -> SelectType:
    # TODO: rename to just resolve_metrics_percentile once the non layer code can be retired
    if fixed_percentile is None:
        fixed_percentile = args["percentile"]
    if fixed_percentile not in constants.METRIC_PERCENTILES:
        raise IncompatibleMetricsQuery("Custom quantile incompatible with metrics")
    column = resolve_mri(args["column"])
    return (
        Function(
            "max",
            [
                column,
            ],
            alias,
        )
        if fixed_percentile == 1
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/search/events/datasets/function_aliases.py" line="306">

---

## resolve_division

The `resolve_division` function is used to divide one `SelectType` object by another. It takes in a dividend, a divisor, and an alias, and optionally a fallback value. It returns a `SelectType` object that represents the result of the division.

```python
def resolve_division(
    dividend: SelectType, divisor: SelectType, alias: str, fallback: Any | None = None
) -> SelectType:
    return Function(
        "if",
        [
            Function(
                "greater",
                [divisor, 0],
            ),
            Function(
                "divide",
                [
                    dividend,
                    divisor,
                ],
            ),
            fallback,
        ],
        alias,
    )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/search/events/datasets/function_aliases.py" line="329">

---

## resolve_rounded_timestamp

The `resolve_rounded_timestamp` function is used to round a timestamp to the nearest interval. It takes in an interval and an alias, and optionally a timestamp column. It returns a `SelectType` object that represents the rounded timestamp.

```python
def resolve_rounded_timestamp(
    interval: int, alias: str, timestamp_column: str = "timestamp"
) -> SelectType:
    return Function(
        "toUInt32",
        [
            Function(
                "multiply",
                [
                    Function(
                        "intDiv",
                        [Function("toUInt32", [Column(timestamp_column)]), interval],
                    ),
                    interval,
                ],
            ),
        ],
        alias,
    )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/search/events/datasets/function_aliases.py" line="350">

---

## resolve_random_samples

The `resolve_random_samples` function is used to get a random sample of `SelectType` objects. It takes in a list of columns, an alias, an offset, a limit, and optionally a size. It returns a `SelectType` object that represents the random sample.

```python
def resolve_random_samples(
    columns: list[SelectType],
    alias: str,
    offset: int,
    limit: int,
    size: int = 1,
) -> SelectType:
    seed_str = f"{offset}-{limit}"
    seed = fnv1a_32(seed_str.encode("utf-8"))
    return Function(
        f"groupArraySample({size}, {seed})",
        [Function("tuple", columns)],
        alias,
    )
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
