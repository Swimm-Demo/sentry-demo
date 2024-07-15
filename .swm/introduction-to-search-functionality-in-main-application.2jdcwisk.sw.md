---
title: Introduction to Search Functionality in Main Application
---
Search in the Sentry application is a comprehensive feature that allows users to query and retrieve specific data from the system. It is implemented across various entities such as projects, issues, and events. The search functionality is primarily powered by Snuba, Sentry's own database abstraction layer over ClickHouse. This allows for efficient and flexible querying of event data.

The search functionality is implemented using various Python functions and classes. For example, the `query` function in `src/sentry/search/snuba/executors.py` is a core part of the search functionality. It takes in various parameters like projects, environments, and search filters, and constructs a query to fetch the required data.

Search filters are used to narrow down the search results. These filters are defined in `src/sentry/search/snuba/executors.py` and can include parameters like date ranges, event types, and specific keywords. The `get_search_filter` function is used to find the value of a search filter with a specific name and operator.

The search functionality also supports complex queries like searching for specific versions of releases using semver (Semantic Versioning) queries. This is handled by the `_semver_filter_converter` function in `src/sentry/search/events/filter.py`.

In addition to the basic search functionality, Sentry also provides suggested search results. This is handled by the `get_suggested` function in `src/sentry/search/snuba/executors.py`. It returns search results based on the user's past activity and other factors.

The search functionality is not limited to the Sentry web interface. It is also exposed via the Sentry API, allowing users to perform search queries programmatically.

<SwmSnippet path="/src/sentry/search/snuba/executors.py" line="769">

---

# Query Function

The `query` function is a core part of the search functionality. It takes in various parameters like projects, environments, and search filters, and constructs a query to fetch the required data.

```python
    def query(
        self,
        projects: Sequence[Project],
        retention_window_start: datetime | None,
        group_queryset: BaseQuerySet,
        environments: Sequence[Environment] | None,
        sort_by: str,
        limit: int,
        cursor: Cursor | None,
        count_hits: bool,
        paginator_options: Mapping[str, Any] | None,
        search_filters: Sequence[SearchFilter] | None,
        date_from: datetime | None,
        date_to: datetime | None,
        max_hits: int | None = None,
        referrer: str | None = None,
        actor: Any | None = None,
        aggregate_kwargs: TrendsSortWeights | None = None,
    ) -> CursorResult[Group]:
        now = timezone.now()
        end = None
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/search/snuba/executors.py" line="146">

---

# Search Filters

Search filters are used to narrow down the search results. These filters are defined in `src/sentry/search/snuba/executors.py` and can include parameters like date ranges, event types, and specific keywords. The `get_search_filter` function is used to find the value of a search filter with a specific name and operator.

```python
def get_search_filter(
    search_filters: Sequence[SearchFilter] | None, name: str, operator: str
) -> Any | None:
    """
    Finds the value of a search filter with the passed name and operator. If
    multiple values are found, returns the most restrictive value
    :param search_filters: collection of `SearchFilter` objects
    :param name: Name of the field to find
    :param operator: '<', '>' or '='
    :return: The value of the field if found, else None
    """
    if not search_filters:
        return None
    assert operator in ("<", ">", "=", "IN")
    comparator = max if operator.startswith(">") else min
    found_val = None
    for search_filter in search_filters:
        # Note that we check operator with `startswith` here so that we handle
        # <, <=, >, >=
        if search_filter.key.name == name and search_filter.operator.startswith(operator):
            val = search_filter.value.raw_value
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/search/events/filter.py" line="356">

---

# Semver Filter Converter

The search functionality also supports complex queries like searching for specific versions of releases using semver (Semantic Versioning) queries. This is handled by the `_semver_filter_converter` function.

```python
def _semver_filter_converter(
    search_filter: SearchFilter,
    name: str,
    params: Mapping[str, int | str | datetime] | None,
) -> tuple[str, str, Sequence[str]]:
    """
    Parses a semver query search and returns a snuba condition to filter to the
    requested releases.

    Since we only have semver information available in Postgres currently, we query
    Postgres and return a list of versions to include/exclude. For most customers this
    will work well, however some have extremely large numbers of releases, and we can't
    pass them all to Snuba. To try and serve reasonable results, we:
     - Attempt to query based on the initial semver query. If this returns
       MAX_SEMVER_SEARCH_RELEASES results, we invert the query and see if it returns
       fewer results. If so, we use a `NOT IN` snuba condition instead of an `IN`.
     - Order the results such that the versions we return are semantically closest to
       the passed filter. This means that when searching for `>= 1.0.0`, we'll return
       version 1.0.0, 1.0.1, 1.1.0 before 9.x.x.
    """
    if not params or "organization_id" not in params:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/search/snuba/executors.py" line="1277">

---

# Suggested Search Results

In addition to the basic search functionality, Sentry also provides suggested search results. This is handled by the `get_suggested` function. It returns search results based on the user's past activity and other factors.

```python
    def get_suggested(self, search_filter: SearchFilter) -> Condition:
        """
        Returns the suggested lookup for a search filter.
        """
        attr_entity = self.entities["attrs"]
        users = filter(lambda x: isinstance(x, RpcUser), search_filter.value.raw_value)
        user_ids = [user.id for user in users]
        teams = filter(lambda x: isinstance(x, Team), search_filter.value.raw_value)
        team_ids = [team.id for team in teams]

        operator = Op.NOT_IN if search_filter.is_negation else Op.IN
        null_check_operator = Op.IS_NULL if search_filter.is_negation else Op.IS_NOT_NULL

        conditions = []
        if user_ids:
            suspect_commit_user = Condition(
                Column("owner_suspect_commit_user_id", attr_entity), operator, user_ids
            )
            ownership_rule_user = Condition(
                Column("owner_ownership_rule_user_id", attr_entity), operator, user_ids
            )
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
