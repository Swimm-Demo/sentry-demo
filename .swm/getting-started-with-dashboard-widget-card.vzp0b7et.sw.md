---
title: Getting Started with Dashboard Widget Card
---
A Widget Card in the Dashboards of Sentry is a visual component that displays specific data based on the widget's configuration. It is defined in the `WidgetCard` class in the `static/app/views/dashboards/widgetCard/index.tsx` file. The Widget Card can be customized with various properties such as `api`, `isEditingDashboard`, `location`, `organization`, `selection`, `widget`, `widgetLimitReached`, and `dashboardFilters` among others. These properties control the behavior and the data displayed in the Widget Card.

The `dashboardFilters` property, for instance, is used to apply specific filters to the data displayed in the Widget Card. This is done through the `applyDashboardFilters` method in the `genericWidgetQueries.tsx` file, which modifies the widget's queries based on the provided dashboard filters.

The `WidgetCard` class also contains methods like `renderToolbar` and `renderContextMenu` which are responsible for rendering the toolbar and context menu of the Widget Card respectively. The `render` method is the main method responsible for rendering the entire Widget Card.

The Widget Card also has a styled component `WidgetCardPanel` which is used to style the Widget Card. It controls the appearance of the Widget Card like its margin, visibility, height, and display properties.

In addition to the `WidgetCard` class, there are other related components and utilities in the `widgetCard` directory like `widgetQueries.tsx`, `issueWidgetQueries.tsx`, and `releaseWidgetQueries.tsx` which handle different types of widget queries.

<SwmSnippet path="/static/app/views/dashboards/widgetCard/index.tsx" line="225">

---

# WidgetCard Class

The `WidgetCard` class is where the Widget Card is defined. It contains various properties that control the behavior and the data displayed in the Widget Card.

```tsx
      api,
      organization,
      selection,
      widget,
      isMobile,
      renderErrorMessage,
      tableItemLimit,
      windowWidth,
      noLazyLoad,
      showStoredAlert,
      noDashboardsMEPProvider,
      dashboardFilters,
      isWidgetInvalid,
      location,
    } = this.props;

    if (widget.displayType === DisplayType.TOP_N) {
      const queries = widget.queries.map(query => ({
        ...query,
        // Use the last aggregate because that's where the y-axis is stored
        aggregates: query.aggregates.length
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/dashboards/widgetCard/genericWidgetQueries.tsx" line="127">

---

# applyDashboardFilters Method

The `applyDashboardFilters` method is used to apply specific filters to the data displayed in the Widget Card. It modifies the widget's queries based on the provided dashboard filters.

```tsx
    // We do not fetch data whenever the query name changes.
    // Also don't count empty fields when checking for field changes
    const previousQueries = prevProps.widget.queries;
    const [prevWidgetQueryNames, prevWidgetQueries] = previousQueries.reduce(
      ([names, queries]: [string[], Omit<WidgetQuery, 'name'>[]], {name, ...rest}) => {
        names.push(name);
        rest.fields = rest.fields?.filter(field => !!field) ?? [];

        // Ignore aliases because changing alias does not need a query
        rest = omit(rest, 'fieldAliases');
        queries.push(rest);
        return [names, queries];
      },
      [[], []]
    );

    const nextQueries = widget.queries;
    const [widgetQueryNames, widgetQueries] = nextQueries.reduce(
      ([names, queries]: [string[], Omit<WidgetQuery, 'name'>[]], {name, ...rest}) => {
        names.push(name);
        rest.fields = rest.fields?.filter(field => !!field) ?? [];
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/dashboards/widgetCard/index.tsx" line="75">

---

# WidgetCardPanel Styled Component

The `WidgetCardPanel` is a styled component used to style the Widget Card. It controls the appearance of the Widget Card like its margin, visibility, height, and display properties.

```tsx
  organization: Organization;
  selection: PageFilters;
  widget: Widget;
  widgetLimitReached: boolean;
  dashboardFilters?: DashboardFilters;
  draggableProps?: DraggableProps;
  hideToolbar?: boolean;
  index?: string;
  isEditingWidget?: boolean;
  isMobile?: boolean;
  isPreview?: boolean;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/dashboards/widgetCard/widgetQueries.tsx" line="1">

---

# Related Components and Utilities

In addition to the `WidgetCard` class, there are other related components and utilities in the `widgetCard` directory like `widgetQueries.tsx`, `issueWidgetQueries.tsx`, and `releaseWidgetQueries.tsx` which handle different types of widget queries.

```tsx
import {useContext} from 'react';
import omit from 'lodash/omit';

import type {Client} from 'sentry/api';
import {isMultiSeriesStats} from 'sentry/components/charts/utils';
import type {
  EventsStats,
  MultiSeriesEventsStats,
  Organization,
  PageFilters,
} from 'sentry/types';
import type {Series} from 'sentry/types/echarts';
import type {EventsTableData, TableData} from 'sentry/utils/discover/discoverQuery';
import {DURATION_UNITS, SIZE_UNITS} from 'sentry/utils/discover/fieldRenderers';
import {getAggregateAlias} from 'sentry/utils/discover/fields';
import type {MetricsResultsMetaMapKey} from 'sentry/utils/performance/contexts/metricsEnhancedPerformanceDataContext';
import {useMetricsResultsMeta} from 'sentry/utils/performance/contexts/metricsEnhancedPerformanceDataContext';
import {useMEPSettingContext} from 'sentry/utils/performance/contexts/metricsEnhancedSetting';
import {OnDemandControlConsumer} from 'sentry/utils/performance/contexts/onDemandControl';

import {ErrorsAndTransactionsConfig} from '../datasetConfig/errorsAndTransactions';
```

---

</SwmSnippet>

# Widget Card Functions

This section will cover the main functions of the Widget Card component in the Sentry application.

<SwmSnippet path="/static/app/views/dashboards/widgetCard/index.tsx" line="121">

---

## renderToolbar

The `renderToolbar` method is responsible for rendering the toolbar of the Widget Card. It checks if the dashboard is in editing mode and if so, it returns the Toolbar component with the appropriate props.

```tsx
  renderToolbar() {
    const {
      onEdit,
      onDelete,
      onDuplicate,
      draggableProps,
      hideToolbar,
      isEditingDashboard,
      isMobile,
    } = this.props;

    if (!isEditingDashboard) {
      return null;
    }

    return (
      <Toolbar
        onEdit={onEdit}
        onDelete={onDelete}
        onDuplicate={onDuplicate}
        draggableProps={draggableProps}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/dashboards/widgetCard/index.tsx" line="148">

---

## renderContextMenu

The `renderContextMenu` method is responsible for rendering the context menu of the Widget Card. It checks if the dashboard is in editing mode and if not, it returns the WidgetCardContextMenu component with the appropriate props.

```tsx
  renderContextMenu() {
    const {
      widget,
      selection,
      organization,
      showContextMenu,
      isPreview,
      widgetLimitReached,
      onEdit,
      onDuplicate,
      onDelete,
      isEditingDashboard,
      router,
      location,
      index,
    } = this.props;

    const {seriesData, tableData, pageLinks, totalIssuesCount, seriesResultsType} =
      this.state;

    if (isEditingDashboard) {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/dashboards/widgetCard/genericWidgetQueries.tsx" line="215">

---

## widgetForRequest

The `widgetForRequest` method is used to prepare the widget for a request. It applies the dashboard filters to the widget and cleans it for the request.

```tsx
  widgetForRequest(widget: Widget): Widget {
    widget = this.applyDashboardFilters(widget);
    return cleanWidgetForRequest(widget);
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/dashboards/widgetCard/genericWidgetQueries.tsx" line="199">

---

## applyDashboardFilters

The `applyDashboardFilters` method is used to apply specific filters to the data displayed in the Widget Card. It modifies the widget's queries based on the provided dashboard filters.

```tsx
  applyDashboardFilters(widget: Widget): Widget {
    const {dashboardFilters, skipDashboardFilterParens} = this.props;

    const dashboardFilterConditions = dashboardFiltersToString(dashboardFilters);
    widget.queries.forEach(query => {
      if (dashboardFilterConditions) {
        // If there is no base query, there's no need to add parens
        if (query.conditions && !skipDashboardFilterParens) {
          query.conditions = `(${query.conditions})`;
        }
        query.conditions = query.conditions + ` ${dashboardFilterConditions}`;
      }
    });
    return widget;
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/dashboards/widgetCard/genericWidgetQueries.tsx" line="420">

---

## cleanWidgetForRequest

The `cleanWidgetForRequest` method is used to clean the widget for a request. It removes any unnecessary fields from the widget's queries.

```tsx
export function cleanWidgetForRequest(widget: Widget): Widget {
  const _widget = cloneDeep(widget);
  _widget.queries.forEach(query => {
    query.aggregates = query.aggregates.filter(field => !!field && field !== 'equation|');
    query.columns = query.columns.filter(field => !!field && field !== 'equation|');
  });

  return _widget;
}
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
