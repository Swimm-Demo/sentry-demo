---
title: Introduction to Developer Integration Settings
---
The Organization Developer Settings in Sentry's settings is a feature that allows developers to manage and configure their integrations with Sentry. It provides an interface for creating, editing, and managing both public and internal integrations. Public integrations are available to all Sentry users, while internal integrations are limited to the organization that created them. The settings also allow developers to handle webhook subscriptions and permissions for each integration.

The settings are implemented in the `OrganizationDeveloperSettings` class in the `static/app/views/settings/organizationDeveloperSettings/index.tsx` file. This class extends the `DeprecatedAsyncView` class and manages the state of the developer settings, including the list of applications and the currently selected tab (public or internal). It also provides methods for handling changes in the tab, removing an application, and rendering the list of applications.

The `OrganizationDeveloperSettings` class uses the `analyticsView` property to track user interactions with the developer settings. It also uses the `onTabChange` method to handle changes in the selected tab, and the `renderApplicationRow` method to render each application in the list.

The `OrganizationDeveloperSettings` class also defines methods for rendering the list of public and internal integrations, and for rendering the content of the currently selected tab. The `renderInternalIntegrations` and `renderPublicIntegrations` methods filter the list of applications based on their status and render the list using the `SentryApplicationRow` component. The `renderTabContent` method uses a switch statement to determine which method to call based on the currently selected tab.

The `OrganizationDeveloperSettings` class is exported as a default export wrapped with the `withOrganization` higher-order component. This allows the class to access the current organization as a prop.

<SwmSnippet path="/static/app/views/settings/organizationDeveloperSettings/index.tsx" line="38">

---

# OrganizationDeveloperSettings Class

The `OrganizationDeveloperSettings` class in the `static/app/views/settings/organizationDeveloperSettings/index.tsx` file is the main class that implements the Organization Developer Settings. It extends the `DeprecatedAsyncView` class and manages the state of the developer settings, including the list of applications and the currently selected tab (public or internal). It also provides methods for handling changes in the tab, removing an application, and rendering the list of applications.

```tsx
class OrganizationDeveloperSettings extends DeprecatedAsyncView<Props, State> {
  analyticsView = 'developer_settings' as const;

  getDefaultState(): State {
    const {location} = this.props;
    const value =
      (['public', 'internal'] as const).find(tab => tab === location?.query?.type) ||
      'internal';

    return {
      ...super.getDefaultState(),
      applications: [],
      sentryFunctions: [],
      tab: value,
    };
  }

  get tab() {
    return this.state.tab;
  }

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationDeveloperSettings/index.tsx" line="39">

---

# analyticsView Property

The `analyticsView` property is used to track user interactions with the developer settings. It is set to 'developer_settings' as a constant.

```tsx
  analyticsView = 'developer_settings' as const;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationDeveloperSettings/index.tsx" line="82">

---

# onTabChange Method

The `onTabChange` method is used to handle changes in the selected tab. It updates the state with the new tab value.

```tsx
  onTabChange = (value: Tab) => {
    this.setState({tab: value});
  };
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationDeveloperSettings/index.tsx" line="86">

---

# renderApplicationRow Method

The `renderApplicationRow` method is used to render each application in the list. It uses the `SentryApplicationRow` component to render each application.

```tsx
  renderApplicationRow = (app: SentryApp) => {
    const {organization} = this.props;
    return (
      <SentryApplicationRow
        key={app.uuid}
        app={app}
        organization={organization}
        onRemoveApp={this.removeApp}
      />
    );
  };
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationDeveloperSettings/index.tsx" line="98">

---

# renderInternalIntegrations and renderPublicIntegrations Methods

The `renderInternalIntegrations` and `renderPublicIntegrations` methods are used to render the list of internal and public integrations respectively. They filter the list of applications based on their status and render the list using the `renderApplicationRow` method.

```tsx
  renderInternalIntegrations() {
    const integrations = this.state.applications.filter(
      (app: SentryApp) => app.status === 'internal'
    );
    const isEmpty = integrations.length === 0;

    return (
      <Panel>
        <PanelHeader>{t('Internal Integrations')}</PanelHeader>
        <PanelBody>
          {!isEmpty ? (
            integrations.map(this.renderApplicationRow)
          ) : (
            <EmptyMessage>
              {t('No internal integrations have been created yet.')}
            </EmptyMessage>
          )}
        </PanelBody>
      </Panel>
    );
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationDeveloperSettings/index.tsx" line="140">

---

# renderTabContent Method

The `renderTabContent` method is used to render the content of the currently selected tab. It uses a switch statement to determine which method to call based on the currently selected tab.

```tsx
  renderTabContent(tab: Tab) {
    switch (tab) {
      case 'internal':
        return this.renderInternalIntegrations();
      case 'public':
      default:
        return this.renderPublicIntegrations();
    }
  }
```

---

</SwmSnippet>

# Organization Developer Settings Functions

The Organization Developer Settings are implemented in the `OrganizationDeveloperSettings` class in the `static/app/views/settings/organizationDeveloperSettings/index.tsx` file. This class extends the `DeprecatedAsyncView` class and manages the state of the developer settings, including the list of applications and the currently selected tab (public or internal). It also provides methods for handling changes in the tab, removing an application, and rendering the list of applications.

<SwmSnippet path="/static/app/views/settings/organizationDeveloperSettings/index.tsx" line="41">

---

## getDefaultState

The `getDefaultState` method is used to initialize the state of the `OrganizationDeveloperSettings` class. It sets the initial values for the applications, sentryFunctions, and tab properties of the state.

```tsx
  getDefaultState(): State {
    const {location} = this.props;
    const value =
      (['public', 'internal'] as const).find(tab => tab === location?.query?.type) ||
      'internal';

    return {
      ...super.getDefaultState(),
      applications: [],
      sentryFunctions: [],
      tab: value,
    };
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationDeveloperSettings/index.tsx" line="64">

---

## getEndpoints

The `getEndpoints` method is used to define the endpoints for fetching the list of applications. It returns an array of tuples, where each tuple contains the name of the state property to be updated and the URL of the endpoint.

```tsx
  getEndpoints(): ReturnType<DeprecatedAsyncView['getEndpoints']> {
    const {organization} = this.props;
    const returnValue: [string, string, any?, any?][] = [
      ['applications', `/organizations/${organization.slug}/sentry-apps/`],
    ];
    return returnValue;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationDeveloperSettings/index.tsx" line="72">

---

## removeApp

The `removeApp` method is used to remove an application from the list of applications. It filters out the application to be removed and updates the state with the new list of applications.

```tsx
  removeApp = (app: SentryApp) => {
    const apps = this.state.applications.filter(a => a.slug !== app.slug);
    removeSentryApp(this.api, app).then(
      () => {
        this.setState({applications: apps});
      },
      () => {}
    );
  };
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationDeveloperSettings/index.tsx" line="82">

---

## onTabChange

The `onTabChange` method is used to handle changes in the selected tab. It updates the tab property of the state with the new value.

```tsx
  onTabChange = (value: Tab) => {
    this.setState({tab: value});
  };
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationDeveloperSettings/index.tsx" line="86">

---

## renderApplicationRow

The `renderApplicationRow` method is used to render each application in the list of applications. It uses the `SentryApplicationRow` component to render the details of each application.

```tsx
  renderApplicationRow = (app: SentryApp) => {
    const {organization} = this.props;
    return (
      <SentryApplicationRow
        key={app.uuid}
        app={app}
        organization={organization}
        onRemoveApp={this.removeApp}
      />
    );
  };
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationDeveloperSettings/index.tsx" line="98">

---

## renderInternalIntegrations

The `renderInternalIntegrations` method is used to render the list of internal integrations. It filters the list of applications to include only internal integrations and renders the list using the `SentryApplicationRow` component.

```tsx
  renderInternalIntegrations() {
    const integrations = this.state.applications.filter(
      (app: SentryApp) => app.status === 'internal'
    );
    const isEmpty = integrations.length === 0;

    return (
      <Panel>
        <PanelHeader>{t('Internal Integrations')}</PanelHeader>
        <PanelBody>
          {!isEmpty ? (
            integrations.map(this.renderApplicationRow)
          ) : (
            <EmptyMessage>
              {t('No internal integrations have been created yet.')}
            </EmptyMessage>
          )}
        </PanelBody>
      </Panel>
    );
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationDeveloperSettings/index.tsx" line="120">

---

## renderPublicIntegrations

The `renderPublicIntegrations` method is used to render the list of public integrations. It filters the list of applications to include only public integrations and renders the list using the `SentryApplicationRow` component.

```tsx
  renderPublicIntegrations() {
    const integrations = this.state.applications.filter(app => app.status !== 'internal');
    const isEmpty = integrations.length === 0;

    return (
      <Panel>
        <PanelHeader>{t('Public Integrations')}</PanelHeader>
        <PanelBody>
          {!isEmpty ? (
            integrations.map(this.renderApplicationRow)
          ) : (
            <EmptyMessage>
              {t('No public integrations have been created yet.')}
            </EmptyMessage>
          )}
        </PanelBody>
      </Panel>
    );
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationDeveloperSettings/index.tsx" line="140">

---

## renderTabContent

The `renderTabContent` method is used to render the content of the currently selected tab. It uses a switch statement to determine which method to call based on the currently selected tab.

```tsx
  renderTabContent(tab: Tab) {
    switch (tab) {
      case 'internal':
        return this.renderInternalIntegrations();
      case 'public':
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
