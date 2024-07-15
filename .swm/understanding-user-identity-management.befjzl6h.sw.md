---
title: Understanding User Identity Management
---
Identity in the Main Application refers to the representation of a user within the system. It is used to authenticate and authorize users, as well as to store and manage user-specific data.

The Identity is primarily managed by the RpcIdentity class, which contains attributes such as id, idp_id (IdentityProvider id), user_id, external_id, and data. The get_identity method is used to retrieve the identity provider associated with the identity.

The refresh_identity function is used to update the identity data by making a request to the identity provider's refresh token URL. If the refresh token is missing, an IdentityNotValid exception is raised.

The build_identity function is used to construct an identity from the state data. This function is implemented differently by different identity providers. For example, the Google identity provider decodes the id_token from the state data to construct the identity.

The update_data function in the identity service is used to update an identity's data. This function takes an identity_id and data as parameters and returns an updated RpcIdentity instance.

<SwmSnippet path="/src/sentry/identity/services/identity/serial.py" line="17">

---

# RpcIdentity Class

The RpcIdentity class is used to represent an identity within the system. It contains attributes such as id, idp_id (IdentityProvider id), user_id, external_id, and data.

```python
def serialize_identity(identity: "Identity") -> RpcIdentity:
    return RpcIdentity(
        id=identity.id,
        idp_id=identity.idp_id,
        user_id=identity.user_id,
        external_id=identity.external_id,
        data=identity.data,
    )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/identity/services/identity/impl.py" line="45">

---

# get_identity Function

The get_identity function is used to retrieve the identity provider associated with the identity. It calls the get_identities function to retrieve all identities that match the provided filter and returns the first one.

```python
    def get_identity(self, *, filter: IdentityFilterArgs) -> RpcIdentity | None:
        identities = self.get_identities(filter=filter)
        if len(identities) == 0:
            return None
        return identities[0]
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/identity/oauth2.py" line="181">

---

# refresh_identity Function

The refresh_identity function is used to update the identity data by making a request to the identity provider's refresh token URL. If the refresh token is missing, an IdentityNotValid exception is raised.

```python
    def refresh_identity(self, identity, *args, **kwargs):
        refresh_token = identity.data.get("refresh_token")

        if not refresh_token:
            raise IdentityNotValid("Missing refresh token")

        # XXX(meredith): This is used in VSTS's `get_refresh_token_params`
        kwargs["identity"] = identity
        data = self.get_refresh_token_params(refresh_token, *args, **kwargs)

        req = safe_urlopen(
            url=self.get_refresh_token_url(), headers=self.get_refresh_token_headers(), data=data
        )

        try:
            body = safe_urlread(req)
            payload = orjson.loads(body)
        except orjson.JSONDecodeError:
            payload = {}

        self.handle_refresh_error(req, payload)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/identity/base.py" line="17">

---

# build_identity Function

The build_identity function is used to construct an identity from the state data. This function is implemented differently by different identity providers. For example, the Google identity provider decodes the id_token from the state data to construct the identity.

```python
    def build_identity(self, state):
        """
        Return a mapping containing the identity information.

        - ``state`` is the resulting data captured by the pipeline

        >>> {
        >>>     "id":     "foo@example.com",
        >>>     "email":  "foo@example.com",
        >>>     "name":   "Foo Bar",
        >>>     "scopes": ['email', ...],
        >>>     "data":   { ... },
        >>> }

        The ``id`` key is required.

        The ``id`` may be passed in as a ``MigratingIdentityId`` should the
        the id key be migrating from one value to another and have multiple
        lookup values.

        If the identity can not be constructed an ``IdentityNotValid`` error
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/identity/services/identity/service.py" line="80">

---

# update_data Function

The update_data function in the identity service is used to update an identity's data. This function takes an identity_id and data as parameters and returns an updated RpcIdentity instance.

```python
    def update_data(self, *, identity_id: int, data: Any) -> RpcIdentity | None:
        """
        Updates an Identity's data.
        :param identity_id:
        :return: RpcIdentity
        """
```

---

</SwmSnippet>

# Identity Functions

Let's delve into the main functions related to Identity.

<SwmSnippet path="/src/sentry/identity/services/identity/impl.py" line="42">

---

## get_identities

The `get_identities` function retrieves a list of RpcIdentity instances based on the given filters. It uses the `get_many` function to fetch the identities.

```python
    def get_identities(self, *, filter: IdentityFilterArgs) -> list[RpcIdentity]:
        return self._FQ.get_many(filter=filter)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/identity/services/identity/impl.py" line="45">

---

## get_identity

The `get_identity` function retrieves a single RpcIdentity instance based on the given filters. It uses the `get_identities` function to fetch the identities and returns the first one.

```python
    def get_identity(self, *, filter: IdentityFilterArgs) -> RpcIdentity | None:
        identities = self.get_identities(filter=filter)
        if len(identities) == 0:
            return None
        return identities[0]
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/identity/services/identity/impl.py" line="72">

---

## delete_identities

The `delete_identities` function deletes the set of identities associated with a user and organization context. It uses the `filter` function to find the identities and then deletes them.

```python
    def delete_identities(self, user_id: int, organization_id: int) -> None:
        """
        Deletes the set of identities associated with a user and organization context.
        """
        for ai in AuthIdentity.objects.filter(
            user_id=user_id, auth_provider__organization_id=organization_id
        ):
            ai.delete()
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/identity/services/identity/impl.py" line="81">

---

## update_data

The `update_data` function updates an Identity's data. It first fetches the identity using the `filter` function, then updates the data and returns the updated identity.

```python
    def update_data(self, *, identity_id: int, data: Any) -> RpcIdentity | None:
        identity: Identity | None = Identity.objects.filter(id=identity_id).first()
        if identity is None:
            return None
        identity.update(data=data)
        return serialize_identity(identity)
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
