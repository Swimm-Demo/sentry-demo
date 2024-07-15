---
title: product-On-Demand Metrics Selection Process
---
This document will cover the 'On-Demand Metrics Selection' process in Sentry. We'll cover:

1. The purpose of On-Demand Metrics Selection
2. The decision-making process for using On-Demand Metrics
3. The process of parsing and validating the search query
4. The process of checking if the search query is supported by On-Demand Metrics.

Technical document: <SwmLink doc-title="Understanding _should_use_on_demand_metrics">[Understanding \_should_use_on_demand_metrics](/.swm/understanding-_should_use_on_demand_metrics.bft6gkcg.sw.md)</SwmLink>

# Purpose of On-Demand Metrics Selection

The On-Demand Metrics Selection process is a crucial part of Sentry's performance monitoring platform. It determines whether to use on-demand metrics based on the aggregate and query. This decision affects the accuracy and efficiency of the performance monitoring.

# Decision-Making Process for Using On-Demand Metrics

The decision to use on-demand metrics is based on several factors. First, it checks if the aggregate and query are supported by on-demand metrics but not by standard metrics. It also checks if the dataset is supported and if the aggregate components can be extracted. If all these conditions are met, on-demand metrics are used.

# Parsing and Validating the Search Query

The search query is parsed and validated to ensure it is in the correct format and contains valid data. This process involves checking if the aggregate is a function and if it is, parsing the arguments and returning the function, arguments, and alias. If the aggregate is not a function, an error is raised.

# Checking if the Search Query is Supported by On-Demand Metrics

After parsing and validating the search query, it is checked to see if it is supported by on-demand metrics. This involves checking if any of the supplied tokens contain search filters that can't be handled by standard metrics. If a token is not supported, it is not included in the on-demand metrics.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
