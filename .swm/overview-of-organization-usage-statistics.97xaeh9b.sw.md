---
title: Overview of Organization Usage Statistics
---
Organization stats in the Sentry demo application refers to the usage data that Sentry has received across an entire organization. This data is displayed in various views within the application.

The data is fetched from the `/organizations/{organization.slug}/stats_v2/` endpoint, which returns usage data for the specified organization. The data includes the total number of events, as well as the number of accepted, dropped, filtered, and rate-limited events.

The `OrganizationStats` component in `static/app/views/organizationStats/index.tsx` is responsible for rendering the organization stats. It uses various props such as `organization`, `selection`, and `location` to fetch and display the data.

The `UsageStatsOrganization` component in `static/app/views/organizationStats/usageStatsOrg.tsx` is another key component for displaying organization stats. It inherits from the `DeprecatedAsyncComponent` and makes an API call to fetch the data.

The organization stats data is also used in other components such as `UsageStatsPerMin`, `UsageStatsProjects`, and `UsageTable` to display specific aspects of the data.

<SwmSnippet path="/static/app/views/organizationStats/usageStatsOrg.tsx" line="91">

---

# Fetching Organization Stats

The `endpointPath` getter constructs the API endpoint for fetching organization stats. The `endpointQuery` getter constructs the query parameters for the API call.

```tsx
    const {organization} = this.props;
    return `/organizations/${organization.slug}/stats_v2/`;
  }

  get endpointQueryDatetime() {
    const {dataDatetime} = this.props;
    const queryDatetime =
      dataDatetime.start && dataDatetime.end
        ? {
            start: dataDatetime.start,
            end: dataDatetime.end,
            utc: dataDatetime.utc,
          }
        : {
            statsPeriod: dataDatetime.period || DEFAULT_STATS_PERIOD,
          };
    return queryDatetime;
  }

  get endpointQuery() {
    const {dataDatetime, projectIds} = this.props;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/organizationStats/usageStatsOrg.tsx" line="224">

---

# Displaying Organization Stats

The `chartProps` getter constructs the props for the `UsageChart` component, which is used to display the organization stats.

```tsx
  get chartProps(): UsageChartProps {
    const {dataCategory} = this.props;
    const {error, errors, loading} = this.state;
    const {
      chartStats,
      dataError,
      chartDateInterval,
      chartDateStart,
      chartDateEnd,
      chartDateUtc,
      chartTransform,
    } = this.chartData;

    const hasError = error || !!dataError;
    const chartErrors: any = dataError ? {...errors, data: dataError} : errors; // TODO(ts): AsyncComponent
    const chartProps = {
      isLoading: loading,
      isError: hasError,
      errors: chartErrors,
      title: ' ', // Force the title to be blank
      footer: this.renderChartFooter(),
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/organizationStats/usageStatsOrg.tsx" line="66">

---

# Updating Organization Stats

The `componentDidUpdate` method checks if the props have changed and, if so, reloads the data.

```tsx
  componentDidUpdate(prevProps: UsageStatsOrganizationProps) {
    const {dataDatetime: prevDateTime, projectIds: prevProjectIds} = prevProps;
    const {dataDatetime: currDateTime, projectIds: currProjectIds} = this.props;

    if (
      prevDateTime.start !== currDateTime.start ||
      prevDateTime.end !== currDateTime.end ||
      prevDateTime.period !== currDateTime.period ||
      prevDateTime.utc !== currDateTime.utc ||
      !isEqual(prevProjectIds, currProjectIds)
    ) {
      this.reloadData();
    }
  }
```

---

</SwmSnippet>

# Organization Stats API

Understanding Organization Stats Endpoint

<SwmSnippet path="/static/app/views/organizationStats/index.spec.tsx" line="35">

---

## Organization Stats Endpoint

The endpoint `/organizations/{organization.slug}/stats_v2/` is used to fetch the organization stats data. The `{organization.slug}` part of the URL is a placeholder for the actual organization slug.

```tsx
  const endpoint = `/organizations/${organization.slug}/stats_v2/`;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/organizationStats/types.tsx" line="6">

---

## UsageSeries Interface

The `UsageSeries` interface defines the structure of the data returned by the organization stats endpoint. It includes `start` and `end` properties which likely represent the time range for the stats data.

```tsx
export interface UsageSeries extends SeriesApi {
  // index signature is present because we often send this
  // data to sentry as part of the event context.
  end: string;
  start: string;
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/organizationStats/types.tsx" line="13">

---

## UsageStat Type

The `UsageStat` type further breaks down the stats into `accepted`, `dropped`, `filtered`, and `total` counts, providing more detailed information about the organization's usage.

```tsx
export type UsageStat = {
  accepted: number;
  date: string;
  dropped: {
    total: number;
    other?: number;
  };
  filtered: number;
  total: number;
};
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
