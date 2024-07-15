---
title: Overview of Project Settings
---
In the sentry-demo repository, a 'Project' refers to a specific set of configurations and settings related to error tracking and performance monitoring. It is represented as an object with various properties and methods. The 'Project' object is used throughout the codebase, particularly within the settings directory, to manage and manipulate these configurations.

The 'Project' object is used in various files such as 'projectFiltersSettings.tsx' and 'projectKeys/details/keySettings.tsx'. It contains properties like 'projectId', 'features', and 'description' which are used to manage the project's settings. For example, 'projectId' is used to identify the project, 'features' is a set of enabled features for the project, and 'description' provides a brief explanation of the project.

The 'Project' object is also used in the 'ProjectFiltersSettings' function in 'projectFiltersSettings.tsx' to manage the project's filter settings. This includes enabling or disabling certain filters, and managing filter descriptions.

In addition to managing settings, the 'Project' object is also used in the 'KeySettings' function in 'projectKeys/details/keySettings.tsx' to manage the project's keys. This includes operations like revoking a key.

<SwmSnippet path="/static/app/views/settings/project/projectFilters/projectFiltersSettings.tsx" line="386">

---

# Project in projectFiltersSettings.tsx

In 'projectFiltersSettings.tsx', the 'Project' object is used in the 'ProjectFiltersSettings' function to manage the project's filter settings. This includes enabling or disabling certain filters, and managing filter descriptions.

```tsx
  params: {
    projectId: string;
  };
  project: Project;
};

type Filter = {
  active: boolean | string[];
  description: string;
  hello: string;
  id: string;
  name: string;
};

export function ProjectFiltersSettings({project, params, features}: Props) {
  const organization = useOrganization();
  const {projectId: projectSlug} = params;
  const projectEndpoint = `/projects/${organization.slug}/${projectSlug}/`;
  const filtersEndpoint = `${projectEndpoint}filters/`;

  const {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/project/projectKeys/details/keySettings.tsx" line="32">

---

# Project in projectKeys/details/keySettings.tsx

In 'projectKeys/details/keySettings.tsx', the 'Project' object is used in the 'KeySettings' function to manage the project's keys. This includes operations like revoking a key.

```tsx
    keyId: string;
    projectId: string;
  };
  project: Project;
  updateData: (data: ProjectKey) => void;
};

export function KeySettings({
  onRemove,
  organization,
  project,
  params,
  data,
  updateData,
}: Props) {
  const api = useApi();

  const {keyId, projectId} = params;
  const apiEndpoint = `/projects/${organization.slug}/${projectId}/keys/${keyId}/`;

  const handleRemove = useCallback(async () => {
```

---

</SwmSnippet>

# Project Endpoints

Project Keys and Hooks Endpoints

<SwmSnippet path="/static/app/views/settings/project/projectKeys/details/index.tsx" line="65">

---

## Project Keys Endpoint

This endpoint is used to manage the keys of a project. The keys are used by the SDKs to authenticate the data sent to the server. The endpoint allows for creating, updating, and deleting keys.

```tsx
    <SentryDocumentTitle title={t('Key Details')}>
      <SettingsPageHeader title={t('Key Details')} data-test-id="key-details" />
      <PermissionAlert project={project} />
      <KeyStats api={api} organization={organization} params={params} />
      <KeySettings
        data={projKeyData}
        updateData={onDataChange}
        onRemove={handleRemove}
        organization={organization}
        project={project}
        params={params}
      />
    </SentryDocumentTitle>
  );
}

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/project/projectServiceHookDetails.tsx" line="64">

---

## Project Hooks Endpoint

This endpoint is used to manage the service hooks of a project. Service hooks allow certain events in Sentry to trigger notifications to another service. This endpoint allows for creating, updating, and deleting service hooks.

```tsx
    const {stats} = this.state;
    if (stats === null) {
      return null;
    }
    let emptyStats = true;

    const series = {
      seriesName: t('Events'),
      data: stats.map(p => {
        if (p.total) {
          emptyStats = false;
        }
        return {
          name: p.ts * 1000,
          value: p.total,
        };
      }),
    };

    return (
      <Panel>
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
