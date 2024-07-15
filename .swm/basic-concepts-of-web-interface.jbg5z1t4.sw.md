---
title: Basic Concepts of Web Interface
---
In the Main Application, 'Web' refers to the web interface of the Sentry application. It is responsible for handling HTTP requests and rendering responses. This includes serving static files, processing form data, and managing user sessions.

The 'Web' component is organized into several modules and files, each serving a specific purpose. For instance, the '[urls.py](http://urls.py)' file defines the URL patterns for the application, while the 'frontend' directory contains views that handle requests and render responses.

The 'Web' component also includes a 'js_sdk_loader.py' file, which is responsible for serving a JavaScript file that can be integrated into a website for error tracking and performance monitoring.

Furthermore, the 'Web' component interacts with other parts of the application. For example, it calls functions from the 'db' and 'loader' modules to fetch data from the database and to get the version of the browser SDK, respectively.

<SwmSnippet path="/src/sentry/web/frontend/react_page.py" line="67">

---

# Web Component Structure

The 'handle_react' function is an example of how the 'Web' component handles HTTP requests. It processes the request, performs various checks and operations, and finally renders a response.

```python
    def handle_react(self, request: Request, **kwargs) -> HttpResponse:
        context = {
            "CSRF_COOKIE_NAME": settings.CSRF_COOKIE_NAME,
            "meta_tags": [
                {"property": key, "content": value}
                for key, value in self.meta_tags(request, **kwargs).items()
            ],
            # Rendering the layout requires serializing the active organization.
            # Since we already have it here from the OrganizationMixin, we can
            # save some work and render it faster.
            "org_context": getattr(self, "active_organization", None),
        }

        # Force a new CSRF token to be generated and set in user's
        # Cookie. Alternatively, we could use context_processor +
        # template tag, but in this case, we don't need a form on the
        # page. So there's no point in rendering a random `<input>` field.
        get_csrf_token(request)

        url_name = request.resolver_match.url_name
        url_is_non_customer_domain = (
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/web/frontend/group_event_json.py" line="14">

---

# Interaction with Other Components

The 'Web' component interacts with other parts of the application. For example, it calls the 'get' function from the 'group_event_json.py' file to fetch data from the database.

```python
    def get(self, request: HttpRequest, organization, group_id, event_id_or_latest) -> HttpResponse:
        try:
            # TODO(tkaemming): This should *actually* redirect, see similar
            # comment in ``GroupEndpoint.convert_args``.
            group, _ = get_group_with_redirect(group_id)
        except Group.DoesNotExist:
            raise Http404

        if event_id_or_latest == "latest":
            event = group.get_latest_event()
        else:
            event = eventstore.backend.get_event_by_id(
                group.project.id, event_id_or_latest, group_id=group.id
            )

        if event is None:
            raise Http404

        GroupMeta.objects.populate_cache([group])

        return HttpResponse(json.dumps(event.as_dict()), content_type="application/json")
```

---

</SwmSnippet>

# Authentication Endpoints

Authentication Endpoints

<SwmSnippet path="/src/sentry/web/frontend/auth_login.py" line="381">

---

## AuthLoginView Post Method

The 'post' method in the 'AuthLoginView' class handles the submission of the login form. It checks if the user has submitted the form for login or registration and processes the form accordingly. If the form is valid, it logs in the user and redirects them to the next step in the authentication process. If the form is not valid, it returns an error message to the user.

```python
    def handle_login_form_submit(
        self, request: Request, organization: RpcOrganization, **kwargs
    ) -> HttpResponse:
        """
        Validates a completed login  form, redirecting to the next
        step or returning the form with its errors displayed.
        """
        context = self.get_default_context(request=request, **kwargs)

        login_form = AuthenticationForm(request, request.POST)

        if self.is_ratelimited_login_attempt(request=request, login_form=login_form):
            return self.get_ratelimited_login_form(request=request, login_form=login_form, **kwargs)
        elif not login_form.is_valid():
            context.update({"login_form": login_form, "op": "login"})
            return self.respond_login(request=request, context=context, **kwargs)

        user = login_form.get_user()
        self._handle_login(request=request, user=user, organization=organization)
        metrics.incr("login.attempt", instance="success", skip_internal=True, sample_rate=1.0)
        return self.redirect_to_next_login_step(
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/web/frontend/oauth_token.py" line="50">

---

## OAuthTokenView Get Method

The 'get' method in the 'OAuthTokenView' class handles the retrieval of access tokens or refresh tokens for OAuth. It checks the grant type and processes the request accordingly. If the grant type is 'authorization', it gets the access tokens. If the grant type is 'refresh', it gets the refresh token. It then processes the token details and returns a response with the token information.

```python
    def post(self, request: HttpRequest) -> HttpResponse:
        grant_type = request.POST.get("grant_type")
        client_id = request.POST.get("client_id")
        client_secret = request.POST.get("client_secret")

        metrics.incr(
            "oauth_token.post.start",
            sample_rate=1.0,
            tags={
                "client_id_exists": bool(client_id),
                "client_secret_exists": bool(client_secret),
            },
        )

        if not client_id:
            return self.error(request=request, name="missing_client_id", reason="missing client_id")
        if not client_secret:
            return self.error(
                request=request, name="missing_client_secret", reason="missing client_secret"
            )

```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
