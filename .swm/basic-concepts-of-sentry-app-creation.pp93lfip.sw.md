---
title: Basic Concepts of Sentry App Creation
---
Sentry apps in the main application are primarily created and managed through the `SentryAppCreator` class. This class is responsible for generating and validating unique slugs, creating proxy users, API applications, and the Sentry app itself. It also handles the creation of UI components and integration features for the Sentry app.

The `SentryAppCreator` class uses the `_create_sentry_app` function to create a Sentry app. This function takes in a user, a slug, a proxy user, and an API application as parameters. It then uses these parameters to create a new Sentry app with various properties such as name, slug, author, application ID, owner ID, proxy user ID, scope list, events, schema, webhook URL, redirect URL, and more.

The `SentryAppCreator` class also uses the `_create_ui_components` function to create UI components for the Sentry app. This function iterates over the elements in the schema of the Sentry app and creates a new Sentry app component for each element.

The `SentryAppCreator` class also uses the `_create_integration_feature` function to create integration features for the Sentry app. This function creates a new integration feature for the Sentry app and handles any integrity errors that may occur during the creation process.

The `SentryAppCreator` class is used in the `sentry.sentry_apps.services.app.impl` module. This module imports the `SentryAppCreator` class from the `sentry.sentry_apps.apps` module and uses it to create Sentry apps.

The `SentryAppInstallationCreator` class is used to create installations for Sentry apps. This class is imported from the `sentry.sentry_apps.installations` module in the `sentry.sentry_apps.apps` module.

<SwmSnippet path="/src/sentry/sentry_apps/apps.py" line="280">

---

# SentryAppCreator Class

The `SentryAppCreator` class is responsible for creating and managing Sentry apps. It generates and validates unique slugs, creates proxy users, API applications, and the Sentry app itself. It also handles the creation of UI components and integration features for the Sentry app.

```python
class SentryAppCreator:
    name: str
    author: str
    organization_id: int
    is_internal: bool
    scopes: list[str] = dataclasses.field(default_factory=list)
    events: list[str] = dataclasses.field(default_factory=list)
    webhook_url: str | None = None
    redirect_url: str | None = None
    is_alertable: bool = False
    verify_install: bool = True
    schema: Schema = dataclasses.field(default_factory=dict)
    overview: str | None = None
    allowed_origins: list[str] = dataclasses.field(default_factory=list)
    popularity: int | None = None
    metadata: dict | None = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.is_internal:
            assert (
                not self.verify_install
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_apps/apps.py" line="354">

---

# \_create_sentry_app Function

The `_create_sentry_app` function is used by the `SentryAppCreator` class to create a Sentry app. It takes in a user, a slug, a proxy user, and an API application as parameters and uses these to create a new Sentry app with various properties.

```python
    def _create_sentry_app(
        self, user: User | RpcUser, slug: str, proxy: User, api_app: ApiApplication
    ) -> SentryApp:
        kwargs = {
            "name": self.name,
            "slug": slug,
            "author": self.author,
            "application_id": api_app.id,
            "owner_id": self.organization_id,
            "proxy_user_id": proxy.id,
            "scope_list": self.scopes,
            "events": expand_events(self.events),
            "schema": self.schema or {},
            "webhook_url": self.webhook_url,
            "redirect_url": self.redirect_url,
            "is_alertable": self.is_alertable,
            "verify_install": self.verify_install,
            "overview": self.overview,
            "popularity": self.popularity or SentryApp._meta.get_field("popularity").default,
            "creator_user_id": user.id,
            "creator_label": user.email
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_apps/apps.py" line="384">

---

# \_create_ui_components Function

The `_create_ui_components` function is used by the `SentryAppCreator` class to create UI components for the Sentry app. It iterates over the elements in the schema of the Sentry app and creates a new Sentry app component for each element.

```python
    def _create_ui_components(self, sentry_app: SentryApp) -> None:
        schema = self.schema or {}

        for element in schema.get("elements", []):
            SentryAppComponent.objects.create(
                type=element["type"], sentry_app_id=sentry_app.id, schema=element
            )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_apps/apps.py" line="392">

---

# \_create_integration_feature Function

The `_create_integration_feature` function is used by the `SentryAppCreator` class to create integration features for the Sentry app. It creates a new integration feature for the Sentry app and handles any integrity errors that may occur during the creation process.

```python
    def _create_integration_feature(self, sentry_app: SentryApp) -> None:
        # sentry apps must have at least one feature
        # defaults to 'integrations-api'
        try:
            with transaction.atomic(router.db_for_write(IntegrationFeature)):
                IntegrationFeature.objects.create(
                    target_id=sentry_app.id,
                    target_type=IntegrationTypes.SENTRY_APP.value,
                )
        except IntegrityError:
            with isolation_scope() as scope:
                scope.set_tag("sentry_app", sentry_app.slug)
                sentry_sdk.capture_message("IntegrityError while creating IntegrationFeature")
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_apps/services/app/impl.py" line="22">

---

# SentryAppCreator Usage

The `SentryAppCreator` class is used in the `sentry.sentry_apps.services.app.impl` module. This module imports the `SentryAppCreator` class from the `sentry.sentry_apps.apps` module and uses it to create Sentry apps.

```python
from sentry.sentry_apps.apps import SentryAppCreator
from sentry.sentry_apps.services.app import (
    AppService,
```

---

</SwmSnippet>

# Sentry App Functions

This section provides an overview of the main functions related to Sentry apps in the Sentry application.

<SwmSnippet path="/src/sentry/sentry_apps/apps.py" line="280">

---

## SentryAppCreator

The `SentryAppCreator` class is responsible for creating and managing Sentry apps. It generates and validates unique slugs, creates proxy users, API applications, and the Sentry app itself. It also handles the creation of UI components and integration features for the Sentry app.

```python
class SentryAppCreator:
    name: str
    author: str
    organization_id: int
    is_internal: bool
    scopes: list[str] = dataclasses.field(default_factory=list)
    events: list[str] = dataclasses.field(default_factory=list)
    webhook_url: str | None = None
    redirect_url: str | None = None
    is_alertable: bool = False
    verify_install: bool = True
    schema: Schema = dataclasses.field(default_factory=dict)
    overview: str | None = None
    allowed_origins: list[str] = dataclasses.field(default_factory=list)
    popularity: int | None = None
    metadata: dict | None = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.is_internal:
            assert (
                not self.verify_install
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_apps/apps.py" line="354">

---

## \_create_sentry_app

The `_create_sentry_app` function is used by the `SentryAppCreator` class to create a Sentry app. It takes in a user, a slug, a proxy user, and an API application as parameters and uses these to create a new Sentry app with various properties.

```python
    def _create_sentry_app(
        self, user: User | RpcUser, slug: str, proxy: User, api_app: ApiApplication
    ) -> SentryApp:
        kwargs = {
            "name": self.name,
            "slug": slug,
            "author": self.author,
            "application_id": api_app.id,
            "owner_id": self.organization_id,
            "proxy_user_id": proxy.id,
            "scope_list": self.scopes,
            "events": expand_events(self.events),
            "schema": self.schema or {},
            "webhook_url": self.webhook_url,
            "redirect_url": self.redirect_url,
            "is_alertable": self.is_alertable,
            "verify_install": self.verify_install,
            "overview": self.overview,
            "popularity": self.popularity or SentryApp._meta.get_field("popularity").default,
            "creator_user_id": user.id,
            "creator_label": user.email
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_apps/apps.py" line="384">

---

## \_create_ui_components

The `_create_ui_components` function is used by the `SentryAppCreator` class to create UI components for the Sentry app. It iterates over the elements in the schema of the Sentry app and creates a new Sentry app component for each element.

```python
    def _create_ui_components(self, sentry_app: SentryApp) -> None:
        schema = self.schema or {}

        for element in schema.get("elements", []):
            SentryAppComponent.objects.create(
                type=element["type"], sentry_app_id=sentry_app.id, schema=element
            )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_apps/apps.py" line="392">

---

## \_create_integration_feature

The `_create_integration_feature` function is used by the `SentryAppCreator` class to create integration features for the Sentry app. It creates a new integration feature and handles any integrity errors that may occur during the creation process.

```python
    def _create_integration_feature(self, sentry_app: SentryApp) -> None:
        # sentry apps must have at least one feature
        # defaults to 'integrations-api'
        try:
            with transaction.atomic(router.db_for_write(IntegrationFeature)):
                IntegrationFeature.objects.create(
                    target_id=sentry_app.id,
                    target_type=IntegrationTypes.SENTRY_APP.value,
                )
        except IntegrityError:
            with isolation_scope() as scope:
                scope.set_tag("sentry_app", sentry_app.slug)
                sentry_sdk.capture_message("IntegrityError while creating IntegrationFeature")
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
