---
title: Understanding Common Components
---
Components in the 'Common' directory are reusable pieces of code that can be used across different parts of the application. They are primarily written in TypeScript and use React, a popular JavaScript library for building user interfaces. These components include tables, cells, panels, and providers, among others.

Props, short for properties, are a way of passing data from parent components to child components. They are read-only and help to control a component's behavior and display. For example, in the 'samplesTable' and 'modulePageProviders' components, Props are used to pass various data such as 'compareToDuration', 'duration', 'children', 'features', and 'moduleName'.

The 'samplesTable' and 'tableCells' directories contain components related to displaying data in a tabular format. These components handle the rendering of different types of cells in the table, such as 'throughputCell', 'resourceSizeCell', 'spanIdCell', and others.

The 'modulePageProviders' component is a higher-order component that wraps other components and provides them with certain props or state. In this case, it provides the 'features' prop to the child components.

<SwmSnippet path="/static/app/views/insights/common/components/modulePageProviders.tsx" line="17">

---

# Props in Components

Props, short for properties, are a way of passing data from parent components to child components. They are read-only and help to control a component's behavior and display. For example, in the 'modulePageProviders' component, Props are used to pass various data such as 'children', 'features', and 'moduleName'.

```tsx
interface Props {
  children: React.ReactNode;
  features: ComponentProps<typeof Feature>['features'];
  moduleName: TitleableModuleNames;
  pageTitle?: string;
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/common/components/modulePageProviders.tsx" line="24">

---

# Usage of Components

The 'modulePageProviders' component is a higher-order component that wraps other components and provides them with certain props or state. In this case, it provides the 'features' prop to the child components.

```tsx
export function ModulePageProviders({moduleName, pageTitle, children, features}: Props) {
  const organization = useOrganization();

  const moduleTitle = MODULE_TITLES[moduleName];

  const fullPageTitle = [pageTitle, moduleTitle, INSIGHTS_TITLE]
    .filter(Boolean)
    .join(' — ');

  const defaultBody = (
    <Layout.Page>
      <Feature features={features} organization={organization} renderDisabled={NoAccess}>
        <NoProjectMessage organization={organization}>{children}</NoProjectMessage>
      </Feature>
    </Layout.Page>
  );

  return (
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
