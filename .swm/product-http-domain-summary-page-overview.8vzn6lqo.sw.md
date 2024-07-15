---
title: product-HTTP Domain Summary Page Overview
---
This document will cover the HTTP Domain Summary Page feature in the Sentry application. We'll cover:

1. The purpose of the HTTP Domain Summary Page
2. How data is fetched and processed for the page
3. The flow of data fetching and processing
4. The API requests involved in data fetching

Technical document: <SwmLink doc-title="Understanding HTTPDomainSummaryPage">[Understanding HTTPDomainSummaryPage](/.swm/understanding-httpdomainsummarypage.r6f92ucm.sw.md)</SwmLink>

# HTTP Domain Summary Page

The HTTP Domain Summary Page is a key component in the Sentry application. It provides a detailed overview of HTTP domain metrics, including throughput data, duration data, response code data, and a list of transactions. This information is crucial for users to understand the performance of their applications.

# Fetching and Processing Data

To display the necessary data on the HTTP Domain Summary Page, several hooks and functions are used. These hooks fetch span metrics data and project data, which are then processed and used to render the page. This ensures that the most up-to-date and relevant data is always displayed on the page.

# Data Flow

The data flow starts with fetching the necessary data using specific hooks. The fetched data is then processed and used to render the HTTP Domain Summary Page. This flow ensures that the data displayed on the page is always accurate and up-to-date.

# API Requests

The data fetching process involves making API requests. These requests fetch the necessary data for the HTTP Domain Summary Page. Depending on the configuration, the requests may be batched or made directly. This ensures that the data fetching process is efficient and scalable.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
