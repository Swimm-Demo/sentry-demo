---
title: Understanding Database Models in Main Application
---
Models in the main application of sentry-demo are used as the main data structures for the application. They are defined in various modules such as 'sentry.db.models' and 'django.db.models'. These models are used to define the structure of the database tables and their relationships. For instance, the 'ApiApplication' model in '[sentry.models.apiapplication.py](http://sentry.models.apiapplication.py)' defines the structure of the 'ApiApplication' table in the database. It includes fields like 'client_id', 'client_secret', 'owner', and 'name'. Models are also used to define methods that operate on the data associated with an instance of the model.

<SwmSnippet path="/src/sentry/models/importchunk.py" line="11">

---

# Defining a Model

Here, the `BaseImportChunk` model is defined. It inherits from `DefaultFieldsModel` and defines several fields, such as `import_uuid` (a UUID field), `model` (a character field), and `inserted_map` (a JSON field).

```python
class BaseImportChunk(DefaultFieldsModel):
    """
    Base class representing the map of import pks to final, post-import database pks.
    """

    __relocation_scope__ = RelocationScope.Excluded

    # Every import has a UUID assigned to it. If the import was triggered by a relocation, this UUID
    # simply inherits from the `Relocation` model, and can be used to connect back to it. If it is
    # not done via the `Relocation` pathway (that is, someone triggered it using a `sentry import`
    # command via the CLI), it is randomly generated, but shared between all chunks of the same
    # import.
    import_uuid = UUIDField(db_index=True)

    # The name of model that was imported.
    model = models.CharField(db_index=True, max_length=64)

    # The minimum ordinal (inclusive), relative to the source JSON, imported by this chunk.
    min_ordinal = BoundedBigIntegerField()

    # The maximum ordinal (inclusive), relative to the source JSON, imported by this chunk.
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/models/importchunk.py" line="70">

---

# Using a Model

Here, the `BaseImportChunk` model is used as a base class to define three new models: `RegionImportChunk`, `ControlImportChunk`, and `ControlImportChunkReplica`. This demonstrates how models can be reused and extended.

```python
@region_silo_model
class RegionImportChunk(BaseImportChunk):
    """
    Records the pk mapping for the successful import of instances of a model that lives in the
    region silo.
    """

    __relocation_scope__ = RelocationScope.Excluded

    class Meta:
        app_label = "sentry"
        db_table = "sentry_regionimportchunk"
        unique_together = (("import_uuid", "model", "min_ordinal"),)


@control_silo_model
class ControlImportChunk(BaseImportChunk):
    """
    Records the pk mapping for the successful import of instances of a model that lives in the
    control silo.
    """
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
