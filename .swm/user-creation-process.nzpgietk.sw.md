---
title: User Creation Process
---
<SwmSnippet path="/src/sentry/runner/commands/createuser.py" line="94">

---

# CreateUser Function

The `createuser` function is the main function for creating a new user. It accepts several parameters such as emails, org_id, password, superuser, staff, no_password, no_input, and force_update.

```python
def createuser(
    emails: list[str] | None,
    org_id: str | None,
    password: str | None,
    superuser: bool | None,
    staff: bool | None,
    no_password: bool,
    no_input: bool,
    force_update: bool,
) -> None:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/runner/commands/createuser.py" line="106">

---

This part of the code handles user input validation. It checks if the necessary parameters like emails and password are provided. If not, it prompts the user for input. It also ensures that a user cannot be set as staff without superuser access.

```python
    from django.conf import settings

    if not no_input:
        if not emails:
            emails = _get_email()

        if not (password or no_password):
            password = _get_password()

        if superuser is None:
            superuser = _get_superuser()

    if superuser is None:
        superuser = False

    # Prevent a user from being set to staff without superuser
    if not superuser and staff:
        click.echo("Non-superuser asked to be given staff access, correcting to staff=False")
        staff = False

    # Default staff to match the superuser setting
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/runner/commands/createuser.py" line="137">

---

Here, the function loops through the provided emails, creating or updating user records in the database. If the user already exists and the `force_update` flag is set, the user's details are updated. If the user doesn't exist, a new user is created.

```python
    from sentry import roles
    from sentry.models.user import User

    # Loop through the email list provided.
    for email in emails:
        fields = dict(
            email=email,
            username=email,
            is_superuser=superuser,
            is_staff=staff,
            is_active=True,
        )

        verb = None
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            user = None

        # Update the user if they already exist.
        if user is not None:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/runner/commands/createuser.py" line="171">

---

This section handles organization membership. If the Sentry instance is configured as a single organization, the new user is added to the specified organization or the default organization if none is specified. The user is also added to a single team if one exists.

```python
            if settings.SENTRY_SINGLE_ORGANIZATION:
                from sentry.organizations.services.organization import organization_service

                # Get the org if specified, otherwise use the default.
                if org_id:
                    org_context = organization_service.get_organization_by_id(
                        id=org_id, include_teams=False, include_projects=False
                    )
                    if org_context is None:
                        raise Exception("Organization ID not found")
                    org = org_context.organization
                else:
                    org = organization_service.get_default_organization()

                if superuser:
                    role = roles.get_top_dog().id
                else:
                    role = org.default_role
                member = organization_service.add_organization_member(
                    organization_id=org.id,
                    default_org_role=org.default_role,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/runner/commands/createuser.py" line="205">

---

Finally, the user's password is set and saved. If the user is a superuser and the Sentry instance is self-hosted or a single organization, the `_set_superadmin` function is called. A message is then printed to the console indicating the user's email and whether they were created or updated.

```python
        if password:
            user.set_password(password)
            user.save()

        if superuser and (settings.SENTRY_SELF_HOSTED or settings.SENTRY_SINGLE_ORGANIZATION):
            _set_superadmin(user)

        click.echo(f"User {verb}: {email}")
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

<SwmSnippet path="/src/sentry/runner/commands/createuser.py" line="94">

---

# createuser Function

The `createuser` function is the entry point for creating a new user. It accepts several parameters such as emails, org_id, password, superuser, staff, no_password, no_input, and force_update.

```python
def createuser(
    emails: list[str] | None,
    org_id: str | None,
    password: str | None,
    superuser: bool | None,
    staff: bool | None,
    no_password: bool,
    no_input: bool,
    force_update: bool,
) -> None:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/runner/commands/createuser.py" line="106">

---

This section of the code handles user input validation. It checks if the necessary parameters like emails and password are provided. If not, it prompts the user for input. It also ensures that a user cannot be set as staff without superuser access.

```python
    from django.conf import settings

    if not no_input:
        if not emails:
            emails = _get_email()

        if not (password or no_password):
            password = _get_password()

        if superuser is None:
            superuser = _get_superuser()

    if superuser is None:
        superuser = False

    # Prevent a user from being set to staff without superuser
    if not superuser and staff:
        click.echo("Non-superuser asked to be given staff access, correcting to staff=False")
        staff = False

    # Default staff to match the superuser setting
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/runner/commands/createuser.py" line="137">

---

Here, the function loops through the provided emails, creating or updating user records in the database. If the user already exists and the `force_update` flag is set, the user's details are updated. If the user doesn't exist, a new user is created.

```python
    from sentry import roles
    from sentry.models.user import User

    # Loop through the email list provided.
    for email in emails:
        fields = dict(
            email=email,
            username=email,
            is_superuser=superuser,
            is_staff=staff,
            is_active=True,
        )

        verb = None
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            user = None

        # Update the user if they already exist.
        if user is not None:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/runner/commands/createuser.py" line="171">

---

This section handles organization membership. If the Sentry instance is configured as a single organization, the new user is added to the specified organization or the default organization if none is specified. The user is also added to a single team if one exists.

```python
            if settings.SENTRY_SINGLE_ORGANIZATION:
                from sentry.organizations.services.organization import organization_service

                # Get the org if specified, otherwise use the default.
                if org_id:
                    org_context = organization_service.get_organization_by_id(
                        id=org_id, include_teams=False, include_projects=False
                    )
                    if org_context is None:
                        raise Exception("Organization ID not found")
                    org = org_context.organization
                else:
                    org = organization_service.get_default_organization()

                if superuser:
                    role = roles.get_top_dog().id
                else:
                    role = org.default_role
                member = organization_service.add_organization_member(
                    organization_id=org.id,
                    default_org_role=org.default_role,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/runner/commands/createuser.py" line="205">

---

Finally, the user's password is set and saved. If the user is a superuser and the Sentry instance is self-hosted or a single organization, the `_set_superadmin` function is called. A message is then printed to the console indicating the user's email and whether they were created or updated.

```python
        if password:
            user.set_password(password)
            user.save()

        if superuser and (settings.SENTRY_SELF_HOSTED or settings.SENTRY_SINGLE_ORGANIZATION):
            _set_superadmin(user)

        click.echo(f"User {verb}: {email}")
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
