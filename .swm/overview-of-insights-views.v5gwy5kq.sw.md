---
title: Overview of Insights Views
---
Views in Sentry-Demo refer to the visual components that represent the data and its organization to the user. They are primarily used to structure and display the data fetched from the server.

The views are organized in a hierarchical manner, with each sub-directory representing a different aspect of the application's data. For instance, the 'spanSummaryPage' and 'spans' directories contain views related to span summaries and individual spans respectively.

The 'queryParameters.tsx' file defines the parameters used for querying data. These parameters are used across different views to fetch and display data according to user interactions.

<SwmSnippet path="/static/app/views/insights/common/views/spans/useModuleSort.ts" line="1">

---

# Use of Views in Code

This file demonstrates how views are used to sort modules. The `useModuleSort` function is used to parse a `Sort` object from the URL and apply it to the span module UI.

```typescript
import type {Sort} from 'sentry/utils/discover/fields';
import {decodeSorts} from 'sentry/utils/queryString';
import {useLocation} from 'sentry/utils/useLocation';
import type {QueryParameterNames} from 'sentry/views/insights/common/views/queryParameters';
import {SpanFunction, SpanMetricsField} from 'sentry/views/insights/types';

type Query = {
  [QueryParameterNames.SPANS_SORT]?: string;
  [QueryParameterNames.ENDPOINTS_SORT]?: string;
};

const SORTABLE_FIELDS = [
  `avg(${SpanMetricsField.SPAN_SELF_TIME})`,
  `${SpanFunction.HTTP_ERROR_COUNT}()`,
  `${SpanFunction.SPM}()`,
  `${SpanFunction.TIME_SPENT_PERCENTAGE}()`,
] as const;

export type ValidSort = Sort & {
  field: (typeof SORTABLE_FIELDS)[number];
};
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/common/views/spans/useModuleFilters.ts" line="1">

---

# Use of Views in Filtering

This file shows how views are used to filter modules. The `useModuleFilters` function is used to filter the span modules based on the query parameters in the URL.

```typescript
import pick from 'lodash/pick';

import {useLocation} from 'sentry/utils/useLocation';
import {SpanMetricsField} from 'sentry/views/insights/types';

export type ModuleFilters = {
  [SpanMetricsField.SPAN_ACTION]?: string;
  [SpanMetricsField.SPAN_DOMAIN]?: string;
  [SpanMetricsField.SPAN_GROUP]?: string;
  [SpanMetricsField.SPAN_OP]?: string;
};

export const useModuleFilters = () => {
  const location = useLocation<ModuleFilters>();

  return pick(location.query, [
    SpanMetricsField.SPAN_ACTION,
    SpanMetricsField.SPAN_DOMAIN,
    SpanMetricsField.SPAN_OP,
    SpanMetricsField.SPAN_GROUP,
  ]);
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
