---
title: product-Backfilling Grouping Records for a Project
---
This document will cover the process of backfilling grouping records for a project in Sentry. The process involves several steps:

1. Initialization of the backfill process
2. Fetching events from the Nodestore
3. Sending group and stacktrace data to Seer
4. Submitting the message

Technical document: <SwmLink doc-title="Understanding backfill_seer_grouping_records_for_project">[Understanding backfill_seer_grouping_records_for_project](/.swm/understanding-backfill_seer_grouping_records_for_project.1fv4n129.sw.md)</SwmLink>

# Initialization of Backfill

The backfill process begins with initialization. This step involves logging the start of the process, retrieving the project details from the cache, and checking if the feature is enabled for the project. The last processed group index and project index are also retrieved from Redis or the input parameters. If the feature is not enabled for the project or the project does not exist, the information is logged and the next backfill is called.

# Fetching Events from Nodestore

The next step involves fetching events from the Nodestore. The events are retrieved, processed, and the data is prepared for further steps. The events are fetched using the `lookup_group_data_stacktrace_bulk` function, and then iterated over to extract grouping information and the primary hash.

# Sending Group and Stacktrace to Seer

The group and stacktrace data is then sent to Seer. This is done in a multithreaded manner, processing chunks of data and stacktrace and posting bulk grouping records. The responses from Seer are then aggregated and returned.

# Submitting the Message

The final step in the process is submitting a message. The payload is extracted from the message, billing outcomes are produced, a metric received flag is set for the project, and the message is submitted to the next step.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
