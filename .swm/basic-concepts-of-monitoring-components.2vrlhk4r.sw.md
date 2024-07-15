---
title: Basic Concepts of Monitoring Components
---
Monitors in the views directory of the Sentry-Demo repository refer to components that track and display specific data or events within the application. They are used to observe the state and performance of various aspects of the application, such as issues, stats, and check-ins.

The MonitorsContainer function in the index.tsx file is a React component that wraps the children components with the NoProjectMessage and PageFiltersContainer components. This is used to display a message when there are no projects and to provide page filters.

The monitor member in the overviewRow.tsx and monitorIssues.tsx files is an object of type Monitor. It represents a specific monitor with its associated data and functionalities.

The monitors member in the useMonitorStats.tsx file is an array of monitor IDs. It is used to fetch stats for the specified monitors.

The monitorList member in the overviewTimeline/index.tsx file is an array of Monitor objects. It is used to display an overview timeline of the specified monitors.

<SwmSnippet path="/static/app/views/monitors/overview.tsx" line="51">

---

# Monitors Function

The Monitors function is a React component that uses various hooks to fetch and manage data related to monitors. It uses the useApi, useOrganization, useNavigate, and useLocation hooks to fetch and manage the necessary data.

```tsx
export default function Monitors() {
  const api = useApi();
  const organization = useOrganization();
  const navigate = useNavigate();
  const location = useLocation();
  const platform = decodeScalar(location.query?.platform) ?? null;
  const guide = decodeScalar(location.query?.guide);
  const project = decodeList(location.query?.project);

  const queryKey = makeMonitorListQueryKey(organization, location.query);

  const {
    data: monitorList,
    getResponseHeader: monitorListHeaders,
    isLoading,
    refetch,
  } = useApiQuery<Monitor[]>(queryKey, {
    staleTime: 0,
  });
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/monitors/components/monitorIssues.tsx" line="28">

---

# Monitor Member

The monitor member in the monitorIssues.tsx file is an object of type Monitor. It represents a specific monitor with its associated data and functionalities.

```tsx
  monitor: Monitor;
  monitorEnvs: MonitorEnvironment[];
  orgSlug: string;
};
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/monitors/components/timeline/hooks/useMonitorStats.tsx" line="11">

---

# Monitors Member

The monitors member in the useMonitorStats.tsx file is an array of monitor IDs. It is used to fetch stats for the specified monitors.

```tsx
  monitors: string[];
  /**
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
