---
title: Understanding Insights Queues
---
Queues in the Insights module of Sentry are used to manage and monitor the flow of data processing tasks. They provide a way to handle tasks asynchronously, improving the performance and responsiveness of the application. The queues are used to track metrics such as the average time a task spends in the queue, the average processing time, error rates, and the number of tasks published and processed.

The Queues in Insights are represented in various components, views, and queries. The components include tables and charts that display the metrics related to the queues. The views provide different perspectives of the queue data, such as a summary view and a landing page view. The queries are used to fetch the data related to the queues from the backend.

The Queues also have utility functions and settings that help in managing the queues. These include functions for decoding query parameters and settings for default query filters. There are also referrers that are used to track where the requests are coming from.

<SwmSnippet path="/static/app/views/insights/queues/components/tables/queuesTable.tsx" line="108">

---

# QueuesTable Component

The QueuesTable component is used to display the queue data in a table format. It uses the useQueuesByDestinationQuery hook to fetch the data and the useLocation and useOrganization hooks to get the current location and organization context.

```tsx
export function QueuesTable({error, destination, sort}: Props) {
  const location = useLocation();
  const organization = useOrganization();

  const {data, isLoading, meta, pageLinks} = useQueuesByDestinationQuery({
    destination,
    sort,
    referrer: Referrer.QUEUES_LANDING_DESTINATIONS_TABLE,
  });

  const handleCursor: CursorHandler = (newCursor, pathname, query) => {
    browserHistory.push({
      pathname,
      query: {...query, [QueryParameterNames.DESTINATIONS_CURSOR]: newCursor},
    });
  };

  return (
    <Fragment>
      <GridEditable
        aria-label={t('Queues')}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/queues/queries/useQueuesByDestinationQuery.tsx" line="23">

---

# useQueuesByDestinationQuery Hook

The useQueuesByDestinationQuery hook is used to fetch the queue data based on the destination. It uses the useSpanMetrics function to get the metrics data and the useLocation hook to get the current location context.

```tsx
  sort,
  referrer,
}: Props) {
  const location = useLocation();
  const cursor = decodeScalar(location.query?.[QueryParameterNames.DESTINATIONS_CURSOR]);

  const mutableSearch = new MutableSearch(DEFAULT_QUERY_FILTER);
  if (destination) {
    mutableSearch.addFilterValue('messaging.destination.name', destination, false);
  }
  const response = useSpanMetrics(
    {
      search: mutableSearch,
      fields: [
        'messaging.destination.name',
        'count()',
        'count_op(queue.publish)',
        'count_op(queue.process)',
        'sum(span.duration)',
        'avg(span.duration)',
        'avg_if(span.duration,span.op,queue.publish)',
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/queues/queries/useQueuesByTransactionQuery.tsx" line="23">

---

# useQueuesByTransactionQuery Hook

The useQueuesByTransactionQuery hook is used to fetch the queue data based on the transaction. It uses the useSpanMetrics function to get the metrics data and the useLocation hook to get the current location context.

```tsx
  sort,
  referrer,
}: Props) {
  const location = useLocation();
  const cursor = decodeScalar(location.query?.[QueryParameterNames.TRANSACTIONS_CURSOR]);

  const mutableSearch = new MutableSearch(DEFAULT_QUERY_FILTER);
  if (destination) {
    mutableSearch.addFilterValue('messaging.destination.name', destination);
  }
  const response = useSpanMetrics(
    {
      search: mutableSearch,
      fields: [
        'transaction',
        'span.op',
        'count()',
        'count_op(queue.publish)',
        'count_op(queue.process)',
        'sum(span.duration)',
        'avg(span.duration)',
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/queues/queries/useProcessQueuesTimeSeriesQuery.tsx" line="18">

---

# useProcessQueuesTimeSeriesQuery Hook

The useProcessQueuesTimeSeriesQuery hook is used to fetch the time series data for the process queues. It uses the useSpanMetricsSeries function to get the series data.

```tsx
export function useProcessQueuesTimeSeriesQuery({enabled, destination, referrer}: Props) {
  const search = new MutableSearch('span.op:queue.process');
  if (destination) {
    search.addFilterValue('messaging.destination.name', destination, false);
  }

  return useSpanMetricsSeries(
    {
      yAxis,
      search,
      enabled,
    },
    referrer
  );
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/queues/queries/useQueuesMetricsQuery.tsx" line="23">

---

# useQueuesMetricsQuery Hook

The useQueuesMetricsQuery hook is used to fetch the metrics data for the queues. It uses the useSpanMetrics function to get the metrics data.

```tsx
  if (transaction) {
    mutableSearch.addFilterValue('transaction', transaction);
  }
  const response = useSpanMetrics(
    {
      search: mutableSearch,
      fields: [
        'count()',
        'count_op(queue.publish)',
        'count_op(queue.process)',
        'sum(span.duration)',
        'avg(span.duration)',
        'avg_if(span.duration,span.op,queue.publish)',
        'avg_if(span.duration,span.op,queue.process)',
        'avg(messaging.message.receive.latency)',
        'trace_status_rate(ok)',
        'time_spent_percentage(app,span.duration)',
      ],
      enabled,
      sorts: [],
      limit: 10,
```

---

</SwmSnippet>

# Queue Functions

This section will explain the main functions related to queues in the Sentry application.

<SwmSnippet path="/static/app/views/insights/queues/components/tables/queuesTable.tsx" line="108">

---

## QueuesTable

The `QueuesTable` function is a component that displays the metrics related to the queues in a table format. It uses various hooks and queries to fetch and display the data.

```tsx
export function QueuesTable({error, destination, sort}: Props) {
  const location = useLocation();
  const organization = useOrganization();

  const {data, isLoading, meta, pageLinks} = useQueuesByDestinationQuery({
    destination,
    sort,
    referrer: Referrer.QUEUES_LANDING_DESTINATIONS_TABLE,
  });

  const handleCursor: CursorHandler = (newCursor, pathname, query) => {
    browserHistory.push({
      pathname,
      query: {...query, [QueryParameterNames.DESTINATIONS_CURSOR]: newCursor},
    });
  };

  return (
    <Fragment>
      <GridEditable
        aria-label={t('Queues')}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/queues/queries/useQueuesByDestinationQuery.tsx" line="20">

---

## useQueuesByDestinationQuery

The `useQueuesByDestinationQuery` function is a hook that fetches the queue metrics for a specific destination. It uses the `useSpanMetrics` hook to fetch the data.

```tsx
export function useQueuesByDestinationQuery({
  enabled,
  destination,
  sort,
  referrer,
}: Props) {
  const location = useLocation();
  const cursor = decodeScalar(location.query?.[QueryParameterNames.DESTINATIONS_CURSOR]);

  const mutableSearch = new MutableSearch(DEFAULT_QUERY_FILTER);
  if (destination) {
    mutableSearch.addFilterValue('messaging.destination.name', destination, false);
  }
  const response = useSpanMetrics(
    {
      search: mutableSearch,
      fields: [
        'messaging.destination.name',
        'count()',
        'count_op(queue.publish)',
        'count_op(queue.process)',
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/queues/queries/useQueuesMetricsQuery.tsx" line="18">

---

## useQueuesMetricsQuery

The `useQueuesMetricsQuery` function is a hook that fetches the queue metrics. It uses the `useSpanMetricsSeries` hook to fetch the data.

```tsx
}: Props) {
  const mutableSearch = new MutableSearch(DEFAULT_QUERY_FILTER);
  if (destination) {
    mutableSearch.addFilterValue('messaging.destination.name', destination);
  }
  if (transaction) {
    mutableSearch.addFilterValue('transaction', transaction);
  }
  const response = useSpanMetrics(
    {
      search: mutableSearch,
      fields: [
        'count()',
        'count_op(queue.publish)',
        'count_op(queue.process)',
        'sum(span.duration)',
        'avg(span.duration)',
        'avg_if(span.duration,span.op,queue.publish)',
        'avg_if(span.duration,span.op,queue.process)',
        'avg(messaging.message.receive.latency)',
        'trace_status_rate(ok)',
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/queues/queries/useQueuesByTransactionQuery.tsx" line="20">

---

## useQueuesByTransactionQuery

The `useQueuesByTransactionQuery` function is a hook that fetches the queue metrics for a specific transaction. It uses the `useSpanMetrics` hook to fetch the data.

```tsx
export function useQueuesByTransactionQuery({
  destination,
  enabled,
  sort,
  referrer,
}: Props) {
  const location = useLocation();
  const cursor = decodeScalar(location.query?.[QueryParameterNames.TRANSACTIONS_CURSOR]);

  const mutableSearch = new MutableSearch(DEFAULT_QUERY_FILTER);
  if (destination) {
    mutableSearch.addFilterValue('messaging.destination.name', destination);
  }
  const response = useSpanMetrics(
    {
      search: mutableSearch,
      fields: [
        'transaction',
        'span.op',
        'count()',
        'count_op(queue.publish)',
```

---

</SwmSnippet>

# Queue Endpoints

Understanding Queue Endpoints

<SwmSnippet path="/static/app/views/insights/queues/referrers.ts" line="2">

---

## api.performance.queues.landing-onboarding

This endpoint is used to fetch data for the onboarding landing page of the Queues in the Insights module. It provides an overview of the performance of the queues.

```typescript
  QUEUES_LANDING_ONBOARDING = 'api.performance.queues.landing-onboarding',
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/queues/referrers.ts" line="7">

---

## api.performance.queues.summary

This endpoint is used to fetch a summary of the performance of the queues. It provides a high-level overview of the queue performance metrics.

```typescript
  QUEUES_SUMMARY = 'api.performance.queues.summary',
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
