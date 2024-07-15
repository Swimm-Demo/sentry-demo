---
title: What is Trace Details in Performance Monitoring
---
Trace details in Sentry's Performance monitoring platform provide a deep dive into the performance of individual traces. A trace is a representation of a request as it moves through the various services in a system. Trace details provide a waterfall view of the trace, showing the hierarchy and timing data of all transactions within the trace. This view can help developers identify slow parts in a trace that might be responsible for overall slow performance. The trace details view also includes any errors or performance issues that occurred during the trace, providing a comprehensive view of problems that might affect user experience.

<SwmSnippet path="/static/app/views/performance/traceDetails/newTraceDetailsContent.tsx" line="51">

---

Here we define the properties for the Trace Details view. It includes metadata about the trace, the organization, the trace event view, the trace slug, and any orphan errors. The `handleLimitChange` function is used to handle changes in the limit of displayed transactions.

```tsx
type Props = Pick<RouteComponentProps<{traceSlug: string}, {}>, 'params' | 'location'> & {
  dateSelected: boolean;
  error: QueryError | null;
  isLoading: boolean;
  meta: TraceMeta | null;
  organization: Organization;
  traceEventView: EventView;
  traceSlug: string;
  traces: TraceTree.Transaction[] | null;
  handleLimitChange?: (newLimit: number) => void;
  orphanErrors?: TraceError[];
};
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/traceDetails/newTraceDetailsTraceView.tsx" line="58">

---

This is the main Trace View component. It takes the same properties as the Trace Details view and renders the trace in a waterfall view. The `onRowClick` function is used to handle clicks on individual transactions within the trace.

```tsx
type Props = Pick<RouteComponentProps<{}, {}>, 'location'> & {
  meta: TraceMeta | null;
  onRowClick: (detailKey: EventDetail | SpanDetailProps | undefined) => void;
  organization: Organization;
  rootEvent: EventTransaction | undefined;
  traceEventView: EventView;
  traceSlug: string;
  traceType: TraceType;
  traces: TraceTree.Transaction[];
  filteredEventIds?: Set<string>;
  handleLimitChange?: (newLimit: number) => void;
  orphanErrors?: TraceError[];
  traceInfo?: TraceInfo;
};
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/traceDetails/newTraceDetailsContent.tsx" line="79">

---

In the Trace Details content component, we use the trace information to render the trace header and the trace itself. The `getTraceType` function is used to determine the type of the trace, which can affect how the trace is displayed.

```tsx
function NewTraceDetailsContent(props: Props) {
  const router = useRouter();
  const [detail, setDetail] = useState<EventDetail | SpanDetailProps | undefined>(
    undefined
  );
  const traceInfo = useMemo(
    () => getTraceInfo(props.traces ?? [], props.orphanErrors),
    [props.traces, props.orphanErrors]
  );
  const root = props.traces?.[0];
  const {data: rootEvent, isLoading: isRootEventLoading} = useApiQuery<EventTransaction>(
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/traceDetails/newTraceDetailsTraceView.tsx" line="185">

---

# TraceInfo

`traceInfo` is a property of the transaction object that contains information about the trace. It includes details about the children transactions, event id, and visibility status of the transaction. It is used in the `renderTransaction` function to generate the trace view.

```tsx
      isLast: boolean;
      isOrphan: boolean;
      numberOfHiddenTransactionsAbove: number;
      traceInfo: TraceInfo;
    }
  ) {
    const {children, event_id: eventId} = transaction;
    // Add 1 to the generation to make room for the "root trace"
    const generation = transaction.generation + 1;

    const isVisible = isRowVisible(transaction, filteredEventIds);

    const accumulated: AccType = children.reduce(
      (acc: AccType, child: TraceFullDetailed, idx: number) => {
        const isLastChild = idx === children.length - 1;
        const hasChildren = child.children.length > 0;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/traceDetails/newTraceDetailsTraceView.tsx" line="389">

---

# TraceView

`traceView` is a React component that represents the trace details view. It includes the `TraceViewHeader` and `TraceViewHeaderContainer` components, which display information about the trace and its transactions. The `traceView` is returned by the `TraceView` function and is used to render the trace details view.

```tsx
      ? getMeasurements(traces[0], bounds)
      : undefined;

  const traceView = (
    <TraceDetailBody>
      <DividerHandlerManager.Provider interactiveLayerRef={traceViewRef}>
        <DividerHandlerManager.Consumer>
          {({dividerPosition}) => (
            <ScrollbarManager.Provider
              dividerPosition={dividerPosition}
              interactiveLayerRef={virtualScrollbarContainerRef}
              isEmbedded
            >
              <StyledTracePanel>
                <TraceViewHeader
                  traceInfo={traceInfo}
                  traceType={traceType}
                  traceViewHeaderRef={traceViewRef}
                  organization={organization}
                  event={props.rootEvent}
                />
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/traceDetails/newTraceDetailsContent.tsx" line="81">

---

# Detail

`detail` is a state variable in the `NewTraceDetailsContent` function that holds the details of the event or span that is currently selected. It is used to display the details of the selected event or span in the trace details view.

```tsx
  const [detail, setDetail] = useState<EventDetail | SpanDetailProps | undefined>(
    undefined
  );
  const traceInfo = useMemo(
    () => getTraceInfo(props.traces ?? [], props.orphanErrors),
    [props.traces, props.orphanErrors]
  );
  const root = props.traces?.[0];
  const {data: rootEvent, isLoading: isRootEventLoading} = useApiQuery<EventTransaction>(
    [
      `/organizations/${props.organization.slug}/events/${root?.project_slug}:${root?.event_id}/`,
      {
        query: {
          referrer: 'trace-details-summary',
        },
      },
    ],
    {
      staleTime: Infinity,
      enabled: !!(props.traces && props.traces.length > 0),
    }
```

---

</SwmSnippet>

# Trace Details Functions

This section will cover the main functions used in the Trace Details functionality of Sentry's Performance monitoring platform.

<SwmSnippet path="/static/app/views/performance/traceDetails/utils.tsx" line="130">

---

## getTraceInfo

The `getTraceInfo` function is used to gather information about a trace. It takes an array of traces and orphan errors as input and returns an object containing information about the trace such as the number of errors, performance issues, transactions, and the start and end timestamps of the trace.

```tsx
export function getTraceInfo(
  traces: TraceFullDetailed[] = [],
  orphanErrors: TraceError[] = []
) {
  const initial = {
    projects: new Set<string>(),
    errors: new Set<string>(),
    performanceIssues: new Set<string>(),
    transactions: new Set<string>(),
    startTimestamp: Number.MAX_SAFE_INTEGER,
    endTimestamp: 0,
    maxGeneration: 0,
    trailingOrphansCount: 0,
  };

  const transactionsInfo = traces.reduce(
    (info: TraceInfo, trace: TraceFullDetailed) =>
      reduceTrace<TraceInfo>(trace, transactionVisitor(), info),
    initial
  );

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/traceDetails/utils.tsx" line="169">

---

## isRootTransaction

The `isRootTransaction` function is a helper function used to determine if a given transaction is a root transaction. A root transaction is a transaction that has no parent. This function returns a boolean value indicating whether the given transaction is a root transaction.

```tsx
export function isRootTransaction(trace: TraceFullDetailed): boolean {
  // Root transactions has no parent_span_id
  return trace.parent_span_id === null;
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/traceDetails/utils.tsx" line="42">

---

## getTraceDetailsUrl

The `getTraceDetailsUrl` function is used to generate the URL for the trace details page. It takes an object containing the organization, trace slug, date selection, timestamp, and event ID as input and returns a URL object.

```tsx
  const queryParams = {
    ...location.query,
    statsPeriod,
    [PAGE_URL_PARAM.PAGE_START]: start,
    [PAGE_URL_PARAM.PAGE_END]: end,
  };

  if (organization.features.includes('trace-view-v1')) {
    if (spanId) {
      queryParams.node = [`span-${spanId}`, `txn-${eventId}`];
    }
    return {
      pathname: normalizeUrl(
        `/organizations/${organization.slug}/performance/trace/${traceSlug}/`
      ),
      query: {
        ...queryParams,
        timestamp: getTimeStampFromTableDateField(timestamp),
        eventId,
        demo,
        source,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/organizations/pageFilters/parse.tsx" line="203">

---

## normalizeDateTimeParams

The `normalizeDateTimeParams` function is used to normalize the DateTime components of the page filters. It takes the page filter parameters and an options object as input and returns a normalized version of the DateTime parameters.

```tsx
/**
 * Normalizes the DateTime components of the page filters.
 *
 * NOTE: This has some additional functionality for handling `page*` filters
 *       that will override the standard `start`/`end`/`statsPeriod` filters.
 *
 * NOTE: This does *NOT* normalize the `project` or `environment` components of
 *       the page filter parameters. See `getStateFromQuery` for normalization
 *       of the project and environment parameters.
 */
export function normalizeDateTimeParams(
  params: InputParams,
  options: DateTimeNormalizeOptions = {}
): ParsedParams {
  const {
    allowEmptyPeriod = false,
    allowAbsoluteDatetime = true,
    allowAbsolutePageDatetime = false,
    defaultStatsPeriod = DEFAULT_STATS_PERIOD,
  } = options;

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/queryClient.tsx" line="121">

---

## useApiQuery

The `useApiQuery` function is a wrapper around React Query's useQuery function. It takes a query key and options as input and returns the result of the query. This function is used to execute the request using the query key URL.

```tsx
export function useApiQuery<TResponseData, TError = RequestError>(
  queryKey: ApiQueryKey,
  options: UseApiQueryOptions<TResponseData, TError>
): UseApiQueryResult<TResponseData, TError> {
  const api = useApi({persistInFlight: PERSIST_IN_FLIGHT});
  const queryFn = fetchDataQuery(api);

  const {data, ...rest} = useQuery(queryKey, queryFn, options);

  const queryResult = {
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
