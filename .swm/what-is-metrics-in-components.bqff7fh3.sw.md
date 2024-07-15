---
title: What is Metrics in Components
---
Metrics in the Components directory of the sentry-demo repository refer to the measurement and analysis of application data. They are used to monitor application performance and identify issues or areas for improvement.

The Metrics component is organized into several sub-components, each serving a specific purpose. For instance, the 'chart' sub-component is responsible for visualizing the metrics data in various chart formats.

The 'metricSamplesTable.tsx' file defines the structure of the metrics data table. It includes fields such as 'project', 'id', 'span.op', 'span.description', and others which represent different aspects of the metrics data.

The 'CombinedMetricChartProps' interface in 'chart/types.tsx' defines the properties for the combined metric chart component. This includes properties like 'displayType', 'series', 'additionalSeries', and others which control the appearance and functionality of the chart.

The 'metric' member in 'mriSelect/metricListItemDetails.tsx' represents a specific metric item in the list. It includes properties like 'isDuplicateWithDifferentUnit', 'metric', 'onTagClick', and others which control the behavior and display of the metric item.

The 'result' constant in 'metricSamplesTable.tsx' and 'mriSelect/index.tsx' is used to store the result of a metrics sample query. It is used to update the metrics samples and check if the MRI (Metric Resource Identifier) is supported.

The 'baseChartProps' variable in 'chart/chart.tsx' is used to set the base properties for the chart component. This includes properties like 'heightOptions' and 'dateTimeOptions' which control the size and time range of the chart.

<SwmSnippet path="/static/app/components/metrics/chart/useMetricChartSamples.tsx" line="76">

---

# Metrics in useMetricChartSamples

The 'useMetricChartSamples' function is used to generate metric chart samples. It takes in options such as 'timeseries', 'aggregation', 'highlightedSampleId', 'onSampleClick', 'samples', and 'unit'. The function uses these options to generate a chart that visualizes the metrics data.

```tsx
  samples,
  unit = '',
}: UseMetricChartSamplesOptions) {
  const theme = useTheme();
  const chartRef = useRef<ReactEchartsRef>(null);

  const [valueRect, setValueRect] = useState(() => getValueRectFromSeries(timeseries));

  const samplesById = useMemo(() => {
    return (samples ?? []).reduce((acc, sample) => {
      acc[sample.id] = sample;
      return acc;
    }, {});
  }, [samples]);

  useEffect(() => {
    // Changes in timeseries change the valueRect since the timeseries yAxis auto scales
    // and scatter yAxis needs to match the scale
    setValueRect(getValueRectFromSeries(timeseries));
  }, [timeseries]);

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/metrics/mriSelect/metricListItemDetails.tsx" line="40">

---

# Metrics in MetricListItemDetails

The 'MetricListItemDetails' function is used to display details of a specific metric item. It takes in parameters such as 'metric', 'selectedProjects', 'onTagClick', and 'isDuplicateWithDifferentUnit'. The function uses these parameters to generate a detailed view of a specific metric item.

```tsx
export function MetricListItemDetails({
  metric,
  selectedProjects,
  onTagClick,
  isDuplicateWithDifferentUnit,
}: {
  isDuplicateWithDifferentUnit: boolean;
  metric: MetricMeta;
  onTagClick: (mri: MRI, tag: string) => void;
  selectedProjects: Project[];
}) {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/metrics/metricSamplesTable.tsx" line="222">

---

# Metrics in result

The 'result' constant is used to store the result of a metrics sample query. It is used to update the metrics samples and check if the MRI (Metric Resource Identifier) is supported.

```tsx
  const result = useMetricsSamples({
    fields,
    datetime,
    max: focusArea?.max,
    min: focusArea?.min,
    mri: resolvedMRI,
    aggregation: resolvedAggregation,
    query,
    referrer: 'api.organization.metrics-samples',
    enabled,
    sort: sortQuery,
    limit: 20,
  });
```

---

</SwmSnippet>

# Metrics Functionality

This section will explain the main functions related to the Metrics functionality in the Sentry application.

<SwmSnippet path="/static/app/components/metrics/customMetricsEventData.tsx" line="45">

---

## flattenMetricsSummary

The `flattenMetricsSummary` function is used to flatten the metrics summary into an array of objects. Each object contains an item from the metrics summary and its corresponding MRI (Metric Resource Identifier).

```tsx
function flattenMetricsSummary(
  metricsSummary: MetricsSummary
): {item: MetricsSummaryItem; mri: MRI}[] {
  return (
    Object.entries(metricsSummary) as [
      keyof MetricsSummary,
      MetricsSummary[keyof MetricsSummary],
    ][]
  )
    .flatMap(([mri, items]) => (items || []).map(item => ({item, mri})))
    .filter(entry => !isExtractedCustomMetric(entry));
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/metrics/useMetricsSamples.tsx" line="105">

---

## getSummaryValueForAggregation

The `getSummaryValueForAggregation` function is used to get the summary value for a given aggregation. It takes the summary and aggregation as parameters and returns the corresponding summary value.

```tsx
export function getSummaryValueForAggregation(
  summary: Summary,
  aggregation?: MetricAggregation
) {
  switch (aggregation) {
    case 'count':
      return summary.count;
    case 'min':
      return summary.min;
    case 'max':
      return summary.max;
    case 'sum':
      return summary.sum;
    case 'avg':
    default:
      return summary.sum / summary.count;
  }
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/metrics/chart/useMetricChartSamples.tsx" line="71">

---

## useMetricChartSamples

The `useMetricChartSamples` function is a custom hook that is used to manage the state and interactions of the metric chart samples. It includes several state variables and functions for handling click events, fetching tag values, and applying chart properties.

```tsx
export function useMetricChartSamples({
  timeseries,
  highlightedSampleId,
  onSampleClick,
  aggregation,
  samples,
  unit = '',
}: UseMetricChartSamplesOptions) {
  const theme = useTheme();
  const chartRef = useRef<ReactEchartsRef>(null);

  const [valueRect, setValueRect] = useState(() => getValueRectFromSeries(timeseries));

  const samplesById = useMemo(() => {
    return (samples ?? []).reduce((acc, sample) => {
      acc[sample.id] = sample;
      return acc;
    }, {});
  }, [samples]);

  useEffect(() => {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/metrics/chart/useMetricReleases.tsx" line="54">

---

## useMetricReleases

The `useMetricReleases` function is a custom hook that is used to fetch and manage the state of the metric releases. It includes several state variables and functions for fetching data, handling click events, and applying chart properties.

```tsx
  const {
    datetime: {start, end, period},
    projects,
    environments,
  } = selection;

  const fetchData = useCallback(async () => {
    const queryObj: ReleaseQuery = {
      start,
      end,
      project: projects,
      environment: environments,
      statsPeriod: period,
    };
    let hasMore = true;
    const newReleases: Release[] = [];
    while (hasMore) {
      try {
        api.clear();

        const [releaseBatch, , resp] = await api.requestPromise(
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
