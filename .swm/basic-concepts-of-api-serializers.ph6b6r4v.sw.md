---
title: Basic concepts of Api Serializers
---
Serializers in the Api of sentry-demo are used to convert complex data types, like Django models, into Python native datatypes that can then be easily rendered into JSON, XML or other content types. They provide a mechanism of deserialization which validates the incoming data.

The Serializer class in sentry-demo is a base class for creating serializers. It provides a basic structure for serializing and deserializing data. The Serializer class is used throughout the codebase, and is often subclassed to create custom serializers for specific models.

The `ApiApplicationSerializer` class is an example of a custom serializer. It inherits from the Serializer class and overrides the `serialize` method to define the serialization logic for the `ApiApplication` model. The `serialize` method takes an instance of `ApiApplication` and returns a dictionary that represents the serialized data.

<SwmSnippet path="/src/sentry/api/serializers/base.py" line="27">

---

# Base Serializer

This is the base `serialize` function. It takes a list of objects and a user, and optionally a serializer. It turns a model (or list of models) into a python object made entirely of primitives. If no serializer is provided, it looks up the Serializer in the registry by the objects' type.

```python
def serialize(
    objects: Any | Sequence[Any],
    user: Any | None = None,
    serializer: Any | None = None,
    **kwargs: Any,
) -> Any:
    """
    Turn a model (or list of models) into a python object made entirely of primitives.

    :param objects: A list of objects
    :param user: The user who will be viewing the objects. Omit to view as `AnonymousUser`.
    :param serializer: The `Serializer` class whose logic we'll use to serialize
        `objects` (see below.) Omit to just look up the Serializer in the
        registry by the `objects`'s type.
    :param kwargs Any
    :returns A list of the serialized versions of `objects`.
    """
    if user is None:
        user = AnonymousUser()

    if not objects:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/serializers/models/apiapplication.py" line="10">

---

# Custom Serializers

This is an example of a custom serializer. The `ApiApplicationSerializer` class inherits from the Serializer class and overrides the `serialize` method to define the serialization logic for the `ApiApplication` model. The `serialize` method takes an instance of `ApiApplication` and returns a dictionary that represents the serialized data.

```python
class ApiApplicationSerializer(Serializer):
    def serialize(self, obj, attrs, user):
        is_secret_visible = obj.date_added > timezone.now() - timedelta(days=1)
        return {
            "id": obj.client_id,
            "clientID": obj.client_id,
            "clientSecret": obj.client_secret if is_secret_visible else None,
            "name": obj.name,
            "homepageUrl": obj.homepage_url,
            "privacyUrl": obj.privacy_url,
            "termsUrl": obj.terms_url,
            "allowedOrigins": obj.get_allowed_origins(),
            "redirectUris": obj.get_redirect_uris(),
        }
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/serializers/models/user.py" line="114">

---

# Using Serializers

This is an example of how to use a serializer. The `UserSerializer` class is used to serialize instances of the `User` model. It defines the `serialize` method which takes an instance of `User` and returns a dictionary that represents the serialized data. It also defines the `get_attrs` method which fetches all of the associated data needed to serialize the objects in `item_list`.

```python
class UserSerializer(Serializer):
    def _user_is_requester(self, obj: User, requester: User | AnonymousUser | RpcUser) -> bool:
        if isinstance(requester, User):
            return bool(requester == obj)
        if isinstance(requester, RpcUser):
            return bool(requester.id == obj.id)
        return False

    def _get_identities(
        self, item_list: Sequence[User], user: User
    ) -> dict[int, list[AuthIdentity]]:

        if not (env.request and has_elevated_mode(env.request)):
            item_list = [x for x in item_list if x.id == user.id]

        queryset = AuthIdentity.objects.filter(
            user_id__in=[i.id for i in item_list]
        ).select_related(
            "auth_provider",
        )

```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
