---
title: What are Performance Trends
---
Trends in Sentry's performance monitoring platform refer to the statistical analysis of performance data over time. It is used to identify patterns and anomalies in the performance of your application.

The Trends feature provides a visual representation of the performance trends of your application. It uses various metrics such as trend percentage, trend difference, and count percentage to analyze the performance data.

Trends are calculated using a derived trend change type, which is determined based on the organization's features. This derived trend change type is then used to color-code the trend lines for better visual understanding.

The Trends feature also provides a summary view, which generates a performance event view based on the location, projects, and organization. This view is used to display the trends data.

Trends data is composed of events and projects. Each event contains data related to a specific transaction, including its trend difference, trend percentage, and count percentage.

Trends also provide the ability to change the trend function, which allows you to customize the way trends are calculated and displayed based on your specific needs.

<SwmSnippet path="/static/app/views/performance/trends/types.tsx" line="107">

---

## Trends Data

Trends data is composed of events and projects. Each event contains data related to a specific transaction, including its trend difference, trend percentage, and count percentage.

```tsx
  events: TrendsDataEvents;
  projects: Project[];
  stats: TrendsStats;
};
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/trends/content.tsx" line="88">

---

## Trend Function Change

Trends also provide the ability to change the trend function, which allows you to customize the way trends are calculated and displayed based on your specific needs.

```tsx
  handleTrendFunctionChange = (field: string) => {
    const {organization, location} = this.props;
```

---

</SwmSnippet>

# Trends Functions

This section provides an overview of the main functions used in the Trends feature.

<SwmSnippet path="/static/app/views/performance/trends/utils/index.tsx" line="154">

---

## getCurrentTrendFunction

The `getCurrentTrendFunction` function is used to get the current trend function based on the location and trend function field. It finds the trend function in the `TRENDS_FUNCTIONS` array that matches the trend function field. If no match is found, it defaults to the second function in the `TRENDS_FUNCTIONS` array.

```tsx
export function getCurrentTrendFunction(
  location: Location,
  _trendFunctionField?: TrendFunctionField
): TrendFunction {
  const trendFunctionField =
    _trendFunctionField ?? decodeScalar(location?.query?.trendFunction);
  const trendFunction = TRENDS_FUNCTIONS.find(({field}) => field === trendFunctionField);
  return trendFunction || TRENDS_FUNCTIONS[1];
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/trends/utils/generateTrendFunctionAsString.tsx" line="6">

---

## generateTrendFunctionAsString

The `generateTrendFunctionAsString` function is used to generate a string representation of the trend function. It takes the trend function field and trend parameter as arguments and returns a string that represents the trend function.

```tsx
export default function generateTrendFunctionAsString(
  trendFunction: TrendFunctionField,
  trendParameter: string
): string {
  return generateFieldAsString({
    kind: 'function',
    function: [
      trendFunction as AggregationKeyWithAlias,
      trendParameter,
      undefined,
      undefined,
    ],
  });
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/trends/utils/index.tsx" line="340">

---

## normalizeTrends

The `normalizeTrends` function is used to normalize the trends data. It takes an array of trends data and returns a new array where each trend data is normalized. The normalization process includes adding a received time for the transaction so calls to get baseline always line up with the transaction.

```tsx
/**
 * This will normalize the trends transactions while the current trend function and current data are out of sync
 * To minimize extra renders with missing results.
 */
export function normalizeTrends(
  data: Array<TrendsTransaction>
): Array<NormalizedTrendsTransaction> {
  const received_at = moment(); // Adding the received time for the transaction so calls to get baseline always line up with the transaction
  return data.map(row => {
    return {
      ...row,
      received_at,
      transaction: row.transaction,
    } as NormalizedTrendsTransaction;
  });
}
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
