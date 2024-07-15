---
title: Overview of HTTP Monitoring in Insights
---
HTTP in the Insights module of the Sentry application refers to the tracking and monitoring of HTTP requests and responses. It provides a detailed view of the HTTP traffic, including the status codes, response times, and other related metrics.

The HTTP module is organized into several subdirectories, each serving a specific purpose. The 'data' directory contains definitions related to HTTP data, the 'utils' directory includes utility functions and hooks, and the 'views' directory holds the React components for the user interface.

The 'httpSamplesPanel.tsx' file in the 'components' directory is a key part of the HTTP module. It defines a React component that displays a panel of HTTP samples. This panel provides a detailed view of individual HTTP requests, including their status codes, durations, and other related metrics.

The 'httpLandingPage.tsx' file in the 'views' directory defines the landing page of the HTTP module. It uses the 'chartFilters' and 'tableFilters' constants to filter the HTTP data displayed on the page. The 'domainsListResponse' constant is used to fetch the list of domains for the HTTP data.

The 'httpDomainSummaryPage.tsx' file in the 'views' directory defines a page that provides a summary of the HTTP data for a specific domain. The 'Query' type defined in this file represents the query parameters for fetching the domain summary.

<SwmSnippet path="/static/app/views/insights/http/views/httpLandingPage.tsx" line="48">

---

# HTTP Landing Page

The HTTP Landing Page is the main entry point to the HTTP module. It uses several hooks and constants to fetch and display HTTP data. The `useLocationQuery` hook is used to parse the query parameters from the URL, and the `useSpanMetrics` hook is used to fetch the HTTP data.

```tsx
export function HTTPLandingPage() {
  const organization = useOrganization();
  const location = useLocation();
  const onboardingProject = useOnboardingProject();

  const sortField = decodeScalar(location.query?.[QueryParameterNames.DOMAINS_SORT]);

  // TODO: Pull this using `useLocationQuery` below
  const sort = decodeSorts(sortField).filter(isAValidSort).at(0) ?? DEFAULT_SORT;

  const query = useLocationQuery({
    fields: {
      'span.domain': decodeScalar,
    },
  });

  const chartFilters = {
    ...BASE_FILTERS,
  };

  const tableFilters = {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/http/components/httpSamplesPanel.tsx" line="70">

---

# HTTP Samples Panel

The HTTP Samples Panel is a component that displays a panel of HTTP samples. It uses the `useLocationQuery` hook to parse the query parameters from the URL, and the `useDebouncedState` hook to manage the state of the highlighted span ID.

```tsx
export function HTTPSamplesPanel() {
  const router = useRouter();
  const location = useLocation();

  const query = useLocationQuery({
    fields: {
      project: decodeScalar,
      domain: decodeScalar,
      transaction: decodeScalar,
      transactionMethod: decodeScalar,
      panel: decodePanel,
      responseCodeClass: decodeResponseCodeClass,
      spanSearchQuery: decodeScalar,
    },
  });

  const organization = useOrganization();

  const {projects} = useProjects();
  const {selection} = usePageFilters();
  const supportedTags = useSpanFieldSupportedTags();
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/http/views/httpLandingPage.tsx" line="91">

---

# HTTP Data Fetching

The HTTP data is fetched using the `useSpanMetricsSeries` hook. This hook takes a configuration object that specifies the search query, the fields to fetch, and the referrer. The data is then stored in the `throughputData`, `durationData`, and `responseCodeData` constants.

```tsx
  const {
    isLoading: isThroughputDataLoading,
    data: throughputData,
    error: throughputError,
  } = useSpanMetricsSeries(
    {
      search: MutableSearch.fromQueryObject(chartFilters),
      yAxis: ['spm()'],
    },
    Referrer.LANDING_THROUGHPUT_CHART
  );

  const {
    isLoading: isDurationDataLoading,
    data: durationData,
    error: durationError,
  } = useSpanMetricsSeries(
    {
      search: MutableSearch.fromQueryObject(chartFilters),
      yAxis: [`avg(span.self_time)`],
    },
```

---

</SwmSnippet>

# HTTP Endpoints

Understanding HTTP Endpoints in Sentry

<SwmSnippet path="/static/app/views/insights/http/referrers.tsx" line="2">

---

## api.performance.http.landing-domains

The 'api.performance.http.landing-domains' endpoint is used to fetch the landing domains related to the performance of the HTTP requests.

```tsx
  LANDING_DOMAINS = 'api.performance.http.landing-domains',
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/http/referrers.tsx" line="3">

---

## api.performance.http.landing-domains-list

The 'api.performance.http.landing-domains-list' endpoint is used to fetch a list of landing domains related to the performance of the HTTP requests.

```tsx
  LANDING_DOMAINS_LIST = 'api.performance.http.landing-domains-list',
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
