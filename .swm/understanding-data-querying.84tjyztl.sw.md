---
title: Understanding Data Querying
---
In the context of the sentry-demo repository, 'Data' refers to the information that is being processed and manipulated by the querying system. This data is primarily handled through the use of queries, which are defined and executed in various parts of the codebase.

The data is processed through a series of steps, starting with the generation of queries. The 'generate_queries' function in 'src/sentry/sentry_metrics/querying/data/parsing.py' is responsible for this, creating multiple queries based on a base query.

These queries are then compiled and parsed using the 'compile' and '\_parse_mql' functions respectively. The parsed queries are then validated and transformed through the use of visitors, which are added using the 'add_visitor' function.

The 'run_queries' function in 'src/sentry/sentry_metrics/querying/data/api.py' is responsible for executing a list of these queries. It does this by building a base query with shared metadata, parsing the query plan to obtain a series of queries, and then running preparation steps on these queries.

The data is then scheduled for execution using the 'schedule' function, and the request to execute the query is built using the '\_build_request' function. If a query is empty, an empty QueryResult is created using the 'empty_from' function.

Finally, the results of the queries are processed and returned. This entire process allows for the efficient and flexible handling of data within the sentry-demo repository.

<SwmSnippet path="/src/sentry/sentry_metrics/querying/data/parsing.py" line="62">

---

# Generating Queries

The 'generate_queries' function is responsible for creating multiple queries based on a base query. These queries are then compiled and parsed using the 'compile' and '\_parse_mql' functions respectively.

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

# Running Queries

The 'run_queries' function is responsible for executing a list of these queries. It does this by building a base query with shared metadata, parsing the query plan to obtain a series of queries, and then running preparation steps on these queries.

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

<SwmSnippet path="/src/sentry/sentry_metrics/querying/data/execution.py" line="821">

---

# Scheduling and Building Requests

The data is then scheduled for execution using the 'schedule' function, and the request to execute the query is built using the '\_build_request' function.

```python
    def schedule(self, intermediate_query: IntermediateQuery, query_type: QueryType):
        """
        Lazily schedules an IntermediateQuery for execution and runs initialization code for each ScheduledQuery.
        """
        # By default, we always want to have a totals query.
        totals_query = ScheduledQuery(
            type=ScheduledQueryType.TOTALS,
            metrics_query=intermediate_query.metrics_query,
            order=intermediate_query.order,
            limit=intermediate_query.limit,
            unit_family=intermediate_query.unit_family,
            unit=intermediate_query.unit,
            scaling_factor=intermediate_query.scaling_factor,
            mappers=intermediate_query.mappers,
        )

        # In case the user chooses to run also a series query, we will duplicate the query and chain it after totals.
        series_query = None
        if query_type == QueryType.TOTALS_AND_SERIES:
            series_query = replace(totals_query, type=ScheduledQueryType.SERIES)

```

---

</SwmSnippet>

# Data Handling Functions

This section will cover the main functions involved in the handling of data in the sentry-demo repository.

<SwmSnippet path="/src/sentry/sentry_metrics/querying/data/parsing.py" line="62">

---

## generate_queries

The 'generate_queries' function is responsible for creating multiple queries based on a base query.

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

## run_queries

The 'run_queries' function is responsible for executing a list of these queries. It does this by building a base query with shared metadata, parsing the query plan to obtain a series of queries, and then running preparation steps on these queries.

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

<SwmSnippet path="/src/sentry/sentry_metrics/querying/data/execution.py" line="821">

---

## schedule

The 'schedule' function is used to lazily schedule an IntermediateQuery for execution and runs initialization code for each ScheduledQuery.

```python
    def schedule(self, intermediate_query: IntermediateQuery, query_type: QueryType):
        """
        Lazily schedules an IntermediateQuery for execution and runs initialization code for each ScheduledQuery.
        """
        # By default, we always want to have a totals query.
        totals_query = ScheduledQuery(
            type=ScheduledQueryType.TOTALS,
            metrics_query=intermediate_query.metrics_query,
            order=intermediate_query.order,
            limit=intermediate_query.limit,
            unit_family=intermediate_query.unit_family,
            unit=intermediate_query.unit,
            scaling_factor=intermediate_query.scaling_factor,
            mappers=intermediate_query.mappers,
        )

        # In case the user chooses to run also a series query, we will duplicate the query and chain it after totals.
        series_query = None
        if query_type == QueryType.TOTALS_AND_SERIES:
            series_query = replace(totals_query, type=ScheduledQueryType.SERIES)

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_metrics/querying/data/execution.py" line="640">

---

## \_build_request

The '\_build_request' function is used to build a Snuba Request given a MetricsQuery to execute.

```python
    def _build_request(self, query: MetricsQuery) -> Request:
        """
        Builds a Snuba Request given a MetricsQuery to execute.

        Returns:
            A Snuba Request object which contains the query to execute.
        """
        return Request(
            # The dataset used here is arbitrary, since the `run_query` function will infer it internally.
            dataset=Dataset.Metrics.value,
            query=query,
            app_id="default",
            tenant_ids={"referrer": self._referrer, "organization_id": self._organization.id},
        )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_metrics/querying/data/execution.py" line="345">

---

## empty_from

The 'empty_from' function is used to create a new empty QueryResult from a ScheduledQuery. If a query is empty, an empty QueryResult is created using this function.

```python
    def empty_from(cls, scheduled_query: ScheduledQuery) -> "QueryResult":
        """
        Creates a new empty QueryResult from a ScheduledQuery.

        The idea behind using an empty query result is to be able to represent the values of queries that are not run
        by the executor (for example because they are empty). Representing such queries as empty results in a cleaner
        implementation of the downstream code since no modifications need to be done. It's not ideal but it simplifies
        the code quite a bit.

        Returns:
            An empty QueryResult which contains no data.
        """
        series_query = None
        totals_query = None

        # For now, we naively assume that if a query has a next, the first is a totals query and the second is a series
        # query.
        if scheduled_query.next is not None:
            totals_query = scheduled_query
            series_query = scheduled_query.next
        else:
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
