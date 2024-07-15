---
title: product-Configuration Flow in Sentry
---
This document will cover the Configuration Flow in Sentry, which includes:

1. Loading and configuring Sentry
2. Setting up the environment
3. Initializing the application
4. Validating Snuba
5. Configuring the SDK
6. Capturing events and metrics
7. Displaying the context of a frame in the Sentry UI.

Technical document: <SwmLink doc-title="Understanding the Configuration Flow">[Understanding the Configuration Flow](/.swm/understanding-the-configuration-flow.a9swddz8.sw.md)</SwmLink>

# Loading and configuring Sentry

The configuration flow starts with loading and configuring Sentry. This is done by checking if the `_SENTRY_SKIP_CONFIGURATION` environment variable is not set to `1`. If it's not set, the `configure` function is imported and called. This function is responsible for loading the necessary configurations for Sentry to operate.

# Setting up the environment

The `configure` function sets up the environment based on two different config files. It checks if the configuration has been installed, and if not, it sets up the environment, adds additional mimetypes for static files, checks if the configuration file exists, and initializes the app. This ensures that the environment is properly configured for Sentry to operate.

# Initializing the application

The `initialize_app` function is responsible for initializing the application with the given configuration. It sets up various settings, validates the configuration, and sets up the services. This includes setting up the integration app for Single Org / Self-Hosted as it doesn't make much sense to use 2 separate apps for SSO and integration.

# Validating Snuba

The `validate_snuba` function ensures that everything related to Snuba is in sync. It checks if all Snuba required backends are set and if the eventstream is Snuba compatible. If not, it raises a ConfigurationError. This ensures that the data flow between Sentry and Snuba is properly configured.

# Configuring the SDK

The `configure_sdk` function sets up the SDK for Sentry, including the transport mechanism for sending events and metrics to Sentry. It fetches the SDK configuration options which include settings for event reporting, transaction sampling, and release information. It also modifies the transport mechanism to include metrics about the number of events sent to Sentry.

# Capturing events and metrics

The `_capture_anything` function captures any event and increments a metric if the event is sent upstream. It also checks if the SDK upstream metrics are enabled and filters out statsd envelope items unless allowed by a separate sample rate. This function is responsible for capturing and tracking events and metrics in Sentry.

# Displaying the context of a frame in the Sentry UI

The `Context` function is used to display the context of a frame in the Sentry UI. It is the final step in the configuration flow, where the copied context is displayed. This allows users to understand the context in which an event or error occurred.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
