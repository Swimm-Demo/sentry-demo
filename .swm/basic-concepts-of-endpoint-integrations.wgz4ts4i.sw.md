---
title: Basic Concepts of Endpoint Integrations
---
Integrations in the Endpoints directory of the sentry-demo repository refer to the various ways in which the application interfaces with external services. These integrations are organized into different categories, such as 'organization_integrations' and 'doc_integrations', each with its own set of functionalities.

The 'organization_integrations' category, for instance, contains the 'OrganizationIntegrationsEndpoint' class which is responsible for listing all the available integrations for a particular organization. It handles GET requests and returns a list of active, disabled, or pending deletion integrations for the organization.

On the other hand, the 'doc_integrations' category contains the 'DocIntegrationsEndpoint' class which handles both GET and POST requests. The GET method retrieves all document integrations, while the POST method allows for the creation of new document integrations.

<SwmSnippet path="/src/sentry/api/endpoints/integrations/organization_integrations/index.py" line="79">

---

# OrganizationIntegrationsEndpoint

This is the 'get' method of the 'OrganizationIntegrationsEndpoint' class. It handles GET requests and returns a list of active, disabled, or pending deletion integrations for the organization. The method first retrieves the list of integrations from the database, then filters them based on the provided parameters, and finally returns the filtered list.

```python
    def get(
        self,
        request: Request,
        organization_context: RpcUserOrganizationContext,
        organization: RpcOrganization,
    ) -> Response:
        """
        Lists all the available Integrations for an Organization.
        """
        feature_filters = request.GET.getlist("features", [])
        # TODO: Remove provider_key in favor of ProviderKey after removing from frontend
        provider_key = request.GET.get("providerKey")
        if provider_key is None:
            provider_key = request.GET.get("provider_key", "")
        include_config_raw = request.GET.get("includeConfig")

        # Include the configurations by default if includeConfig is not present.
        # TODO(mgaeta): HACK. We need a consistent way to get booleans from query parameters.
        include_config = include_config_raw != "0"

        queryset = OrganizationIntegration.objects.filter(
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/integrations/doc_integrations/details.py" line="12">

---

# DocIntegrationsEndpoint

This is the 'DocIntegration' class. It represents a document integration, which is a type of integration that connects the application with a document service.

```python
from sentry.api.serializers.rest_framework import DocIntegrationSerializer
from sentry.models.integrations.doc_integration import DocIntegration
from sentry.models.integrations.integration_feature import IntegrationFeature, IntegrationTypes
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/integrations/install_request.py" line="19">

---

# get_provider_name

This is the 'get_provider_name' function. It takes a provider type and a provider slug as parameters, and returns the display name for the provider. This function is used to retrieve the name of the integration provider.

```python
def get_provider_name(provider_type: str, provider_slug: str) -> str | None:
    """
    The things that users think of as "integrations" are actually three
    different things: integrations, plugins, and sentryapps. A user requesting
    than an integration be installed only actually knows the "provider" they
    want and not what type they want. This function looks up the display name
    for the integration they want installed.

    :param provider_type: One of: "first_party", "plugin", or "sentry_app".
    :param provider_slug: The unique identifier for the provider.
    :return: The display name for the provider or None.
    """
    if provider_type == "first_party":
        if integrations.exists(provider_slug):
            return integrations.get(provider_slug).name
    elif provider_type == "plugin":
        if plugins.exists(provider_slug):
            return plugins.get(provider_slug).title
    elif provider_type == "sentry_app":
        sentry_app = app_service.get_sentry_app_by_slug(slug=provider_slug)
        if sentry_app:
```

---

</SwmSnippet>

# Endpoints Explanation

Understanding DocIntegrationDetailsEndpoint and OrganizationPluginsConfigsEndpoint

<SwmSnippet path="/src/sentry/api/endpoints/integrations/doc_integrations/details.py" line="20">

---

## DocIntegrationDetailsEndpoint

The `DocIntegrationDetailsEndpoint` class defines endpoints for handling HTTP requests related to Document Integrations. It includes methods for handling GET, PUT, and DELETE requests. The GET method retrieves the details of a specific Document Integration. The PUT method updates the details of a specific Document Integration. The DELETE method deletes a specific Document Integration.

```python
class DocIntegrationDetailsEndpoint(DocIntegrationBaseEndpoint):
    owner = ApiOwner.INTEGRATIONS
    publish_status = {
        "DELETE": ApiPublishStatus.UNKNOWN,
        "GET": ApiPublishStatus.UNKNOWN,
        "PUT": ApiPublishStatus.UNKNOWN,
    }

    def get(self, request: Request, doc_integration: DocIntegration) -> Response:
        return self.respond(serialize(doc_integration, request.user), status=status.HTTP_200_OK)

    def put(self, request: Request, doc_integration: DocIntegration) -> Response:
        data = request.json_body
        data["metadata"] = self.generate_incoming_metadata(request)

        serializer = DocIntegrationSerializer(doc_integration, data=data)
        if serializer.is_valid():
            doc_integration = serializer.save()
            return Response(
                serialize(doc_integration, request.user),
                status=status.HTTP_200_OK,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/integrations/plugins/configs_index.py" line="19">

---

## OrganizationPluginsConfigsEndpoint

The `OrganizationPluginsConfigsEndpoint` class defines an endpoint for handling HTTP requests related to Plugin Configurations within an Organization. It includes a method for handling GET requests. The GET method retrieves a list of plugin configurations for a specific organization, including a `projectList` for each plugin which contains all the projects that have that specific plugin both configured and enabled.

```python
@region_silo_endpoint
class OrganizationPluginsConfigsEndpoint(OrganizationEndpoint):
    owner = ApiOwner.INTEGRATIONS
    publish_status = {
        "GET": ApiPublishStatus.UNKNOWN,
    }

    def get(self, request: Request, organization) -> Response:
        """
        List one or more plugin configurations, including a `projectList` for each plugin which contains
        all the projects that have that specific plugin both configured and enabled.

        - similar to the `OrganizationPluginsEndpoint`, and can eventually replace it

        :qparam plugins array[string]: an optional list of plugin ids (slugs) if you want specific plugins.
                                    If not set, will return configurations for all plugins.
        """

        desired_plugins = []
        for slug in request.GET.getlist("plugins") or ():
            # if the user request a plugin that doesn't exist, throw 404
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
