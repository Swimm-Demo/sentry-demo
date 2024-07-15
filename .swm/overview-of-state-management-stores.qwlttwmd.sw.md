---
title: Overview of State Management Stores
---
In the context of the sentry-demo repository, 'Stores' refer to the data management system used within the application. They are responsible for managing and storing the state of different aspects of the application. For instance, the 'organizationStore' manages the state related to organizations, while the 'projectsStore' manages the state related to projects. These stores are implemented using TypeScript and are located in the 'static/app/stores' directory. They provide methods for updating and retrieving the state, and they trigger updates when the state changes.

The 'loading' property found in many of the stores is a common pattern used to track the loading state of asynchronous operations. When an asynchronous operation such as a network request is initiated, 'loading' is set to true. Once the operation is complete, 'loading' is set to false. This allows the UI to provide feedback to the user about the loading state of the operation.

The 'loaded' property, on the other hand, is used to indicate whether the data has been loaded. This is particularly useful in scenarios where data is fetched from a server. When the data is successfully fetched and stored, 'loaded' is set to true.

<SwmSnippet path="/static/app/stores/organizationStore.tsx" line="29">

---

# OrganizationStore

The OrganizationStore is responsible for managing the state related to organizations. It provides a 'get' method for retrieving the state, and an 'onUpdate' method for updating the state.

```tsx
const storeConfig: OrganizationStoreDefinition = {
  state: {
    dirty: false,
    loading: true,
    organization: null,
    error: null,
    errorType: null,
  },
  init() {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/stores/projectsStore.tsx" line="64">

---

# ProjectsStore

The ProjectsStore is responsible for managing the state related to projects. It provides a 'loadInitialData' method for loading the initial state.

```tsx
  loadInitialData(items: Project[]) {
    this.state = {
      projects: items.toSorted((a, b) => a.slug.localeCompare(b.slug)),
      loading: false,
    };

    this.trigger(new Set(items.map(x => x.id)));
  },
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/stores/organizationStore.tsx" line="30">

---

# Loading and Loaded Properties

The 'loading' and 'loaded' properties are common patterns used to track the loading state of asynchronous operations and whether the data has been loaded, respectively. When an asynchronous operation such as a network request is initiated, 'loading' is set to true. Once the operation is complete, 'loading' is set to false. When the data is successfully fetched and stored, 'loaded' is set to true.

```tsx
  state: {
    dirty: false,
    loading: true,
    organization: null,
    error: null,
    errorType: null,
  },
```

---

</SwmSnippet>

# Store Endpoints

Understanding Store Endpoints

<SwmSnippet path="/static/app/stores/organizationStore.tsx" line="55">

---

## onUpdate (organizationStore.tsx)

The `onUpdate` method in the `organizationStore` is used to update the state of the organization. It takes an updated organization object and an options object as parameters. If the replace option is true, it replaces the current organization state with the updated organization. Otherwise, it merges the updated organization with the current organization state. After updating the state, it triggers an update to notify other parts of the application about the state change.

```tsx
  onUpdate(updatedOrg: Organization, {replace = false} = {}) {
    const organization = replace
      ? updatedOrg
      : {...this.state.organization, ...updatedOrg};
    this.state = {
      loading: false,
      dirty: false,
      errorType: null,
      error: null,
      organization,
    };
    this.trigger(this.get());

    ReleaseStore.updateOrganization(organization);
    LatestContextStore.onUpdateOrganization(organization);
    HookStore.getCallback(
      'react-hook:route-activated',
      'setOrganization'
    )?.(organization);
  },
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/stores/projectsStore.tsx" line="64">

---

## loadInitialData (projectsStore.tsx)

The `loadInitialData` method in the `projectsStore` is used to load the initial state of the projects. It takes an array of projects as a parameter and sets the state of the projects to the provided array. It also sets the loading state to false, indicating that the initial data has been loaded. After setting the state, it triggers an update to notify other parts of the application about the state change.

```tsx
  loadInitialData(items: Project[]) {
    this.state = {
      projects: items.toSorted((a, b) => a.slug.localeCompare(b.slug)),
      loading: false,
    };
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
