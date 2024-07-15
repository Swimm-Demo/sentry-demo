---
title: product-Span Details Display Feature
---
This document will cover the 'Span Details Display' feature in the Sentry application. We'll cover:

1. Fetching project data
2. Displaying span details
3. Traversing through child transactions of a span
4. Generating the URL for the results view page.

Technical document: <SwmLink doc-title="Understanding NewTraceDetailsSpanDetail">[Understanding NewTraceDetailsSpanDetail](/.swm/understanding-newtracedetailsspandetail.z6yupf76.sw.md)</SwmLink>

# Fetching Project Data

The application fetches project data using a feature called 'useProjects'. This feature retrieves project data from the ProjectsStore, which is a repository of all project data. It allows the application to select specific project slugs and search for more projects that may not be in the project store. This is crucial for the 'Span Details Display' feature as it needs to find the project related to the event.

# Displaying Span Details

The application displays the details of a span in a trace. A span is a single operation within a trace, like a SQL query or a function call. The application checks if the span is a gap span and renders the appropriate details. It also calculates various metrics related to the span such as duration, start and end timestamps, and unknown keys. This provides the user with a detailed view of the span.

# Traversing Child Transactions

The application allows users to traverse through child transactions of a span. A child transaction is a transaction that is started by another transaction. The application checks if there are child transactions and creates an EventView object for them. This allows the user to navigate through the child transactions of a span, providing a deeper understanding of the trace.

# Generating Results View URL

The application generates the URL for the results view page. The results view page displays the results of a search or a set of events. The URL is generated based on the properties of the EventView object, which includes parameters such as slugs, search, limit, lastSearch, and cursor. This allows the user to revisit the results view page with the same parameters.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
