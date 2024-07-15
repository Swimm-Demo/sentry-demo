---
title: product-Event Statistics Retrieval
---
This document will cover the Event Statistics Retrieval feature, which includes:

1. Fetching event statistics
2. Matching conditions for traces
3. Processing results
4. Finalizing results.

Technical document: <SwmLink doc-title="Understanding get_event_stats Function">[Understanding get_event_stats Function](/.swm/understanding-get_event_stats-function.d67g4ybe.sw.md)</SwmLink>

# Fetching Event Statistics

The process begins with the initiation of fetching event statistics. This is the entry point for the retrieval of event statistics. The necessary parameters are initialized and the process of fetching the statistics is started.

# Matching Conditions for Traces

The system fetches traces that match certain conditions. These conditions could be based on metrics or spans. The traces are then refined based on the fetched traces. This step is crucial in ensuring that only relevant traces are considered for the final results.

# Processing Results

The results of the queries are processed. This involves translating column names, processing field metadata, and transforming the result rows. The processed data and metadata are then returned in a dictionary format.

# Finalizing Results

The final results of the process are processed. This involves taking the results of various queries, processing them, and combining them into a list of TraceResult objects. This final list of TraceResult objects is the end product of the Event Statistics Retrieval feature.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
