---
title: Overview of Web Assets Plugins
---
Plugins in Sentry are additional modules that provide extra functionality and integration with various services. They are used to extend the capabilities of the Sentry application. For example, they can be used to integrate with different issue tracking systems, or to add support for additional programming languages and frameworks.

Plugins are implemented as separate components within the Sentry codebase. Each plugin has its own directory under the `static/app/plugins` directory, and contains a set of TypeScript files that define its functionality. The `index.tsx` file is the entry point for each plugin, and it typically imports and exports various components and utilities from other files in the same directory.

The `basePlugin.tsx` file defines the `BasePlugin` class, which is the base class for all plugins. Each plugin extends this base class and overrides its methods to provide its specific functionality. The `BasePlugin` class has a `plugin` member, which is an instance of the `Plugin` type. This instance contains the data for the plugin, such as its ID and settings.

The `registry.tsx` file defines the `Registry` class, which is used to manage the registered plugins. It provides methods to add, get, and load plugins. The `plugins` object exported from `index.tsx` includes these methods, as well as the `BasePlugin` and `DefaultIssuePlugin` classes.

The `components` directory under `static/app/plugins` contains various React components that are used by the plugins. For example, the `pluginIcon.tsx` file defines the `PluginIcon` component, which is used to display the icon for a plugin. It uses a set of predefined icons for specific plugins, and a default icon for others.

<SwmSnippet path="/static/app/plugins/components/settings.tsx" line="37">

---

# Plugin Components

The `PluginSettings` class is a React component that provides the settings interface for a plugin. It extends the `PluginComponentBase` class and overrides its methods to handle the loading and saving of plugin settings. The `onSubmit` method is used to save the settings when the form is submitted.

```tsx
class PluginSettings<
  P extends Props = Props,
  S extends State = State,
> extends PluginComponentBase<P, S> {
  constructor(props: P, context: any) {
    super(props, context);

    Object.assign(this.state, {
      fieldList: null,
      initialData: null,
      formData: null,
      errors: {},
      rawData: {},
      // override default FormState.READY if api requests are
      // necessary to even load the form
      state: FormState.LOADING,
      wasConfiguredOnPageLoad: false,
    });
  }

  trackPluginEvent = (eventKey: IntegrationAnalyticsKey) => {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/plugins/registry.tsx" line="13">

---

# Plugin Registry

The `Registry` class is used to manage the registered plugins. It provides methods to add, get, and load plugins. The `load` method is used to load a plugin's assets and instantiate it. The `get` method is used to retrieve a loaded plugin.

```tsx
export default class Registry {
  plugins: Record<string, PluginComponent> = {};
  assetCache: Record<string, HTMLScriptElement> = {};

  isLoaded(data: Plugin) {
    return defined(this.plugins[data.id]);
  }

  load(
    data: Plugin,
    callback: (instance: DefaultIssuePlugin | DefaultPlugin | SessionStackPlugin) => void
  ) {
    let remainingAssets = data.assets.length;
    // TODO(dcramer): we should probably register all valid plugins
    const finishLoad = () => {
      if (!defined(this.plugins[data.id])) {
        if (data.type === 'issue-tracking') {
          this.plugins[data.id] = DefaultIssuePlugin;
        } else {
          this.plugins[data.id] = DefaultPlugin;
        }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/plugins/basePlugin.tsx" line="11">

---

# BasePlugin Class

The `BasePlugin` class is the base class for all plugins. Each plugin extends this base class and overrides its methods to provide its specific functionality. The `plugin` member of the `BasePlugin` class is an instance of the `Plugin` type, which contains the data for the plugin.

```tsx
class BasePlugin {
  plugin: Plugin;
  constructor(data: Plugin) {
    this.plugin = data;
  }

  renderSettings(props: Props) {
    return <Settings plugin={this.plugin} {...props} />;
  }
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/plugins/index.tsx" line="1">

---

# Plugin Index

The `index.tsx` file is the entry point for the plugins module. It imports and exports various components and utilities, including the `BasePlugin` and `DefaultIssuePlugin` classes, and the `registry` object. The `plugins` object exported from this file includes these classes and objects, as well as methods to add and load plugins.

```tsx
import BasePlugin from 'sentry/plugins/basePlugin';
import DefaultIssuePlugin from 'sentry/plugins/defaultIssuePlugin';
import Registry from 'sentry/plugins/registry';

import SessionStackContextType from './sessionstack/contexts/sessionstack';
import Jira from './jira';
import SessionStackPlugin from './sessionstack';

const contexts: Record<string, React.ElementType> = {};
const registry = new Registry();

// Register legacy plugins

// Sessionstack
registry.add('sessionstack', SessionStackPlugin);
contexts.sessionstack = SessionStackContextType;

// Jira
registry.add('jira', Jira);

export {BasePlugin, DefaultIssuePlugin, registry};
```

---

</SwmSnippet>

# Plugin Functions

This section provides an overview of the main functions related to plugins in the Sentry application.

<SwmSnippet path="/static/app/plugins/components/settings.tsx" line="71">

---

## Plugin Lifecycle Functions

The `getPluginEndpoint` function is used to construct the API endpoint URL for a specific plugin. It uses the slug of the organization, project, and plugin to form the URL.

```tsx
  getPluginEndpoint() {
    const org = this.props.organization;
    const project = this.props.project;
    return `/projects/${org.slug}/${project.slug}/plugins/${this.props.plugin.id}/`;
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/plugins/components/settings.tsx" line="67">

---

The `fetchData` function is used to fetch the data for a plugin from the API. It makes a request to the plugin's endpoint and updates the component's state with the received data.

```tsx
  componentDidMount() {
    this.fetchData();
  }

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/plugins/components/settings.tsx" line="85">

---

The `onSubmit` function is used when the plugin's settings form is submitted. It makes a request to the plugin's endpoint with the form data. If the plugin was not configured when the page loaded, it also sends an installation event for analytics purposes.

```tsx

  onSubmit() {
    if (!this.state.wasConfiguredOnPageLoad) {
      // Users cannot install plugins like other integrations but we need the events for the funnel
      // we will treat a user saving a plugin that wasn't already configured as an installation event
      this.trackPluginEvent('integrations.installation_start');
    }

    let repo = this.state.formData.repo;
    repo = repo && parseRepo(repo);
    const parsedFormData = {...this.state.formData, repo};
    this.api.request(this.getPluginEndpoint(), {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/plugins/registry.tsx" line="21">

---

The `load` function is used to load a plugin. It checks if the plugin is already loaded, and if not, it loads the plugin's assets and registers the plugin.

```tsx
  load(
    data: Plugin,
    callback: (instance: DefaultIssuePlugin | DefaultPlugin | SessionStackPlugin) => void
  ) {
    let remainingAssets = data.assets.length;
    // TODO(dcramer): we should probably register all valid plugins
    const finishLoad = () => {
      if (!defined(this.plugins[data.id])) {
        if (data.type === 'issue-tracking') {
          this.plugins[data.id] = DefaultIssuePlugin;
        } else {
          this.plugins[data.id] = DefaultPlugin;
        }
      }
      console.info(
        '[plugins] Loaded ' + data.id + ' as {' + this.plugins[data.id].name + '}'
      );
      callback(this.get(data));
    };

    if (remainingAssets === 0) {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/plugins/pluginComponentBase.tsx" line="143">

---

The `onSaveComplete` function is called when the saving of a plugin's settings is completed. It clears any indicators and calls the provided callback function.

```tsx
  onSaveComplete(callback, ...args) {
    clearIndicators();
    callback = callbackWithArgs(this, callback, ...args);
    callback?.();
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/plugins/components/issueActions.tsx" line="471">

---

The `getPluginConfigureUrl` function is used to construct the URL for configuring a plugin. It uses the slug of the organization, project, and plugin to form the URL.

```tsx
  getPluginConfigureUrl() {
    const org = this.getOrganization();
    const project = this.getProject();
    const plugin = this.props.plugin;
    return '/' + org.slug + '/' + project.slug + '/settings/plugins/' + plugin.slug;
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
