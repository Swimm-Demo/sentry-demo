---
title: Introduction to Metric Alert Rule Details
---
In the context of the Metric component, 'Details' refers to the specific information and data related to a metric alert rule. This includes the rule's configuration, its history of triggering incidents, and the visual representation of the metric data over time.

The 'Details' are implemented across several TypeScript files in the 'metric/details' directory. These files define various styled components, constants, and functions that collectively render the detailed view of a metric alert rule.

For instance, the 'metricChart.tsx' file contains the logic for displaying the metric data in a chart format. It uses various constants and props such as 'project', 'organization', 'query', and 'selectedIncident' to fetch and display the relevant data.

Another key part of the 'Details' is the 'MetricHistory' function defined in 'metricHistory.tsx'. This function uses the 'incidents' prop to display a history of incidents triggered by the metric alert rule.

The 'Details' also include additional information such as 'queryExtras' which are used to modify the data query based on certain conditions, and the 'State' type which is a TypeScript Record type used to manage the component's state.

<SwmSnippet path="/static/app/views/alerts/rules/metric/details/sidebar.tsx" line="218">

---

# Alert Rule Details

This line of code displays the heading 'Alert Rule Details', indicating the start of the detailed view for a metric alert rule.

```tsx
        <Heading>{t('Alert Rule Details')}</Heading>
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/alerts/rules/metric/details/utils.tsx" line="23">

---

# Date Handling in Details

This comment indicates that the current date is used in the 'Details' view, specifically for handling the 'endDate' of an alert.

```tsx
  // make a copy of now since we will modify endDate and use now for comparing
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/alerts/rules/metric/details/utils.spec.tsx" line="18">

---

# Testing Details

These test cases validate the behavior of the 'Details' view, specifically how it handles the dates for active, recently closed, and older alerts.

```tsx
  it('should use current date for an active alert', () => {
    const incident = IncidentFixture({
      dateStarted: '2022-05-16T18:55:00Z',
      dateClosed: null,
      alertRule: MetricRuleFixture({timeWindow: 1}),
    });
    const result = buildMetricGraphDateRange(incident);
    expect(result).toEqual({start: '2022-05-16T17:40:00', end: now});
    expect(moment(result.end).diff(moment(result.start), 'minutes')).toBe(140);
  });

  it('should use current date for a recently closed alert', () => {
    const incident = IncidentFixture({
      dateStarted: '2022-05-16T18:55:00Z',
      dateClosed: '2022-05-16T18:57:00Z',
      alertRule: MetricRuleFixture({timeWindow: 1}),
    });
    const result = buildMetricGraphDateRange(incident);
    expect(result).toEqual({start: '2022-05-16T17:40:00', end: now});
    expect(moment(result.end).diff(moment(result.start), 'minutes')).toBe(140);
  });
```

---

</SwmSnippet>

# Details Functions

The 'Details' are implemented across several TypeScript files in the 'metric/details' directory. These files define various styled components, constants, and functions that collectively render the detailed view of a metric alert rule.

<SwmSnippet path="/static/app/views/alerts/rules/metric/details/body.tsx" line="143">

---

## queryWithTypeFilter

The `queryWithTypeFilter` constant is used to construct a query string with an event type filter. This is used when fetching metric data for the chart.

```tsx
  const {dataset, aggregate, query} = rule;

  const eventType = extractEventTypeFilterFromRule(rule);
  const queryWithTypeFilter = (
    query ? `(${query}) AND (${eventType})` : eventType
  ).trim();
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/alerts/rules/metric/details/body.tsx" line="149">

---

## relativeOptions

The `relativeOptions` constant is used to determine the relative time period options for the metric data chart. It includes a custom option for the last 14 days if the rule's time window is greater than 1.

```tsx
  const relativeOptions = {
    ...SELECTOR_RELATIVE_PERIODS,
    ...(rule.timeWindow > 1 ? {[TimePeriod.FOURTEEN_DAYS]: t('Last 14 days')} : {}),
  };
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/alerts/rules/metric/details/body.tsx" line="154">

---

## isSnoozed

The `isSnoozed` constant is a boolean value that indicates whether the rule is currently snoozed. This is used to conditionally render a snooze alert in the UI.

```tsx
  const isSnoozed = rule.snooze;
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
