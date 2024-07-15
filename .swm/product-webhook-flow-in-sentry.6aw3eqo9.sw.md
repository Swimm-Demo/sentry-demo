---
title: product-Webhook Flow in Sentry
---
This document will cover the Webhook Flow in Sentry, which includes:

1. Sending Webhooks
2. Recording Responses and Handling Errors
3. Checking if Integration is Broken
4. Notifying about Disabled Integration

Technical document: <SwmLink doc-title="Webhook Flow in Sentry">[Webhook Flow in Sentry](/.swm/webhook-flow-in-sentry.752svqaz.sw.md)</SwmLink>

# Sending Webhooks

The process begins with the initiation of the webhook flow. This is triggered when there are changes in resources that need to be communicated to external services. The system identifies the installation associated with the changes and triggers the webhook flow if the installation exists.

# Recording Responses and Handling Errors

Once the webhook flow is initiated, the system sends the webhook request and logs the response. If there's a timeout or connection error during this process, the system records the timeout and re-raises the exception. If the response status code indicates an error, the system raises the corresponding error. If the action is not 'event.alert', the system records the response for disabling integration.

# Checking if Integration is Broken

The system checks if the integration is broken by using the Integration Request Buffer. If the integration is broken, the system disables the Sentry app.

# Notifying about Disabled Integration

If the integration is disabled, the system notifies the owners of the organization about the disabled integration. It creates a message with the necessary context and sends it asynchronously.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
