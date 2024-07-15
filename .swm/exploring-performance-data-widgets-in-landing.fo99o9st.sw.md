---
title: Exploring Performance Data Widgets in Landing
---
Widgets in the Landing section of the sentry-demo repository refer to visual components that display performance data. They are defined in various TypeScript (tsx) files within the 'static/app/views/performance/landing/widgets' directory.

Each widget is defined with specific properties such as title, tooltip, and data type. These properties are used to customize the appearance and functionality of the widget.

The widgets are used to visualize different types of performance data. For example, there are widgets for displaying trends, histograms, and performance scores.

The widgets are designed to be interactive. They can be customized and manipulated by the user to display different types of data and metrics.

The widgets make use of a variety of queries and visualizations to fetch and display data. These are defined in the 'Queries' constants in the widget files.

<SwmSnippet path="/static/app/views/performance/landing/widgets/widgetDefinitions.tsx" line="12">

---

# Widget Definitions

This is where the ChartDefinition interface is defined. It includes properties like dataType, fields, title, titleTooltip, and others that are used to customize the appearance and functionality of the widgets.

```tsx
export interface ChartDefinition {
  dataType: GenericPerformanceWidgetDataType;
  fields: string[];
  // Additional fields to get requested but are not directly used in visualization.
  title: string;

  titleTooltip: string;
  // The first field in the list will be treated as the primary field in most widgets (except for special casing).
  allowsOpenInDiscover?: boolean;

  chartColor?: string;
  secondaryFields?: string[]; // Optional. Will default to colors depending on placement in list or colors from the chart itself.

  vitalStops?: {
    meh: number;
    poor: number;
  };
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/landing/widgets/components/widgetContainer.tsx" line="131">

---

# Widget Props

The `widgetProps` constant is used to define the properties of a widget. It includes properties from the chartDefinition, chartSetting, and other components.

```tsx
  const widgetProps = {
    ...chartDefinition,
    chartSetting,
    chartDefinition,
    InteractiveTitle:
      showNewWidgetDesign && allowedCharts.length > 2
        ? containerProps => (
            <WidgetInteractiveTitle
              {...containerProps}
              eventView={widgetEventView}
              allowedCharts={allowedCharts}
              chartSetting={chartSetting}
              setChartSetting={setChartSetting}
              rowChartSettings={rowChartSettings}
            />
          )
        : null,
    ContainerActions: !showNewWidgetDesign
      ? containerProps => (
          <WidgetContainerActions
            {...containerProps}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/landing/widgets/components/widgetContainer.tsx" line="170">

---

# Widget Usage

Here, `widgetProps` is used to customize the titleTooltip and dataType of the widget. Depending on the dataType, different types of widgets like TrendsWidget are returned.

```tsx
  const titleTooltip = showNewWidgetDesign ? '' : widgetProps.titleTooltip;

  switch (widgetProps.dataType) {
    case GenericPerformanceWidgetDataType.TRENDS:
      return (
        <TrendsWidget {...passedProps} {...widgetProps} titleTooltip={titleTooltip} />
      );
    case GenericPerformanceWidgetDataType.AREA:
      return (
        <SingleFieldAreaWidget
          {...passedProps}
          {...widgetProps}
          titleTooltip={titleTooltip}
```

---

</SwmSnippet>

# Widget Directory

This directory contains various TypeScript (tsx) files each defining a different type of widget. For example, 'singleFieldAreaWidget.tsx' defines a widget for displaying a single field area, 'vitalWidget.tsx' defines a widget for displaying vital statistics, and so on.

# Widget Functions

This section will explain the main functions of the widgets in the sentry-demo repository.

<SwmSnippet path="/static/app/views/performance/landing/widgets/widgets/histogramWidget.tsx" line="19">

---

## HistogramWidget

The `HistogramWidget` function is used to create a histogram widget. It uses the `HistogramQuery` component to fetch the data and the `transformHistogramQuery` function to transform the data into a format suitable for the histogram. The `HistogramWidget` also uses the `useMemo` hook to memoize the result of the `HistogramQuery` component to avoid unnecessary re-renders.

```tsx
export function HistogramWidget(props: PerformanceWidgetProps) {
  const location = useLocation();
  const mepSetting = useMEPSettingContext();
  const {ContainerActions, InteractiveTitle} = props;
  const globalSelection = props.eventView.getPageFilters();

  const Queries = useMemo(() => {
    return {
      chart: {
        fields: props.fields,
        component: provided => (
          <HistogramQuery
            limit={QUERY_LIMIT_PARAM}
            {...provided}
            eventView={provided.eventView}
            location={location}
            numBuckets={20}
            dataFilter="exclude_outliers"
            queryExtras={getMEPQueryParams(mepSetting)}
          />
        ),
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/landing/widgets/widgets/trendsWidget.tsx" line="19">

---

## TrendsWidget

The `TrendsWidget` function is used to create a trends widget. It uses the `TrendsDiscoverQuery` component to fetch the data. The `TrendsWidget` also uses the `useMemo` hook to memoize the result of the `TrendsDiscoverQuery` component to avoid unnecessary re-renders.

```tsx
  getProjectID,
  getSelectedProjectPlatforms,
  handleTrendsClick,
  trendsTargetRoute,
} from 'sentry/views/performance/utils';

import {Chart} from '../../../trends/chart';
import {TrendChangeType, TrendFunctionField} from '../../../trends/types';
import {excludeTransaction} from '../../utils';
import {Accordion} from '../components/accordion';
import {GenericPerformanceWidget} from '../components/performanceWidget';
import SelectableList, {
  GrowLink,
  ListClose,
  RightAlignedCell,
  Subtitle,
  WidgetEmptyStateWarning,
} from '../components/selectableList';
import {transformTrendsDiscover} from '../transforms/transformTrendsDiscover';
import type {PerformanceWidgetProps, QueryDefinition, WidgetDataResult} from '../types';
import {QUERY_LIMIT_PARAM, TOTAL_EXPANDABLE_ROWS_HEIGHT} from '../utils';
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/landing/widgets/widgets/vitalWidget.tsx" line="19">

---

## VitalWidget

The `VitalWidget` function is used to create a vital widget. It uses the `DiscoverQuery` component to fetch the data. The `VitalWidget` also uses the `useMemo` hook to memoize the result of the `DiscoverQuery` component to avoid unnecessary re-renders.

```tsx
} from 'sentry/utils/performance/contexts/metricsEnhancedSetting';
import {usePageAlert} from 'sentry/utils/performance/contexts/pageAlert';
import type {VitalData} from 'sentry/utils/performance/vitals/vitalsCardsDiscoverQuery';
import {decodeList} from 'sentry/utils/queryString';
import {MutableSearch} from 'sentry/utils/tokenizeSearch';
import {useLocation} from 'sentry/utils/useLocation';
import withApi from 'sentry/utils/withApi';
import {
  DisplayModes,
  transactionSummaryRouteWithQuery,
} from 'sentry/views/performance/transactionSummary/utils';
import {
  createUnnamedTransactionsDiscoverTarget,
  UNPARAMETERIZED_TRANSACTION,
} from 'sentry/views/performance/utils';
import {vitalDetailRouteWithQuery} from 'sentry/views/performance/vitalDetail/utils';
import {_VitalChart} from 'sentry/views/performance/vitalDetail/vitalChart';

import {excludeTransaction} from '../../utils';
import {VitalBar} from '../../vitalsCards';
import {Accordion} from '../components/accordion';
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
