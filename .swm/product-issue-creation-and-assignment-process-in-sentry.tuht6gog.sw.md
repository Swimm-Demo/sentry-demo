---
title: product-Issue Creation and Assignment Process in Sentry
---
This document will cover the 'create_issue' process in Sentry, which includes:

1. Creating an issue in Jira
2. Handling the assignee change
3. Assigning or deassigning groups to matching users
4. Sending a message to the user informing them of the assignment.

Technical document: <SwmLink doc-title="create_issue">[create_issue](/.swm/understanding-the-create_issue-process.dops7jhr.sw.md)</SwmLink>

# Creating an issue in Jira

The 'create_issue' process begins with the creation of an issue in Jira. The raw form data is formatted into a dictionary and a POST request is made to the 'CREATE_URL'.

# Handling the assignee change

The next step in the process is to handle the assignee change. If the data contains a 'changelog', the assignee change and status change are handled before a response is returned. If the assignee field has changed, the assignee's email is retrieved and the 'sync_group_assignee_inbound' function is called with the assignee's email and the issue key. If the assignee is not present, the 'sync_group_assignee_inbound' function is called with None as the email and the assign flag set to False.

# Assigning or deassigning groups to matching users

The 'sync_group_assignee_inbound' function assigns or deassigns groups to matching users based on the assign flag. If the assign flag is False, it deassigns the group from the user. If the assign flag is True, it assigns the group to the user.

# Sending a message to the user

The process ends with a message being sent to the user informing them of the assignment. The content of the message is determined by the 'message' parameter. If the 'update' parameter is True, it updates the existing message; otherwise, it sends a new message.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
