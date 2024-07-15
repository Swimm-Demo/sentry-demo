---
title: Overview of Performance Insights Views
---
Insights in the Views directory refers to a collection of views that provide detailed performance monitoring and error tracking data for different aspects of the application. These views are categorized into different subdirectories such as HTTP, database, cache, mobile, and more, each providing specific insights related to that category.

For instance, the HTTP views provide insights into the HTTP domain, while the database views provide insights into database performance. Each of these categories has a landing page and a summary page, which provide an overview and detailed summary of the performance data respectively.

The insights views are a crucial part of Sentry's performance monitoring capabilities, allowing developers to gain a deep understanding of their application's performance and identify potential issues.

<SwmSnippet path="/static/app/views/insights/settings.ts" line="62">

---

# Insights Constants

The `INSIGHTS_TITLE` and `INSIGHTS_BASE_URL` constants are used to define the title and base URL for the insights views. These constants are used throughout the application to reference the insights views.

```typescript
export const INSIGHTS_TITLE = t('Insights');
export const INSIGHTS_BASE_URL = 'insights';
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/routes.tsx" line="1436">

---

# Insights Routes

`INSIGHTS_BASE_URL` is used in the application's routing configuration to define the paths for the insights views. This ensures that the correct views are displayed when navigating to the insights URLs.

```tsx
      from="/llm-monitoring/"
      to={`/${INSIGHTS_BASE_URL}/${MODULE_BASE_URLS[ModuleName.AI]}/`}
    />
  ) : (
    <Redirect
      from="/organizations/:orgId/llm-monitoring/"
      to={`/organizations/:orgId/${INSIGHTS_BASE_URL}/${MODULE_BASE_URLS[ModuleName.AI]}/`}
    />
  );

  const insightsRedirects = Object.values(MODULE_BASE_URLS)
    .map(
      moduleBaseURL =>
        moduleBaseURL && (
          <Redirect
            key={moduleBaseURL}
            from={`${moduleBaseURL}/*`}
            to={`/${INSIGHTS_BASE_URL}/${moduleBaseURL}/:splat`}
          />
        )
    )
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/common/queries/useDiscover.ts" line="17">

---

# Insights Queries

The `useDiscover` function is used to fetch performance data for the insights views. It takes a set of options and returns the corresponding performance data. This function is used in various insights views to fetch the necessary data.

```typescript
interface UseMetricsOptions<Fields> {
  cursor?: string;
  enabled?: boolean;
  fields?: Fields;
  limit?: number;
  pageFilters?: PageFilters;
  search?: MutableSearch | string; // TODO - ideally this probably would be only `Mutable Search`, but it doesn't handle some situations well
  sorts?: Sort[];
}

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

# Insights Directories

The insights views are organized into different directories based on the type of insights they provide. For example, the `http` directory contains views for HTTP insights, while the `mobile` directory contains views for mobile insights. Each directory contains a set of related views and utility functions.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
