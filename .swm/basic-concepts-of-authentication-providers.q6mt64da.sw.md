---
title: Basic Concepts of Authentication Providers
---
Providers in the Auth module of the sentry-demo project are classes or modules that handle the specifics of different authentication methods. They are responsible for managing the flow of authentication, including handling OAuth2 callbacks, SAML2 assertions, and other provider-specific details.

For example, the `OAuth2Provider` class in the `sentry.auth.providers.oauth2` module is a base class for OAuth2-based providers. It defines methods for getting client IDs and secrets, building identity data from OAuth2 responses, and setting up the authentication pipeline.

Similarly, the `Provider` class in the `sentry.auth.provider` module is a base class for all authentication providers. It provides a common interface for all providers, ensuring they can be used interchangeably in the authentication system.

There are also specific provider classes for different authentication methods, such as `FlyOAuth2Provider` for [Fly.io](http://Fly.io)'s OAuth2 service, `Auth0SAML2Provider` for Auth0's SAML2 service, and others. These classes inherit from the base classes and implement the specifics of their respective authentication methods.

<SwmSnippet path="/src/sentry/auth/providers/saml2/provider.py" line="195">

---

# Provider Classes

The `SAML2Provider` class is an example of a provider. It defines methods for setting up the authentication pipeline, building the configuration from the state, and building the identity from the state. It also defines an abstract method `get_saml_setup_pipeline` that must be implemented by subclasses.

```python
class SAML2Provider(Provider, abc.ABC):
    """
    Base SAML2 Authentication provider. SAML style authentication plugins
    should implement this.

    - The provider must implement the `get_configure_view`.

    - The provider must implement the `get_saml_setup_pipeline`. The
      AuthView(s) passed in this method MUST bind the `idp` configuration
      object. The dict should match the shape:

      >>> state.get('idp')
      {
        'entity_id': # Identity Provider entity ID. Usually a URL
        'x509cert':  # Identity Provider x509 public certificate
        'sso_url':   # Identity Provider Single Sign-On URL
        'slo_url':   # identity Provider Single Sign-Out URL
      }

      The provider may also bind the `advanced` configuration. This dict
      provides advanced SAML configurations. The dict should match the shape:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/auth/providers/dummy.py" line="24">

---

The `DummyProvider` class is a simple provider used for testing. It implements the `Provider` interface, providing dummy implementations of the required methods.

```python
class DummyProvider(Provider):
    name = "Dummy"

    def get_auth_pipeline(self):
        return [AskEmail()]

    def build_identity(self, state):
        return {
            "id": MigratingIdentityId(
                id=state.get("id", state["email"]), legacy_id=state.get("legacy_email")
            ),
            "email": state["email"],
            "email_verified": state["email_verified"],
            "name": "Dummy",
        }

    def refresh_identity(self, auth_identity):
        pass

    def build_config(self, state):
        return {}
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/auth/providers/saml2/provider.py" line="146">

---

# Provider Usage

Here's an example of how a provider is used. The `get_provider` function is called to get the provider for a given organization, and then the provider is used to perform authentication tasks.

```python
    def dispatch(self, request: Request, organization_slug):
        provider = get_provider(organization_slug)
        if provider is None:
```

---

</SwmSnippet>

# Provider Endpoints

Understanding Provider Endpoints

<SwmSnippet path="/src/sentry/auth/providers/fly/constants.py" line="1">

---

## [Fly.io](http://Fly.io) Provider Endpoints

The `AUTHORIZE_URL` is the endpoint where the OAuth2 authorization process is initiated for the [Fly.io](http://Fly.io) provider. It is used to redirect the user to the [Fly.io](http://Fly.io)'s authorization page where they can grant permissions to the application.

```python
AUTHORIZE_URL = "https://api.fly.io/oauth/authorize"

ACCESS_TOKEN_URL = "https://api.fly.io/oauth/token"
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/auth/providers/saml2/provider.py" line="51">

---

## SAML2 Provider Endpoints

The `SAML2LoginView` class defines a dispatch method which is an endpoint for initiating the SAML2 login process. If a SAMLResponse is present in the request, it processes the response, otherwise it redirects the user to the SAML2 login page.

```python
class SAML2LoginView(AuthView):
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
