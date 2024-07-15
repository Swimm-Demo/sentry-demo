---
title: product-Optimized Search Query Flow in Sentry
---
This document will cover the Optimized Search Query Flow in Sentry, which includes:

1. Processing of search parameters
2. Selection of search strategy
3. Execution of search query
4. Pagination and aggregation of results.

Technical document: <SwmLink doc-title="Understanding the Optimized Search Query Flow">[Understanding the Optimized Search Query Flow](/.swm/understanding-the-optimized-search-query-flow.e8cky3lj.sw.md)</SwmLink>

# Processing of Search Parameters

The search parameters such as fields, search filters, environments, sort order, pagination details, organization, project ids, and time period are processed. Special filters like 'viewed_by_me' are handled separately as they are not valid Snuba fields but are convenience aliases for the frontend.

# Selection of Search Strategy

Based on the processed parameters, an appropriate strategy is chosen to execute the search query. The system first tries to use the materialized view strategy. If it cannot handle the parameters, it falls back to the scalar strategy. If the scalar strategy also cannot handle the parameters, it falls back to the aggregated strategy.

# Execution of Search Query

The search query is executed using the selected strategy. The search filters are converted into snuba conditions and an attempt is made to compress the conditions for query optimization.

# Pagination and Aggregation of Results

The result of the query is then paginated and the final aggregation step is performed. The replay ids are used as the only filter in the aggregation step.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
