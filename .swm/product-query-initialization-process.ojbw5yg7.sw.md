---
title: product-Query Initialization Process
---
This document will cover the process of initializing a query in the Sentry application. We'll cover:

1. How the initialization process starts
2. How the query parameters are parsed
3. How the query string is parsed
4. How the user tag is fetched for a given key-value pair

Technical document: <SwmLink doc-title="Understanding __init__ Function">[Understanding \__init_\_ Function](/.swm/understanding-__init__-function.iw383sls.sw.md)</SwmLink>

# Initialization of Query

The initialization process starts when an object of a class is instantiated. This is used to set up the QueryBuilder class with the necessary parameters such as projects, query parameters, and pagination arguments. It also sets up various properties of the class.

# Parsing of Query Parameters

The query parameters are parsed during the initialization process. This includes the 'orderBy' query parameter. The system iterates over the 'orderBy' parameters, determines the direction of ordering (ascending or descending), and parses the field for ordering. The result is a list of objects.

# Parsing of Query String

The query string is parsed to return a structured dictionary of query term values. The system tokenizes the query and processes each token based on its key.

# Fetching User Tag

The user tag is fetched for a given key-value pair. The system fetches the user object for the given projects and filters. It performs a query and then finds unique user objects from the results.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
