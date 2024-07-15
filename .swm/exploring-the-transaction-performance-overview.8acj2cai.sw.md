---
title: Exploring the Transaction Performance Overview
---
The Transaction Overview in the Transaction Summary is a comprehensive view of a specific transaction in the Sentry application. It provides detailed information about the performance and errors of a particular transaction. This includes charts for visualizing transaction performance, a summary of key transaction attributes, and a list of related issues.

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionOverview/index.tsx" line="61">

---

The `TransactionOverview` function is the main component for the Transaction Overview. It uses various hooks and context providers to fetch and manage the data needed for the overview. It also defines several sub-components used in the overview.

```tsx
function TransactionOverview(props: Props) {
  const api = useApi();

  const {location, selection, organization, projects} = props;

  useEffect(() => {
    loadOrganizationTags(api, organization.slug, selection);
    addRoutePerformanceContext(selection);
    trackAnalytics('performance_views.transaction_summary.view', {
      organization,
    });
  }, [selection, organization, api]);

  return (
    <MEPSettingProvider>
      <PageLayout
        location={location}
        organization={organization}
        projects={projects}
        tab={Tab.TRANSACTION_SUMMARY}
        getDocumentTitle={getDocumentTitle}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionOverview/charts.tsx" line="83">

---

The `TransactionSummaryCharts` function is responsible for rendering the charts in the Transaction Overview. It handles changes in display mode and trend display, and uses the `useMEPSettingContext` and `useMetricsCardinalityContext` hooks to get additional data for the charts.

```tsx
function TransactionSummaryCharts({
  totalValue,
  eventView,
  organization,
  location,
  currentFilter,
  withoutZerofill,
  project,
}: Props) {
  function handleDisplayChange(value: string) {
    const display = decodeScalar(location.query.display, DisplayModes.DURATION);
    trackAnalytics('performance_views.transaction_summary.change_chart_display', {
      organization,
      from_chart: display,
      to_chart: value,
    });

    browserHistory.push({
      pathname: location.pathname,
      query: {
        ...removeHistogramQueryStrings(location, [ZOOM_START, ZOOM_END]),
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionOverview/content.tsx" line="90">

---

The `SummaryContent` function is a sub-component of the Transaction Overview that renders the main content of the overview. It handles search, tag URL generation, cell actions, transactions list sort change, and more. It also uses the `useMEPDataContext` hook to get additional data for the content.

```tsx
function SummaryContent({
  eventView,
  location,
  totalValues,
  spanOperationBreakdownFilter,
  organization,
  projects,
  isLoading,
  error,
  projectId,
  transactionName,
  onChangeFilter,
}: Props) {
  const routes = useRoutes();
  const mepDataContext = useMEPDataContext();

  function handleSearch(query: string) {
    const queryParams = normalizeDateTimeParams({
      ...(location.query || {}),
      query,
    });
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionOverview/latencyChart/content.tsx" line="46">

---

The `Content` function in the `latencyChart` directory is responsible for fetching and rendering a bar chart that shows event volume for each duration bucket. This graph visualizes how many transactions were recorded at each duration bucket, showing the modality of the transaction.

```tsx
function Content({
  organization,
  query,
  start,
  end,
  statsPeriod,
  environment,
  project,
  location,
  currentFilter,
  queryExtras,
  totalCount,
}: Props) {
  const [zoomError, setZoomError] = useState(false);

  function handleMouseOver() {
    // Hide the zoom error tooltip on the next hover.
    if (zoomError) {
      setZoomError(false);
    }
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionOverview/index.tsx" line="61">

---

# Transaction Overview Function

The `TransactionOverview` function is the main function for the Transaction Overview. It uses the `useApi` hook to get the API client, and the `loadOrganizationTags` and `addRoutePerformanceContext` functions to load the organization's tags and add performance context to the route respectively. It returns the `MEPSettingProvider` and `PageLayout` components, which are responsible for providing the settings and layout for the Transaction Overview.

```tsx
function TransactionOverview(props: Props) {
  const api = useApi();

  const {location, selection, organization, projects} = props;

  useEffect(() => {
    loadOrganizationTags(api, organization.slug, selection);
    addRoutePerformanceContext(selection);
    trackAnalytics('performance_views.transaction_summary.view', {
      organization,
    });
  }, [selection, organization, api]);

  return (
    <MEPSettingProvider>
      <PageLayout
        location={location}
        organization={organization}
        projects={projects}
        tab={Tab.TRANSACTION_SUMMARY}
        getDocumentTitle={getDocumentTitle}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionOverview/index.tsx" line="105">

---

# Transaction Name

The `transactionName` is a key property in the Transaction Overview. It is used to identify the specific transaction that the overview is about. It is used in the `getDocumentTitle` function to generate the document title, and in the `SummaryContent` component to display the transaction name.

```tsx
    transactionName,
    transactionThreshold,
    transactionThresholdMetric,
  } = props;

  const mepContext = useMEPDataContext();
  const mepSetting = useMEPSettingContext();
  const mepCardinalityContext = useMetricsCardinalityContext();
  const queryExtras = getTransactionMEPParamsIfApplicable(
    mepSetting,
    mepCardinalityContext,
    organization
  );

  const queryData = useDiscoverQuery({
    eventView: getTotalsEventView(organization, eventView),
    orgSlug: organization.slug,
    location,
    transactionThreshold,
    transactionThresholdMetric,
    referrer: 'api.performance.transaction-summary',
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionOverview/index.tsx" line="62">

---

# API Usage

The `api` constant is obtained from the `useApi` hook and is used to make API requests. It is used in the `loadOrganizationTags` function to load the organization's tags, and in the `useDiscoverQuery` hook to make a query to the Discover API.

```tsx
  const api = useApi();

  const {location, selection, organization, projects} = props;

  useEffect(() => {
    loadOrganizationTags(api, organization.slug, selection);
    addRoutePerformanceContext(selection);
    trackAnalytics('performance_views.transaction_summary.view', {
      organization,
    });
  }, [selection, organization, api]);

  return (
    <MEPSettingProvider>
      <PageLayout
        location={location}
        organization={organization}
        projects={projects}
        tab={Tab.TRANSACTION_SUMMARY}
        getDocumentTitle={getDocumentTitle}
        generateEventView={generateEventView}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionOverview/index.tsx" line="106">

---

# Transaction Threshold

The `transactionThreshold` is a property that represents the threshold for the transaction. It is used in the `useDiscoverQuery` hook to make a query to the Discover API with the specified threshold.

```tsx
    transactionThreshold,
    transactionThresholdMetric,
  } = props;

  const mepContext = useMEPDataContext();
  const mepSetting = useMEPSettingContext();
  const mepCardinalityContext = useMetricsCardinalityContext();
  const queryExtras = getTransactionMEPParamsIfApplicable(
    mepSetting,
    mepCardinalityContext,
    organization
  );

  const queryData = useDiscoverQuery({
    eventView: getTotalsEventView(organization, eventView),
    orgSlug: organization.slug,
    location,
    transactionThreshold,
    transactionThresholdMetric,
    referrer: 'api.performance.transaction-summary',
    queryExtras,
```

---

</SwmSnippet>

# Transaction Overview Functions

Let's delve into the key functions that power the Transaction Overview feature in the Sentry application.

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionOverview/index.tsx" line="61">

---

## TransactionOverview Function

The `TransactionOverview` function is the main function that renders the Transaction Overview page. It uses the `useApi` hook to get an API client, and it also uses the `useEffect` hook to load organization tags and add route performance context when the component mounts or updates. The function returns a `PageLayout` component that displays the transaction summary.

```tsx
function TransactionOverview(props: Props) {
  const api = useApi();

  const {location, selection, organization, projects} = props;

  useEffect(() => {
    loadOrganizationTags(api, organization.slug, selection);
    addRoutePerformanceContext(selection);
    trackAnalytics('performance_views.transaction_summary.view', {
      organization,
    });
  }, [selection, organization, api]);

  return (
    <MEPSettingProvider>
      <PageLayout
        location={location}
        organization={organization}
        projects={projects}
        tab={Tab.TRANSACTION_SUMMARY}
        getDocumentTitle={getDocumentTitle}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/useApi.tsx" line="28">

---

## useApi Function

The `useApi` function is a custom hook that returns an API client. This client is used to make requests to the backend. The function takes an options object as a parameter, which can be used to provide a pre-existing API client and to control whether requests should be persisted after the component unmounts.

```tsx
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

  useEffect(() => clearOnUnmount, [clearOnUnmount]);

  return api;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/actionCreators/tags.tsx" line="31">

---

## loadOrganizationTags Function

The `loadOrganizationTags` function is used to load an organization's tags based on a global selection value. It makes a GET request to the `/organizations/${orgSlug}/tags/` endpoint to fetch the tags. The function also resets the `TagStore` before making the request.

```tsx
export function loadOrganizationTags(
  api: Client,
  orgSlug: string,
  selection: PageFilters
): Promise<void> {
  TagStore.reset();

  const query: Query = selection.datetime
    ? {...normalizeDateTimeParams(selection.datetime)}
    : {};
  query.use_cache = '1';

  if (selection.projects) {
    query.project = selection.projects.map(String);
  }

  return api
    .requestPromise(`/organizations/${orgSlug}/tags/`, {
      method: 'GET',
      query,
    })
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/utils/index.tsx" line="292">

---

## addRoutePerformanceContext Function

The `addRoutePerformanceContext` function is used to add performance context to the current route. It calculates the period in seconds based on the provided selection and sets it as an attribute on the current transaction. It also groups the period into one of several predefined ranges and sets it as another attribute on the transaction.

```tsx
export function addRoutePerformanceContext(selection: PageFilters) {
  const transaction = getCurrentSentryReactRootSpan();
  const days = statsPeriodToDays(
    selection.datetime.period,
    selection.datetime.start,
    selection.datetime.end
  );
  const oneDay = 86400;
  const seconds = Math.floor(days * oneDay);

  transaction?.setAttribute('query.period', seconds.toString());
  let groupedPeriod = '>30d';
  if (seconds <= oneDay) {
    groupedPeriod = '<=1d';
  } else if (seconds <= oneDay * 7) {
    groupedPeriod = '<=7d';
  } else if (seconds <= oneDay * 14) {
    groupedPeriod = '<=14d';
  } else if (seconds <= oneDay * 30) {
    groupedPeriod = '<=30d';
  }
```

---

</SwmSnippet>

# Transaction Overview Endpoints

Transaction Overview Endpoints

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionOverview/durationPercentileChart/content.tsx" line="74">

---

## /organizations/{organization.slug}/events/ Endpoint

This endpoint is used to fetch and render a bar chart that shows event volume for each duration bucket. The data fetched from this endpoint is used to visualize how many transactions were recorded at each duration bucket, showing the modality of the transaction.

```tsx
    [`/organizations/${organization.slug}/events/`, {query: apiPayload}],
    {
      staleTime: 0,
    }
  );
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionOverview/trendChart/index.tsx" line="79">

---

## /organizations/{organization.slug}/events-stats/ Endpoint

This endpoint is used to fetch and render an area chart that shows user misery over a period. The data fetched from this endpoint is used to visualize the user misery, which is a measure of the number of unique users who have experienced an error over the number of unique users in a given time period.

```tsx
    const unselected = Object.keys(selected).filter(key => !selected[key]);

    const to = {
      ...location,
      query: {
        ...location.query,
        unselectedSeries: unselected,
      },
    };
    browserHistory.push(to);
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
