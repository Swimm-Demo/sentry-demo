---
title: Getting Started with Project Detail View
---
Project Detail in the views directory refers to the detailed view of a specific project within the Sentry application. It is implemented in the `projectDetail.tsx` file. This view is responsible for displaying various information about a project, such as its performance, transactions, sessions, and other related data. It fetches the project data using the `useProjects` hook and the project's ID from the URL parameters. The view also includes various features based on the organization's settings, such as performance view and discover basic.

The `ProjectDetail` function uses several constants to manage the state and behavior of the view. For instance, `hasPerformance` and `hasDiscover` are used to check if the organization has certain features enabled. `projectId` is used to store the ID of the current project. `isProjectStabilized` is a flag that checks if the project ID is consistent across different parts of the application state. `visibleCharts` determines which charts to display based on the project's data.

The `ProjectDetail` function also defines several callback functions to handle specific actions within the view. For example, `onRetryProjects` is used to fetch the organization details again when an error occurs. `handleSearch` is used to update the URL with the new search query when the user performs a search.

The `ProjectDetail` view is rendered using various components. These include `SentryDocumentTitle` for setting the page title, `PageFiltersContainer` for managing filters, `Layout` components for structuring the page, and various project-specific components like `ProjectScoreCards`, `ProjectTeamAccess`, `ProjectLatestAlerts`, `ProjectLatestReleases`, and `ProjectQuickLinks`.

The `projectDetail.spec.tsx` file contains tests for the `ProjectDetail` view. It checks for scenarios like rendering an error if the project is not found, rendering a warning if the user is not a member of the project, rendering the project details correctly, and syncing the project with the slug.

<SwmSnippet path="/static/app/views/projectDetail/projectDetail.tsx" line="54">

---

# Project Detail Function

The `ProjectDetail` function is the main function in this file. It uses several constants to manage the state and behavior of the view. For instance, `hasPerformance` and `hasDiscover` are used to check if the organization has certain features enabled. `projectId` is used to store the ID of the current project. `isProjectStabilized` is a flag that checks if the project ID is consistent across different parts of the application state. `visibleCharts` determines which charts to display based on the project's data.

```tsx
export default function ProjectDetail({router, location, organization}: Props) {
  const api = useApi();
  const params = useParams();
  const {projects, fetching: loadingProjects} = useProjects();
  const {selection} = usePageFilters();
  const project = projects.find(p => p.slug === params.projectId);
  const {query} = location.query;
  const hasPerformance = organization.features.includes('performance-view');
  const hasDiscover = organization.features.includes('discover-basic');
  const hasTransactions = hasPerformance && project?.firstTransactionEvent;
  const projectId = project?.id;
  const isProjectStabilized =
    defined(project?.id) &&
    project.id === location.query.project &&
    project.id === String(selection.projects[0]);
  const hasSessions = project?.hasSessions ?? null;
  const hasOnlyBasicChart = !hasPerformance && !hasDiscover && !hasSessions;
  const title = routeTitleGen(
    t('Project %s', params.projectId),
    organization.slug,
    false
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/projectDetail/projectDetail.tsx" line="84">

---

# Callback Functions

The `ProjectDetail` function also defines several callback functions to handle specific actions within the view. For example, `onRetryProjects` is used to fetch the organization details again when an error occurs. `handleSearch` is used to update the URL with the new search query when the user performs a search.

```tsx
  const onRetryProjects = useCallback(() => {
    fetchOrganizationDetails(api, params.orgId, true, false);
  }, [api, params.orgId]);

  const handleSearch = useCallback(
    (searchQuery: string) => {
      router.replace({
        pathname: location.pathname,
        query: {
          ...location.query,
          query: searchQuery,
        },
      });
    },
    [router, location.query, location.pathname]
  );

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/projectDetail/projectDetail.tsx" line="225">

---

# Rendering the View

The `ProjectDetail` view is rendered using various components. These include `SentryDocumentTitle` for setting the page title, `PageFiltersContainer` for managing filters, `Layout` components for structuring the page, and various project-specific components like `ProjectScoreCards`, `ProjectTeamAccess`, `ProjectLatestAlerts`, `ProjectLatestReleases`, and `ProjectQuickLinks`.

```tsx
                  organization={organization}
                  isProjectStabilized={isProjectStabilized}
                  selection={selection}
                  hasSessions={hasSessions}
                  hasTransactions={hasTransactions}
                  query={query}
                  project={project}
                  location={location}
                />
                {isProjectStabilized && (
                  <Fragment>
                    {visibleCharts.map((id, index) => (
                      <ProjectCharts
                        location={location}
                        organization={organization}
                        router={router}
                        key={`project-charts-${id}`}
                        chartId={id}
                        chartIndex={index}
                        projectId={project?.id}
                        hasSessions={hasSessions}
```

---

</SwmSnippet>

# Testing the View

The `projectDetail.spec.tsx` file contains tests for the `ProjectDetail` view. It checks for scenarios like rendering an error if the project is not found, rendering a warning if the user is not a member of the project, rendering the project details correctly, and syncing the project with the slug.

# ProjectDetail View Functions

This section will explain the main functions and components used in the ProjectDetail view of the Sentry application.

<SwmSnippet path="/static/app/views/projectDetail/projectDetail.tsx" line="54">

---

## ProjectDetail Function

The `ProjectDetail` function is the main component of the ProjectDetail view. It uses several hooks and constants to manage the state and behavior of the view, fetch the project data, and render various components based on the project's data and the organization's settings.

```tsx
export default function ProjectDetail({router, location, organization}: Props) {
  const api = useApi();
  const params = useParams();
  const {projects, fetching: loadingProjects} = useProjects();
  const {selection} = usePageFilters();
  const project = projects.find(p => p.slug === params.projectId);
  const {query} = location.query;
  const hasPerformance = organization.features.includes('performance-view');
  const hasDiscover = organization.features.includes('discover-basic');
  const hasTransactions = hasPerformance && project?.firstTransactionEvent;
  const projectId = project?.id;
  const isProjectStabilized =
    defined(project?.id) &&
    project.id === location.query.project &&
    project.id === String(selection.projects[0]);
  const hasSessions = project?.hasSessions ?? null;
  const hasOnlyBasicChart = !hasPerformance && !hasDiscover && !hasSessions;
  const title = routeTitleGen(
    t('Project %s', params.projectId),
    organization.slug,
    false
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/useProjects.tsx" line="141">

---

## useProjects Hook

The `useProjects` hook is used to fetch the project data from the ProjectsStore. It also provides a way to select specific project slugs, and search for more projects that may not be in the project store.

```tsx
/**
 * Provides projects from the ProjectsStore
 *
 * This hook also provides a way to select specific project slugs, and search
 * (type-ahead) for more projects that may not be in the project store.
 *
 * NOTE: Currently ALL projects are always loaded, but this hook is designed
 * for future-compat in a world where we do _not_ load all projects.
 */
function useProjects({limit, slugs, orgId: propOrgId}: Options = {}) {
  const api = useApi();

  const organization = useOrganization({allowNull: true});
  const store = useLegacyStore(ProjectsStore);

  const orgId = propOrgId ?? organization?.slug ?? organization?.slug;

  const storeSlugs = new Set(store.projects.map(t => t.slug));
  const slugsToLoad = slugs?.filter(slug => !storeSlugs.has(slug)) ?? [];
  const shouldLoadSlugs = slugsToLoad.length > 0;

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/useApi.tsx" line="24">

---

## useApi Hook

The `useApi` hook returns an API client that will have its requests canceled when the owning React component is unmounted. It is used in the ProjectDetail function to make API requests.

```tsx
/**
 * Returns an API client that will have its requests canceled when the owning
 * React component is unmounted (may be disabled via options).
 */
function useApi({persistInFlight, api: providedApi}: Options = {}) {
  const localApi = useRef<Client>();

  // Lazily construct the client if we weren't provided with one
  if (localApi.current === undefined && providedApi === undefined) {
    localApi.current = new Client();
  }

  // Use the provided client if available
  const api = providedApi ?? localApi.current!;

  // Clear API calls on unmount (if persistInFlight is disabled
  const clearOnUnmount = useCallback(() => {
    if (!persistInFlight) {
      api.clear();
    }
  }, [api, persistInFlight]);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/useParams.tsx" line="6">

---

## useParams Hook

The `useParams` hook is used to access the URL parameters. In the ProjectDetail function, it is used to get the project's ID from the URL.

```tsx
export function useParams<P = Record<string, string>>(): P {
  const contextParams = useRouteContext().params;

  // Memoize params as mutating for customer domains causes other hooks
  // that depend on `useParams()` to refresh infinitely.
  return useMemo(() => {
    if (USING_CUSTOMER_DOMAIN && CUSTOMER_DOMAIN && contextParams.orgId === undefined) {
      // We do not know if the caller of this hook requires orgId, so we populate orgId implicitly.
      return {...contextParams, orgId: CUSTOMER_DOMAIN};
    }
    return contextParams;
  }, [contextParams]);
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/projectDetail/projectDetail.tsx" line="58">

---

## usePageFilters Hook

The `usePageFilters` hook is used in the ProjectDetail function to manage the page filters.

```tsx
  const {selection} = usePageFilters();
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
