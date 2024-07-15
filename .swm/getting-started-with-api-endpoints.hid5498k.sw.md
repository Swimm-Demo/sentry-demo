---
title: Getting started with API Endpoints
---
Endpoints in the sentry-demo repo are defined as classes that inherit from the Endpoint class. They are used to handle HTTP requests and responses. Each endpoint class defines methods corresponding to HTTP verbs (GET, POST, PUT, DELETE) to handle different types of requests. These methods contain the logic for processing the request and returning a response. For example, the `ApiApplicationsEndpoint` class in `src/sentry/api/endpoints/api_applications.py` defines `get` and `post` methods to handle GET and POST requests respectively.

Endpoints are typically associated with specific resources in the application, such as users, tokens, or applications. For instance, the `ApiTokensEndpoint` in `src/sentry/api/endpoints/api_tokens.py` is associated with API tokens. It provides methods to get, post, and delete tokens.

Endpoints also define authentication and permission classes to control access. For example, the `ApiApplicationsEndpoint` class uses the `SessionAuthentication` authentication class and the `IsAuthenticated` permission class. This means that a user must be authenticated through a session to access the endpoints defined in this class.

In addition to handling requests, endpoints can also define additional methods to perform specific tasks. For example, the `ApiTokensEndpoint` class defines a `get_appropriate_user_id` method to determine the user ID to use for a request.

<SwmSnippet path="/src/sentry/api/endpoints/organization_onboarding_continuation_email.py" line="43">

---

# OrganizationOnboardingContinuationEmail Endpoint

This endpoint is used to handle requests related to the onboarding continuation email for an organization. The `post` method is used to process POST requests. It validates the request data, constructs a message, sends it asynchronously, and records the action in the analytics.

```python
class OrganizationOnboardingContinuationEmail(OrganizationEndpoint):
    publish_status = {
        "POST": ApiPublishStatus.PRIVATE,
    }
    owner = ApiOwner.TELEMETRY_EXPERIENCE
    # let anyone in the org use this endpoint
    permission_classes = ()

    def post(self, request: Request, organization: Organization):
        serializer = OnboardingContinuationSerializer(data=request.data)
        if not serializer.is_valid():
            return self.respond(serializer.errors, status=400)

        msg = MessageBuilder(
            **get_request_builder_args(
                request.user, organization, serializer.validated_data["platforms"]
            )
        )
        msg.send_async([request.user.email])
        analytics.record(
            "onboarding_continuation.sent",
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/system_options.py" line="26">

---

# SystemOptionsEndpoint

This endpoint is used to handle requests related to system options. It defines `get` and `put` methods to handle GET and PUT requests respectively. The `get` method retrieves system options based on the request, and the `put` method updates system options based on the data in the request.

```python
class SystemOptionsEndpoint(Endpoint):
    publish_status = {
        "GET": ApiPublishStatus.PRIVATE,
        "PUT": ApiPublishStatus.PRIVATE,
    }
    owner = ApiOwner.OPEN_SOURCE
    permission_classes = (SuperuserPermission,)

    def get(self, request: Request) -> Response:
        query = request.GET.get("query")
        if query == "is:required":
            option_list = options.filter(flag=options.FLAG_REQUIRED)
        elif query:
            return Response(f"{query} is not a supported search query", status=400)
        else:
            option_list = options.all()

        smtp_disabled = not is_smtp_enabled()

        results = {}
        for k in option_list:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/group_details.py" line="130">

---

# GroupDetailsEndpoint

This endpoint is used to handle requests related to group details. The `get` method retrieves details of an individual issue. It uses several helper methods to gather the necessary data, such as `get_environments`, `_get_activity`, and `_get_seen_by`.

``````````````````python
    def get(self, request: Request, group) -> Response:
        """
        Retrieve an Issue
        `````````````````

        Return details on an individual issue. This returns the basic stats for
        the issue (title, last seen, first seen), some overall numbers (number
        of comments, user reports) as well as the summarized event data.

        :pparam string organization_id_or_slug: the id or slug of the organization.
        :pparam string issue_id: the ID of the issue to retrieve.
        :auth: required
        """
        from sentry.utils import snuba

        try:
            # TODO(dcramer): handle unauthenticated/public response

            organization = group.project.organization
            environments = get_environments(request, organization)
            environment_ids = [e.id for e in environments]
``````````````````

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/api_applications.py" line="14">

---

# ApiApplicationsEndpoint

This endpoint is used to handle requests related to API applications. It defines `get` and `post` methods to handle GET and POST requests respectively. The `get` method retrieves API applications for the authenticated user, and the `post` method creates a new API application for the authenticated user.

```python
class ApiApplicationsEndpoint(Endpoint):
    publish_status = {
        "GET": ApiPublishStatus.UNKNOWN,
        "POST": ApiPublishStatus.UNKNOWN,
    }
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        queryset = ApiApplication.objects.filter(
            owner_id=request.user.id, status=ApiApplicationStatus.active
        )

        return self.paginate(
            request=request,
            queryset=queryset,
            order_by="name",
            paginator_cls=OffsetPaginator,
            on_results=lambda x: serialize(x, request.user),
        )

```

---

</SwmSnippet>

# Endpoint Explanations

Endpoints Overview

<SwmSnippet path="/src/sentry/api/endpoints/organization_events_spans_performance.py" line="153">

---

## OrganizationEventsSpansPerformanceEndpoint

The `OrganizationEventsSpansPerformanceEndpoint` class defines an endpoint that handles GET requests. The `get` method is used to retrieve data, likely related to the performance of spans within events for an organization.

```python
class OrganizationEventsSpansPerformanceEndpoint(OrganizationEventsSpansEndpointBase):
    publish_status = {
        "GET": ApiPublishStatus.PRIVATE,
    }

    def get(self, request: Request, organization: Organization) -> Response:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/user_social_identities_index.py" line="13">

---

## UserSocialIdentitiesIndexEndpoint

The `UserSocialIdentitiesIndexEndpoint` class defines an endpoint that handles GET requests. The `get` method is used to retrieve a list of an account's associated identities, such as GitHub when trying to add a repo.

``````````````````````````python
class UserSocialIdentitiesIndexEndpoint(UserEndpoint):
    publish_status = {
        "GET": ApiPublishStatus.PRIVATE,
    }
    owner = ApiOwner.ENTERPRISE

    def get(self, request: Request, user) -> Response:
        """
        List Account's Identities
        `````````````````````````

        List an account's associated identities (e.g. github when trying to add a repo)

        :auth: required
        """

        identity_list = list(UserSocialAuth.objects.filter(user=user))
        return Response(serialize(identity_list))
``````````````````````````

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
