---
title: Introduction to Authentication and Access Control Services
---
Services in the Auth module of the sentry-demo project are a collection of functionalities that handle authentication and access control. They are organized into two main categories: Auth services and Access services.

Auth services, defined in the 'auth' directory, are responsible for creating and managing authentication identities. They provide functionalities such as creating an authentication identity, getting organization authentication configuration, and more. The 'auth_service' constant is an instance of the AuthService class, which provides these functionalities.

Access services, defined in the 'access' directory, handle access control and permissions. They provide functionalities such as checking if an authentication identity is valid, getting the authentication state of a user, querying the SSO state, and more. The 'access_service' constant is an instance of the AccessService class, which provides these functionalities.

The services interact with each other to provide a comprehensive authentication and access control system. For example, the 'get_user_auth_state' function in the AccessService uses the 'auth_service' to get the authentication identity of a user, and then checks if the identity is valid.

<SwmSnippet path="/src/sentry/auth/services/auth/service.py" line="15">

---

# AuthService

The AuthService class provides methods for managing authentication identities. It includes methods for getting organization authentication configuration, creating an authentication identity, and more. The 'auth_service' constant is an instance of this class.

```python
class AuthService(RpcService):
    key = "auth"
    local_mode = SiloMode.CONTROL

    @classmethod
    def get_local_implementation(cls) -> RpcService:
        from sentry.auth.services.auth.impl import DatabaseBackedAuthService

        return DatabaseBackedAuthService()

    @rpc_method
    @abc.abstractmethod
    def get_org_auth_config(
        self, *, organization_ids: list[int]
    ) -> list[RpcOrganizationAuthConfig]:
        pass

    # TODO: Denormalize this scim enabled flag onto organizations?
    # This is potentially a large list
    @rpc_method
    @abc.abstractmethod
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/auth/services/access/service.py" line="128">

---

# AccessService

The AccessService class provides methods for handling access control and permissions. It includes methods for checking if an authentication identity is valid, getting the authentication state of a user, querying the SSO state, and more. The 'access_service' constant is an instance of this class.

```python
def impl_by_region_resources() -> AccessService:
    from sentry.auth.services.access.impl import RegionAccessService

    return RegionAccessService()


def impl_by_control_resources() -> AccessService:
    from sentry.auth.services.access.impl import ControlAccessService

    return ControlAccessService()
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/auth/services/access/impl.py" line="15">

---

# Interaction between services

The services interact with each other to provide a comprehensive authentication and access control system. For example, the 'get_user_auth_state' function in the AccessService uses the 'auth_service' to get the authentication identity of a user, and then checks if the identity is valid.

```python
from sentry.models.organizationmembermapping import OrganizationMemberMapping
from sentry.organizations.services.organization import RpcOrganizationMemberSummary
from sentry.users.services.user.service import user_service
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
