---
title: Basic Concepts of Organization Integration Management
---
Organization Integrations in Sentry are connections between Sentry and third-party applications, such as GitHub, Slack, Jira, etc. These integrations provide additional functionality and smoother workflows for Sentry users. They are defined and managed in the settings of an organization.

In the codebase, the 'organization' property is often seen in the context of integrations. This property is of the type 'Organization' and it represents the organization that the integration belongs to. It is used in various components related to integrations, such as 'IntegrationMainSettings', 'InstalledIntegration', 'AddIntegration', and more.

The 'integration' property, of the type 'Integration', represents the specific integration instance. It is used in components like 'IntegrationMainSettings' to handle actions such as updating the integration settings.

The 'onUpdate' function, seen in 'IntegrationMainSettings', is a callback function that is triggered when the integration settings are successfully updated. This allows the component to react to changes in the integration settings.

In 'AddIntegration', the 'onInstall' function is a callback that is triggered when a new integration is installed. This allows the component to react to the installation of a new integration.

In 'InstalledIntegration', the 'onDisable' and 'onRemove' functions are callbacks that are triggered when an integration is disabled or removed, respectively. These allow the component to react to these events.

<SwmSnippet path="/static/app/views/settings/organizationIntegrations/addIntegration.tsx" line="19">

---

# Organization Property

The 'organization' property is of the type 'Organization' and it represents the organization that the integration belongs to. It is used in various components related to integrations.

```tsx
  organization: Organization;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationIntegrations/integrationMainSettings.tsx" line="11">

---

# Integration Property

The 'integration' property, of the type 'Integration', represents the specific integration instance. It is used in components like 'IntegrationMainSettings' to handle actions such as updating the integration settings.

```tsx
  integration: Integration;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationIntegrations/integrationMainSettings.tsx" line="12">

---

# onUpdate Function

The 'onUpdate' function, seen in 'IntegrationMainSettings', is a callback function that is triggered when the integration settings are successfully updated. This allows the component to react to changes in the integration settings.

```tsx
  onUpdate: () => void;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationIntegrations/addIntegration.tsx" line="18">

---

# onInstall Function

In 'AddIntegration', the 'onInstall' function is a callback that is triggered when a new integration is installed. This allows the component to react to the installation of a new integration.

```tsx
  onInstall: (data: IntegrationWithConfig) => void;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationIntegrations/installedIntegration.tsx" line="28">

---

# onDisable and onRemove Functions

In 'InstalledIntegration', the 'onDisable' and 'onRemove' functions are callbacks that are triggered when an integration is disabled or removed, respectively. These allow the component to react to these events.

```tsx
  onDisable: (integration: Integration) => void;
  onRemove: (integration: Integration) => void;
```

---

</SwmSnippet>

# Organization Integrations Functions

This section discusses the main functions related to Organization Integrations in Sentry. These functions are used to manage and interact with the integrations, providing additional functionality and smoother workflows for Sentry users.

<SwmSnippet path="/static/app/views/settings/organizationIntegrations/abstractIntegrationDetailedView.tsx" line="186">

---

## renderConfigurations

The `renderConfigurations` function is an abstract method that is expected to be implemented in subclasses. It returns the list of configurations for the integration.

```tsx
  // Returns the list of configurations for the integration
  abstract renderConfigurations(): React.ReactNode;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationIntegrations/abstractIntegrationDetailedView.tsx" line="339">

---

## renderInformationCard

The `renderInformationCard` function is used to render the information about the integration description and features. It uses several other functions and components to construct the information card.

```tsx
  // Returns the information about the integration description and features
  renderInformationCard() {
    const {FeatureList} = getIntegrationFeatureGate();

    return (
      <Fragment>
        <Flex>
          <FlexContainer>
            <Description dangerouslySetInnerHTML={{__html: marked(this.description)}} />
            <FeatureList
              {...this.featureProps}
              provider={{key: this.props.params.integrationSlug}}
            />
            {this.renderPermissions()}
            {this.alerts.map((alert, i) => (
              <Alert key={i} type={alert.type} showIcon>
                <span
                  dangerouslySetInnerHTML={{__html: singleLineRenderer(alert.text)}}
                />
              </Alert>
            ))}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationIntegrations/integrationServerlessFunctions.tsx" line="42">

---

## getEndpoints

The `getEndpoints` function is used to define the API endpoints to fetch data from. It is used in the `IntegrationServerlessFunctions` component to fetch the serverless functions related to the integration.

```tsx
      [
        'serverlessFunctions',
        `/organizations/${orgSlug}/integrations/${this.props.integration.id}/serverless-functions/`,
      ],
    ];
  }

  get serverlessFunctions() {
    return this.state.serverlessFunctions;
```

---

</SwmSnippet>

# Integration and Plugin Endpoints

Integration and Plugin Endpoints

<SwmSnippet path="/static/app/views/settings/organizationIntegrations/configureIntegration.tsx" line="143">

---

## Integration Endpoint

This endpoint is used to fetch or update the configuration of a specific integration for an organization. The organization's slug and the integration's id are used to construct the URL for the endpoint. Depending on the HTTP method used, this endpoint can either return the current configuration of the integration or update the configuration based on the provided data.

```tsx

  if (isLoadingConfig || isLoadingIntegration || isLoadingPlugins) {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationIntegrations/configureIntegration.tsx" line="74">

---

## Plugin Endpoint

This endpoint is used to fetch the configurations of all plugins for an organization. The organization's slug is used to construct the URL for the endpoint. The response from this endpoint includes a list of all plugins and their configurations for the organization.

```tsx
  return [`/organizations/${organization.slug}/plugins/configs/`];
};
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
