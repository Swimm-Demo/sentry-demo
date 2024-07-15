---
title: product-Updating Member Roles in an Organization
---
This document will cover the process of updating a member's roles within an organization and its teams. We'll cover:

1. Validating incoming data
2. Sending necessary emails
3. Assigning roles
4. Saving changes.

Technical document: <SwmLink doc-title="put">[put](/.swm/understanding-the-put-function.lkr1eynu.sw.md)</SwmLink>

# Validating incoming data

The first step in updating a member's roles is to validate the incoming data. This ensures that the data is correct and meets the necessary requirements. If the data is not valid, an error is raised and the process is halted.

# Sending necessary emails

Once the data is validated, the system determines whether the member is pending. If the member is pending, an invite email or a Single Sign-On (SSO) link email is sent depending on the authentication provider. This email contains necessary information for the member to join the organization.

# Assigning roles

After the email is sent, the system assigns the organization and team roles to the member. The roles are determined based on the validated data. The system also verifies the team IDs and checks if the requester has access to the teams.

# Saving changes

Finally, the changes are saved. This includes updating the member's roles and saving the team assignments. The system also handles any necessary updates to the organization options, flags, and avatar, and handles 2FA and email verification requirements.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
