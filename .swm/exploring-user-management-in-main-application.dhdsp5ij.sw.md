---
title: Exploring User Management in Main Application
---
Users in the Main Application are managed through a dedicated service, as seen in the `src/sentry/users/services/user/service.py` file. This service is responsible for creating, retrieving, and managing user data.

The UserService makes use of a delegation pattern, as indicated by the `create_delegation()` method call. This allows the service to delegate certain tasks to other objects, promoting loose coupling and separation of concerns.

The `get_or_create_by_email` function in `src/sentry/users/services/user/impl.py` is a key part of the user management process. It retrieves a user by their email, or creates a new user if one does not already exist. This function also handles transactions, ensuring data consistency.

The UserService also interacts with the `User` model, which represents the user data in the database. The `User` model is used in various operations such as creating a new user or updating an existing one.

The UserService also handles user authentication. It uses the `AuthIdentity` model to manage authentication identities for users. This allows the service to support multiple authentication methods.

The UserService also provides methods for retrieving and updating user options, as seen in `src/sentry/users/services/user_option/service.py`. User options are additional settings or preferences associated with a user.

<SwmSnippet path="/src/sentry/users/services/user/service.py" line="331">

---

# UserService

The UserService is instantiated here. It uses the delegation pattern, which allows it to delegate certain tasks to other objects, promoting loose coupling and separation of concerns.

```python
user_service = UserService.create_delegation()
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/users/services/user/impl.py" line="204">

---

# get_or_create_by_email

This function retrieves a user by their email, or creates a new user if one does not already exist. It also handles transactions, ensuring data consistency.

```python
    def get_or_create_by_email(
        self, *, email: str, ident: str | None = None, referrer: str | None = None
    ) -> UserCreateResult:
        with transaction.atomic(router.db_for_write(User)):
            rpc_user = self.get_user_by_email(email=email, ident=ident)
            if rpc_user:
                return UserCreateResult(user=rpc_user, created=False)

            # Create User if it doesn't exist
            user = User.objects.create(
                username=f"{slugify(str.split(email, '@')[0])}-{uuid4().hex}",
                email=email,
                name=email,
            )
            user_signup.send_robust(
                sender=self, user=user, source="api", referrer=referrer or "unknown"
            )
            user.update(flags=F("flags").bitor(User.flags.newsletter_consent_prompt))

            return UserCreateResult(user=serialize_rpc_user(user), created=True)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/users/services/user/model.py" line="98">

---

# User Model

The UserService interacts with the `User` model, which represents the user data in the database. The `User` model is used in various operations such as creating a new user or updating an existing one.

```python
    def get_username(self) -> str:  # API compatibility with ORM User
        return self.username
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/users/services/user/impl.py" line="225">

---

# AuthIdentity Model

The UserService uses the `AuthIdentity` model to manage authentication identities for users. This allows the service to support multiple authentication methods.

```python
    def get_user_by_email(
        self,
        *,
        email: str,
        ident: str | None = None,
    ) -> RpcUser | None:
        user_query = User.objects.filter(email__iexact=email, is_active=True)
        if user_query.exists():
            # Users are not supposed to have the same email but right now our auth pipeline let this happen
            # So let's not break the user experience. Instead return the user with auth identity of ident or
            # the first user if ident is None
            user = user_query[0]
            if user_query.count() > 1:
                logger.warning("Email has multiple users", extra={"email": email})
                if ident:
                    identity_query = AuthIdentity.objects.filter(user__in=user_query, ident=ident)
                    if identity_query.exists():
                        user = identity_query[0].user
                    if identity_query.count() > 1:
                        logger.warning(
                            "Email has two auth identity for the same ident",
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/users/services/user_option/service.py" line="1">

---

# User Options

The UserService also provides methods for retrieving and updating user options. User options are additional settings or preferences associated with a user.

```python
# Please do not use
#     from __future__ import annotations
# in modules such as this one where hybrid cloud data models or service classes are
# defined, because we want to reflect on type annotations and avoid forward references.

from abc import abstractmethod
from typing import Any

from sentry.auth.services.auth import AuthenticationContext
from sentry.hybridcloud.rpc.filter_query import OpaqueSerializedResponse
from sentry.hybridcloud.rpc.service import RpcService, rpc_method
from sentry.silo.base import SiloMode
from sentry.users.services.user import RpcUser
from sentry.users.services.user_option import RpcUserOption, UserOptionFilterArgs


def get_option_from_list(
    options: list[RpcUserOption],
    *,
    key: str | None = None,
    user_id: int | None = None,
```

---

</SwmSnippet>

# User Functions Overview

This section provides an overview of the main functions related to Users in the sentry-demo repository.

<SwmSnippet path="/src/sentry/users/services/user/service.py" line="25">

---

## UserService

The UserService class is the main entry point for interacting with user data. It provides methods for creating, retrieving, and updating users. The UserService uses a delegation pattern, as indicated by the 'create_delegation()' method call on line 331. This allows the service to delegate certain tasks to other objects, promoting loose coupling and separation of concerns.

```python
class UserService(RpcService):
    key = "user"
    local_mode = SiloMode.CONTROL

    @classmethod
    def get_local_implementation(cls) -> RpcService:
        from sentry.users.services.user.impl import DatabaseBackedUserService

        return DatabaseBackedUserService()

    @rpc_method
    @abstractmethod
    def serialize_many(
        self,
        *,
        filter: UserFilterArgs,
        as_user: RpcUser | None = None,
        auth_context: AuthenticationContext | None = None,
        serializer: UserSerializeType | None = None,
    ) -> list[OpaqueSerializedResponse]:
        """
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/users/services/user/service.py" line="59">

---

## get_many

The 'get_many' function retrieves a list of users based on the provided filter. The filter is an instance of UserFilterArgs, which allows specifying various criteria for filtering users.

```python
    def get_many(self, *, filter: UserFilterArgs) -> list[RpcUser]:
        """
        Get a list of users as RpcUser objects.

        :param filter: Filtering options. See UserFilterArgs
        """
        pass
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/users/services/user/service.py" line="109">

---

## get_many_by_id

The 'get_many_by_id' function retrieves multiple users by their IDs. It uses a region local cache to minimize network overhead.

```python
        """

    def get_many_by_id(self, *, ids: list[int]) -> list[RpcUser]:
        """
        Get many users by id.

        Will use region local cache to minimize network overhead.
        Cache keys in regions will be expired as users are updated via outbox receivers.

        :param ids: A list of user ids to fetch
        """
        return get_many_by_id(ids)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/users/services/user/service.py" line="137">

---

## get_existing_usernames

The 'get_existing_usernames' function retrieves all usernames from the provided list that belong to existing users.

```python
    def get_existing_usernames(self, *, usernames: list[str]) -> list[str]:
        """
        Get all usernames from the set that belong to existing users.

        :param usernames: A list of usernames to match
        """
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/users/services/user/service.py" line="146">

---

## get_organizations

The 'get_organizations' function retrieves summary data for all organizations of which the user is a member. The organizations may span multiple regions.

```python
    def get_organizations(
        self,
        *,
        user_id: int,
        only_visible: bool = False,
    ) -> list[RpcOrganizationMapping]:
        """
        Get summary data for all organizations of which the user is a member.

        The organizations may span multiple regions.

        :param user_id: The user to find organizations from.
        :param only_visible: Whether or not to only fetch visible organizations
        """
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/users/services/user/service.py" line="193">

---

## get_user

The 'get_user' function retrieves a single user by their ID. The result of this method is cached to improve performance.

```python
    def get_user(self, user_id: int) -> RpcUser | None:
        """
        Get a single user by id

        The result of this method is cached.

        :param user_id: The user to fetch
        """
        return get_user(user_id)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/users/services/user/impl.py" line="204">

---

## get_or_create_by_email

The 'get_or_create_by_email' function retrieves a user by their email, or creates a new user if one does not already exist. This function also handles transactions, ensuring data consistency.

```python
    def get_or_create_by_email(
        self, *, email: str, ident: str | None = None, referrer: str | None = None
    ) -> UserCreateResult:
        with transaction.atomic(router.db_for_write(User)):
            rpc_user = self.get_user_by_email(email=email, ident=ident)
            if rpc_user:
                return UserCreateResult(user=rpc_user, created=False)

            # Create User if it doesn't exist
            user = User.objects.create(
                username=f"{slugify(str.split(email, '@')[0])}-{uuid4().hex}",
                email=email,
                name=email,
            )
            user_signup.send_robust(
                sender=self, user=user, source="api", referrer=referrer or "unknown"
            )
            user.update(flags=F("flags").bitor(User.flags.newsletter_consent_prompt))

            return UserCreateResult(user=serialize_rpc_user(user), created=True)
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
