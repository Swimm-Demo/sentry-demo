---
title: What is Span Processing
---
Spans in the Sentry demo repository refer to the segments of a trace. They represent a set of operations or tasks within a transaction. Each span has a start time, end time, and metadata to describe the operation. Spans can be nested, forming a tree structure, and each span can have zero or more spans as its children. This structure allows for detailed, hierarchical tracing of how transactions are processed in the system.

<SwmSnippet path="/static/app/components/events/interfaces/spans/index.tsx" line="88">

---

This is the main function for the Spans interface. It takes in an event and organization as props, and uses these to parse the trace and create a waterfall model. The waterfall model is then used to filter and track analytics for the spans. The function returns a container with the trace errors and the span search bar.

```tsx
function SpansInterface({event, affectedSpanIds, organization}: Props) {
  const parsedTrace = useMemo(() => parseTrace(event), [event]);
  const waterfallModel = useMemo(
    () => new WaterfallModel(event, affectedSpanIds),
    [event, affectedSpanIds]
  );

  const handleSpanFilter = (searchQuery: string) => {
    waterfallModel.querySpanSearch(searchQuery);

    trackAnalytics('performance_views.event_details.search_query', {
      organization,
    });
  };

  return (
    <Container hasErrors={!isEmptyObject(event.errors)}>
      <QuickTraceContext.Consumer>
        {quickTrace => {
          const errors: TraceError[] | undefined =
            quickTrace?.currentEvent && !isTraceError(quickTrace?.currentEvent)
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/spans/spanContext.tsx" line="1">

---

This file defines the SpanContext, which provides functions for managing the expanded state of spans. It includes functions to add and remove expanded spans, check if a span is expanded, and mark if an anchored span is mounted.

```tsx
import {Component, createContext} from 'react';

import type {ProcessedSpanType} from './types';

export type SpanContextProps = {
  addExpandedSpan: (span: Readonly<ProcessedSpanType>, callback?: () => void) => void;
  didAnchoredSpanMount: () => boolean;
  isSpanExpanded: (span: Readonly<ProcessedSpanType>) => boolean;
  markAnchoredSpanIsMounted: () => void;
  removeExpandedSpan: (span: Readonly<ProcessedSpanType>, callback?: () => void) => void;
};

const SpanContext = createContext<SpanContextProps>({
  didAnchoredSpanMount: () => false,
  markAnchoredSpanIsMounted: () => undefined,
  addExpandedSpan: () => undefined,
  removeExpandedSpan: () => undefined,
  isSpanExpanded: () => false,
});

type Props = {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/spans/types.tsx" line="26">

---

This is the definition of the SpanDatabaseAttributes interface. It represents the database-related attributes of a span, such as the name, operation, system, and user of the database.

```tsx
interface SpanDatabaseAttributes {
  'db.name'?: string;
  'db.operation'?: string;
  'db.system'?: string;
  'db.user'?: string;
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/spans/types.tsx" line="194">

---

This is the definition of the RawSpanType interface. It includes a data field that combines SpanSourceCodeAttributes and SpanDatabaseAttributes, along with other span properties.

```tsx
  op: string;
  rootSpanID: string;
  rootSpanStatus: string | undefined;
  spans: SpanType[];
  traceEndTimestamp: number;
  traceID: string;
  traceStartTimestamp: number;
  count?: number;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/spans/spanTree.tsx" line="44">

---

This file defines the SpanTree component. It manages the rendering of the span tree, including handling scrolling, toggling span trees, and rendering span rows. It also includes logic for determining which spans are visible and should be rendered.

```tsx
type PropType = ScrollbarManagerChildrenProps & {
  dragProps: DragManagerChildrenProps;
  filterSpans: FilterSpans | undefined;
  operationNameFilters: ActiveOperationFilter;
  organization: Organization;
  spanContextProps: SpanContext.SpanContextProps;
  spans: EnhancedProcessedSpanType[];
  traceViewHeaderRef: React.RefObject<HTMLDivElement>;
  traceViewRef: React.RefObject<HTMLDivElement>;
  waterfallModel: WaterfallModel;
  focusedSpanIds?: Set<string>;
};

type StateType = {
  headerPos: number;
  spanRows: Record<string, {spanRow: React.RefObject<HTMLDivElement>; treeDepth: number}>;
};

const listRef = createRef<ReactVirtualizedList>();

class SpanTree extends Component<PropType> {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/spans/spanBar.tsx" line="176">

---

This file defines the SpanBar component. It handles the rendering of individual span bars in the span tree, including the display of span details and error badges. It also manages the state of whether the span details are shown or hidden.

```tsx
export class SpanBar extends Component<SpanBarProps, SpanBarState> {
  state: SpanBarState = {
    showDetail: false,
  };

  componentDidMount() {
    this._mounted = true;
    if (this.spanRowDOMRef.current) {
      this.props.storeSpanBar(this);
      this.connectObservers();
    }

    if (this.spanTitleRef.current) {
      this.spanTitleRef.current.addEventListener('wheel', this.handleWheel, {
        passive: false,
      });
    }

    // On mount, it is necessary to set the left styling of the content here due to the span tree being virtualized.
    // If we rely on the scrollBarManager to set the styling, it happens too late and awkwardly applies an animation.
    if (this.spanContentRef) {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/spans/aggregateSpans.tsx" line="21">

---

This file defines the AggregateSpans component. It fetches and displays aggregate span data for a given transaction. It uses the SpanWaterfallModel to generate a waterfall view of the spans.

```tsx
type SpanSamples = Array<[string, string]>;

type AggregateSpanRow = {
  'avg(absolute_offset)': number;
  'avg(duration)': number;
  'avg(exclusive_time)': number;
  'count()': number;
  description: string;
  group: string;
  is_segment: number;
  node_fingerprint: string;
  parent_node_fingerprint: string;
  samples: SpanSamples;
  start_ms: number;
};

const ALLOWED_BACKENDS = ['indexedSpans', 'nodestore'];

export function useAggregateSpans({
  transaction,
  httpMethod,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/spans/index.tsx" line="207">

---

# Span Creation

Here we see the creation of a Span component, which is used to represent a span in the user interface.

```tsx
export const Spans = withOrganization(SpansInterface);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/spans/spanDetail.tsx" line="108">

---

# Span Usage

Here we see how the `projects` constant is used to find a specific project based on the `projectID` of an event.

```tsx
  const {projects} = useProjects();
  const project = projects.find(p => p.id === props.event.projectID);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/spans/spanBar.tsx" line="141">

---

# Span Count

The `numOfSpans` member is used to keep track of the number of span children. This is used for display purposes in the user interface.

```tsx
  numOfSpanChildren: number;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/spans/spanDetail.tsx" line="114">

---

# Span Details

Here we see how the details of a span, such as its operation and origin, are tracked for analytics purposes.

```tsx
    const {span, organization, event} = props;
    if (!('op' in span)) {
      return;
    }

    trackAnalytics('performance_views.event_details.open_span_details', {
      organization,
      operation: span.op ?? 'undefined',
      origin: span.origin ?? 'undefined',
      project_platform: event.platform ?? 'undefined',
    });
```

---

</SwmSnippet>

# Understanding Spans

This section provides an overview of the key functions related to Spans in the Sentry demo repository.

<SwmSnippet path="/static/app/components/events/interfaces/spans/utils.tsx" line="250">

---

## generateRootSpan

The `generateRootSpan` function creates a root span for a given trace. The root span includes various properties such as trace ID, span ID, start and end timestamps, operation name, description, and other data related to the trace. This function is crucial for initializing the root span of a trace, which serves as the parent for all other spans in the trace.

```tsx
export function generateRootSpan(
  trace: ParsedTraceType
): RawSpanType | AggregateSpanType {
  const rootSpan = {
    trace_id: trace.traceID,
    span_id: trace.rootSpanID,
    parent_span_id: trace.parentSpanID,
    start_timestamp: trace.traceStartTimestamp,
    timestamp: trace.traceEndTimestamp,
    op: trace.op,
    description: trace.description,
    data: {},
    status: trace.rootSpanStatus,
    hash: trace.hash,
    exclusive_time: trace.exclusiveTime,
    count: trace.count,
    frequency: trace.frequency,
    total: trace.total,
  };

  return rootSpan;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/spans/utils.tsx" line="399">

---

## getSpanSubTimings

The `getSpanSubTimings` function retrieves the sub-timings for a given span. Sub-timings represent different segments of the span's total duration. This function is used to break down a span's duration into smaller segments, providing more detailed insights into the span's execution.

```tsx
  if (span.type) {
    return null; // narrow to RawSpanType
  }
  const op = getSpanOperation(span);
  if (!op) {
    return null;
  }
  const timingDefinitions = SPAN_SUB_TIMINGS[op];
  if (!timingDefinitions) {
    return null;
  }

  const timings: SubTimingInfo[] = [];
  const spanStart = subTimingMarkToTime(span, SpanSubTimingMark.SPAN_START);
  const spanEnd = subTimingMarkToTime(span, SpanSubTimingMark.SPAN_END);

  const TEN_MS = 0.001;

  for (const def of timingDefinitions) {
    const start = subTimingMarkToTime(span, def.startMark);
    const end = subTimingMarkToTime(span, def.endMark);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/spans/utils.tsx" line="520">

---

## parseTrace

The `parseTrace` function processes a trace and its spans. It initializes a parsed trace object with properties such as operation name, child spans, start and end timestamps, trace ID, and other trace-related data. It then reduces the spans in the trace, adding them to the parsed trace object. This function is essential for processing and preparing a trace and its spans for further analysis or visualization.

```tsx
  const init: ParsedTraceType = {
    op: rootSpanOpName,
    childSpans: {},
    traceStartTimestamp: event.startTimestamp,
    traceEndTimestamp: event.endTimestamp,
    traceID,
    rootSpanID,
    rootSpanStatus,
    parentSpanID,
    spans,
    description,
    hash,
    exclusiveTime,
    count,
    frequency,
    total,
  };

  const reduced: ParsedTraceType = spans.reduce((acc, inputSpan) => {
    let span: SpanType = inputSpan;

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/spans/newTraceDetailsSpanTree.tsx" line="979">

---

## hasAllSpans

The `hasAllSpans` function checks if a trace contains all of its spans. It uses a heuristic that favors false negatives over false positives, meaning it's more likely to indicate that a trace doesn't have all its spans when it actually does. This function is used to warn users when a trace might be missing some spans.

```tsx
function hasAllSpans(trace: ParsedTraceType): boolean {
  const {traceEndTimestamp, spans} = trace;
  if (spans.length < 999) {
    return true;
  }

  const lastSpan = spans.reduce((latest, span) =>
    latest.timestamp > span.timestamp ? latest : span
  );
  const missingDuration = traceEndTimestamp - lastSpan.timestamp;

  return missingDuration < 0.1;
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/spans/utils.tsx" line="608">

---

## sortSpans

The `sortSpans` function sorts spans based on their start timestamps. It's used to order spans chronologically, which is crucial for accurately representing the sequence of operations in a trace.

```tsx
function sortSpans(firstSpan: SpanType, secondSpan: SpanType) {
  // orphan spans come after non-orphan spans.

  if (isOrphanSpan(firstSpan) && !isOrphanSpan(secondSpan)) {
    // sort secondSpan before firstSpan
    return 1;
  }

  if (!isOrphanSpan(firstSpan) && isOrphanSpan(secondSpan)) {
    // sort firstSpan before secondSpan
    return -1;
  }

  // sort spans by their start timestamp in ascending order

  if (firstSpan.start_timestamp < secondSpan.start_timestamp) {
    // sort firstSpan before secondSpan
    return -1;
  }

  if (firstSpan.start_timestamp === secondSpan.start_timestamp) {
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
