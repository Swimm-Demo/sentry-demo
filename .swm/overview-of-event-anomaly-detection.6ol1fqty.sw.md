---
title: Overview of Event Anomaly Detection
---
The Event Statistical Detector in Sentry is a mechanism that helps in identifying and analyzing anomalies or significant changes in event data. It is primarily used to detect regressions in performance metrics such as duration and throughput.

The detector operates by comparing event data over different periods. It uses statistical methods to identify significant changes or outliers in the data, which could indicate a performance regression.

The Event Statistical Detector is implemented across several components in the Sentry application. These components include event comparison, event throughput, regression message, and others. Each of these components plays a specific role in the detection and presentation of statistical anomalies.

For example, the event comparison component is responsible for comparing different events and highlighting the differences. The event throughput component, on the other hand, is used to calculate and display the throughput of events.

The regression message component is used to display messages related to detected regressions. It uses the data provided by the Event Statistical Detector to generate meaningful messages for the user.

Overall, the Event Statistical Detector is a crucial part of Sentry's performance monitoring capabilities. It provides valuable insights into the performance of the application and helps in identifying potential issues early.

<SwmSnippet path="/static/app/components/events/eventStatisticalDetector/eventComparison/index.tsx" line="1">

---

# Event Comparison Component

The event comparison component is responsible for comparing different events and highlighting the differences. It uses the data provided by the Event Statistical Detector to generate meaningful messages for the user.

```tsx
import {useMemo} from 'react';
import styled from '@emotion/styled';
import moment from 'moment';

import {EventDataSection} from 'sentry/components/events/eventDataSection';
import {EventDisplay} from 'sentry/components/events/eventStatisticalDetector/eventComparison/eventDisplay';
import {t} from 'sentry/locale';
import {space} from 'sentry/styles/space';
import type {Event, Project} from 'sentry/types';

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/eventStatisticalDetector/eventThroughput.tsx" line="198">

---

# Event Throughput Component

The event throughput component is used to calculate and display the throughput of events. It uses the `useThroughputStats` function to gather the necessary data for this calculation.

```tsx
function useThroughputStats({datetime, event, group}: UseThroughputStatsOptions) {
  const location = useLocation();
  const organization = useOrganization();

  const evidenceData = event.occurrence!.evidenceData;

  const statsType = getStatsType(group);

  // START Functions ====================

  const functionStats = useProfileEventsStats({
    dataset: 'profileFunctions',
    datetime,
    query: `fingerprint:${evidenceData?.fingerprint}`,
    referrer: 'api.profiling.functions.regression.stats',
    yAxes: ['count()'],
    // only make query if statsType matches
    enabled: statsType === 'functions',
  });

  const functionInterval = useMemo(() => {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/eventStatisticalDetector/regressionMessage.tsx" line="1">

---

# Regression Message Component

The regression message component is used to display messages related to detected regressions. It uses the data provided by the Event Statistical Detector to generate meaningful messages for the user.

```tsx
import {useMemo} from 'react';
import styled from '@emotion/styled';

import {LinkButton} from 'sentry/components/button';
import {DateTime} from 'sentry/components/dateTime';
import {DataSection} from 'sentry/components/events/styles';
import Link from 'sentry/components/links/link';
import PerformanceDuration from 'sentry/components/performanceDuration';
import {Tooltip} from 'sentry/components/tooltip';
import {IconOpen} from 'sentry/icons';
```

---

</SwmSnippet>

# Event Statistical Detector Functions

In this section, we will discuss the main functions of the Event Statistical Detector and how they contribute to the detection and analysis of performance regressions.

<SwmSnippet path="/static/app/components/events/eventStatisticalDetector/regressionMessage.tsx" line="30">

---

## EventStatisticalDetectorMessage

The `EventStatisticalDetectorMessage` function is the main entry point for the Event Statistical Detector. It takes an event and a group as arguments and determines the type of issue. Depending on the issue type, it either returns a `EventStatisticalDetectorRegressedPerformanceMessage` or a `EventStatisticalDetectorRegressedFunctionMessage`.

```tsx
function EventStatisticalDetectorMessage({
  event,
  group,
}: EventStatisticalDetectorMessageProps) {
  switch (group.issueType) {
    case IssueType.PERFORMANCE_DURATION_REGRESSION:
    case IssueType.PERFORMANCE_ENDPOINT_REGRESSION: {
      return (
        <EventStatisticalDetectorRegressedPerformanceMessage
          event={event}
          group={group}
        />
      );
    }
    case IssueType.PROFILE_FUNCTION_REGRESSION_EXPERIMENTAL:
    case IssueType.PROFILE_FUNCTION_REGRESSION: {
      return (
        <EventStatisticalDetectorRegressedFunctionMessage event={event} group={group} />
      );
    }
    default: {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/eventStatisticalDetector/regressionMessage.tsx" line="56">

---

## EventStatisticalDetectorRegressedPerformanceMessage

The `EventStatisticalDetectorRegressedPerformanceMessage` function is used when the issue type is a performance regression. It calculates the performance metrics before and after the regression and generates a message detailing the changes.

```tsx
function EventStatisticalDetectorRegressedPerformanceMessage({
  event,
}: EventStatisticalDetectorMessageProps) {
  const now = useMemo(() => new Date(), []);

  const organization = useOrganization();

  const {transaction, breakpoint, aggregateRange1, aggregateRange2, trendPercentage} =
    event?.occurrence?.evidenceData ?? {};

  const {end: afterDateTime} = useRelativeDateTime({
    anchor: breakpoint,
    relativeDays: 14,
  });

  const transactionSummaryLink = transactionSummaryRouteWithQuery({
    orgSlug: organization.slug,
    transaction,
    query: {},
    trendFunction: 'p95',
    projectID: event.projectID,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/eventStatisticalDetector/regressionMessage.tsx" line="132">

---

## EventStatisticalDetectorRegressedFunctionMessage

The `EventStatisticalDetectorRegressedFunctionMessage` function is used when the issue type is a function regression. It calculates the function metrics before and after the regression and generates a message detailing the changes.

```tsx
function EventStatisticalDetectorRegressedFunctionMessage({
  event,
}: EventStatisticalDetectorMessageProps) {
  const evidenceData = event?.occurrence?.evidenceData;
  const absoluteChange = evidenceData?.trendDifference;
  const percentageChange = evidenceData?.trendPercentage;
  const detectionTime = new Date(evidenceData?.breakpoint * 1000);
  const functionName = evidenceData?.function as string;

  return (
    <DataSection>
      <div style={{display: 'inline'}}>
        {tct(
          '[functionName] had [change] in duration (P95) from [before] to [after] around [date] at [time]. The example profiles may indicate what changed in the regression.',
          {
            functionName: <code>{functionName}</code>,
            change:
              defined(absoluteChange) && defined(percentageChange)
                ? t(
                    'a %s (%s) increase',
                    <PerformanceDuration abbreviation nanoseconds={absoluteChange} />,
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
