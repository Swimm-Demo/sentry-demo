---
title: product-Data Query Initialization and Resolution in Sentry
---
This document will cover the **init** flow in the Sentry product, which includes:

1. Initializing various attributes of the QueryBuilder class
2. Converting passed parameters into a dataclass
3. Resolving various aspects of a query
4. Constructing a list of Snql Columns or Functions based on the provided list of discover fields
5. Prioritizing keys included as URL parameters over the same keys included in the search
6. Resolving boolean conditions
7. Converting an aggregate filter into a condition.

Technical document: <SwmLink doc-title="__init__ flow">[\__init_\_ flow](/.swm/__init__-flow.0dn7zcg1.sw.md)</SwmLink>

# Initializing various attributes of the QueryBuilder class

The **init** function is a special method in Python classes, often referred to as the class constructor. This function is called when an object is created from a class and it allows the class to initialize the attributes of the class. In this case, the **init** function is used to initialize various attributes of the QueryBuilder class such as dataset, params, config, snuba_params, query, selected_columns, groupby_columns, equations, orderby, limit, offset, limitby, turbo, sample_rate, array_join, and entity.

# Converting passed parameters into a dataclass

The \_dataclass_params function is a helper function used within the **init** function. Its purpose is to convert the passed parameters into a dataclass. This function takes in two parameters: snuba_params and params. If snuba_params is not None, it returns snuba_params directly. Otherwise, it constructs a new SnubaParams object based on the provided params.

# Resolving various aspects of a query

The resolve_query function is responsible for resolving various aspects of a query such as time conditions, conditions, parameters, columns, order by, and group by. This function is called within the **init** function.

# Constructing a list of Snql Columns or Functions based on the provided list of discover fields

The resolve_select function is called within resolve_query. It constructs a list of Snql Columns or Functions based on the provided list of discover fields. It also sets a tag to indicate if the query has equations.

# Prioritizing keys included as URL parameters over the same keys included in the search

The resolve_params function is also called within resolve_query. It prioritizes keys included as URL parameters over the same keys included in the search. It also checks for various conditions such as date range, project IDs, and environments.

# Resolving boolean conditions

The resolve_boolean_conditions function takes a list of parsed terms and returns two lists of conditions. It checks if there are any invalid queries and raises an error if found. It then splits the terms based on the presence of OR and AND operators and recursively resolves the boolean conditions for each split.

# Converting an aggregate filter into a condition

The convert_aggregate_filter_to_condition function takes an aggregate filter and converts it into a condition. It first gets the function result type of the filter key name and then resolves the measurement value if a unit is found. It then checks the operator of the filter and returns the appropriate condition.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
