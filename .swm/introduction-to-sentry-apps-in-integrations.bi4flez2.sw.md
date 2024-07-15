---
title: Introduction to Sentry Apps in Integrations
---
Sentry Apps in the Integrations module are a key part of the Sentry platform. They are used to integrate third-party services into Sentry, enhancing its functionality and user experience. These apps are defined and managed through the `SentryApp` class, which is imported from the `sentry.models.integrations.sentry_app` module in various files within the `src/sentry/api/endpoints/integrations/sentry_apps/` directory.

The `SentryApp` class is used to create, manage, and interact with Sentry Apps. It is used in conjunction with other classes such as `SentryAppInstallation` and `SentryAppCreator` to handle the installation and creation of Sentry Apps respectively.

The `SentryAppInstallation` class, imported from the `sentry.models.integrations.sentry_app_installation` module, is used to manage the installation of Sentry Apps. It is used in various files within the `src/sentry/api/endpoints/integrations/sentry_apps/` directory to handle the installation details of Sentry Apps.

The `SentryAppCreator` class, imported from the `sentry.sentry_apps.apps` module, is used to create new Sentry Apps. It is used in the `src/sentry/api/endpoints/integrations/sentry_apps/index.py` file to handle the creation of Sentry Apps.

The `RpcSentryApp` class, imported from the `sentry.sentry_apps.services.app` module, is used to interact with Sentry Apps. It is used in the `src/sentry/api/endpoints/integrations/sentry_apps/interaction.py` file to handle interactions with Sentry Apps.

<SwmSnippet path="/src/sentry/api/endpoints/integrations/sentry_apps/details.py" line="24">

---

# SentryApp Class

The `SentryApp` class is used to define and manage Sentry Apps. It is imported from the `sentry.models.integrations.sentry_app` module.

```python
from sentry.models.integrations.sentry_app import SentryApp
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/integrations/sentry_apps/installation/index.py" line="18">

---

# SentryAppInstallation Class

The `SentryAppInstallation` class is used to manage the installation of Sentry Apps. It is imported from the `sentry.models.integrations.sentry_app_installation` module.

```python
from sentry.models.integrations.sentry_app_installation import SentryAppInstallation
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/integrations/sentry_apps/index.py" line="20">

---

# SentryAppCreator Class

The `SentryAppCreator` class is used to create new Sentry Apps. It is imported from the `sentry.sentry_apps.apps` module.

```python
from sentry.sentry_apps.apps import SentryAppCreator
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/integrations/sentry_apps/interaction.py" line="13">

---

# RpcSentryApp Class

The `RpcSentryApp` class is used to interact with Sentry Apps. It is imported from the `sentry.sentry_apps.services.app` module.

```python
from sentry.sentry_apps.services.app import RpcSentryApp, app_service
```

---

</SwmSnippet>

# Sentry Apps Functions

This section discusses the main functions related to Sentry Apps in the Sentry platform.

<SwmSnippet path="/src/sentry/models/integrations/sentry_app.py" line="1">

---

## SentryApp

The `SentryApp` class is used to create, manage, and interact with Sentry Apps. It is used in various files within the `src/sentry/api/endpoints/integrations/sentry_apps/` directory.

```python
import hmac
import itertools
import uuid
from hashlib import sha256
from typing import Any, ClassVar

from django.db import models, router, transaction
from django.db.models import QuerySet
from django.utils import timezone
from rest_framework.request import Request

from sentry.backup.dependencies import NormalizedModelName, get_model_name
from sentry.backup.sanitize import SanitizableField, Sanitizer
from sentry.backup.scopes import RelocationScope
from sentry.constants import (
    SENTRY_APP_SLUG_MAX_LENGTH,
    SentryAppInstallationStatus,
    SentryAppStatus,
)
from sentry.db.models import (
    ArrayField,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/models/integrations/sentry_app_installation.py" line="1">

---

## SentryAppInstallation

The `SentryAppInstallation` class is used to manage the installation of Sentry Apps. It is used in various files within the `src/sentry/api/endpoints/integrations/sentry_apps/` directory to handle the installation details of Sentry Apps.

```python
from __future__ import annotations

import uuid
from collections.abc import Collection, Mapping
from itertools import chain
from typing import TYPE_CHECKING, Any, ClassVar, overload

from django.db import models
from django.db.models import OuterRef, QuerySet, Subquery
from django.utils import timezone

from sentry.auth.services.auth import AuthenticatedToken
from sentry.backup.scopes import RelocationScope
from sentry.constants import SentryAppInstallationStatus
from sentry.db.models import BoundedPositiveIntegerField, FlexibleForeignKey, control_silo_model
from sentry.db.models.fields.hybrid_cloud_foreign_key import HybridCloudForeignKey
from sentry.db.models.outboxes import ReplicatedControlModel
from sentry.db.models.paranoia import ParanoidManager, ParanoidModel
from sentry.projects.services.project import RpcProject
from sentry.sentry_apps.services.app.model import RpcSentryAppComponent, RpcSentryAppInstallation
from sentry.types.region import find_regions_for_orgs
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_apps/apps.py" line="1">

---

## SentryAppCreator

The `SentryAppCreator` class is used to create new Sentry Apps. It is used in the `src/sentry/api/endpoints/integrations/sentry_apps/index.py` file to handle the creation of Sentry Apps.

```python
from __future__ import annotations

import dataclasses
from collections.abc import Iterable, Mapping
from dataclasses import field
from itertools import chain
from typing import Any

import sentry_sdk
from django.db import IntegrityError, router, transaction
from django.db.models import Q
from django.http.request import HttpRequest
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from sentry_sdk.api import isolation_scope

from sentry import analytics, audit_log
from sentry.api.helpers.slugs import sentry_slugify
from sentry.auth.staff import has_staff_option
from sentry.constants import SentryAppStatus
from sentry.coreapi import APIError
```

---

</SwmSnippet>

## RpcSentryApp

The `RpcSentryApp` class is used to interact with Sentry Apps. It is used in the `src/sentry/api/endpoints/integrations/sentry_apps/interaction.py` file to handle interactions with Sentry Apps.

# Sentry Apps API Endpoints

Sentry Apps API Endpoints

<SwmSnippet path="/src/sentry/api/endpoints/integrations/sentry_apps/details.py" line="40">

---

## SentryAppDetailsEndpoint

The `SentryAppDetailsEndpoint` class defines the API endpoints for retrieving, updating, and deleting a specific Sentry App. It uses HTTP methods like GET, PUT, and DELETE to perform these operations. The `get` method retrieves the details of a Sentry App, the `put` method updates the details of a Sentry App, and the `delete` method removes a Sentry App.

```python
@control_silo_endpoint
class SentryAppDetailsEndpoint(SentryAppBaseEndpoint):
    owner = ApiOwner.INTEGRATIONS
    publish_status = {
        "DELETE": ApiPublishStatus.UNKNOWN,
        "GET": ApiPublishStatus.UNKNOWN,
        "PUT": ApiPublishStatus.UNKNOWN,
    }
    permission_classes = (SentryAppDetailsEndpointPermission,)

    def get(self, request: Request, sentry_app) -> Response:
        return Response(serialize(sentry_app, request.user, access=request.access))

    @catch_raised_errors
    def put(self, request: Request, sentry_app) -> Response:
        if sentry_app.metadata.get("partnership_restricted", False):
            return Response(
                {"detail": PARTNERSHIP_RESTRICTED_ERROR_MESSAGE},
                status=403,
            )
        owner_context = organization_service.get_organization_by_id(
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/integrations/sentry_apps/installation/index.py" line="26">

---

## SentryAppInstallationsEndpoint

The `SentryAppInstallationsEndpoint` class defines the API endpoints for retrieving and creating installations of Sentry Apps. The `get` method retrieves all installations of a Sentry App for a specific organization. The `post` method creates a new installation of a Sentry App for a specific organization.

```python
@control_silo_endpoint
class SentryAppInstallationsEndpoint(SentryAppInstallationsBaseEndpoint):
    owner = ApiOwner.INTEGRATIONS
    publish_status = {
        "GET": ApiPublishStatus.UNKNOWN,
        "POST": ApiPublishStatus.UNKNOWN,
    }

    def get(self, request: Request, organization) -> Response:
        queryset = SentryAppInstallation.objects.filter(organization_id=organization.id)

        return self.paginate(
            request=request,
            queryset=queryset,
            order_by="-date_added",
            paginator_cls=OffsetPaginator,
            on_results=lambda x: serialize(x, request.user, access=request.access),
        )

    def post(self, request: Request, organization) -> Response:
        serializer = SentryAppInstallationsSerializer(data=request.data)
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
