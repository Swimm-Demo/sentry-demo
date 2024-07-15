---
title: product-User Avatar Management
---
This document will cover the process of identifying the organization, retrieving and resizing user avatars, and updating user avatars in the Sentry application. We'll cover:

1. How the organization is identified
2. How user avatars are retrieved and resized
3. How user avatars are updated

Technical document: <SwmLink doc-title="Understanding _find_implicit_slug Function">[Understanding \_find_implicit_slug Function](/.swm/understanding-_find_implicit_slug-function.g81xepjb.sw.md)</SwmLink>

# Identifying the Organization

The first step in the process is to identify the organization that the user belongs to. This is done by checking the subdomain of the request. If a subdomain is present and it's not the same as the active organization, the subdomain is used as the organization identifier.

# Retrieving and Resizing User Avatars

Once the organization is identified, the system retrieves the user's avatar based on the avatar ID provided in the request. If a size parameter is provided, the system retrieves a cached photo of that size. If the photo is not in the cache, the system opens the photo file, resizes the image, and saves it to the cache. This ensures that the avatar is displayed correctly across different devices and screen sizes.

# Updating User Avatars

The final step in the process is to update the user's avatar. This is done by preparing the outboxes before the update. The system finds the regions for the user and creates control outboxes for each region. These outboxes are then saved correctly to ensure that the update is successful.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
