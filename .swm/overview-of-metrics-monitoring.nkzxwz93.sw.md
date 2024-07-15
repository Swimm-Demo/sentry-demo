---
title: Overview of Metrics Monitoring
---
Metrics in the Views directory of the sentry-demo repository refers to the functionality that allows the tracking and monitoring of various aspects of the application's performance. It is implemented through a series of components, utilities, and types that work together to provide a comprehensive metrics system.

The MetricsContainer component, for instance, is a wrapper component that checks if the user has access to the custom metrics feature. If the user doesn't have access, a warning message is displayed. Otherwise, it renders the children components within the NoProjectMessage component.

The Metrics function in the metrics.tsx file is the main component for the Metrics feature. It uses the useOrganization hook to get the current organization and tracks the page view and visit metrics. It also checks if the organization has custom metrics extraction rules and renders the appropriate components accordingly.

The MetricsQuery type is used to define the structure of a metrics query. It is used in various places in the codebase, such as in the MetricQueryContextMenu component, which provides a context menu for metrics queries.

The metrics/utils directory contains a series of utility functions and hooks that are used across the Metrics feature. These utilities handle various tasks such as managing the metrics interval parameter, generating a new metrics widget, parsing metric widgets query parameters, and more.

<SwmSnippet path="/static/app/views/metrics/metrics.tsx" line="23">

---

# Metrics Function

The Metrics function is the main component for the Metrics feature. It uses the useOrganization hook to get the current organization and tracks the page view and visit metrics. It also checks if the organization has custom metrics extraction rules and renders the appropriate components accordingly.

```tsx
function Metrics() {
  const organization = useOrganization();

  useEffect(() => {
    trackAnalytics('ddm.page-view', {
      organization,
    });
    Sentry.metrics.increment('ddm.visit');
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <SentryDocumentTitle title={t('Metrics')} orgSlug={organization.slug}>
      {hasCustomMetricsExtractionRules(organization) ? (
        <VirtualMetricsContextProvider>
          <MetricsContextProvider>
            <WrappedPageFiltersContainer>
              <MetricsLayout />
            </WrappedPageFiltersContainer>
          </MetricsContextProvider>
        </VirtualMetricsContextProvider>
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/metrics/metricQueryContextMenu.tsx" line="45">

---

# Metrics Query

The MetricsQuery type is used to define the structure of a metrics query. It is used in various places in the codebase, such as in the MetricQueryContextMenu component, which provides a context menu for metrics queries.

```tsx
type ContextMenuProps = {
  displayType: MetricDisplayType;
  metricsQuery: MetricsQuery;
  widgetIndex: number;
};

export function MetricQueryContextMenu({
  metricsQuery,
  displayType,
  widgetIndex,
}: ContextMenuProps) {
  const {getExtractionRule} = useVirtualMetricsContext();
  const organization = useOrganization();
  const router = useRouter();

  const {removeWidget, duplicateWidget, widgets} = useMetricsContext();
  const createAlert = useMemo(
    () => getCreateAlert(organization, metricsQuery),
    [metricsQuery, organization]
  );
  const createDashboardWidget = useCreateDashboardWidget(
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/metrics/utils/useMetricsIntervalParam.tsx" line="93">

---

# Metrics Utilities

The metrics/utils directory contains a series of utility functions and hooks that are used across the Metrics feature. These utilities handle various tasks such as managing the metrics interval parameter, generating a new metrics widget, parsing metric widgets query parameters, and more.

```tsx
export function useMetricsIntervalParam() {
  const {datetime} = usePageFilters().selection;
  const {interval} = useLocationQuery({fields: {interval: decodeScalar}});
  const {widgets} = useMetricsContext();
  const updateQuery = useUpdateQuery();

  const hasSetMetric = useMemo(
    () =>
      widgets.some(
        widget => isMetricsQueryWidget(widget) && parseMRI(widget.mri)!.type === 's'
      ),
    [widgets]
  );

  const handleIntervalChange = useCallback(
    (newInterval: string) => {
      updateQuery({interval: newInterval}, {replace: true});
    },
    [updateQuery]
  );

```

---

</SwmSnippet>

# Metrics Feature Functions

This section will cover the main functions related to the Metrics feature in the sentry-demo repository.

<SwmSnippet path="/static/app/views/metrics/index.tsx" line="12">

---

## MetricsContainer

The MetricsContainer is a wrapper component that checks if the user has access to the custom metrics feature. If the user doesn't have access, a warning message is displayed. Otherwise, it renders the children components within the NoProjectMessage component.

```tsx
function MetricsContainer({children}: Props) {
  const organization = useOrganization();

  return (
    <Feature
      features={['custom-metrics']}
      requireAll
      organization={organization}
      renderDisabled={() => (
        <Layout.Page withPadding>
          <Alert type="warning">{t("You don't have access to this feature")}</Alert>
        </Layout.Page>
      )}
    >
      <NoProjectMessage organization={organization}>{children}</NoProjectMessage>
    </Feature>
  );
}

export default MetricsContainer;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/metrics/metrics.tsx" line="23">

---

## Metrics

The Metrics function is the main component for the Metrics feature. It uses the useOrganization hook to get the current organization and tracks the page view and visit metrics. It also checks if the organization has custom metrics extraction rules and renders the appropriate components accordingly.

```tsx
function Metrics() {
  const organization = useOrganization();

  useEffect(() => {
    trackAnalytics('ddm.page-view', {
      organization,
    });
    Sentry.metrics.increment('ddm.visit');
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <SentryDocumentTitle title={t('Metrics')} orgSlug={organization.slug}>
      {hasCustomMetricsExtractionRules(organization) ? (
        <VirtualMetricsContextProvider>
          <MetricsContextProvider>
            <WrappedPageFiltersContainer>
              <MetricsLayout />
            </WrappedPageFiltersContainer>
          </MetricsContextProvider>
        </VirtualMetricsContextProvider>
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/metrics/utils/index.tsx" line="9">

---

## MetricsQuery

The MetricsQuery type is used to define the structure of a metrics query. It is used in various places in the codebase, such as in the MetricQueryContextMenu component, which provides a context menu for metrics queries.

```tsx
import {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/metrics/utils/metricsChartPalette.tsx" line="36">

---

## getCachedChartPalette

The getCachedChartPalette function is used to get a cached chart palette that includes all of the given series names. It checks if a palette already exists in the cache that includes all the series names. If it does, it moves the cached palette to the end of the cache, making it the most recent one.

```tsx
export function getCachedChartPalette(
  cache: Readonly<Record<string, string>>[],
  seriesNames: string[]
): Readonly<Record<string, string>> {
  // Check if we already have a palette that includes all of the given seriesNames
  // We search in reverse to get the most recent palettes first
  let cacheIndex = -1;
  for (let i = cache.length - 1; i >= 0; i--) {
    const palette = cache[i];
    if (seriesNames.every(seriesName => seriesName in palette)) {
      cacheIndex = i;
      break;
    }
  }

  if (cacheIndex > -1) {
    const cachedPalette = cache[cacheIndex];
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
