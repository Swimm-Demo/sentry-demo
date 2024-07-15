---
title: Overview of Trace Details in Performance
---
New trace details in the Performance section of the Sentry application refers to the detailed information about a specific trace. A trace represents a series of events, or transactions, in an application that are connected by a trace ID. The new trace details feature provides a comprehensive view of the trace, including its associated issues, profiling information, spans, transactions, and any errors that occurred during the trace. It also includes visualizations and metrics to help developers understand the performance characteristics of the trace.

The new trace details feature is implemented across several directories and files in the codebase. The main entry point is the `TraceView` function in the `index.tsx` file, which uses various hooks and components to fetch and display the trace data. The trace data is fetched from the API using the `useTrace` hook and other related hooks in the `traceApi` directory. The fetched data is then passed to various components in the `traceDrawer` and `traceState` directories for rendering.

The `traceDrawer` directory contains components for the drawer UI that displays the detailed trace information. The `details` subdirectory within `traceDrawer` contains components for each type of detail, such as issues, profiling, span, and transaction. The `traceState` directory contains components and hooks for managing the state of the trace view, including search functionality and tab management.

The `NO_PERFORMANCE_ISSUES` constant in the `trace.tsx` file is used to represent a scenario where there are no performance issues associated with a trace. This constant is used in the rendering of the trace details.

<SwmSnippet path="/static/app/views/performance/newTraceDetails/traceApi/useTrace.tsx" line="22">

---

# Fetching Trace Data

The `fetchTrace` function is used to fetch trace data from the API. It takes an API client and a set of parameters, including the organization slug, a query string, and the trace ID, and returns a promise that resolves to the trace data.

```tsx
  params: {
    orgSlug: string;
    query: string;
    traceId: string;
  }
): Promise<TraceSplitResults<TraceFullDetailed>> {
  return api.requestPromise(
    `/organizations/${params.orgSlug}/events-trace/${params.traceId}/?${params.query}`
  );
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/newTraceDetails/traceDrawer/traceDrawer.tsx" line="1">

---

# Rendering Trace Details

The `traceDrawer` directory contains components for the drawer UI that displays the detailed trace information. The `details` subdirectory within `traceDrawer` contains components for each type of detail, such as issues, profiling, span, and transaction.

```tsx
import {useCallback, useLayoutEffect, useMemo, useRef, useState} from 'react';
import {type Theme, useTheme} from '@emotion/react';
import styled from '@emotion/styled';
import pick from 'lodash/pick';

import type {Tag} from 'sentry/actionCreators/events';
import {Button} from 'sentry/components/button';
import {IconChevron, IconPanel, IconPin} from 'sentry/icons';
import {t} from 'sentry/locale';
import {space} from 'sentry/styles/space';
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/newTraceDetails/traceState/index.tsx" line="1">

---

# Managing Trace View State

The `traceState` directory contains components and hooks for managing the state of the trace view, including search functionality and tab management.

```tsx
import {makeCombinedReducers} from 'sentry/utils/useCombinedReducer';
import {tracePreferencesReducer} from 'sentry/views/performance/newTraceDetails/traceState/tracePreferences';
import {traceRovingTabIndexReducer} from 'sentry/views/performance/newTraceDetails/traceState/traceRovingTabIndex';
import {traceSearchReducer} from 'sentry/views/performance/newTraceDetails/traceState/traceSearch';
import {traceTabsReducer} from 'sentry/views/performance/newTraceDetails/traceState/traceTabs';

// Ensure that TS will throw an error if we forget to handle a reducer action case.
// We do this because the reducer is combined with other reducers and we want to ensure
// that we handle all possible actions from inside this reducer.
export function traceReducerExhaustiveActionCheck(_x: never): void {}
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
