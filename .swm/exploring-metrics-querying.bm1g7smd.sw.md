---
title: Exploring Metrics Querying
---
Querying in Sentry metrics refers to the process of retrieving and manipulating data stored in the metrics system. This is achieved through various modules and classes such as QueryOrder, QueryResult, and QueryExpression, among others.

The QueryOrder module is used to define the order in which data is retrieved from the metrics system. This can be useful when you need to sort data in a specific way, for example, by date or by a specific metric.

The QueryResult module is used to handle the results of a query. This includes the actual data retrieved from the metrics system, as well as any metadata associated with the query.

The QueryExpression module is used to define the actual query that is sent to the metrics system. This includes the metrics to retrieve, the conditions to apply, and the order in which to retrieve the data.

Other modules, such as QueriedMetricsVisitor and QueryType, provide additional functionality for querying data, such as visiting queried metrics and defining different types of queries.

<SwmSnippet path="/src/sentry/sentry_metrics/querying/types.py" line="34">

---

# QueryOrder

The QueryOrder module is used to define the order in which data is retrieved from the metrics system. This can be useful when you need to sort data in a specific way, for example, by date or by a specific metric.

```python
class QueryOrder(Enum):
    """
    Represents the order of the query.
    """

    ASC = "asc"
    DESC = "desc"

    @classmethod
    # Used `Union` because `|` conflicts with the parser.
    def from_string(cls, value: str) -> Union["QueryOrder", None]:
        for v in cls:
            if v.value == value:
                return v

        return None

    def to_snuba_order(self) -> Direction:
        if self == QueryOrder.ASC:
            return Direction.ASC
        elif self == QueryOrder.DESC:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_metrics/querying/data/execution.py" line="569">

---

# QueryResult

The QueryResult module is used to handle the results of a query. This includes the actual data retrieved from the metrics system, as well as any metadata associated with the query.

```python
class PartialQueryResult:
    """
    Represents a partial query result which contains all the queries that are linearly dependent and their results.

    This result is stored in the array of results for each ScheduledQuery that has a next parameter.

    Attributes:
        previous_queries: All the previous queries that have been executed as part of a single list of chained queries,
            defined via the next parameter of ScheduledQuery.
    """

    previous_queries: list[tuple[ScheduledQuery, Mapping[str, Any], bool]]

    def to_query_result(self) -> QueryResult:
        """
        Transforms a PartialQueryResult in a QueryResult by taking the last query that was executed in the list.

        Returns:
            A QueryResult which contains the data of the last query executed as part of this PartialQueryResult.
        """
        # For now, we naively return the first scheduled query and result, but this is just because
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_metrics/querying/data/parsing.py" line="62">

---

# QueryExpression

The QueryExpression module is used to define the actual query that is sent to the metrics system. This includes the metrics to retrieve, the conditions to apply, and the order in which to retrieve the data.

```python
    def generate_queries(
        self,
    ) -> Generator[tuple[QueryExpression, QueryOrder | None, int | None], None, None]:
        """
        Generates multiple queries given a base query.

        Returns:
            A generator which can be used to obtain a query to execute and its details.
        """
        for mql_query in self._mql_queries:
            compiled_mql_query = mql_query.compile()

            query_expression = (
                self._parse_mql(compiled_mql_query.mql)
                # We validate the query.
                .add_visitor(QueryValidationV2Visitor())
                # We inject the environment filter in each timeseries.
                .add_visitor(EnvironmentsInjectionVisitor(self._environments))
                # We transform all `release:latest` filters into the actual latest releases.
                .add_visitor(
                    QueryConditionsCompositeVisitor(
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_metrics/querying/data/api.py" line="29">

---

# Additional Modules

Other modules, such as QueriedMetricsVisitor and QueryType, provide additional functionality for querying data, such as visiting queried metrics and defining different types of queries.

```python
def run_queries(
    mql_queries: Sequence[MQLQuery],
    start: datetime,
    end: datetime,
    interval: int,
    organization: Organization,
    projects: Sequence[Project],
    environments: Sequence[Environment],
    referrer: str,
    query_type: QueryType = QueryType.TOTALS_AND_SERIES,
) -> MQLQueriesResult:
    """
    Runs a list of MQLQuery(s) that are executed in Snuba.

    Returns:
        A MQLQueriesResult object which encapsulates the results of the plan and allows a QueryTransformer
        to be run on the data.
    """
    # We build the basic query that contains the metadata which will be shared across all queries.
    base_query = MetricsQuery(
        start=start,
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
