---
title: Getting Started with the Breadcrumb Component
---
Breadcrumbs in the Sentry-demo repository refer to a specific component used to display a trail of events or steps leading to a certain event. This component is primarily used for error tracking and performance monitoring, providing a visual representation of the event path.

The Breadcrumbs component is defined in the 'breadcrumbs.tsx' file, located in the 'events/interfaces/breadcrumbs' directory. It uses several properties and methods to render and manage the breadcrumbs, such as 'Props', 'Breadcrumbs', 'useProjects', 'isEventId', and 'useApiQuery'.

The 'Props' interface defines the properties that the Breadcrumbs component expects. These properties include 'breadcrumbs', 'displayRelativeTime', 'onSwitchTimeFormat', 'organization', 'searchTerm', 'event', 'relativeTime', and 'emptyMessage'.

The 'Breadcrumbs' function is the main function of the component. It uses the properties defined in 'Props' to fetch the necessary data, handle user interactions, and render the breadcrumbs.

The 'useProjects' function is used to fetch the projects from the ProjectsStore. The 'isEventId' function checks if a given string is an event id. The 'useApiQuery' function wraps React Query's useQuery for consistent usage in the Sentry app.

The 'breadcrumbs.tsx' file also contains several styled components and constants that define the look and feel of the breadcrumbs. These include 'StyledBreadcrumbPanelTable', 'Time', 'StyledIconSort', 'PanelDragHandle', 'VirtualizedList', and 'BreadcrumbRow'.

<SwmSnippet path="/static/app/components/events/interfaces/breadcrumbs/breadcrumbs.tsx" line="105">

---

# Breadcrumbs Component

The 'Breadcrumbs' function is the main function of the component. It uses the properties defined in 'Props' to fetch the necessary data, handle user interactions, and render the breadcrumbs.

```tsx
function Breadcrumbs({
  breadcrumbs,
  displayRelativeTime,
  onSwitchTimeFormat,
  organization,
  searchTerm,
  event,
  relativeTime,
  emptyMessage,
}: Props) {
  const {projects, fetching: loadingProjects} = useProjects();

  const maybeProject = !loadingProjects
    ? projects.find(project => {
        return event && project.id === event.projectID;
      })
    : null;

  const listRef = useRef<List>(null);

  const sentryTransactionIds = useMemo(() => {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/breadcrumbs/breadcrumbs.tsx" line="92">

---

# Props Interface

The 'Props' interface defines the properties that the Breadcrumbs component expects. These properties include 'breadcrumbs', 'displayRelativeTime', 'onSwitchTimeFormat', 'organization', 'searchTerm', 'event', 'relativeTime', and 'emptyMessage'.

```tsx
interface Props
  extends Pick<
    BreadcrumbProps,
    'event' | 'organization' | 'searchTerm' | 'relativeTime' | 'displayRelativeTime'
  > {
  breadcrumbs: BreadcrumbWithMeta[];
  emptyMessage: Pick<
    React.ComponentProps<typeof PanelTable>,
    'emptyMessage' | 'emptyAction'
  >;
  onSwitchTimeFormat: () => void;
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/useProjects.tsx" line="150">

---

# useProjects Function

The 'useProjects' function is used to fetch the projects from the ProjectsStore.

```tsx
function useProjects({limit, slugs, orgId: propOrgId}: Options = {}) {
  const api = useApi();

  const organization = useOrganization({allowNull: true});
  const store = useLegacyStore(ProjectsStore);

  const orgId = propOrgId ?? organization?.slug ?? organization?.slug;

  const storeSlugs = new Set(store.projects.map(t => t.slug));
  const slugsToLoad = slugs?.filter(slug => !storeSlugs.has(slug)) ?? [];
  const shouldLoadSlugs = slugsToLoad.length > 0;

  const [state, setState] = useState<State>({
    initiallyLoaded: !store.loading && !shouldLoadSlugs,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/breadcrumbs/breadcrumb/data/default.tsx" line="57">

---

# isEventId Function

The 'isEventId' function checks if a given string is an event id.

```tsx
export function isEventId(maybeEventId: string): boolean {
  // maybeEventId is an event id if it's a hex string of 32 characters long
  return /^[a-fA-F0-9]{32}$/.test(maybeEventId);
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/queryClient.tsx" line="121">

---

# useApiQuery Function

The 'useApiQuery' function wraps React Query's useQuery for consistent usage in the Sentry app.

```tsx
export function useApiQuery<TResponseData, TError = RequestError>(
  queryKey: ApiQueryKey,
  options: UseApiQueryOptions<TResponseData, TError>
): UseApiQueryResult<TResponseData, TError> {
  const api = useApi({persistInFlight: PERSIST_IN_FLIGHT});
  const queryFn = fetchDataQuery(api);

  const {data, ...rest} = useQuery(queryKey, queryFn, options);

  const queryResult = {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/breadcrumbs/breadcrumbs.tsx" line="248">

---

# Styled Components and Constants

The 'breadcrumbs.tsx' file also contains several styled components and constants that define the look and feel of the breadcrumbs. These include 'StyledBreadcrumbPanelTable', 'Time', 'StyledIconSort', 'PanelDragHandle', 'VirtualizedList', and 'BreadcrumbRow'.

```tsx
export const StyledBreadcrumbPanelTable = styled(PanelTable)`
  display: grid;
  overflow: hidden;
  grid-template-columns: 64px 140px 1fr 106px 100px;
  margin-bottom: 1px;

  > * {
    :nth-child(-n + 6) {
      border-bottom: 1px solid ${p => p.theme.border};
      border-radius: 0;
      /* This is to fix a small issue with the border not being fully visible on smaller devices */
      margin-bottom: 1px;

      /* Type */
      :nth-child(6n-5) {
        text-align: center;
      }
    }

    /* Scroll bar header */
    :nth-child(6) {
```

---

</SwmSnippet>

# Breadcrumbs Component Functions

This section explains the main functions of the Breadcrumbs component in the Sentry-demo repository.

<SwmSnippet path="/static/app/components/events/interfaces/breadcrumbs/breadcrumbs.tsx" line="38">

---

## Props

The 'Props' interface defines the properties that the Breadcrumbs component expects. These properties include 'breadcrumbs', 'displayRelativeTime', 'onSwitchTimeFormat', 'organization', 'searchTerm', 'event', 'relativeTime', and 'emptyMessage'.

```tsx
  breadcrumbs: BreadcrumbWithMeta[];
  displayRelativeTime: boolean;
  event: BreadcrumbProps['event'];
  index: number;
  organization: Organization;
  relativeTime: string;
  searchTerm: string;
  transactionEvents: BreadcrumbTransactionEvent[] | undefined;
}

interface BreadCrumbListClass extends Omit<List, 'props'> {
  props: SharedListProps;
}

interface RenderBreadCrumbRowProps {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/breadcrumbs/breadcrumbs.tsx" line="105">

---

## Breadcrumbs

The 'Breadcrumbs' function is the main function of the component. It uses the properties defined in 'Props' to fetch the necessary data, handle user interactions, and render the breadcrumbs.

```tsx
function Breadcrumbs({
  breadcrumbs,
  displayRelativeTime,
  onSwitchTimeFormat,
  organization,
  searchTerm,
  event,
  relativeTime,
  emptyMessage,
}: Props) {
  const {projects, fetching: loadingProjects} = useProjects();

  const maybeProject = !loadingProjects
    ? projects.find(project => {
        return event && project.id === event.projectID;
      })
    : null;

  const listRef = useRef<List>(null);

  const sentryTransactionIds = useMemo(() => {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/useProjects.tsx" line="150">

---

## useProjects

The 'useProjects' function is used to fetch the projects from the ProjectsStore.

```tsx
function useProjects({limit, slugs, orgId: propOrgId}: Options = {}) {
  const api = useApi();

  const organization = useOrganization({allowNull: true});
  const store = useLegacyStore(ProjectsStore);

  const orgId = propOrgId ?? organization?.slug ?? organization?.slug;

  const storeSlugs = new Set(store.projects.map(t => t.slug));
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/breadcrumbs/breadcrumb/data/default.tsx" line="57">

---

## isEventId

The 'isEventId' function checks if a given string is an event id.

```tsx
export function isEventId(maybeEventId: string): boolean {
  // maybeEventId is an event id if it's a hex string of 32 characters long
  return /^[a-fA-F0-9]{32}$/.test(maybeEventId);
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/queryClient.tsx" line="121">

---

## useApiQuery

The 'useApiQuery' function wraps React Query's useQuery for consistent usage in the Sentry app.

```tsx
export function useApiQuery<TResponseData, TError = RequestError>(
  queryKey: ApiQueryKey,
  options: UseApiQueryOptions<TResponseData, TError>
): UseApiQueryResult<TResponseData, TError> {
  const api = useApi({persistInFlight: PERSIST_IN_FLIGHT});
  const queryFn = fetchDataQuery(api);

  const {data, ...rest} = useQuery(queryKey, queryFn, options);

  const queryResult = {
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
