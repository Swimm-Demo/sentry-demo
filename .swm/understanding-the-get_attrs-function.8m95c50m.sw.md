---
title: Understanding the get_attrs Function
---
<SwmSnippet path="/src/sentry/api/serializers/models/group.py" line="188">

---

# get_attrs Function

The `get_attrs` function is a method that retrieves a variety of attributes related to a list of `Group` objects. It takes in a list of `Group` objects, a `user`, and any additional arguments. The function populates the cache with the `GroupMeta` objects related to the `Group` objects in the list. It also prefetches related objects to avoid unnecessary queries.

```python
    def get_attrs(
        self, item_list: Sequence[Group], user: Any, **kwargs: Any
    ) -> MutableMapping[Group, MutableMapping[str, Any]]:
        GroupMeta.objects.populate_cache(item_list)

        # Note that organization is necessary here for use in `_get_permalink` to avoid
        # making unnecessary queries.
        prefetch_related_objects(item_list, "project__organization")

        if user.is_authenticated and item_list:
            bookmarks = set(
                GroupBookmark.objects.filter(user_id=user.id, group__in=item_list).values_list(
                    "group_id", flat=True
                )
            )
            seen_groups = dict(
                GroupSeen.objects.filter(user_id=user.id, group__in=item_list).values_list(
                    "group_id", "last_seen"
                )
            )
            subscriptions = self._get_subscriptions(item_list, user)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/serializers/models/group.py" line="197">

---

# User Authentication and Data Retrieval

If the user is authenticated and the item list is not empty, the function retrieves bookmarks, seen groups, and subscriptions related to the user and the groups in the item list. If the user is not authenticated or the item list is empty, it sets bookmarks, seen groups, and subscriptions to their default values.

```python
        if user.is_authenticated and item_list:
            bookmarks = set(
                GroupBookmark.objects.filter(user_id=user.id, group__in=item_list).values_list(
                    "group_id", flat=True
                )
            )
            seen_groups = dict(
                GroupSeen.objects.filter(user_id=user.id, group__in=item_list).values_list(
                    "group_id", "last_seen"
                )
            )
            subscriptions = self._get_subscriptions(item_list, user)
        else:
            bookmarks = set()
            seen_groups = {}
            subscriptions = defaultdict(lambda: (False, False, None))
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/serializers/models/group.py" line="214">

---

# Resolving Assignees and Resolutions

The function then serializes assignees for the groups in the item list and resolves any release or commit resolutions. It also retrieves any users related to the resolutions or ignored items and serializes them.

```python
        resolved_assignees = self._serialize_assignees(item_list)

        ignore_items = {g.group_id: g for g in GroupSnooze.objects.filter(group__in=item_list)}

        release_resolutions, commit_resolutions = self._resolve_resolutions(item_list, user)

        user_ids = {
            user_id
            for user_id in itertools.chain(
                (r[-1] for r in release_resolutions.values()),
                (r.actor_id for r in ignore_items.values()),
            )
            if user_id is not None
        }
        if user_ids:
            serialized_users = user_service.serialize_many(
                filter={"user_ids": user_ids, "is_active": True},
                as_user=serialize_generic_user(user),
            )
            actors = {id: u for id, u in zip(user_ids, serialized_users)}
        else:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/serializers/models/group.py" line="237">

---

# Final Data Compilation

Finally, the function compiles all the retrieved and processed data into a result dictionary. For each group in the item list, it includes the group's id, assignee, bookmark status, subscription status, seen status, annotations, ignore status, resolution, share id, and authorization status. It also includes whether the group is unhandled and any additional seen stats.

```python
        share_ids = dict(
            GroupShare.objects.filter(group__in=item_list).values_list("group_id", "uuid")
        )

        seen_stats = self._get_seen_stats(item_list, user)

        organization_id_list = list({item.project.organization_id for item in item_list})
        # if no groups, then we can't proceed but this seems to be a valid use case
        if not item_list:
            return {}
        if len(organization_id_list) > 1:
            # this should never happen but if it does we should know about it
            logger.warning(
                "Found multiple organizations for groups: %s, with orgs: %s",
                [item.id for item in item_list],
                organization_id_list,
            )

        # should only have 1 org at this point
        organization_id = organization_id_list[0]

```

---

</SwmSnippet>

# Flow drill down

```mermaid
graph TD;

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

<SwmSnippet path="/src/sentry/api/serializers/models/group.py" line="188">

---

# get_attrs Function

The `get_attrs` function is a method that retrieves a variety of attributes related to a list of `Group` objects. It takes in a list of `Group` objects, a `user`, and any additional arguments. The function populates the cache with the `GroupMeta` objects related to the `Group` objects in the list. It also prefetches related objects to avoid unnecessary queries.

```python
    def get_attrs(
        self, item_list: Sequence[Group], user: Any, **kwargs: Any
    ) -> MutableMapping[Group, MutableMapping[str, Any]]:
        GroupMeta.objects.populate_cache(item_list)

        # Note that organization is necessary here for use in `_get_permalink` to avoid
        # making unnecessary queries.
        prefetch_related_objects(item_list, "project__organization")

        if user.is_authenticated and item_list:
            bookmarks = set(
                GroupBookmark.objects.filter(user_id=user.id, group__in=item_list).values_list(
                    "group_id", flat=True
                )
            )
            seen_groups = dict(
                GroupSeen.objects.filter(user_id=user.id, group__in=item_list).values_list(
                    "group_id", "last_seen"
                )
            )
            subscriptions = self._get_subscriptions(item_list, user)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/serializers/models/group.py" line="197">

---

# User Authentication and Data Retrieval

If the user is authenticated and the item list is not empty, the function retrieves bookmarks, seen groups, and subscriptions related to the user and the groups in the item list. If the user is not authenticated or the item list is empty, it sets bookmarks, seen groups, and subscriptions to their default values.

```python
        if user.is_authenticated and item_list:
            bookmarks = set(
                GroupBookmark.objects.filter(user_id=user.id, group__in=item_list).values_list(
                    "group_id", flat=True
                )
            )
            seen_groups = dict(
                GroupSeen.objects.filter(user_id=user.id, group__in=item_list).values_list(
                    "group_id", "last_seen"
                )
            )
            subscriptions = self._get_subscriptions(item_list, user)
        else:
            bookmarks = set()
            seen_groups = {}
            subscriptions = defaultdict(lambda: (False, False, None))
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/serializers/models/group.py" line="214">

---

# Resolving Assignees and Resolutions

The function then serializes assignees for the groups in the item list and resolves any release or commit resolutions. It also retrieves any users related to the resolutions or ignored items and serializes them.

```python
        resolved_assignees = self._serialize_assignees(item_list)

        ignore_items = {g.group_id: g for g in GroupSnooze.objects.filter(group__in=item_list)}

        release_resolutions, commit_resolutions = self._resolve_resolutions(item_list, user)

        user_ids = {
            user_id
            for user_id in itertools.chain(
                (r[-1] for r in release_resolutions.values()),
                (r.actor_id for r in ignore_items.values()),
            )
            if user_id is not None
        }
        if user_ids:
            serialized_users = user_service.serialize_many(
                filter={"user_ids": user_ids, "is_active": True},
                as_user=serialize_generic_user(user),
            )
            actors = {id: u for id, u in zip(user_ids, serialized_users)}
        else:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/serializers/models/group.py" line="237">

---

# Final Data Compilation

Finally, the function compiles all the retrieved and processed data into a result dictionary. For each group in the item list, it includes the group's id, assignee, bookmark status, subscription status, seen status, annotations, ignore status, resolution, share id, and authorization status. It also includes whether the group is unhandled and any additional seen stats.

```python
        share_ids = dict(
            GroupShare.objects.filter(group__in=item_list).values_list("group_id", "uuid")
        )

        seen_stats = self._get_seen_stats(item_list, user)

        organization_id_list = list({item.project.organization_id for item in item_list})
        # if no groups, then we can't proceed but this seems to be a valid use case
        if not item_list:
            return {}
        if len(organization_id_list) > 1:
            # this should never happen but if it does we should know about it
            logger.warning(
                "Found multiple organizations for groups: %s, with orgs: %s",
                [item.id for item in item_list],
                organization_id_list,
            )

        # should only have 1 org at this point
        organization_id = organization_id_list[0]

```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
