---
title: product-get_access_token Flow
---
This document will cover the 'get_access_token' flow, which includes:

1. The initiation of the OAuth flow and access token retrieval
2. Handling of incoming requests and assignee changes
3. Synchronization of group assignees and assignment of users to groups
4. Deassignment of groups and cache invalidation
5. Project deletion and saving with unique identifiers.

Technical document: <SwmLink doc-title="get_access_token flow">[get_access_token flow](/.swm/get_access_token-flow.gqhdbxbu.sw.md)</SwmLink>

# Initiation of the OAuth flow and access token retrieval

The 'get_access_token' function initiates the OAuth flow. It uses the verifier and request token from the first step to retrieve an access token. If the verifier is not provided, an error is raised. The function then constructs an OAuth1 object with the necessary parameters and makes a POST request to the access token URL. The response is parsed and returned as a dictionary.

# Handling of incoming requests and assignee changes

The 'post' function is triggered upon receiving a request. It first clears any existing tags and context. It then attempts to get the integration from the token provided in the request. If the token is invalid, it logs a warning and returns a 400 response. If the request data does not contain a 'changelog', it logs an info message and returns a response. If the data does contain a 'changelog', it calls the 'handle_assignee_change' function.

# Synchronization of group assignees and assignment of users to groups

The 'sync_group_assignee_inbound' function assigns linked groups to matching users. It first checks if there are any affected groups. If there are none, it logs an info message and returns an empty list. If there are affected groups and assign is set to False, it deassigns all the affected groups. If assign is set to True, it assigns the groups to the user.

# Deassignment of groups and cache invalidation

The 'deassign' function is responsible for removing the assignment of a group. It first checks if there is a previous assignee for the group and if so, it deletes the assignment. It also creates an activity log for the unassignment action and clears the ownership cache for the deassigned group.

# Project deletion and saving with unique identifiers

The 'delete' function is used to delete a project. It manually cascades the deletion due to the lack of a foreign key relationship. It also removes notification settings for the project. The 'save' function is used to save a project. If the project does not have a slug, it generates one. If the 'SENTRY_USE_SNOWFLAKE' setting is enabled, it saves the project with a snowflake ID.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
