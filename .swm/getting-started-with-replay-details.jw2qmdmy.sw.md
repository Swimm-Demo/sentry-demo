---
title: Getting started with Replay Details
---
Detail in Replays refers to the specific information about a replay. It includes various aspects such as network details, accessibility details, trace details, and console details. Each of these aspects is represented as a separate directory under the 'detail' directory in 'replays'.

The 'detail' in Replays also includes a 'page.tsx' file which seems to be the main component for rendering the detail page of a replay. It uses various properties like 'replayRecord', 'orgSlug', 'projectSlug', 'replayErrors', 'isVideoReplay', and 'isLoading' to manage the state and behavior of the detail page.

In the 'trace' directory under 'detail', there's a 'useReplayTraces.tsx' file which contains a custom hook for fetching the traceIds and the minimum timestamp associated with each id, for a replay record. It uses the 'replayRecord' property to fetch this data.

The 'detail' in Replays also includes other directories like 'console', 'accessibility', 'network', each containing specific details related to their respective aspects of a replay.

<SwmSnippet path="/static/app/views/replays/detail/network/details/index.tsx" line="26">

---

# Detail Tab

This code snippet shows the usage of the 'Detail' tab. The 'getParamValue' function is used to get the current tab in the detail view. Depending on the tab, different components are rendered to display the respective details.

```tsx
  projectId,
  startTimestampMs,
}: Props) {
  const {getParamValue: getDetailTab} = useUrlParams('n_detail_tab', 'details');

  if (!item || !projectId) {
    return null;
  }

  const visibleTab = getDetailTab() as TabKey;

  return (
    <Fragment>
      <DetailsSplitDivider
        isHeld={isHeld}
        onClose={onClose}
        onDoubleClick={onDoubleClick}
        onMouseDown={onMouseDown}
      >
        <NetworkDetailsTabs underlined={false} />
      </DetailsSplitDivider>
```

---

</SwmSnippet>

# Detail Directory Structure

The 'detail' directory under 'replays' contains several subdirectories, each representing a different aspect of a replay. For example, the 'network' directory contains details about the network interactions during the replay, while the 'accessibility' directory contains details about any accessibility issues encountered during the replay.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
