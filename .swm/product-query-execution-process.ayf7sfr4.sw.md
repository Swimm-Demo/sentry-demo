---
title: product-Query Execution Process
---
This document will cover the process of running a query in the Sentry application, which includes:

1. Preparing the query
2. Transforming the query
3. Retrieving the data
4. Applying additional transformations

Technical document: <SwmLink doc-title="Understanding run_query">[Understanding run_query](/.swm/understanding-run_query.0zsu6ljp.sw.md)</SwmLink>

# Preparing the Query

The process begins with the preparation of the query. This involves setting up the necessary parameters and the query framework. The parameters include the referrer, whether to use cache, and the source of the query. The query framework includes the groupby aliases, which are the raw groupbys. This step is crucial as it sets the stage for the rest of the process.

# Transforming the Query

Once the query is prepared, it is transformed into a metrics query. This involves transforming different parts of the query such as the orderby part and the select part. The orderby part of the query is transformed into a format suitable for a metrics query. Similarly, the select part of the query is also transformed into a format suitable for a metrics query. This step ensures that the query is in the right format for the metrics data retrieval process.

# Retrieving the Data

After the query is transformed, the data retrieval process begins. This involves retrieving time series data for the given query. The function sets up the query parameters and intervals. Depending on the presence of groupby in the metrics query, it either runs an initial query to get the groups or directly builds the Snuba queries. The function then loops through the entities and runs the queries, applying group limit filters if necessary. The results are then converted and returned. This step is crucial as it fetches the required data based on the transformed query.

# Applying Additional Transformations

Once the data is retrieved, additional transformations are applied if necessary. This involves applying transformations specific to certain operations. For example, for the team_key_transaction operation, the transformed metrics query undergoes additional transformations. This step ensures that the retrieved data is in the desired format and ready for use.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
