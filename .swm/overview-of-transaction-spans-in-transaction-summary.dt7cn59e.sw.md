---
title: Overview of Transaction Spans in Transaction Summary
---
Transaction spans in the Sentry Demo application refer to the individual units of work in a transaction. They provide a detailed view of the latency distribution and performance of each operation in a transaction. This granular information is useful in understanding where time is spent in the execution of a transaction.

The TransactionSpans component in the file 'transactionSpans/index.tsx' is responsible for rendering the spans of a transaction. It uses the 'SpansContent' component to display the content of the spans and the 'generateSpansEventView' function to generate the event view for the spans.

The 'transaction' constant in the file 'spanSummary/spanSummaryTable.tsx' is used to filter the spans based on the transaction. It is part of the filters used in the 'useSpansIndexed' hook which fetches the span data.

The 'transactionDuration' member in the file 'spanDetails/spanDetailsTable.tsx' represents the total duration of the transaction. It is used in the 'SpanDurationBar' component to calculate the width of the duration bar based on the span duration and the total transaction duration.

The 'transaction' constant in the file 'spanSummary/content.tsx' is used to fetch the span metrics. It is part of the filters used in the 'useSpanMetrics' hook which fetches the span metrics data.

The 'transaction' constant in the file 'spanSummary/spanSummaryCharts.tsx' is used to fetch the span metrics series. It is part of the filters used in the 'useSpanMetricsSeries' hook which fetches the span metrics series data.

The 'transactionId' constant in the file 'spanSummary/spanSummaryTable.tsx' is used to map the transaction duration. It is used in the 'SpanSummaryTable' component to add the transaction duration to each row of the table.

The 'transactionName' member in the file 'spanDetails/spanDetailsTable.tsx' is used to display the name of the transaction in the 'SpanTable' component.

The 'transactionName' member in the file 'suspectSpansTable.tsx' is used to display the name of the transaction in the 'SuspectSpansTable' component.

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionSpans/index.tsx" line="21">

---

# TransactionSpans Component

The TransactionSpans component is responsible for rendering the spans of a transaction. It uses the 'SpansContent' component to display the content of the spans and the 'generateSpansEventView' function to generate the event view for the spans.

```tsx
function TransactionSpans(props: Props) {
  const {location, organization, projects} = props;

  return (
    <PageLayout
      location={location}
      organization={organization}
      projects={projects}
      tab={Tab.SPANS}
      getDocumentTitle={getDocumentTitle}
      generateEventView={generateSpansEventView}
      childComponent={SpansContent}
    />
  );
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionSpans/spanSummary/spanSummaryTable.tsx" line="115">

---

# Transaction Filter

The 'transaction' constant is used to filter the spans based on the transaction. It is part of the filters used in the 'useSpansIndexed' hook which fetches the span data.

```tsx
    'span.group': groupId,
    'span.op': spanOp,
    transaction: transaction as string,
  };

  const sort = useSpanSummarySort();
  const spanSearchString = new MutableSearch(spansQuery ?? '').formatString();
  const search = MutableSearch.fromQueryObject(filters);
  search.addStringMultiFilter(spanSearchString);

  const {
    data: rowData,
    pageLinks,
    isLoading: isRowDataLoading,
  } = useSpansIndexed(
    {
      fields: [
        SpanIndexedField.ID,
        SpanIndexedField.TRANSACTION_ID,
        SpanIndexedField.TIMESTAMP,
        SpanIndexedField.SPAN_DURATION,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionSpans/spanDetails/spanDetailsTable.tsx" line="236">

---

# Transaction Duration

The 'transactionDuration' member represents the total duration of the transaction. It is used in the 'SpanDurationBar' component to calculate the width of the duration bar based on the span duration and the total transaction duration.

```tsx
type SpanDurationBarProps = {
  spanDuration: number;
  spanOp: string;
  transactionDuration: number;
};

export function SpanDurationBar(props: SpanDurationBarProps) {
  const {spanOp, spanDuration, transactionDuration} = props;
  const widthPercentage = spanDuration / transactionDuration;
  const position = widthPercentage < 0.7 ? 'right' : 'inset';

  return (
    <DurationBar>
      <div style={{width: toPercent(widthPercentage)}}>
        <Tooltip
          title={tct('[percentage] of the transaction ([duration])', {
            percentage: formatPercentage(widthPercentage),
            duration: formatTraceDuration(transactionDuration),
          })}
          containerDisplayMode="block"
        >
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionSpans/spanSummary/content.tsx" line="105">

---

# Transaction Metrics

The 'transaction' constant is used to fetch the span metrics. It is part of the filters used in the 'useSpanMetrics' hook which fetches the span metrics data.

```tsx
    'span.group': groupId,
    'span.op': spanOp,
    transaction: transactionName,
  };

  const {data: spanHeaderData} = useSpanMetrics(
    {
      search: MutableSearch.fromQueryObject(filters),
      fields: ['span.description', 'sum(span.duration)', 'count()'],
      sorts: [{field: 'sum(span.duration)', kind: 'desc'}],
    },
    SpanSummaryReferrer.SPAN_SUMMARY_HEADER_DATA
  );

  // Average span duration must be queried for separately, since it could get broken up into multiple groups if used in the first query
  const {data: avgDurationData} = useSpanMetrics(
    {
      search: MutableSearch.fromQueryObject(filters),
      fields: ['avg(span.duration)'],
    },
    SpanSummaryReferrer.SPAN_SUMMARY_HEADER_DATA
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionSpans/spanDetails/spanDetailsTable.tsx" line="49">

---

# Transaction Name

The 'transactionName' member is used to display the name of the transaction in the 'SpanTable' component.

```tsx
  isLoading: boolean;
  location: Location;
  organization: Organization;
  transactionName: string;
  pageLinks?: string | null;
  project?: Project;
  suspectSpan?: SuspectSpan;
};

export default function SpanTable(props: Props) {
  const {
    location,
    organization,
    project,
    examples,
    suspectSpan,
    isLoading,
    pageLinks,
    transactionName,
  } = props;

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionSpans/suspectSpansTable.tsx" line="26">

---

# Transaction Name in SuspectSpansTable

The 'transactionName' member is used to display the name of the transaction in the 'SuspectSpansTable' component.

```tsx
  sort: SpanSort;
  suspectSpans: SuspectSpans;
  totals: SpansTotalValues | null;
  transactionName: string;
  project?: Project;
};

export default function SuspectSpansTable(props: Props) {
  const {
    location,
    organization,
    transactionName,
    isLoading,
    suspectSpans,
    totals,
    sort,
    project,
  } = props;

  const data: TableDataRowWithExtras[] = suspectSpans.map(suspectSpan => ({
    operation: suspectSpan.op,
```

---

</SwmSnippet>

# Transaction Spans Functions

This section will explain the main functions related to transaction spans in the Sentry Demo application.

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionSpans/index.tsx" line="21">

---

## TransactionSpans

The TransactionSpans component is responsible for rendering the spans of a transaction. It uses the 'SpansContent' component to display the content of the spans and the 'generateSpansEventView' function to generate the event view for the spans.

```tsx
function TransactionSpans(props: Props) {
  const {location, organization, projects} = props;

  return (
    <PageLayout
      location={location}
      organization={organization}
      projects={projects}
      tab={Tab.SPANS}
      getDocumentTitle={getDocumentTitle}
      generateEventView={generateSpansEventView}
      childComponent={SpansContent}
    />
  );
}

function getDocumentTitle(transactionName: string): string {
  const hasTransactionName =
    typeof transactionName === 'string' && String(transactionName).trim().length > 0;

  if (hasTransactionName) {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionSpans/spanSummary/spanSummaryTable.tsx" line="126">

---

## useSpansIndexed

The 'useSpansIndexed' hook is used to fetch the span data. The 'transaction' constant is part of the filters used in this hook to filter the spans based on the transaction.

```tsx
    data: rowData,
    pageLinks,
    isLoading: isRowDataLoading,
  } = useSpansIndexed(
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionSpans/spanDetails/spanDetailsTable.tsx" line="242">

---

## SpanDurationBar

The SpanDurationBar component is used to display the duration of a span as a bar. The 'transactionDuration' member represents the total duration of the transaction and is used to calculate the width of the duration bar based on the span duration and the total transaction duration.

```tsx
export function SpanDurationBar(props: SpanDurationBarProps) {
  const {spanOp, spanDuration, transactionDuration} = props;
  const widthPercentage = spanDuration / transactionDuration;
  const position = widthPercentage < 0.7 ? 'right' : 'inset';

  return (
    <DurationBar>
      <div style={{width: toPercent(widthPercentage)}}>
        <Tooltip
          title={tct('[percentage] of the transaction ([duration])', {
            percentage: formatPercentage(widthPercentage),
            duration: formatTraceDuration(transactionDuration),
          })}
          containerDisplayMode="block"
        >
          <DurationBarSection style={{backgroundColor: pickBarColor(spanOp)}}>
            <DurationPill durationDisplay={position} showDetail={false}>
              <PerformanceDuration abbreviation milliseconds={spanDuration} />
            </DurationPill>
          </DurationBarSection>
        </Tooltip>
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionSpans/spanSummary/content.tsx" line="147">

---

## useSpanMetrics

The 'useSpanMetrics' hook is used to fetch the span metrics data. The 'transaction' constant is part of the filters used in this hook to filter the span metrics based on the transaction.

```tsx
  if (!data || data.length === 0) {
    return undefined;
  }

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionSpans/spanSummary/spanSummaryCharts.tsx" line="147">

---

## useSpanMetricsSeries

The 'useSpanMetricsSeries' hook is used to fetch the span metrics series data. The 'transaction' constant is part of the filters used in this hook to filter the span metrics series based on the transaction.

```tsx
            error={throughputError}
            chartColors={[THROUGHPUT_COLOR]}
            tooltipFormatterOptions={{
              valueFormatter: value => formatRate(value, RateUnit.PER_MINUTE),
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/transactionSummary/transactionSpans/spanSummary/spanSummaryTable.tsx" line="101">

---

## SpanSummaryTable

The SpanSummaryTable component is used to display a table of spans. The 'transactionId' constant is used to map the transaction duration. It is used in this component to add the transaction duration to each row of the table.

```tsx
export default function SpanSummaryTable(props: Props) {
  const {project} = props;
  const organization = useOrganization();
  const supportedTags = useSpanFieldSupportedTags();
  const {spanSlug} = useParams();
  const navigate = useNavigate();
  const [spanOp, groupId] = spanSlug.split(':');

  const location = useLocation();
  const {transaction} = location.query;
  const spansCursor = decodeScalar(location.query?.[QueryParameterNames.SPANS_CURSOR]);
  const spansQuery = decodeScalar(location.query.spansQuery);

  const filters: SpanMetricsQueryFilters = {
    'span.group': groupId,
    'span.op': spanOp,
    transaction: transaction as string,
  };

  const sort = useSpanSummarySort();
  const spanSearchString = new MutableSearch(spansQuery ?? '').formatString();
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
