---
title: Getting started with Data Queries
---
Queries in the Sentry-Demo project are used to fetch and manipulate data. They are used in various parts of the application to interact with the backend services and retrieve the necessary data. The queries are constructed using different parameters and options, which are then passed to the API request functions.

The queries are used in different contexts, for example, to fetch span metrics, releases, or event details. They are defined in functions like `useSpansIndexed`, `useSpanMetrics`, `useMetrics`, and `useDiscover` in the `useDiscover.ts` file. These functions use the `useDiscover` function to construct and execute the queries.

The `useDiscover` function takes in options, dataset, and referrer as parameters. It constructs an `eventView` object using the provided options and dataset, and then uses this `eventView` to make an API request using the `useWrappedDiscoverQuery` function.

The `queryFn` function in `useReleases.tsx` is another example of a query. It makes a GET request to the API using the `api.requestPromise` function. The `queryKey` is used as the path for the API request, and the query parameters are passed in the `query` option.

The `queryString` constant in `useSpanSamples.tsx` is an example of a query string that is used in an API request. It is constructed using the `query.formatString()` function and then passed as a parameter to the `useQuery` function, which makes the actual API request.

<SwmSnippet path="/static/app/views/insights/common/queries/useDiscover.ts" line="60">

---

# useDiscover Function

The `useDiscover` function is used to construct and execute a query. It takes in options, dataset, and referrer as parameters. It constructs an `eventView` object using the provided options and dataset, and then uses this `eventView` to make an API request using the `useWrappedDiscoverQuery` function.

```typescript
const useDiscover = <T extends Extract<keyof ResponseType, string>[], ResponseType>(
  options: UseMetricsOptions<T> = {},
  dataset: DiscoverDatasets,
  referrer: string
) => {
  const {
    fields = [],
    search = undefined,
    sorts = [],
    limit,
    cursor,
    pageFilters: pageFiltersFromOptions,
  } = options;

  const pageFilters = usePageFilters();

  const eventView = getEventView(
    search,
    fields,
    sorts,
    pageFiltersFromOptions ?? pageFilters.selection,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/common/queries/useDiscover.ts" line="27">

---

# useSpansIndexed Function

The `useSpansIndexed` function is an example of a query function. It uses the `useDiscover` function to construct and execute a query.

```typescript
export const useSpansIndexed = <Fields extends SpanIndexedField[]>(
  options: UseMetricsOptions<Fields> = {},
  referrer: string
) => {
  return useDiscover<Fields, SpanIndexedResponse>(
    options,
    DiscoverDatasets.SPANS_INDEXED,
    referrer
  );
};
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/common/queries/useReleases.tsx" line="66">

---

# queryFn Function

The `queryFn` function in `useReleases.tsx` is another example of a query. It makes a GET request to the API using the `api.requestPromise` function. The `queryKey` is used as the path for the API request, and the query parameters are passed in the `query` option.

```tsx
        queryFn: () =>
          api.requestPromise(queryKey[0], {
            method: 'GET',
            query: queryKey[1]?.query,
          }) as Promise<TableData>,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/common/queries/useSpanSamples.tsx" line="92">

---

# queryString Constant

The `queryString` constant in `useSpanSamples.tsx` is an example of a query string that is used in an API request. It is constructed using the `query.formatString()` function and then passed as a parameter to the `useQuery` function, which makes the actual API request.

```tsx
    groupId && transactionName && !isLoadingSeries && pageFilter.isReady
  );

  const queryString = query.formatString();

  const result = useQuery<SpanSample[]>({
    queryKey: [
      'span-samples',
      groupId,
      transactionName,
      dateCondtions.statsPeriod,
      dateCondtions.start,
      dateCondtions.end,
      queryString,
      additionalFields?.join(','),
    ],
    queryFn: async () => {
      const {data} = await api.requestPromise(
        `${url}?${qs.stringify({
          ...dateCondtions,
          ...{utc: location.query.utc},
```

---

</SwmSnippet>

# Query Functions Overview

This section provides an overview of the main query functions in the Sentry-Demo project.

<SwmSnippet path="/static/app/views/insights/common/queries/useSpansQuery.tsx" line="33">

---

## useSpansQuery

The `useSpansQuery` function is used to fetch span metrics. It takes an `eventView` object as a parameter, which contains the details of the event to be fetched. The function uses the `useWrappedDiscoverTimeseriesQuery` or `useWrappedDiscoverQuery` function to make the actual API request, depending on whether the query is a timeseries query or not.

```tsx
  limit?: number;
  referrer?: string;
}) {
  const isTimeseriesQuery = (eventView?.yAxis?.length ?? 0) > 0;
  const queryFunction = isTimeseriesQuery
    ? useWrappedDiscoverTimeseriesQuery
    : useWrappedDiscoverQuery;

  const {isReady: pageFiltersReady} = usePageFilters();

  if (eventView) {
    const newEventView = eventView.clone();
    const response = queryFunction<T>({
      eventView: newEventView,
      initialData,
      limit,
      // We always want to wait until the pageFilters are ready to prevent clobbering requests
      enabled: (enabled || enabled === undefined) && pageFiltersReady,
      referrer,
      cursor,
    });
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/common/queries/useSpanSamples.tsx" line="34">

---

## useSpanSamples

The `useSpanSamples` function is used to fetch span samples. It constructs a query string using the `query.formatString()` function and then uses the `useQuery` function to make the API request. The response from the API is then processed and returned.

```tsx
  | SpanIndexedField.TRANSACTION_ID
  | SpanIndexedField.PROJECT
  | SpanIndexedField.TIMESTAMP
  | SpanIndexedField.ID
  | SpanIndexedField.PROFILE_ID
  | SpanIndexedField.HTTP_RESPONSE_CONTENT_LENGTH
  | SpanIndexedField.TRACE
>;

export const useSpanSamples = (options: Options) => {
  const organization = useOrganization();
  const url = `/api/0/organizations/${organization.slug}/spans-samples/`;
  const api = useApi();
  const pageFilter = usePageFilters();
  const {
    groupId,
    transactionName,
    transactionMethod,
    release,
    spanSearch,
    additionalFields,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/common/queries/useReleases.tsx" line="42">

---

## useReleases

The `useReleases` function is used to fetch release metrics. It constructs a new query using the `EventView.fromNewQueryWithPageFilters` function and then uses the `useDiscoverQuery` function to make the API request. The response from the API is then processed and returned.

```tsx
  const releaseMetrics = useQueries({
    queries: chunks.map(releases => {
      const newQuery: NewQuery = {
        name: '',
        fields: ['release', 'count()'],
        query: `transaction.op:ui.load ${escapeFilterValue(
          `release:[${releases.map(r => `"${r.version}"`).join()}]`
        )}`,
        dataset: DiscoverDatasets.METRICS,
        version: 2,
        projects: selection.projects,
      };
      const eventView = EventView.fromNewQueryWithPageFilters(newQuery, selection);
      const queryKey = [
        `/organizations/${organization.slug}/events/`,
        {
          query: {
            ...eventView.getEventsAPIPayload(location),
            referrer: 'api.starfish.mobile-release-selector',
          },
        },
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/common/queries/useDiscover.ts" line="34">

---

## useDiscover

The `useDiscover` function is used to fetch event details. It constructs an `eventView` object using the provided options and dataset, and then uses this `eventView` to make an API request using the `useWrappedDiscoverQuery` function. The response from the API is then processed and returned.

```typescript
    referrer
  );
};

export const useSpanMetrics = <Fields extends SpanMetricsProperty[]>(
  options: UseMetricsOptions<Fields> = {},
  referrer: string
) => {
  return useDiscover<Fields, SpanMetricsResponse>(
    options,
    DiscoverDatasets.SPANS_METRICS,
    referrer
  );
};

export const useMetrics = <Fields extends MetricsProperty[]>(
  options: UseMetricsOptions<Fields> = {},
  referrer: string
) => {
  return useDiscover<Fields, MetricsResponse>(
    options,
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
