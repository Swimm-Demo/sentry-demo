---
title: What is Issue List Overview
---
The Issue List in Sentry's demo application is a crucial component that provides an overview of all the issues reported in the system. It is primarily implemented in the 'overview.tsx' file within the 'issueList' directory. This component is responsible for displaying the issues in a paginated list, with each issue represented by a row in the list.

The Issue List also provides various actions that can be performed on the issues. These actions are defined in the 'actions' directory within the 'issueList' directory. Actions include resolving issues, reviewing issues, and sorting options. The actions are triggered by user interactions and can modify the state of the issues in the list.

The 'IssueListContainer' component in 'index.tsx' serves as the container for the Issue List. It includes components for handling scenarios where there are no projects or issues to display. It also sets up the page title and analytics hooks.

The 'utils' directory within the 'issueList' directory contains utility functions and hooks that are used across the Issue List component. These utilities include parsing issue priority search and handling selected saved searches.

The 'queries' directory within the 'issueList' directory contains hooks for fetching saved searches for the organization. These hooks are used to retrieve and manage the saved searches that are displayed in the Issue List.

<SwmSnippet path="/static/app/views/issueList/overview.tsx" line="84">

---

# Issue List Overview

This file contains the main implementation of the Issue List. It defines the layout of the list, the data to be displayed for each issue, and the actions that can be performed on the issues. It also handles the state of the list, including loading states and pagination.

```tsx
const MAX_ITEMS = 25;
// the default period for the graph in each issue row
const DEFAULT_GRAPH_STATS_PERIOD = '24h';
// the allowed period choices for graph in each issue row
const DYNAMIC_COUNTS_STATS_PERIODS = new Set(['14d', '24h', 'auto']);
const MAX_ISSUES_COUNT = 100;

type Params = {
  orgId: string;
};

type Props = {
  api: Client;
  location: Location;
  organization: Organization;
  params: Params;
  savedSearch: SavedSearch;
  savedSearchLoading: boolean;
  savedSearches: SavedSearch[];
  selectedSearchId: string;
  selection: PageFilters;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/issueList/actions/index.tsx" line="179">

---

# Issue List Actions

This file defines the actions that can be performed on the issues in the list. These actions include resolving issues, reviewing issues, and sorting options. The actions are triggered by user interactions and can modify the state of the issues in the list.

```tsx
}: IssueListActionsProps) {
  const api = useApi();
  const queryClient = useQueryClient();
  const organization = useOrganization();
  const {
    pageSelected,
    multiSelected,
    anySelected,
    allInQuerySelected,
    selectedIdsSet,
    selectedProjectSlug,
    setAllInQuerySelected,
  } = useSelectedGroupsState();
  const [isSavedSearchesOpen] = useSyncedLocalStorageState(
    SAVED_SEARCHES_SIDEBAR_OPEN_LOCALSTORAGE_KEY,
    false
  );

  const disableActions = useMedia(
    `(max-width: ${
      isSavedSearchesOpen ? theme.breakpoints.xlarge : theme.breakpoints.medium
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/issueList/index.tsx" line="1">

---

# Issue List Container

This file defines the 'IssueListContainer' component, which serves as the container for the Issue List. It includes components for handling scenarios where there are no projects or issues to display. It also sets up the page title and analytics hooks.

```tsx
import NoProjectMessage from 'sentry/components/noProjectMessage';
import PageFiltersContainer from 'sentry/components/organizations/pageFilters/container';
import SentryDocumentTitle from 'sentry/components/sentryDocumentTitle';
import {t} from 'sentry/locale';
import useRouteAnalyticsHookSetup from 'sentry/utils/routeAnalytics/useRouteAnalyticsHookSetup';
import useOrganization from 'sentry/utils/useOrganization';

type Props = {
  children: React.ReactNode;
};

function IssueListContainer({children}: Props) {
  const organization = useOrganization();
  useRouteAnalyticsHookSetup();

  return (
    <SentryDocumentTitle title={t('Issues')} orgSlug={organization.slug}>
      <PageFiltersContainer>
        <NoProjectMessage organization={organization}>{children}</NoProjectMessage>
      </PageFiltersContainer>
    </SentryDocumentTitle>
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/issueList/utils/useSelectedSavedSearch.tsx" line="17">

---

# Issue List Utilities

This file is part of the 'utils' directory within the 'issueList' directory, which contains utility functions and hooks that are used across the Issue List component. These utilities include parsing issue priority search and handling selected saved searches.

```tsx
  const params = useParams();

  const {data: savedSearches} = useFetchSavedSearchesForOrg(
    {orgSlug: organization.slug},
    {notifyOnChangeProps: ['data']}
  );

  const selectedSearchId: string | undefined = params.searchId;

  // If there's no direct saved search being requested (via URL route)
  // *AND* there's no query in URL, then check if there is pinned search
  const selectedSavedSearch =
    !selectedSearchId &&
    (location.query.query === null || location.query.query === undefined)
      ? savedSearches?.find(search => search.isPinned)
      : savedSearches?.find(({id}) => id === selectedSearchId);

  return useMemo(
    () =>
      selectedSavedSearch?.isPinned
        ? {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/issueList/queries/useFetchSavedSearchesForOrg.tsx" line="1">

---

# Issue List Queries

This file is part of the 'queries' directory within the 'issueList' directory, which contains hooks for fetching saved searches for the organization. These hooks are used to retrieve and manage the saved searches that are displayed in the Issue List.

```tsx
import type {SavedSearch} from 'sentry/types/group';
import type {UseApiQueryOptions} from 'sentry/utils/queryClient';
import {useApiQuery} from 'sentry/utils/queryClient';

type FetchSavedSearchesForOrgParameters = {
  orgSlug: string;
};

type FetchSavedSearchesForOrgResponse = SavedSearch[];

export const makeFetchSavedSearchesForOrgQueryKey = ({
  orgSlug,
}: FetchSavedSearchesForOrgParameters) =>
  [`/organizations/${orgSlug}/searches/`] as const;

export const useFetchSavedSearchesForOrg = (
  {orgSlug}: FetchSavedSearchesForOrgParameters,
  options: Partial<UseApiQueryOptions<FetchSavedSearchesForOrgResponse>> = {}
) => {
  return useApiQuery<FetchSavedSearchesForOrgResponse>(
    makeFetchSavedSearchesForOrgQueryKey({orgSlug}),
```

---

</SwmSnippet>

# Issue List Functions

This section will explain the main functions of the Issue List in the Sentry demo application.

<SwmSnippet path="/static/app/views/issueList/overview.tsx" line="156">

---

## IssueListOverview

The `IssueListOverview` class is the main component for the Issue List. It maintains the state of the Issue List, including the list of issues, the selected issues, and the current page links. It also handles the lifecycle methods for the component, such as `componentDidMount` and `componentDidUpdate`, to fetch the necessary data.

```tsx
class IssueListOverview extends Component<Props, State> {
  state: State = this.getInitialState();

  getInitialState() {
    const realtimeActiveCookie = Cookies.get('realtimeActive');
    const realtimeActive =
      typeof realtimeActiveCookie === 'undefined'
        ? false
        : realtimeActiveCookie === 'true';

    return {
      groupIds: [],
      actionTaken: false,
      selectAllActive: false,
      realtimeActive,
      pageLinks: '',
      queryCount: 0,
      queryCounts: {},
      queryMaxCount: 0,
      error: null,
      issuesLoading: true,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/issueList/actions/index.tsx" line="166">

---

## IssueListActions

The `IssueListActions` function defines the actions that can be performed on the issues in the Issue List. These actions include deleting, merging, and updating issues. The actions are triggered by user interactions and can modify the state of the issues in the list.

```tsx
function IssueListActions({
  allResultsVisible,
  displayReprocessingActions,
  groupIds,
  onActionTaken,
  onDelete,
  onSelectStatsPeriod,
  onSortChange,
  queryCount,
  query,
  selection,
  sort,
  statsPeriod,
}: IssueListActionsProps) {
  const api = useApi();
  const queryClient = useQueryClient();
  const organization = useOrganization();
  const {
    pageSelected,
    multiSelected,
    anySelected,
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
