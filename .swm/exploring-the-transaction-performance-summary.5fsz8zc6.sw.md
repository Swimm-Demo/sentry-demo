---
title: Exploring the Transaction Performance Summary
---
The Transaction Summary in the Performance section of the Sentry application provides a comprehensive overview of a specific transaction. It includes various charts and tables that display detailed performance metrics related to the transaction. These metrics include duration percentiles, event metrics, vital statistics, latency details, and more. The summary also includes a breakdown of transaction events, replays, spans, profiles, tags, and vitals, each providing specific insights into the transaction's performance. For instance, the transaction events view provides a list of all events related to the transaction, while the transaction spans view provides a detailed breakdown of the transaction's spans.

The Transaction Summary also includes a feature for detecting anomalies in transaction data. This feature uses statistical methods to identify unusual patterns in the transaction data that may indicate performance issues. The anomalies are presented in a dedicated chart and table, providing a visual representation of the detected anomalies and their details.

Furthermore, the Transaction Summary provides utilities for generating views and handling transaction thresholds. These utilities are used to customize the presentation of transaction data according to the user's preferences and to manage the performance thresholds that trigger alerts.

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionOverview/charts.tsx" line="83">

---

# Transaction Summary Charts

The `TransactionSummaryCharts` function is responsible for rendering the charts in the Transaction Summary. It uses various helper functions and components to generate the charts and handle user interactions such as changing the display mode or the trend function.

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

<SwmSnippet path="/static/app/views/performance/transactionSummary/tabs.tsx" line="1">

---

# Transaction Summary Tabs

The `Tab` enum defines the different tabs available in the Transaction Summary. Each tab corresponds to a different view in the Transaction Summary.

```tsx
enum Tab {
  TRANSACTION_SUMMARY = 'summary',
  WEB_VITALS = 'vitals',
  TAGS = 'tags',
  EVENTS = 'events',
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/utils.tsx" line="89">

---

# Transaction Summary Route

The `transactionSummaryRouteWithQuery` function is used to generate the route for the Transaction Summary with the appropriate query parameters.

```tsx
  trendFunction?: string;
  unselectedSeries?: string | string[];
}) {
  const pathname = generateTransactionSummaryRoute({
    orgSlug,
    subPath,
  });

  let searchFilter: typeof query.query;
  if (typeof query.query === 'string') {
    searchFilter = normalizeSearchConditions(query.query).formatString();
  } else {
    searchFilter = query.query;
  }

  return {
    pathname,
    query: {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionOverview/charts.tsx" line="174">

---

# Transaction Summary Cleanup Flag

The `hasTransactionSummaryCleanupFlag` constant is used to determine if the 'performance-transaction-summary-cleanup' feature is enabled. This feature affects the display options available in the Transaction Summary.

```tsx
    organization
  );

  const hasTransactionSummaryCleanupFlag = organization.features.includes(
    'performance-transaction-summary-cleanup'
  );

  const displayOptions = generateDisplayOptions(currentFilter).filter(
    option =>
      (hasTransactionSummaryCleanupFlag && option.value !== DisplayModes.USER_MISERY) ||
      !hasTransactionSummaryCleanupFlag
  );
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
