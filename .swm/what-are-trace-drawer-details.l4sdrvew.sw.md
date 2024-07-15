---
title: What are Trace Drawer Details
---
Details in the Trace drawer refer to the specific information about a trace or span in the Sentry application. This information is organized into different sections, each represented by a TypeScript (tsx) file in the 'details' directory. These sections include transaction details, span details, profiling details, and issues related to the trace or span.

The 'TraceDrawerComponents' constant in 'styles.tsx' file is a collection of styled components used across different sections of the Trace drawer. This constant is imported and used in various files within the 'details' directory to maintain a consistent look and feel across the Trace drawer.

Each section in the Trace drawer provides specific details about a trace or span. For example, the 'transaction' directory contains sections like 'opsBreakDown', 'request', 'breadCrumbs', 'measurements', and others. Each of these sections provides specific details about a transaction in the trace.

Similarly, the 'span' directory contains sections like 'description', 'tags', 'ancestry', 'alerts', 'http', and others. Each of these sections provides specific details about a span in the trace.

The 'profiling' directory contains a 'profilePreview.tsx' file, which is used to display a preview of the profiling data for a trace.

The 'issues' directory contains files that handle the display of issues related to a trace or span. The 'issues.tsx' file lists the issues, while the 'issueSummary.tsx' file provides a summary of each issue.

# TraceDrawerComponents

The 'TraceDrawerComponents' constant is a collection of styled components used across different sections of the Trace drawer. This constant is imported and used in various files within the 'details' directory to maintain a consistent look and feel across the Trace drawer.

# Transaction Details

The 'transaction' directory contains sections like 'opsBreakDown', 'request', 'breadCrumbs', 'measurements', and others. Each of these sections provides specific details about a transaction in the trace.

# Span Details

The 'span' directory contains sections like 'description', 'tags', 'ancestry', 'alerts', 'http', and others. Each of these sections provides specific details about a span in the trace.

<SwmSnippet path="/static/app/views/performance/newTraceDetails/traceDrawer/details/profiling/profilePreview.tsx" line="1">

---

# Profiling Details

The 'profiling' directory contains a 'profilePreview.tsx' file, which is used to display a preview of the profiling data for a trace.

```tsx
import {useMemo, useState} from 'react';
import styled from '@emotion/styled';

import emptyStateImg from 'sentry-images/spot/profiling-empty-state.svg';

import {Button} from 'sentry/components/button';
import {SectionHeading} from 'sentry/components/charts/styles';
import InlineDocs from 'sentry/components/events/interfaces/spans/inlineDocs';
import ExternalLink from 'sentry/components/links/externalLink';
import LoadingIndicator from 'sentry/components/loadingIndicator';
import {FlamegraphPreview} from 'sentry/components/profiling/flamegraph/flamegraphPreview';
import QuestionTooltip from 'sentry/components/questionTooltip';
import {t, tct} from 'sentry/locale';
import {space} from 'sentry/styles/space';
import type {EventTransaction, Organization} from 'sentry/types';
import {defined} from 'sentry/utils';
import {trackAnalytics} from 'sentry/utils/analytics';
import type {CanvasView} from 'sentry/utils/profiling/canvasView';
import {colorComponentsToRGBA} from 'sentry/utils/profiling/colors/utils';
import {Flamegraph as FlamegraphModel} from 'sentry/utils/profiling/flamegraph';
import {FlamegraphThemeProvider} from 'sentry/utils/profiling/flamegraph/flamegraphThemeProvider';
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/newTraceDetails/traceDrawer/details/issues/issues.tsx" line="1">

---

# Issues Details

The 'issues' directory contains files that handle the display of issues related to a trace or span. The 'issues.tsx' file lists the issues, while the 'issueSummary.tsx' file provides a summary of each issue.

```tsx
import {useMemo} from 'react';
import styled from '@emotion/styled';

import ActorAvatar from 'sentry/components/avatar/actorAvatar';
import Count from 'sentry/components/count';
import EventOrGroupExtraDetails from 'sentry/components/eventOrGroupExtraDetails';
import LoadingError from 'sentry/components/loadingError';
import LoadingIndicator from 'sentry/components/loadingIndicator';
import Panel from 'sentry/components/panels/panel';
import PanelHeader from 'sentry/components/panels/panelHeader';
import PanelItem from 'sentry/components/panels/panelItem';
import {IconWrapper} from 'sentry/components/sidebarSection';
import GroupChart from 'sentry/components/stream/groupChart';
import {IconUser} from 'sentry/icons';
import {t, tct, tn} from 'sentry/locale';
import {space} from 'sentry/styles/space';
import type {Group, Organization} from 'sentry/types';
import type {
  TraceError,
  TraceErrorOrIssue,
  TracePerformanceIssue,
```

---

</SwmSnippet>

# Details in Trace Drawer

This section provides an overview of the functions and components in the 'details' directory of the Sentry application. These functions and components provide specific details about a trace or span in the Sentry application.

<SwmSnippet path="/static/app/views/performance/newTraceDetails/traceDrawer/details/styles.tsx" line="54">

---

## TraceDrawerComponents

The 'TraceDrawerComponents' constant is a collection of styled components used across different sections of the Trace drawer. This constant is imported and used in various files within the 'details' directory to maintain a consistent look and feel across the Trace drawer.

```tsx
const DetailContainer = styled('div')`
  display: flex;
  flex-direction: column;
  gap: ${space(2)};
  padding: ${space(1)};

  ${DataSection} {
    padding: 0;
  }
`;

const FlexBox = styled('div')`
  display: flex;
  align-items: center;
`;

const Actions = styled(FlexBox)`
  gap: ${space(0.5)};
  flex-wrap: wrap;
  justify-content: end;
  width: 100%;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/newTraceDetails/traceDrawer/details/transaction/index.tsx" line="97">

---

## Transaction Details

The 'transaction' directory contains sections like 'opsBreakDown', 'request', 'breadCrumbs', 'measurements', and others. Each of these sections provides specific details about a transaction in the trace.

```tsx
}: TraceTreeNodeDetailsProps<TraceTreeNode<TraceTree.Transaction>>) {
  const location = useLocation();
  const {projects} = useProjects();
  const issues = useMemo(() => {
    return [...node.errors, ...node.performance_issues];
  }, [node.errors, node.performance_issues]);

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/newTraceDetails/traceDrawer/details/span/index.tsx" line="97">

---

## Span Details

The 'span' directory contains sections like 'description', 'tags', 'ancestry', 'alerts', 'http', and others. Each of these sections provides specific details about a span in the trace.

```tsx
          projectSlug={event.projectSlug}
          profileId={profileId || ''}
        >
          <ProfileContext.Consumer>
            {profiles => (
              <ProfileGroupProvider
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/newTraceDetails/traceDrawer/details/profiling/profilePreview.tsx" line="50">

---

## Profiling Details

The 'profiling' directory contains a 'profilePreview.tsx' file, which is used to display a preview of the profiling data for a trace.

```tsx
  const organization = useOrganization();
  const [canvasView, setCanvasView] = useState<CanvasView<FlamegraphModel> | null>(null);

  const profile = useMemo(() => {
    const threadId = profileGroup.profiles[profileGroup.activeProfileIndex]?.threadId;
    if (!defined(threadId)) {
      return null;
    }
    return profileGroup.profiles.find(p => p.threadId === threadId) ?? null;
  }, [profileGroup.profiles, profileGroup.activeProfileIndex]);

  const transactionHasProfile = useMemo(() => {
    return (node.parent_transaction?.profiles?.length ?? 0) > 0;
  }, [node]);

  const flamegraph = useMemo(() => {
    if (!transactionHasProfile || !profile) {
      return FlamegraphModel.Example();
    }

    return new FlamegraphModel(profile, {});
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/newTraceDetails/traceDrawer/details/transaction/index.tsx" line="100">

---

## Issues

The 'issues' directory contains files that handle the display of issues related to a trace or span. The 'issues.tsx' file lists the issues, while the 'issueSummary.tsx' file provides a summary of each issue.

```tsx
  const issues = useMemo(() => {
    return [...node.errors, ...node.performance_issues];
  }, [node.errors, node.performance_issues]);
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
