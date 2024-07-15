---
title: product-Trend Calculation Feature
---
This document will cover the 'Trend Calculation' feature in the Sentry application. We'll cover:

1. The purpose of the trend calculation feature.
2. The process of constructing the necessary columns for trend calculation.
3. The process of retrieving necessary parameters for the trend calculation.
4. The process of handling the retrieval of event stats data.
5. The process of formatting the results of top events timeseries.

Technical document: <SwmLink doc-title="Understanding get_trend_columns Flow">[Understanding get_trend_columns Flow](/.swm/understanding-get_trend_columns-flow.4g2mvima.sw.md)</SwmLink>

# Purpose of the Trend Calculation Feature

The trend calculation feature in Sentry is used to calculate high confidence trends based on user timeseries queries. This feature is essential for users to understand the trends in their data over time, which can help them make informed decisions about their application's performance and reliability.

# Constructing Necessary Columns for Trend Calculation

The first step in the trend calculation process is to construct the necessary columns for the calculation. This involves selecting a baseline function, a column, and a middle value. The system checks if the selected baseline function is supported, and then constructs the necessary columns for the t-test and other calculations. The constructed columns are then returned as a list.

# Retrieving Necessary Parameters for the Trend Calculation

The next step is to retrieve the necessary parameters for the trend calculation. This involves checking if the organization has the necessary feature for trend calculation. If it does, the system retrieves the necessary parameters from the request and the organization. It also handles the parsing and validation of the request parameters.

# Handling the Retrieval of Event Stats Data

Once the necessary parameters have been retrieved, the system handles the retrieval of event stats data. This involves constructing a `TrendQueryBuilder` object and using it to perform the trend query. The results of the query are then processed and returned.

# Formatting the Results of Top Events Timeseries

The final step in the trend calculation process is to format the results of the top events timeseries. This involves dividing the top functions data into chunks and running queries on each chunk. The results of these queries are then formatted and returned to the user.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
