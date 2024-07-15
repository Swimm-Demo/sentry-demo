---
title: product-Initialization and Loading of Performance Issues
---
This document will cover the process of initializing and loading performance issues in Sentry. The topics we'll cover are:

1. Initializing the process
2. Loading performance issues
3. Querying trace data
4. Augmenting transactions with spans.

Technical document: <SwmLink doc-title="Understanding the `__init__` Method">[Understanding the \`\__init_\_\` Method](/.swm/understanding-the-__init__-method.kfbdumf7.sw.md)</SwmLink>

# Initializing the process

The process begins with the initialization of an instance of a class with specific attributes such as event, errors, children, and performance issues. It also checks if there are any issues associated with the event and based on a specific flag, it decides which method to call to load performance issues.

# Loading performance issues

The next step in the process is to load performance issues. Depending on a specific parameter, it either gets a simple span or fetches more detailed information about the issue occurrences and their spans. The function then appends the performance issues to a list.

# Querying trace data

The process then queries the DiscoverQueryBuilder to get transaction and error data for a given trace_id. It also processes the results to join group IDs from the occurrence dataset to transactions data.

# Augmenting transactions with spans

The final step in the process is to augment the transactions with parent, error, and problem data. It also links transactions, performance issues, and errors.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
