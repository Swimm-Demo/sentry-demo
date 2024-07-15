---
title: Introduction to Replay Functionality in Views
---
Replays in the Sentry-Demo application refer to the functionality that allows developers to replay specific events or issues for debugging purposes. This feature is particularly useful for understanding the sequence of actions that led to an error or performance issue.

The Replays feature is implemented across several components within the 'views' directory. The main components include the 'ReplaysList', 'ReplayTable', and 'ReplaysContainer'.

The 'ReplaysList' component fetches and displays a list of replays. It uses the 'useFetchReplayList' hook to fetch the replays and the 'ReplayTable' component to display them.

The 'ReplayTable' component is responsible for rendering the table that displays the replays. It receives the replays as a prop and maps over them to create table rows. Each row represents a replay and contains information such as the replay's OS, browser, duration, and error count.

The 'ReplaysContainer' component is a wrapper component that ensures the user has selected a project. If no project is selected, it displays a 'NoProjectMessage'.

<SwmSnippet path="/static/app/views/replays/list/replaysList.tsx" line="21">

---

# ReplaysList Component

The 'ReplaysList' component fetches and displays a list of replays. It uses the 'useFetchReplayList' hook to fetch the replays and the 'ReplayTable' component to display them.

```tsx
function ReplaysList() {
  const organization = useOrganization();

  const query = useLocationQuery({
    fields: {
      cursor: decodeScalar,
      end: decodeScalar,
      environment: decodeList,
      project: decodeList,
      query: decodeScalar,
      sort: value => decodeScalar(value, '-started_at'),
      start: decodeScalar,
      statsPeriod: decodeScalar,
      utc: decodeScalar,
    },
  });

  const {
    data: replays,
    getResponseHeader,
    isLoading,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/replays/list/replaysList.tsx" line="87">

---

# ReplayTable Component

The 'ReplayTable' component is responsible for rendering the table that displays the replays. It receives the replays as a prop and maps over them to create table rows. Each row represents a replay and contains information such as the replay's OS, browser, duration, and error count.

```tsx
    <Fragment>
      <ReplayTable
        referrerLocation={'replay'}
        fetchError={error}
        isFetching={isLoading}
        replays={replays}
        sort={decodeSorts(query.sort).at(0)}
        visibleColumns={visibleCols}
        showDropdownFilters
        emptyMessage={
          allSelectedProjectsNeedUpdates && hasReplayClick ? (
            <Fragment>
              {t('Unindexed search field')}
              <EmptyStateSubheading>
                {tct('Field [field] requires an [sdkPrompt]', {
                  field: <strong>'click'</strong>,
                  sdkPrompt: <strong>{t('SDK version >= 7.44.0')}</strong>,
                })}
              </EmptyStateSubheading>
            </Fragment>
          ) : undefined
```

---

</SwmSnippet>

# ReplaysContainer Component

The 'ReplaysContainer' component is a wrapper component that ensures the user has selected a project. If no project is selected, it displays a 'NoProjectMessage'.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
