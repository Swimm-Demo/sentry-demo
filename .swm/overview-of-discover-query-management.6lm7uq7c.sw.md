---
title: Overview of Discover Query Management
---
Discover in the Main Application refers to a functionality that allows users to save and manage their queries. This is primarily handled by the `DiscoverSavedQuery` class, which represents a saved Discover query. It contains various fields such as `projects`, `organization`, `name`, `query`, `version`, and `dataset` among others, which define the properties of a saved query.

The `DiscoverSavedQuery` class is used in various parts of the application. For instance, it is used in migrations to create and modify the `DiscoverSavedQuery` model. It is also used in tasks for bulk deletion of saved queries.

The Discover functionality also includes endpoints for managing key transactions and homepage queries. These endpoints allow users to create, retrieve, update, and delete key transactions and homepage queries. They use the `DiscoverSavedQuery` model to perform these operations.

<SwmSnippet path="/src/sentry/discover/models.py" line="81">

---

# DiscoverSavedQuery Class

This is the `DiscoverSavedQuery` class which represents a saved Discover query. It contains various fields such as `projects`, `organization`, `name`, `query`, `version`, and `dataset` among others, which define the properties of a saved query.

```python
class DiscoverSavedQuery(Model):
    """
    A saved Discover query
    """

    __relocation_scope__ = RelocationScope.Excluded

    projects = models.ManyToManyField("sentry.Project", through=DiscoverSavedQueryProject)
    organization = FlexibleForeignKey("sentry.Organization")
    created_by_id = HybridCloudForeignKey("sentry.User", null=True, on_delete="SET_NULL")
    name = models.CharField(max_length=255)
    query = JSONField()
    version = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    visits = BoundedBigIntegerField(null=True, default=1)
    last_visited = models.DateTimeField(null=True, default=timezone.now)
    is_homepage = models.BooleanField(null=True, blank=True)
    dataset = BoundedPositiveIntegerField(
        choices=DiscoverSavedQueryTypes.as_choices(), default=DiscoverSavedQueryTypes.DISCOVER
    )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/migrations/0522_migrate_discover_savedquery_worldmaps.py" line="12">

---

# Usage in Migrations

`DiscoverSavedQuery` is used in migrations to filter saved queries that contain a specific display type.

```python
) -> None:
    DiscoverSavedQuery = apps.get_model("sentry", "DiscoverSavedQuery")
    savedQueries = DiscoverSavedQuery.objects.filter(query__contains={"display": "worldmap"})
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/discover/tasks.py" line="6">

---

# Usage in Tasks

`DiscoverSavedQuery` is also used in tasks for bulk deletion of saved queries.

```python
deletions.default_manager.register(models.DiscoverSavedQuery, BulkModelDeletionTask)
deletions.default_manager.register(models.DiscoverSavedQueryProject, BulkModelDeletionTask)
```

---

</SwmSnippet>

# Discover Endpoints

Discover Endpoints

<SwmSnippet path="/src/sentry/discover/endpoints/discover_saved_queries.py" line="21">

---

## DiscoverSavedQueriesEndpoint

The `DiscoverSavedQueriesEndpoint` class defines endpoints for getting and posting saved queries. The `get` method retrieves a list of saved queries for an organization, while the `post` method creates a new saved query.

```python
@region_silo_endpoint
class DiscoverSavedQueriesEndpoint(OrganizationEndpoint):
    publish_status = {
        "GET": ApiPublishStatus.UNKNOWN,
        "POST": ApiPublishStatus.UNKNOWN,
    }
    owner = ApiOwner.PERFORMANCE
    permission_classes = (DiscoverSavedQueryPermission,)

    def has_feature(self, organization, request):
        return features.has(
            "organizations:discover", organization, actor=request.user
        ) or features.has("organizations:discover-query", organization, actor=request.user)

    def get(self, request: Request, organization) -> Response:
        """
        List saved queries for organization
        """
        if not self.has_feature(organization, request):
            return self.respond(status=404)

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/discover/endpoints/discover_saved_query_detail.py" line="116">

---

## DiscoverSavedQueryVisitEndpoint

The `DiscoverSavedQueryVisitEndpoint` class defines an endpoint for posting visits to a saved query. The `post` method updates the `last_visited` and `visits` fields of the saved query.

```python
@region_silo_endpoint
class DiscoverSavedQueryVisitEndpoint(DiscoverSavedQueryBase):
    publish_status = {
        "POST": ApiPublishStatus.PRIVATE,
    }

    def has_feature(self, organization, request):
        return features.has("organizations:discover-query", organization, actor=request.user)

    def post(self, request: Request, organization, query) -> Response:
        """
        Update last_visited and increment visits counter
        """
        if not self.has_feature(organization, request):
            return self.respond(status=404)

        query.visits = F("visits") + 1
        query.last_visited = timezone.now()
        query.save(update_fields=["visits", "last_visited"])

        return Response(status=204)
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
