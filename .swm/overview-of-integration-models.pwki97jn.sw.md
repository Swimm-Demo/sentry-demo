---
title: Overview of Integration Models
---
Integrations in the Models directory of the sentry-demo repository refer to the various classes and modules that facilitate the integration of external services and tools with the Sentry application. These integrations can range from document-based integrations, represented by the `DocIntegration` class, to more complex integrations like `SentryApp` and `IntegrationFeature`. The `IntegrationFeature` class, for instance, represents a specific feature of an integration, and contains methods for managing and interacting with these features.

The `DocIntegration` class represents document-based integrations that can be found in Sentry but are installed via code change. It contains fields like `name`, `slug`, `author`, `description`, `url`, and `popularity` among others. This class is used in various parts of the codebase, such as in the `DocIntegrationAvatar` class, which associates a `DocIntegration` with a logo photo file.

The `ProjectIntegration` class, although deprecated and soon to be removed, represents project integrations. It is associated with a specific project and integration ID, and contains a `config` field for storing integration-specific configuration data.

The `Integration` class is another key component of the integration system. It is used in various parts of the codebase, and is often imported from the `sentry.models.integrations.integration` module. It is also used in the `OrganizationIntegration` class, which represents the integration of an organization.

<SwmSnippet path="/src/sentry/models/integrations/integration.py" line="22">

---

# Integration Class

The `Integration` class is a key component of the integration system. It is used in various parts of the codebase, and is often imported from the `sentry.models.integrations.integration` module.

```python
    from sentry.integrations.base import (
        IntegrationFeatures,
        IntegrationInstallation,
        IntegrationProvider,
    )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/models/integrations/integration.py" line="120">

---

# DocIntegration Class

The `DocIntegration` class represents document-based integrations that can be found in Sentry but are installed via code change. It contains fields like `name`, `slug`, `author`, `description`, `url`, and `popularity` among others.

```python
        Returns None if the OrganizationIntegration was not created
        """
        from sentry.models.integrations.organization_integration import OrganizationIntegration

        if not isinstance(organization_id, int):
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/models/integrations/integration_feature.py" line="22">

---

# IntegrationFeature Class

The `IntegrationFeature` class represents a specific feature of an integration, and contains methods for managing and interacting with these features.

```python
class Feature:
    API = 0
    ISSUE_LINK = 1
    STACKTRACE_LINK = 2
    EVENT_HOOKS = 3
    PROJECT_MANAGEMENT = 4
    INCIDENT_MANAGEMENT = 5
    FEATURE_FLAG = 6
    ALERTS = 7
    RELEASE_MANAGEMENT = 8
    VISUALIZATION = 9
    CHAT = 11
    SESSION_REPLAY = 12

    @classmethod
    def as_choices(cls) -> tuple[tuple[int, str], ...]:
        return (
            (cls.API, "integrations-api"),
            (cls.ISSUE_LINK, "integrations-issue-link"),
            (cls.STACKTRACE_LINK, "integrations-stacktrace-link"),
            (cls.EVENT_HOOKS, "integrations-event-hooks"),
```

---

</SwmSnippet>

# Integration Functions

This section provides an overview of the main classes and functions related to integrations in the Sentry application.

<SwmSnippet path="/src/sentry/models/integrations/integration_feature.py" line="22">

---

## IntegrationFeature

The `IntegrationFeature` class represents a specific feature of an integration. It contains methods like `as_choices`, `as_str`, and `description` for managing and interacting with these features.

```python
class Feature:
    API = 0
    ISSUE_LINK = 1
    STACKTRACE_LINK = 2
    EVENT_HOOKS = 3
    PROJECT_MANAGEMENT = 4
    INCIDENT_MANAGEMENT = 5
    FEATURE_FLAG = 6
    ALERTS = 7
    RELEASE_MANAGEMENT = 8
    VISUALIZATION = 9
    CHAT = 11
    SESSION_REPLAY = 12

    @classmethod
    def as_choices(cls) -> tuple[tuple[int, str], ...]:
        return (
            (cls.API, "integrations-api"),
            (cls.ISSUE_LINK, "integrations-issue-link"),
            (cls.STACKTRACE_LINK, "integrations-stacktrace-link"),
            (cls.EVENT_HOOKS, "integrations-event-hooks"),
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/models/integrations/doc_integration.py" line="16">

---

## DocIntegration

The `DocIntegration` class represents document-based integrations. These integrations are installed via code change and can be found in Sentry.

```python

    name = models.CharField(max_length=64)
    slug = SentrySlugField(max_length=64, unique=True, db_index=False)
    author = models.CharField(max_length=255)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/models/integrations/integration.py" line="59">

---

## Integration

The `Integration` class is a key component of the integration system. It is used in various parts of the codebase and is often imported from the `sentry.models.integrations.integration` module.

```python
    status = BoundedPositiveIntegerField(
        default=ObjectStatus.ACTIVE, choices=ObjectStatus.as_choices(), null=True
    )
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
