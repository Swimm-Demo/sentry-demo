---
title: product-User Creation Process
---
This document will cover the User Creation Process in Sentry, which includes: 1. User Input Validation 2. User Record Creation or Update 3. Organization Membership Assignment 4. Password Setting and Saving

Technical document: <SwmLink doc-title="User Creation Process">[User Creation Process](/.swm/user-creation-process.nzpgietk.sw.md)</SwmLink>

# User Input Validation

The first step in the user creation process is validating the user's input. This involves checking if the necessary parameters like emails and password are provided. If not, the user is prompted for input. Additionally, it ensures that a user cannot be set as staff without superuser access. This is important to maintain the integrity and security of the system.

# User Record Creation or Update

After validation, the system loops through the provided emails, creating or updating user records in the database. If the user already exists and the 'force_update' flag is set, the user's details are updated. If the user doesn't exist, a new user is created. This ensures that the system maintains up-to-date user records and avoids duplication.

# Organization Membership Assignment

The next step is handling organization membership. If the Sentry instance is configured as a single organization, the new user is added to the specified organization or the default organization if none is specified. The user is also added to a single team if one exists. This step is crucial for managing user access and permissions within the organization.

# Password Setting and Saving

Finally, the user's password is set and saved. If the user is a superuser and the Sentry instance is self-hosted or a single organization, the 'set_superadmin' function is called. A message is then printed to the console indicating the user's email and whether they were created or updated. This step ensures the security of the user's account and provides feedback on the user creation process.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
