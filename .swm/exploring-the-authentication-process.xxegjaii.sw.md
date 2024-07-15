---
title: Exploring the Authentication Process
---
Auth, short for authentication, in the Main Application refers to the process of verifying the identity of a user or system. It is a crucial part of the security system, ensuring that only authorized users or systems have access to certain resources or functionalities.

The authentication process in the Main Application involves several functions and methods. For instance, the `exchange_token` function in `src/sentry/auth/providers/oauth2.py` is used to exchange an authorization code for an access token. This function is part of the OAuth2 authentication flow.

Another important function is `get_user_auth_state` in `src/sentry/auth/services/access/service.py`, which retrieves the authentication state of a user. This function is used in various parts of the application to determine the user's access permissions.

The `is_system_auth` function in `src/sentry/auth/system.py` checks if Sentry itself is making the API request. This is an example of system-level authentication.

The `dispatch` function in `src/sentry/auth/providers/saml2/provider.py` is part of the SAML2 authentication flow. It handles the SAML response from the identity provider and proceeds to the next step in the authentication pipeline.

In addition to these, there are several other functions and methods involved in the authentication process, each serving a specific purpose in the overall authentication flow.

<SwmSnippet path="/src/sentry/auth/providers/oauth2.py" line="89">

---

## OAuth2 Authentication

The `exchange_token` function is used to exchange an authorization code for an access token. This function is part of the OAuth2 authentication flow.

```python
    def exchange_token(self, request: Request, helper, code):
        # TODO: this needs the auth yet
        data = self.get_token_params(code=code, redirect_uri=helper.get_redirect_url())
        req = safe_urlopen(self.access_token_url, data=data)
        body = safe_urlread(req)
        if req.headers["Content-Type"].startswith("application/x-www-form-urlencoded"):
            return dict(parse_qsl(body))
        return orjson.loads(body)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/auth/services/access/service.py" line="99">

---

## User Authentication State

The `get_user_auth_state` function retrieves the authentication state of a user. This function is used in various parts of the application to determine the user's access permissions.

```python
    def get_user_auth_state(
        self,
        *,
        user_id: int | None,
        is_superuser: bool,
        is_staff: bool,
        organization_id: int | None,
        org_member: RpcOrganizationMemberSummary | None,
    ) -> RpcAuthState:
        sso_state = self.query_sso_state(
            organization_id=organization_id, is_super_user=is_superuser, member=org_member
        )

        # Unfortunately we are unable to combine the is_superuser and is_staff
        # into a single argument b/c query_sso_state specifically needs is_superuser
        if (is_superuser or is_staff) and user_id is not None:
            # "permissions" is a bit of a misnomer -- these are all admin level permissions, and the intent is that if you
            # have them, you can only use them when you are acting, as a superuser or staff.  This is intentional.
            permissions = list(self.get_permissions_for_user(user_id))
        else:
            permissions = []
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/auth/system.py" line="101">

---

## System Authentication

The `is_system_auth` function checks if Sentry itself is making the API request. This is an example of system-level authentication.

```python
def is_system_auth(auth: object) -> bool:
    """:returns True when Sentry itself is hitting the API."""
    from sentry.auth.services.auth import AuthenticatedToken

    if isinstance(auth, AuthenticatedToken):
        return auth.kind == "system"
    return isinstance(auth, SystemToken)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/auth/providers/saml2/provider.py" line="52">

---

## SAML2 Authentication

The `dispatch` function is part of the SAML2 authentication flow. It handles the SAML response from the identity provider and proceeds to the next step in the authentication pipeline.

```python
    def dispatch(self, request: Request, helper) -> HttpResponse:
        if "SAMLResponse" in request.POST:
            return helper.next_step()

        provider = helper.provider

        # During the setup pipeline, the provider will not have been configured yet,
        # so build the config first from the state.
        if not provider.config:
            provider.config = provider.build_config(helper.fetch_state())

        if request.subdomain:
            # See auth.helper.handle_existing_identity()
            helper.bind_state("subdomain", request.subdomain)

        saml_config = build_saml_config(provider.config, helper.organization.slug)
        auth = build_auth(request, saml_config)

        return self.redirect(auth.login())
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
