---
title: Overview of Integration Tasks
---
Integrations in the Sentry tasks module refer to the various tasks that are performed to integrate Sentry with external services. These tasks include syncing comments, statuses, and metadata, migrating repositories and issues, and checking subscriptions. Each integration task is defined in its own Python file within the 'sentry/tasks/integrations' directory.

The 'logger' object, imported in several integration task files, is used for logging events that occur during the execution of these tasks. This helps in debugging and tracking the flow of these tasks.

The 'Integration' model, imported in some of the task files, represents an integration instance with an external service. It is used to store and manage the data related to each integration.

The '**init**.py' files in the 'sentry/tasks/integrations' directory and its subdirectories (like 'vsts' and 'github') are used to initialize these directories as Python packages, and to define the public interface of these packages.

<SwmSnippet path="/src/sentry/tasks/integrations/migrate_opsgenie_plugins.py" line="1">

---

# Integration Tasks

This file is an example of an integration task. It contains the task for migrating Opsgenie plugins. The 'logger' object is used for logging events during the execution of this task.

```python
import logging

from django.db import router, transaction

from sentry.integrations.services.integration.service import integration_service
from sentry.models.integrations.integration import Integration
from sentry.models.integrations.organization_integration import OrganizationIntegration
from sentry.models.project import Project
from sentry.models.rule import Rule
from sentry.tasks.base import instrumented_task, retry
from sentry.utils import metrics

ALERT_LEGACY_INTEGRATIONS = {"id": "sentry.rules.actions.notify_event.NotifyEventAction"}
ALERT_LEGACY_INTEGRATIONS_WITH_NAME = {
    "id": "sentry.rules.actions.notify_event.NotifyEventAction",
    "name": "Send a notification (for all legacy integrations)",
}
logger = logging.getLogger(__name__)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/models/integrations/integration.py" line="1">

---

# Integration Model

The 'Integration' model is used to represent an integration instance with an external service. It is used to store and manage the data related to each integration.

```python
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, ClassVar

from django.db import IntegrityError, models, router, transaction

from sentry.backup.dependencies import NormalizedModelName, get_model_name
from sentry.backup.sanitize import SanitizableField, Sanitizer
from sentry.backup.scopes import RelocationScope
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/integrations/__init__.py" line="1">

---

# Initialization Files

The '**init**.py' files in the 'sentry/tasks/integrations' directory and its subdirectories (like 'vsts' and 'github') are used to initialize these directories as Python packages, and to define the public interface of these packages.

```python
import logging

from django.conf import settings

from sentry import features
```

---

</SwmSnippet>

# Integration Tasks Overview

This section provides an overview of the main functions in the 'sentry/tasks/integrations' directory.

<SwmSnippet path="/src/sentry/tasks/integrations/sync_metadata.py" line="14">

---

## Sync Metadata

The `sync_metadata` function is used to synchronize the metadata of an integration. It imports the `Integration` model and uses it to get the integration instance by its ID.

```python
@retry(on=(IntegrationError,), exclude=(Integration.DoesNotExist,))
def sync_metadata(integration_id: int) -> None:
    from sentry.integrations.jira.integration import JiraIntegration
    from sentry.integrations.jira_server.integration import JiraServerIntegration

    integration = Integration.objects.get(id=integration_id)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/integrations/migrate_opsgenie_plugins.py" line="5">

---

## Migrate Opsgenie Plugin

The `migrate_opsgenie_plugin` function is used to migrate the Opsgenie plugin. It imports the `Integration` and `OrganizationIntegration` models and uses them to manage the data related to the integration.

```python
from sentry.integrations.services.integration.service import integration_service
from sentry.models.integrations.integration import Integration
from sentry.models.integrations.organization_integration import OrganizationIntegration
from sentry.models.project import Project
from sentry.models.rule import Rule
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/integrations/migrate_issues.py" line="5">

---

## Migrate Issues

The `migrate_issues` function is used to migrate issues. It imports the `Integration` model and uses it to manage the data related to the integration.

```python
from sentry.models.groupmeta import GroupMeta
from sentry.models.integrations.external_issue import ExternalIssue
from sentry.models.integrations.integration import Integration
from sentry.models.project import Project
from sentry.plugins.base import plugins
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/integrations/migrate_repo.py" line="2">

---

## Migrate Repo

The `migrate_repo` function is used to migrate repositories. It imports the `Integration` model and uses it to manage the data related to the integration.

```python
from sentry.integrations.services.integration import integration_service
from sentry.integrations.services.repository import repository_service
from sentry.models.integrations.integration import Integration
from sentry.models.organization import Organization
from sentry.models.repository import Repository
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/integrations/sync_status_inbound.py" line="11">

---

## Sync Status Inbound

The `sync_status_inbound` function is used to synchronize the status of an integration from an external service to Sentry. It imports the `Integration` model and uses it to manage the data related to the integration.

```python
from sentry.models.group import Group, GroupStatus
from sentry.models.groupresolution import GroupResolution
from sentry.models.integrations.integration import Integration
from sentry.models.organization import Organization
from sentry.models.release import Release, ReleaseStatus, follows_semver_versioning_scheme
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/integrations/sync_status_outbound.py" line="2">

---

## Sync Status Outbound

The `sync_status_outbound` function is used to synchronize the status of an integration from Sentry to an external service. It imports the `Integration` model and uses it to manage the data related to the integration.

```python
from sentry.integrations.services.integration import integration_service
from sentry.models.group import Group, GroupStatus
from sentry.models.integrations.external_issue import ExternalIssue
from sentry.models.integrations.integration import Integration
from sentry.silo.base import SiloMode
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/integrations/vsts/subscription_check.py" line="5">

---

## VSTS Subscription Check

The `vsts_subscription_check` function is used to check the subscription status of a VSTS integration. It imports the `Integration` model and uses it to get the integration instance by its ID.

```python
from sentry.models.apitoken import generate_token
from sentry.models.integrations.integration import Integration
from sentry.shared_integrations.exceptions import ApiError, ApiUnauthorized
from sentry.silo.base import SiloMode
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
