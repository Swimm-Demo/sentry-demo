---
title: product-Database Insights Display Feature
---
This document will cover the Database Insights Display feature of the sentry-demo repository. We'll cover:

1. The purpose of the Database Insights Display feature
2. How data is fetched and managed
3. User onboarding and data tracking
4. Data processing and display

Technical document: <SwmLink doc-title="Understanding the DatabaseLandingPage">[Understanding the DatabaseLandingPage](/.swm/understanding-the-databaselandingpage.avu339al.sw.md)</SwmLink>

# Purpose of the Database Insights Display feature

The Database Insights Display feature is a central component that orchestrates the display of database insights. It leverages several hooks to fetch and manage data, and handles user interactions such as search and navigation.

# Data Fetching and Management

The Database Insights Display feature fetches span metrics data from the Discover service to populate the database insights charts and tables. It also tracks analytics events related to the database insights. It checks if the module has ever sent data and sends an analytics event accordingly.

# User Onboarding and Data Tracking

The Database Insights Display feature determines if the user is in the onboarding process. If the user is onboarding, the feature returns the onboarding project. This information is used to customize the user interface accordingly. The feature also checks if the current project selection has received a first insight span. This information is used to determine if the module has ever sent data, which is then tracked.

# Data Processing and Display

The Database Insights Display feature processes the data into a specific format. It uses the `useSpanMetricsSeries` function to pass the options and referrer to `useDiscoverSeries` along with a specific dataset. It then uses the `useWrappedDiscoverTimeseriesQuery` function to get the result and parses the data into a specific format.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
