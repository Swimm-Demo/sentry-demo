---
title: Understanding Issue Details Views
---
Issue details in the Sentry demo application refer to the specific information and data related to an error or issue that has been tracked and logged by the Sentry system. This includes data such as the error message, stack trace, the file and line number where the error occurred, and other relevant data. The issue details are used to help developers understand the cause of the error and how to fix it.

The issue details are displayed in various views within the application. For example, in the 'groupDetails' view, the details of a specific issue group are displayed. This includes the use of analytics to track when the issue details are viewed. In the 'groupRelatedIssues' and 'groupSimilarIssues' views, the application fetches and displays issues that are related or similar to the current issue, helping developers understand if the error is part of a larger problem.

In the 'groupEventDetails' view, the details of a specific event within an issue group are displayed. This includes the event's stack trace, tags, user feedback, and other relevant data. The 'groupMerged' view displays the details of issues that have been merged into the current issue group.

The 'actions' view allows developers to perform various actions on the issue, such as sharing the issue, subscribing to updates, or merging the issue with others. The 'participantList' component displays a list of users and teams who are participating in the resolution of the issue.

<SwmSnippet path="/static/app/views/issueDetails/groupDetails.tsx" line="551">

---

# Issue Details in groupDetails View

In the 'groupDetails' view, the details of a specific issue group are displayed. This includes the use of analytics to track when the issue details are viewed.

```tsx
  const groupEventType = useLoadedEventType();
  const user = useUser();

  useRouteAnalyticsEventNames('issue_details.viewed', 'Issue Details: Viewed');
  useRouteAnalyticsParams({
    ...getAnalyticsDataForGroup(group),
    ...getAnalyticsDataForEvent(event),
    ...getAnalyicsDataForProject(project),
    tab,
    stream_index: typeof stream_index === 'string' ? Number(stream_index) : undefined,
    query: typeof query === 'string' ? query : undefined,
    // Alert properties track if the user came from email/slack alerts
    alert_date:
      typeof alert_date === 'string' ? getUtcDateString(Number(alert_date)) : undefined,
    alert_rule_id: typeof alert_rule_id === 'string' ? alert_rule_id : undefined,
    alert_type: typeof alert_type === 'string' ? alert_type : undefined,
    ref_fallback,
    group_event_type: groupEventType,
    has_hierarchical_grouping:
      !!organization.features?.includes('grouping-stacktrace-ui') &&
      !!(event?.metadata?.current_tree_label || event?.metadata?.finest_tree_label),
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/issueDetails/groupEventDetails/groupEventDetailsContent.tsx" line="266">

---

# Issue Details in groupEventDetails View

In the 'groupEventDetails' view, the details of a specific event within an issue group are displayed. This includes the event's stack trace, tags, user feedback, and other relevant data.

```tsx
function ResourcesAndPossibleSolutionsIssueDetailsContent({
  event,
  project,
  group,
}: Required<GroupEventDetailsContentProps>) {
  return (
    <ErrorBoundary mini>
      <ResourcesAndPossibleSolutions event={event} project={project} group={group} />
    </ErrorBoundary>
  );
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/issueDetails/groupRelatedIssues/index.tsx" line="1">

---

# Issue Details in groupRelatedIssues View

In the 'groupRelatedIssues' view, the application fetches and displays issues that are related to the current issue, helping developers understand if the error is part of a larger problem.

```tsx
import {Fragment} from 'react';
import type {RouteComponentProps} from 'react-router';
import styled from '@emotion/styled';

import {LinkButton} from 'sentry/components/button';
import GroupList from 'sentry/components/issues/groupList';
import Link from 'sentry/components/links/link';
import LoadingError from 'sentry/components/loadingError';
import LoadingIndicator from 'sentry/components/loadingIndicator';
import {t} from 'sentry/locale';
import {space} from 'sentry/styles/space';
import {useApiQuery} from 'sentry/utils/queryClient';
import useOrganization from 'sentry/utils/useOrganization';

type RouteParams = {
  groupId: string;
};

type Props = RouteComponentProps<RouteParams, {}>;

type RelatedIssuesResponse = {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/issueDetails/traceTimeline/traceIssue.tsx" line="19">

---

# Issue Details in TraceIssueEvent Function

The 'TraceIssueEvent' function is used to display the details of a specific issue event within a trace timeline. This includes the event's title, subtitle, message, and other relevant data.

```tsx
export function TraceIssueEvent({event}: TraceIssueEventProps) {
  const organization = useOrganization();
  const project = useProjectFromSlug({organization, projectSlug: event['project.name']});
  const issueId = event['issue.id'];
  const {title, subtitle, message} = getTitleSubtitleMessage(event);
  const avatarSize = parseInt(space(4), 10);

  const referrer = 'issue_details.related_trace_issue';

  return (
    <Fragment>
      <TraceIssueLinkContainer
        to={{
          pathname: `/organizations/${organization.slug}/issues/${issueId}/events/${event.id}/`,
          query: {
            referrer: referrer,
          },
        }}
        onClick={() => {
          trackAnalytics(`${referrer}.trace_issue_clicked`, {
            organization,
```

---

</SwmSnippet>

# Issue Details Functions

This section provides an overview of the main functions used in the 'Issue details' functionality of the Sentry demo application.

<SwmSnippet path="/static/app/views/issueDetails/utils.tsx" line="156">

---

## useFetchIssueTagsForDetailsPage

The `useFetchIssueTagsForDetailsPage` function is a custom hook that fetches the tags for a specific issue. It uses the `useApiQuery` hook to make the API request, and returns the data, loading state, and error state. This function is used to fetch and display the tags of an issue in the issue details page.

```tsx
export const useFetchIssueTagsForDetailsPage = (
  {
    groupId,
    orgSlug,
    environment = [],
    isStatisticalDetector = false,
    statisticalDetectorParameters,
  }: {
    environment: string[];
    orgSlug: string;
    groupId?: string;
    isStatisticalDetector?: boolean;
    statisticalDetectorParameters?: {
      durationBaseline: number;
      end: string;
      start: string;
      transaction: string;
    };
  },
  {enabled = true}: {enabled?: boolean} = {}
) => {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/issueDetails/traceTimeline/useTraceTimelineEvents.tsx" line="47">

---

## useTraceTimelineEvents

The `useTraceTimelineEvents` function is a custom hook that fetches the events for a specific trace. It uses the `useApiQuery` hook to make the API request, and returns the events, loading state, and error state. This function is used to fetch and display the events of a trace in the issue details page.

```tsx
export function useTraceTimelineEvents({event}: UseTraceTimelineEventsOptions): {
  endTimestamp: number;
  isError: boolean;
  isLoading: boolean;
  oneOtherIssueEvent: TimelineEvent | undefined;
  startTimestamp: number;
  traceEvents: TimelineEvent[];
} {
  const organization = useOrganization();
  // If the org has global views, we want to look across all projects,
  // otherwise, just look at the current project.
  const hasGlobalViews = organization.features.includes('global-views');
  const project = hasGlobalViews ? -1 : event.projectID;
  const {start, end} = getTraceTimeRangeFromEvent(event);

  const traceId = event.contexts?.trace?.trace_id ?? '';
  const enabled = !!traceId;
  const {
    data: issuePlatformData,
    isLoading: isLoadingIssuePlatform,
    isError: isErrorIssuePlatform,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/actionCreators/group.tsx" line="443">

---

## useFetchIssueTags

The `useFetchIssueTags` function is a custom hook that fetches the tags for a specific issue. It uses the `useApiQuery` hook to make the API request, and returns the data, loading state, and error state. This function is used to fetch and display the tags of an issue in various views within the application.

```tsx
export const useFetchIssueTags = (
  parameters: FetchIssueTagsParameters,
  {
    enabled = true,
    ...options
  }: Partial<UseApiQueryOptions<GroupTagsResponse | Tag[]>> = {}
) => {
  return useApiQuery<GroupTagsResponse | Tag[]>(makeFetchIssueTagsQueryKey(parameters), {
    staleTime: 30000,
    enabled: defined(parameters.groupId) && enabled,
    ...options,
  });
};
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/useOrganization.tsx" line="16">

---

## useOrganization

The `useOrganization` function is a custom hook that retrieves the current organization from the application's state. It is used in various functions to provide the organization context needed for API requests and other operations.

```tsx
// The additional signatures provide proper type hints for when we set
// `allowNull` to true.

function useOrganization(opts?: Options<false>): Organization;
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
