---
title: Understanding the Import Process
---
<SwmSnippet path="/src/sentry/tasks/relocation.py" line="1049">

---

# Importing Process

The importing process starts with the `importing` function. This function initiates the relocation task and opens the relocation file. It then calls the `import_in_organization_scope` function with the relocation data and other parameters.

```python
def importing(uuid: str) -> None:
    """
    Perform the import on the actual live instance we are targeting.

    This function is NOT idempotent - if an import breaks, we should just abandon it rather than
    trying it again!
    """

    relocation: Relocation | None
    attempts_left: int
    (relocation, attempts_left) = start_relocation_task(
        uuid=uuid,
        task=OrderedTask.IMPORTING,
        allowed_task_attempts=MAX_SLOW_TASK_ATTEMPTS,
    )
    if relocation is None:
        return

    with retry_task_or_fail_relocation(
        relocation,
        OrderedTask.IMPORTING,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/backup/imports.py" line="520">

---

The `import_in_organization_scope` function performs an import in the `Organization` scope. It imports only models with `RelocationScope.User` or `RelocationScope.Organization` from the provided `src` file. It then calls the `_import` function.

```python
def import_in_organization_scope(
    src: IO[bytes],
    *,
    decryptor: Decryptor | None = None,
    flags: ImportFlags | None = None,
    org_filter: set[str] | None = None,
    printer: Printer,
):
    """
    Perform an import in the `Organization` scope, meaning that only models with
    `RelocationScope.User` or `RelocationScope.Organization` will be imported from the provided
    `src` file.

    The `org_filter` argument allows imports to be filtered by organization slug. If the argument
    is set to `None`, there is no filtering, meaning all encountered organizations and users are
    imported.
    """

    # Import here to prevent circular module resolutions.
    from sentry.models.organization import Organization

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/backup/imports.py" line="86">

---

The `_import` function is the core of the import process. It reads the content of the import file, processes it, and writes the data into the database. It also resolves organization slugs from the primary key map and creates organization slugs.

```python
def _import(
    src: IO[bytes],
    scope: ImportScope,
    *,
    decryptor: Decryptor | None = None,
    flags: ImportFlags | None = None,
    filter_by: Filter | None = None,
    printer: Printer,
):
    """
    Imports core data for a Sentry installation.

    It is generally preferable to avoid calling this function directly, as there are certain
    combinations of input parameters that should not be used together. Instead, use one of the other
    wrapper functions in this file, named `import_in_XXX_scope()`.
    """

    # Import here to prevent circular module resolutions.
    from sentry.models.email import Email
    from sentry.models.organization import Organization
    from sentry.models.organizationmember import OrganizationMember
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/backup/imports.py" line="392">

---

The `do_writes` function is responsible for writing the imported data into the database. It iterates over the models in the content and calls the `do_write` function for each model.

```python
    # Extract some write logic into its own internal function, so that we may call it irrespective
    # of how we do atomicity: on a per-model (if using multiple dbs) or global (if using a single
    # db) basis.
    def do_writes(pk_map: PrimaryKeyMap) -> None:
        nonlocal deferred_org_auth_tokens, import_write_context

        for model_name, json_data, offset in yield_json_models(content):
            if model_name == org_auth_token_model_name:
                deferred_org_auth_tokens.append(json_data)
                continue

            do_write(import_write_context, pk_map, model_name, json_data, offset)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/backup/imports.py" line="405">

---

The `resolve_org_slugs_from_pk_map` function resolves slugs for all imported organization models via the PrimaryKeyMap and reconciles their slug globally by issuing a slug update. It then calls the `bulk_create_organization_slugs` function.

```python
    # Resolves slugs for all imported organization models via the PrimaryKeyMap and reconciles
    # their slug globally via control silo by issuing a slug update.
    def resolve_org_slugs_from_pk_map(pk_map: PrimaryKeyMap):
        from sentry.services.organization import organization_provisioning_service

        org_pk_mapping = pk_map.mapping[str(org_model_name)]
        if not org_pk_mapping:
            return

        slug_mapping: dict[int, str] = {}
        for old_primary_key in org_pk_mapping:
            org_id, _, org_slug = org_pk_mapping[old_primary_key]
            slug_mapping[org_id] = org_slug or ""

        if len(slug_mapping) > 0:
            # HACK(azaslavsky): Okay, this gets a bit complicated, but bear with me: the following
            # `bulk_create...` calls will result in some actions on the control silo that call back
            # into this region. So the client (this region) calls the server (the control silo)
            # which may need to make one or more calls back into the client (this region). Because
            # some of our `OrganizationMemberTeam` outboxes may not be drained due to the HACK we
            # performed in `import_export/impl.py` (see that file for more details), there may be a
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/services/organization/provisioning.py" line="141">

---

The `bulk_create_organization_slugs` function creates slug reservations for imported organizations that already exist on the region. It calls the `bulk_create_organization_slug_reservations` function to create the slug reservations.

```python
    def bulk_create_organization_slugs(
        self, slug_mapping: dict[int, str], region_name: str | None = None
    ):
        """
        CAUTION: DO NOT USE THIS OUTSIDE OF THE IMPORT/RELOCATION CONTEXT

        Organizations are meant to be provisioned via the
         `provision_organization_in_region` method, which handles both slug
         reservation and organization creation.

        Bulk creates slug reservations for imported organizations that already
        exist on the region. Each target organization is provided as a tuple of
        Organization ID (int) and base slug (str).

        :param org_ids_and_slugs: A set of tuples containing an organization ID
        and base slug.
        :param region_name: The region where the imported organizations exist
        :return:
        """
        destination_region_name = self._validate_or_default_region(region_name=region_name)

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/hybridcloud/services/control_organization_provisioning/impl.py" line="256">

---

The `bulk_create_organization_slug_reservations` function creates slug reservations for imported organizations that already exist on the region. It saves the slug reservations and validates that the primary slug has been updated.

```python
    def bulk_create_organization_slug_reservations(
        self,
        *,
        region_name: str,
        slug_mapping: dict[int, str],
    ) -> None:
        slug_reservations_to_create: list[OrganizationSlugReservation] = []

        with outbox_context(transaction.atomic(router.db_for_write(OrganizationSlugReservation))):
            for org_id, slug in slug_mapping.items():
                slug_reservation = OrganizationSlugReservation(
                    slug=self._generate_org_slug(slug=slug, region_name=region_name),
                    organization_id=org_id,
                    reservation_type=OrganizationSlugReservationType.TEMPORARY_RENAME_ALIAS.value,
                    user_id=-1,
                    region_name=region_name,
                )
                slug_reservation.save(unsafe_write=True)

                slug_reservations_to_create.append(slug_reservation)

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/backup/imports.py" line="295">

---

# Importing Data

The `do_write` function is the starting point of the import process. It takes in various parameters including the model name and JSON data to be imported. It then retrieves the model's dependencies and uses the `ImportExportService` to get the appropriate importer for the model. The `import_by_model` function is then called with the necessary parameters to perform the actual import.

```python
    # Perform the write of a single model.
    def do_write(
        import_write_context: ImportWriteContext,
        pk_map: PrimaryKeyMap,
        model_name: NormalizedModelName,
        json_data: Any,
        offset: int,
    ) -> None:
        model_relations = import_write_context.dependencies.get(model_name)
        if not model_relations:
            return

        dep_models = {get_model_name(d) for d in model_relations.get_dependencies_for_relocation()}
        import_by_model = ImportExportService.get_importer_for_model(model_relations.model)
        model_name_str = str(model_name)
        min_ordinal = offset + 1

        extra = {
            "model_name": model_name_str,
            "import_uuid": flags.import_uuid,
            "min_ordinal": min_ordinal,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/backup/services/import_export/impl.py" line="104">

---

The `import_by_model` function is responsible for importing a single model. It validates the input parameters, retrieves the model, and checks if it can be imported based on its silo mode. It then deserializes the JSON data into model instances and writes them to the database. If any errors occur during this process, they are handled and an appropriate `RpcImportError` is returned.

```python
    """

    def import_by_model(
        self,
        *,
        model_name: str,
        scope: RpcImportScope | None = None,
        flags: RpcImportFlags,
        filter_by: list[RpcFilter],
        pk_map: RpcPrimaryKeyMap,
        json_data: str,
        min_ordinal: int,
    ) -> RpcImportResult:
        if min_ordinal < 1:
            return RpcImportError(
                kind=RpcImportErrorKind.InvalidMinOrdinal,
                on=InstanceID(model_name),
                reason=f"The model `{model_name}` was offset with an invalid `min_ordinal` of `{min_ordinal}`",
            )

        batch_model_name = NormalizedModelName(model_name)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/backup/mixins.py" line="13">

---

The `write_relocation_import` function is called within `import_by_model` to perform the actual database write. It checks for potential collisions based on unique sets and handles them appropriately. If the model instance is new, it is saved to the database and its primary key is returned along with the `ImportKind.Inserted` flag. If the model instance already exists, it is either updated or its existing primary key is returned with the `ImportKind.Existing` flag, depending on the `overwrite_configs` flag.

```python
    """

    # TODO(getsentry/team-ospo#190): Clean up the type checking in this method.
    def write_relocation_import(
        self, scope: ImportScope, flags: ImportFlags
    ) -> tuple[int, ImportKind] | None:
        # Get all unique sets that will potentially cause collisions.
        uniq_sets = dependencies()[get_model_name(self)].get_uniques_without_foreign_keys()  # type: ignore[arg-type]

        # Don't use this mixin for models with multiple unique sets; write custom logic instead.
        assert len(uniq_sets) <= 1

        # Must set `__relocation_custom_ordinal__` on models that use this mixin.
        assert getattr(self.__class__, "__relocation_custom_ordinal__", None) is not None

        if self.get_relocation_scope() == RelocationScope.Config:  # type: ignore[attr-defined]
            if len(uniq_sets) == 1:
                uniq_set = uniq_sets[0]
                query = dict()
                for uniq_field_name in uniq_set:
                    if getattr(self, uniq_field_name, None) is not None:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/event_manager.py" line="442">

---

The `save` function is the final step in the import process. It normalizes the event data, retrieves the project, and prepares the job data. Depending on the event type, it calls either `save_transaction_events` or `save_generic_events` to save the event data. It also handles any potential collisions and updates counters and frequencies.

```python
    def save(
        self,
        project_id: int | None,
        raw: bool = False,
        assume_normalized: bool = False,
        start_time: float | None = None,
        cache_key: str | None = None,
        skip_send_first_transaction: bool = False,
        has_attachments: bool = False,
    ) -> Event:
        """
        After normalizing and processing an event, save adjacent models such as
        releases and environments to postgres and write the event into
        eventstream. From there it will be picked up by Snuba and
        post-processing.

        We re-insert events with duplicate IDs into Snuba, which is responsible
        for deduplicating events. Since deduplication in Snuba is on the primary
        key (based on event ID, project ID and day), events with same IDs are only
        deduplicated if their timestamps fall on the same day. The latest event
        always wins and overwrites the value of events received earlier in that day.
```

---

</SwmSnippet>

```mermaid
graph TD;
subgraph src/sentry/backup
  importing:::mainFlowStyle --> import_in_organization_scope:::mainFlowStyle
end
subgraph src/sentry/backup
  import_in_organization_scope:::mainFlowStyle --> _import:::mainFlowStyle
end
subgraph src/sentry/backup
  _import:::mainFlowStyle --> do_writes
end
subgraph src/sentry/backup
  _import:::mainFlowStyle --> resolve_org_slugs_from_pk_map
end
subgraph src/sentry
  _import:::mainFlowStyle --> bulk_create_organization_slugs
end
subgraph src/sentry/backup
  _import:::mainFlowStyle --> do_write:::mainFlowStyle
end
subgraph src/sentry/backup
  do_write:::mainFlowStyle --> import_by_model:::mainFlowStyle
end
subgraph src/sentry/backup
  import_by_model:::mainFlowStyle --> write_relocation_import:::mainFlowStyle
end
subgraph src/sentry
  write_relocation_import:::mainFlowStyle --> save:::mainFlowStyle
end
subgraph src/sentry
  save:::mainFlowStyle --> save_transaction_events
end

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

# Flow drill down

First, we'll zoom into this section of the flow:

```mermaid
graph TD;
subgraph src/sentry
  importing:::mainFlowStyle --> import_in_organization_scope:::mainFlowStyle
end
subgraph src/sentry
  import_in_organization_scope:::mainFlowStyle --> _import:::mainFlowStyle
end
subgraph src/sentry
  _import:::mainFlowStyle --> do_writes
end
subgraph src/sentry
  _import:::mainFlowStyle --> resolve_org_slugs_from_pk_map
end
subgraph src/sentry
  _import:::mainFlowStyle --> bulk_create_organization_slugs
end
subgraph src/sentry
  _import:::mainFlowStyle --> do_write:::mainFlowStyle
end
subgraph src/sentry
  do_write:::mainFlowStyle --> a1h4v[...]
end
subgraph src/sentry
  bulk_create_organization_slugs --> bulk_create_organization_slug_reservations
end
subgraph src/sentry
  resolve_org_slugs_from_pk_map --> bulk_create_organization_slugs
end

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="1049">

---

# Importing Process

The importing process starts with the `importing` function. This function initiates the relocation task and opens the relocation file. It then calls the `import_in_organization_scope` function with the relocation data and other parameters.

```python
def importing(uuid: str) -> None:
    """
    Perform the import on the actual live instance we are targeting.

    This function is NOT idempotent - if an import breaks, we should just abandon it rather than
    trying it again!
    """

    relocation: Relocation | None
    attempts_left: int
    (relocation, attempts_left) = start_relocation_task(
        uuid=uuid,
        task=OrderedTask.IMPORTING,
        allowed_task_attempts=MAX_SLOW_TASK_ATTEMPTS,
    )
    if relocation is None:
        return

    with retry_task_or_fail_relocation(
        relocation,
        OrderedTask.IMPORTING,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/backup/imports.py" line="520">

---

The `import_in_organization_scope` function performs an import in the `Organization` scope. It imports only models with `RelocationScope.User` or `RelocationScope.Organization` from the provided `src` file. It then calls the `_import` function.

```python
def import_in_organization_scope(
    src: IO[bytes],
    *,
    decryptor: Decryptor | None = None,
    flags: ImportFlags | None = None,
    org_filter: set[str] | None = None,
    printer: Printer,
):
    """
    Perform an import in the `Organization` scope, meaning that only models with
    `RelocationScope.User` or `RelocationScope.Organization` will be imported from the provided
    `src` file.

    The `org_filter` argument allows imports to be filtered by organization slug. If the argument
    is set to `None`, there is no filtering, meaning all encountered organizations and users are
    imported.
    """

    # Import here to prevent circular module resolutions.
    from sentry.models.organization import Organization

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/backup/imports.py" line="86">

---

The `_import` function is the core of the import process. It reads the content of the import file, processes it, and writes the data into the database. It also resolves organization slugs from the primary key map and creates organization slugs.

```python
def _import(
    src: IO[bytes],
    scope: ImportScope,
    *,
    decryptor: Decryptor | None = None,
    flags: ImportFlags | None = None,
    filter_by: Filter | None = None,
    printer: Printer,
):
    """
    Imports core data for a Sentry installation.

    It is generally preferable to avoid calling this function directly, as there are certain
    combinations of input parameters that should not be used together. Instead, use one of the other
    wrapper functions in this file, named `import_in_XXX_scope()`.
    """

    # Import here to prevent circular module resolutions.
    from sentry.models.email import Email
    from sentry.models.organization import Organization
    from sentry.models.organizationmember import OrganizationMember
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/backup/imports.py" line="392">

---

The `do_writes` function is responsible for writing the imported data into the database. It iterates over the models in the content and calls the `do_write` function for each model.

```python
    # Extract some write logic into its own internal function, so that we may call it irrespective
    # of how we do atomicity: on a per-model (if using multiple dbs) or global (if using a single
    # db) basis.
    def do_writes(pk_map: PrimaryKeyMap) -> None:
        nonlocal deferred_org_auth_tokens, import_write_context

        for model_name, json_data, offset in yield_json_models(content):
            if model_name == org_auth_token_model_name:
                deferred_org_auth_tokens.append(json_data)
                continue

            do_write(import_write_context, pk_map, model_name, json_data, offset)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/backup/imports.py" line="405">

---

The `resolve_org_slugs_from_pk_map` function resolves slugs for all imported organization models via the PrimaryKeyMap and reconciles their slug globally by issuing a slug update. It then calls the `bulk_create_organization_slugs` function.

```python
    # Resolves slugs for all imported organization models via the PrimaryKeyMap and reconciles
    # their slug globally via control silo by issuing a slug update.
    def resolve_org_slugs_from_pk_map(pk_map: PrimaryKeyMap):
        from sentry.services.organization import organization_provisioning_service

        org_pk_mapping = pk_map.mapping[str(org_model_name)]
        if not org_pk_mapping:
            return

        slug_mapping: dict[int, str] = {}
        for old_primary_key in org_pk_mapping:
            org_id, _, org_slug = org_pk_mapping[old_primary_key]
            slug_mapping[org_id] = org_slug or ""

        if len(slug_mapping) > 0:
            # HACK(azaslavsky): Okay, this gets a bit complicated, but bear with me: the following
            # `bulk_create...` calls will result in some actions on the control silo that call back
            # into this region. So the client (this region) calls the server (the control silo)
            # which may need to make one or more calls back into the client (this region). Because
            # some of our `OrganizationMemberTeam` outboxes may not be drained due to the HACK we
            # performed in `import_export/impl.py` (see that file for more details), there may be a
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/services/organization/provisioning.py" line="141">

---

The `bulk_create_organization_slugs` function creates slug reservations for imported organizations that already exist on the region. It calls the `bulk_create_organization_slug_reservations` function to create the slug reservations.

```python
    def bulk_create_organization_slugs(
        self, slug_mapping: dict[int, str], region_name: str | None = None
    ):
        """
        CAUTION: DO NOT USE THIS OUTSIDE OF THE IMPORT/RELOCATION CONTEXT

        Organizations are meant to be provisioned via the
         `provision_organization_in_region` method, which handles both slug
         reservation and organization creation.

        Bulk creates slug reservations for imported organizations that already
        exist on the region. Each target organization is provided as a tuple of
        Organization ID (int) and base slug (str).

        :param org_ids_and_slugs: A set of tuples containing an organization ID
        and base slug.
        :param region_name: The region where the imported organizations exist
        :return:
        """
        destination_region_name = self._validate_or_default_region(region_name=region_name)

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/hybridcloud/services/control_organization_provisioning/impl.py" line="256">

---

The `bulk_create_organization_slug_reservations` function creates slug reservations for imported organizations that already exist on the region. It saves the slug reservations and validates that the primary slug has been updated.

```python
    def bulk_create_organization_slug_reservations(
        self,
        *,
        region_name: str,
        slug_mapping: dict[int, str],
    ) -> None:
        slug_reservations_to_create: list[OrganizationSlugReservation] = []

        with outbox_context(transaction.atomic(router.db_for_write(OrganizationSlugReservation))):
            for org_id, slug in slug_mapping.items():
                slug_reservation = OrganizationSlugReservation(
                    slug=self._generate_org_slug(slug=slug, region_name=region_name),
                    organization_id=org_id,
                    reservation_type=OrganizationSlugReservationType.TEMPORARY_RENAME_ALIAS.value,
                    user_id=-1,
                    region_name=region_name,
                )
                slug_reservation.save(unsafe_write=True)

                slug_reservations_to_create.append(slug_reservation)

```

---

</SwmSnippet>

Now, lets zoom into this section of the flow:

```mermaid
graph TD;
subgraph src/sentry/backup
  do_write:::mainFlowStyle --> import_by_model:::mainFlowStyle
end
subgraph src/sentry/backup
  import_by_model:::mainFlowStyle --> write_relocation_import:::mainFlowStyle
end
subgraph src/sentry/event_manager.py
  write_relocation_import:::mainFlowStyle --> save:::mainFlowStyle
end

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

<SwmSnippet path="/src/sentry/backup/imports.py" line="295">

---

# Importing Data

The `do_write` function is the starting point of the import process. It takes in various parameters including the model name and JSON data to be imported. It then retrieves the model's dependencies and uses the `ImportExportService` to get the appropriate importer for the model. The `import_by_model` function is then called with the necessary parameters to perform the actual import.

```python
    # Perform the write of a single model.
    def do_write(
        import_write_context: ImportWriteContext,
        pk_map: PrimaryKeyMap,
        model_name: NormalizedModelName,
        json_data: Any,
        offset: int,
    ) -> None:
        model_relations = import_write_context.dependencies.get(model_name)
        if not model_relations:
            return

        dep_models = {get_model_name(d) for d in model_relations.get_dependencies_for_relocation()}
        import_by_model = ImportExportService.get_importer_for_model(model_relations.model)
        model_name_str = str(model_name)
        min_ordinal = offset + 1

        extra = {
            "model_name": model_name_str,
            "import_uuid": flags.import_uuid,
            "min_ordinal": min_ordinal,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/backup/services/import_export/impl.py" line="104">

---

The `import_by_model` function is responsible for importing a single model. It validates the input parameters, retrieves the model, and checks if it can be imported based on its silo mode. It then deserializes the JSON data into model instances and writes them to the database. If any errors occur during this process, they are handled and an appropriate `RpcImportError` is returned.

```python
    """

    def import_by_model(
        self,
        *,
        model_name: str,
        scope: RpcImportScope | None = None,
        flags: RpcImportFlags,
        filter_by: list[RpcFilter],
        pk_map: RpcPrimaryKeyMap,
        json_data: str,
        min_ordinal: int,
    ) -> RpcImportResult:
        if min_ordinal < 1:
            return RpcImportError(
                kind=RpcImportErrorKind.InvalidMinOrdinal,
                on=InstanceID(model_name),
                reason=f"The model `{model_name}` was offset with an invalid `min_ordinal` of `{min_ordinal}`",
            )

        batch_model_name = NormalizedModelName(model_name)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/backup/mixins.py" line="13">

---

The `write_relocation_import` function is called within `import_by_model` to perform the actual database write. It checks for potential collisions based on unique sets and handles them appropriately. If the model instance is new, it is saved to the database and its primary key is returned along with the `ImportKind.Inserted` flag. If the model instance already exists, it is either updated or its existing primary key is returned with the `ImportKind.Existing` flag, depending on the `overwrite_configs` flag.

```python
    """

    # TODO(getsentry/team-ospo#190): Clean up the type checking in this method.
    def write_relocation_import(
        self, scope: ImportScope, flags: ImportFlags
    ) -> tuple[int, ImportKind] | None:
        # Get all unique sets that will potentially cause collisions.
        uniq_sets = dependencies()[get_model_name(self)].get_uniques_without_foreign_keys()  # type: ignore[arg-type]

        # Don't use this mixin for models with multiple unique sets; write custom logic instead.
        assert len(uniq_sets) <= 1

        # Must set `__relocation_custom_ordinal__` on models that use this mixin.
        assert getattr(self.__class__, "__relocation_custom_ordinal__", None) is not None

        if self.get_relocation_scope() == RelocationScope.Config:  # type: ignore[attr-defined]
            if len(uniq_sets) == 1:
                uniq_set = uniq_sets[0]
                query = dict()
                for uniq_field_name in uniq_set:
                    if getattr(self, uniq_field_name, None) is not None:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/event_manager.py" line="442">

---

The `save` function is the final step in the import process. It normalizes the event data, retrieves the project, and prepares the job data. Depending on the event type, it calls either `save_transaction_events` or `save_generic_events` to save the event data. It also handles any potential collisions and updates counters and frequencies.

```python
    def save(
        self,
        project_id: int | None,
        raw: bool = False,
        assume_normalized: bool = False,
        start_time: float | None = None,
        cache_key: str | None = None,
        skip_send_first_transaction: bool = False,
        has_attachments: bool = False,
    ) -> Event:
        """
        After normalizing and processing an event, save adjacent models such as
        releases and environments to postgres and write the event into
        eventstream. From there it will be picked up by Snuba and
        post-processing.

        We re-insert events with duplicate IDs into Snuba, which is responsible
        for deduplicating events. Since deduplication in Snuba is on the primary
        key (based on event ID, project ID and day), events with same IDs are only
        deduplicated if their timestamps fall on the same day. The latest event
        always wins and overwrites the value of events received earlier in that day.
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
