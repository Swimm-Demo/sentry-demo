---
title: Basic Concepts of Timeline in Monitors
---
The Timeline in Monitors is a visual representation of the chronological sequence of events. It is implemented using various components and utilities in the 'timeline' directory under 'monitors/components'.

<SwmSnippet path="/static/app/views/monitors/components/timeline/checkInTimeline.tsx" line="33">

---

The Timeline uses a concept of 'msPerPixel' to calculate the position of check-ins on the timeline. It is calculated based on the total elapsed time and the width of the timeline.

```tsx
  const {start, end, timelineWidth} = timeWindowConfig;

  const elapsedMs = end.getTime() - start.getTime();
  const msPerPixel = elapsedMs / timelineWidth;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/monitors/components/timeline/types.tsx" line="23">

---

The 'TimeWindowConfig' interface is a crucial part of the timeline. It holds configuration details for the timeline, such as the start and end of the window, the width of the timeline, and the elapsed minutes based on the selected resolution.

```tsx
export interface TimeWindowConfig {
  /**
   * The time format used for the cursor label and job tick tooltip
   */
  dateLabelFormat: string;
  /**
   * Props to pass to <DateTime> when displaying a time marker
   */
  dateTimeProps: Partial<DateTimeProps>;
  /**
   * The elapsed minutes based on the selected resolution
   */
  elapsedMinutes: number;
  /**
   * The end of the window
   */
  end: Date;
  /**
   * Configuraton for marker intervals
   */
  intervals: MarkerIntervals;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/monitors/components/timeline/timelineCursor.tsx" line="34">

---

The 'useTimelineCursor' function is used to handle the timeline cursor's behavior. It calculates the cursor's position and updates the tooltip text based on the cursor's position.

```tsx
function useTimelineCursor<E extends HTMLElement>({
  enabled = true,
  sticky,
  labelText,
}: Options) {
  const rafIdRef = useRef<number | null>(null);

  const containerRef = useRef<E>(null);
  const labelRef = useRef<HTMLDivElement>(null);

  const [isVisible, setIsVisible] = useState(false);

  const handleMouseMove = useCallback(
    (e: MouseEvent) => {
      if (rafIdRef.current !== null) {
        window.cancelAnimationFrame(rafIdRef.current);
      }

      if (containerRef.current === null) {
        return;
      }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/monitors/components/timeline/timelineZoom.tsx" line="156">

---

The 'timelineSelector' is a part of the timeline zoom functionality. It is a visual representation of the selected area on the timeline.

```tsx
  return {selectionContainerRef: containerRef, isActive, timelineSelector};
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/monitors/components/timeline/gridLines.tsx" line="16">

---

The 'Props' interface in 'gridLines.tsx' holds the properties for the GridLineLabels component. It includes properties like 'timeWindowConfig', 'allowZoom', 'showCursor', and 'showIncidents' which control various aspects of the timeline.

```tsx
interface Props {
  timeWindowConfig: TimeWindowConfig;
  /**
   * Enable zoom selection
   */
  allowZoom?: boolean;
  className?: string;
  /**
   * Enable the timeline cursor
   */
  showCursor?: boolean;
  /**
   * Render sentry service incidents as an overlay
   */
  showIncidents?: boolean;
  /**
   * Enabling causes the cursor tooltip to stick to the top of the viewport.
   */
  stickyCursor?: boolean;
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/monitors/components/timeline/checkInTimeline.tsx" line="13">

---

# TimelineProps Interface

The TimelineProps interface is used to type the props for the CheckInTimeline component. It includes the timeWindowConfig prop which is used to configure the time window of the timeline.

```tsx
interface TimelineProps {
  timeWindowConfig: TimeWindowConfig;
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/monitors/components/timeline/checkInTimeline.tsx" line="31">

---

# CheckInTimeline Function

The CheckInTimeline function is the main component for rendering the timeline. It takes in the bucketedData, timeWindowConfig, and environment as props and uses them to calculate and render the job ticks on the timeline.

```tsx
export function CheckInTimeline(props: CheckInTimelineProps) {
  const {bucketedData, timeWindowConfig, environment} = props;
  const {start, end, timelineWidth} = timeWindowConfig;

  const elapsedMs = end.getTime() - start.getTime();
  const msPerPixel = elapsedMs / timelineWidth;

  const jobTicks = mergeBuckets(bucketedData, environment);

  return (
    <TimelineContainer>
      {jobTicks.map(jobTick => {
        const {
          startTs,
          width: tickWidth,
          envMapping,
          roundedLeft,
          roundedRight,
        } = jobTick;
        const timestampMs = startTs * 1000;
        const left = getBucketedCheckInsPosition(timestampMs, start, msPerPixel);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/monitors/components/timeline/timelineCursor.tsx" line="34">

---

# useTimelineCursor Function

The useTimelineCursor function is a custom hook used to handle the timeline cursor. It takes in options for enabling the cursor, making it sticky, and providing a label text. It returns the cursorContainerRef and the timelineCursor.

```tsx
function useTimelineCursor<E extends HTMLElement>({
  enabled = true,
  sticky,
  labelText,
}: Options) {
  const rafIdRef = useRef<number | null>(null);

  const containerRef = useRef<E>(null);
  const labelRef = useRef<HTMLDivElement>(null);

  const [isVisible, setIsVisible] = useState(false);

  const handleMouseMove = useCallback(
    (e: MouseEvent) => {
      if (rafIdRef.current !== null) {
        window.cancelAnimationFrame(rafIdRef.current);
      }

      if (containerRef.current === null) {
        return;
      }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/monitors/components/timeline/checkInTimeline.tsx" line="119">

---

# JobTick Component

The JobTick component is a styled div that represents a tick on the timeline. It takes in props for the status, whether it's rounded on the left or right, and applies styles accordingly.

```tsx
const JobTick = styled('div')<{
  roundedLeft: boolean;
  roundedRight: boolean;
  status: CheckInStatus;
}>`
  position: absolute;
  top: calc(50% + 1px);
  width: 4px;
  height: 14px;
  transform: translateY(-50%);
  opacity: 0.7;

  ${p => getTickStyle(p.status, p.theme)};

  ${p =>
    p.roundedLeft &&
    `
    border-top-left-radius: 2px;
    border-bottom-left-radius: 2px;
  `};
  ${p =>
```

---

</SwmSnippet>

# Timeline Functions

This section will explain the key functions used in the implementation of the Timeline in the monitors module.

<SwmSnippet path="/static/app/views/monitors/components/timeline/checkInTimeline.tsx" line="31">

---

## CheckInTimeline Function

The `CheckInTimeline` function is a key component of the Timeline. It takes a `CheckInTimelineProps` object as an argument, which includes data about the monitor, the time window configuration, and the environment. The function calculates the elapsed time and the milliseconds per pixel, merges the bucketed data, and returns a `TimelineContainer` that maps over the `jobTicks` to create a visual representation of the timeline.

```tsx
export function CheckInTimeline(props: CheckInTimelineProps) {
  const {bucketedData, timeWindowConfig, environment} = props;
  const {start, end, timelineWidth} = timeWindowConfig;

  const elapsedMs = end.getTime() - start.getTime();
  const msPerPixel = elapsedMs / timelineWidth;

  const jobTicks = mergeBuckets(bucketedData, environment);

  return (
    <TimelineContainer>
      {jobTicks.map(jobTick => {
        const {
          startTs,
          width: tickWidth,
          envMapping,
          roundedLeft,
          roundedRight,
        } = jobTick;
        const timestampMs = startTs * 1000;
        const left = getBucketedCheckInsPosition(timestampMs, start, msPerPixel);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/monitors/components/timeline/utils/mergeBuckets.tsx" line="25">

---

## mergeBuckets Function

The `mergeBuckets` function is used within the `CheckInTimeline` function. It takes the bucketed data and the environment as arguments and merges the buckets based on the environment. The function returns an array of `jobTicks` that represent the merged buckets.

```tsx
export function mergeBuckets(data: MonitorBucketData, environment: string) {
  const minTickWidth = 4;

  const jobTicks: JobTickData[] = [];
  data.reduce(
    (currentJobTick, bucket, i) => {
      const filteredBucket = filterMonitorStatsBucketByEnv(bucket, environment);

      const [timestamp, envMapping] = filteredBucket;
      const envMappingEmpty = isEnvMappingEmpty(envMapping);
      if (!currentJobTick) {
        return envMappingEmpty
          ? currentJobTick
          : generateJobTickFromBucket(filteredBucket, {roundedLeft: true});
      }
      const bucketStatus = getAggregateStatus(envMapping);
      const currJobTickStatus = getAggregateStatus(currentJobTick.envMapping);
      // If the current bucket is empty and our job tick has reached a min width
      if (envMappingEmpty && currentJobTick.width >= minTickWidth) {
        // Then add our current tick to the running list of job ticks to render
        currentJobTick.roundedRight = true;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/monitors/components/timeline/checkInTimeline.tsx" line="22">

---

## getBucketedCheckInsPosition Function

The `getBucketedCheckInsPosition` function is used within the `CheckInTimeline` function to calculate the position of each check-in on the timeline. It takes the timestamp, the start of the timeline, and the milliseconds per pixel as arguments, and returns the position of the check-in.

```tsx
function getBucketedCheckInsPosition(
  timestamp: number,
  timelineStart: Date,
  msPerPixel: number
) {
  const elapsedSinceStart = new Date(timestamp).getTime() - timelineStart.getTime();
  return elapsedSinceStart / msPerPixel;
}
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
