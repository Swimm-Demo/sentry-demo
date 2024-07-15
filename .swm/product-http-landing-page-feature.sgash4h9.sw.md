---
title: product-HTTP Landing Page Feature
---
This document will explain the HTTP Landing Page feature in Sentry. We'll cover:

1. The purpose of the HTTP Landing Page
2. How data is fetched and managed
3. The role of various hooks in data fetching and management
4. The process of rendering the HTTP Landing Page's UI
5. The significance of analytics tracking in the HTTP Landing Page.

Technical document: <SwmLink doc-title="Understanding the HTTPLandingPage">[Understanding the HTTPLandingPage](/.swm/understanding-the-httplandingpage.o6to38rd.sw.md)</SwmLink>

# Purpose of the HTTP Landing Page

The HTTP Landing Page is a central component in Sentry's user interface. It provides a comprehensive view of HTTP data, allowing users to monitor and analyze HTTP performance metrics. This feature is crucial for developers and teams who need to keep track of their application's HTTP performance.

# Fetching and Managing Data

The HTTP Landing Page uses several hooks to fetch and manage data. These hooks retrieve necessary information such as the organization, location, and onboarding project. They also set up filters for charts and tables, define a handler for search functionality, and fetch data for throughput, duration, and response code charts as well as the domains list. This process ensures that the HTTP Landing Page displays the most relevant and up-to-date data.

# Role of Hooks in Data Fetching and Management

Hooks play a crucial role in fetching and managing data for the HTTP Landing Page. For instance, the 'useSpanMetrics' hook fetches span metrics data, the 'useHasDataTrackAnalytics' hook tracks analytics, and the 'useOnboardingProject' hook retrieves the onboarding project. These hooks work together to ensure that the HTTP Landing Page has all the necessary data to provide a comprehensive view of HTTP performance.

# Rendering the HTTP Landing Page's UI

Once the data is fetched and managed, the HTTP Landing Page's UI is rendered. This UI provides a visual representation of the HTTP data, making it easier for users to understand and analyze the performance metrics. The UI includes charts for throughput, duration, and response codes, as well as a domains list.

# Analytics Tracking in the HTTP Landing Page

Analytics tracking is an essential part of the HTTP Landing Page. It uses the 'useHasDataTrackAnalytics' hook to track user interactions with the page. This data is valuable for understanding user behavior and improving the feature based on user needs and preferences.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
