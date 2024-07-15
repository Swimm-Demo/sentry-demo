---
title: Introduction to Profiling in Views
---
Profiling in the views directory of the sentry-demo repository refers to the process of analyzing the performance of the application. It involves collecting data about how the application's code is executed, such as which functions are called and how long they take to run. This information is used to identify bottlenecks and optimize the application for better performance.

The profiling feature is implemented in the 'ProfilingContainer' component in the 'static/app/views/profiling/index.tsx' file. This component checks if the 'profiling' feature is enabled for the organization and renders the children components accordingly. If the feature is not enabled, it displays a warning message.

The 'ProfileSummaryHeader' component in the 'static/app/views/profiling/profileSummary/index.tsx' file uses the 'view' state to determine which view to display, either 'flamegraph' or 'profiles'. The 'view' state is updated based on the 'view' query parameter in the URL.

The 'ProfilesAndTransactionProvider' component in the 'static/app/views/profiling/profilesProvider.tsx' file fetches the profiling data and provides it to the child components through the 'ProfileContext' and 'ProfileTransactionContext'. The 'useProfiles' and 'useProfileTransaction' hooks are used to access this data.

The 'ProfilesSummaryChart' component in the 'static/app/views/profiling/landing/profilesSummaryChart.tsx' file displays a chart of the profiling data. It uses the 'useProfileEventsStats' hook to fetch the data and the 'AreaChart' component to render the chart.

The 'onSetupProfilingClick' function in the 'static/app/views/profiling/content.tsx' file is used to track when the user clicks on the 'Set Up Profiling' button and to display the profiling onboarding panel.

The 'ProfileGroupProvider' component in the 'static/app/views/profiling/profileGroupProvider.tsx' file imports the profiling data and provides it to the child components through the 'ProfileGroupContext'. The 'useProfileGroup' hook is used to access this data.

<SwmSnippet path="/static/app/views/profiling/index.tsx" line="8">

---

# Profiling Feature

The 'ProfilingContainer' component checks if the 'profiling' feature is enabled for the organization and renders the children components accordingly. If the feature is not enabled, it displays a warning message.

```tsx
const profilingFeature = ['profiling'];

type Props = {
  children: React.ReactNode;
};

function ProfilingContainer({children}: Props) {
  const organization = useOrganization();

  return (
    <Feature
      hookName="feature-disabled:profiling-page"
      features={profilingFeature}
      organization={organization}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/profiling/profileSummary/index.tsx" line="79">

---

# Profile Summary View

The 'ProfileSummaryHeader' component uses the 'view' state to determine which view to display, either 'flamegraph' or 'profiles'. The 'view' state is updated based on the 'view' query parameter in the URL.

```tsx
  value: string | string[] | null | undefined,
  defaultValue: 'flamegraph' | 'profiles'
): 'flamegraph' | 'profiles' {
  if (!value || Array.isArray(value)) {
    return defaultValue;
  }
  if (value === 'flamegraph' || value === 'profiles') {
    return value;
  }
  return defaultValue;
}

const DEFAULT_FLAMEGRAPH_PREFERENCES: DeepPartial<FlamegraphState> = {
  preferences: {
    sorting: 'alphabetical' satisfies FlamegraphState['preferences']['sorting'],
  },
};
interface ProfileSummaryHeaderProps {
  location: Location;
  onViewChange: (newView: 'flamegraph' | 'profiles') => void;
  organization: Organization;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/profiling/profilesProvider.tsx" line="53">

---

# Profiling Data Provider

The 'ProfilesAndTransactionProvider' component fetches the profiling data and provides it to the child components through the 'ProfileContext' and 'ProfileTransactionContext'. The 'useProfiles' and 'useProfileTransaction' hooks are used to access this data.

```tsx
const SetProfileProvider = createContext<SetProfileProviderValue | null>(null);

export function useProfiles() {
  const context = useContext(ProfileContext);
  if (!context) {
    throw new Error('useProfiles was called outside of ProfileProvider');
  }
  return context;
}

export function useSetProfiles() {
  const context = useContext(SetProfileProvider);
  if (!context) {
    throw new Error('useSetProfiles was called outside of SetProfileProvider');
  }
  return context;
}

export const ProfileTransactionContext =
  createContext<RequestState<EventTransaction | null> | null>(null);

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/profiling/landing/profilesSummaryChart.tsx" line="1">

---

# Profiling Chart

The 'ProfilesSummaryChart' component displays a chart of the profiling data. It uses the 'useProfileEventsStats' hook to fetch the data and the 'AreaChart' component to render the chart.

```tsx
import {useMemo} from 'react';
import {useTheme} from '@emotion/react';
import styled from '@emotion/styled';

import type {AreaChartProps} from 'sentry/components/charts/areaChart';
import {AreaChart} from 'sentry/components/charts/areaChart';
import ChartZoom from 'sentry/components/charts/chartZoom';
import {t} from 'sentry/locale';
import {space} from 'sentry/styles/space';
import type {PageFilters} from 'sentry/types/core';
import type {Series} from 'sentry/types/echarts';
import {axisLabelFormatter, tooltipFormatter} from 'sentry/utils/discover/charts';
import {aggregateOutputType} from 'sentry/utils/discover/fields';
import {useProfileEventsStats} from 'sentry/utils/profiling/hooks/useProfileEventsStats';
import useRouter from 'sentry/utils/useRouter';

// We want p99 to be before p75 because echarts renders the series in order.
// So if p75 is before p99, p99 will be rendered on top of p75 which will
// cover it up.
const SERIES_ORDER = ['count()', 'p99()', 'p95()', 'p75()'] as const;

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/profiling/content.tsx" line="101">

---

# Profiling Onboarding

The 'onSetupProfilingClick' function is used to track when the user clicks on the 'Set Up Profiling' button and to display the profiling onboarding panel.

```tsx
  // Open the modal on demand
  const onSetupProfilingClick = useCallback(() => {
    trackAnalytics('profiling_views.onboarding', {
      organization,
    });
    SidebarPanelStore.activatePanel(SidebarPanelKey.PROFILING_ONBOARDING);
  }, [organization]);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/profiling/profileGroupProvider.tsx" line="1">

---

# Profiling Data Import

The 'ProfileGroupProvider' component imports the profiling data and provides it to the child components through the 'ProfileGroupContext'. The 'useProfileGroup' hook is used to access this data.

```tsx
import {createContext, useContext, useMemo} from 'react';
import * as Sentry from '@sentry/react';

import type {Frame} from 'sentry/utils/profiling/frame';
import type {ProfileGroup} from 'sentry/utils/profiling/profile/importProfile';
import {importProfile} from 'sentry/utils/profiling/profile/importProfile';

type ProfileGroupContextValue = ProfileGroup;

const ProfileGroupContext = createContext<ProfileGroupContextValue | null>(null);

export function useProfileGroup() {
  const context = useContext(ProfileGroupContext);
  if (!context) {
    throw new Error('useProfileGroup was called outside of ProfileGroupProvider');
  }
  return context;
}

export const LOADING_PROFILE_GROUP: Readonly<ProfileGroup> = {
  name: 'Loading',
```

---

</SwmSnippet>

# Profiling Functions

This section provides an overview of the main functions related to profiling in the Sentry application.

<SwmSnippet path="/static/app/views/profiling/index.tsx" line="14">

---

## ProfilingContainer

The 'ProfilingContainer' component checks if the 'profiling' feature is enabled for the organization and renders the children components accordingly. If the feature is not enabled, it displays a warning message.

```tsx
function ProfilingContainer({children}: Props) {
  const organization = useOrganization();

  return (
    <Feature
      hookName="feature-disabled:profiling-page"
      features={profilingFeature}
      organization={organization}
      renderDisabled={() => (
        <Layout.Page withPadding>
          <Alert type="warning">{t("You don't have access to this feature")}</Alert>
        </Layout.Page>
      )}
    >
      <NoProjectMessage organization={organization}>{children}</NoProjectMessage>
    </Feature>
  );
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/profiling/profileSummary/index.tsx" line="12">

---

## ProfileSummaryHeader

The 'ProfileSummaryHeader' component uses the 'view' state to determine which view to display, either 'flamegraph' or 'profiles'. The 'view' state is updated based on the 'view' query parameter in the URL.

```tsx
import FeedbackWidgetButton from 'sentry/components/feedback/widget/feedbackWidgetButton';
import IdBadge from 'sentry/components/idBadge';
import * as Layout from 'sentry/components/layouts/thirds';
import Link from 'sentry/components/links/link';
import LoadingIndicator from 'sentry/components/loadingIndicator';
import {DatePageFilter} from 'sentry/components/organizations/datePageFilter';
import {EnvironmentPageFilter} from 'sentry/components/organizations/environmentPageFilter';
import PageFilterBar from 'sentry/components/organizations/pageFilterBar';
import PageFiltersContainer from 'sentry/components/organizations/pageFilters/container';
import PerformanceDuration from 'sentry/components/performanceDuration';
import {AggregateFlamegraph} from 'sentry/components/profiling/flamegraph/aggregateFlamegraph';
import {AggregateFlamegraphTreeTable} from 'sentry/components/profiling/flamegraph/aggregateFlamegraphTreeTable';
import {FlamegraphSearch} from 'sentry/components/profiling/flamegraph/flamegraphToolbar/flamegraphSearch';
import type {ProfilingBreadcrumbsProps} from 'sentry/components/profiling/profilingBreadcrumbs';
import {ProfilingBreadcrumbs} from 'sentry/components/profiling/profilingBreadcrumbs';
import {SegmentedControl} from 'sentry/components/segmentedControl';
import SentryDocumentTitle from 'sentry/components/sentryDocumentTitle';
import type {SmartSearchBarProps} from 'sentry/components/smartSearchBar';
import {TabList, Tabs} from 'sentry/components/tabs';
import {MAX_QUERY_LENGTH} from 'sentry/constants';
import {IconPanel} from 'sentry/icons';
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/profiling/profilesProvider.tsx" line="12">

---

## ProfilesAndTransactionProvider

The 'ProfilesAndTransactionProvider' component fetches the profiling data and provides it to the child components through the 'ProfileContext' and 'ProfileTransactionContext'. The 'useProfiles' and 'useProfileTransaction' hooks are used to access this data.

```tsx
import {useSentryEvent} from 'sentry/utils/profiling/hooks/useSentryEvent';
import useApi from 'sentry/utils/useApi';
import useOrganization from 'sentry/utils/useOrganization';
import {useParams} from 'sentry/utils/useParams';

function fetchFlamegraphs(
  api: Client,
  eventId: string,
  projectSlug: Project['slug'],
  orgSlug: Organization['slug']
): Promise<Profiling.ProfileInput> {
  return api
    .requestPromise(
      `/projects/${orgSlug}/${projectSlug}/profiling/profiles/${eventId}/`,
      {
        method: 'GET',
        includeAllArgs: true,
      }
    )
    .then(([data]) => data);
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/profiling/landing/profilesSummaryChart.tsx" line="33">

---

## ProfilesSummaryChart

The 'ProfilesSummaryChart' component displays a chart of the profiling data. It uses the 'useProfileEventsStats' hook to fetch the data and the 'AreaChart' component to render the chart.

```tsx
  hideCount,
}: ProfileSummaryChartProps) {
  const router = useRouter();
  const theme = useTheme();

  const seriesOrder = useMemo(() => {
    if (hideCount) {
      return SERIES_ORDER.filter(s => s !== 'count()');
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/profiling/content.tsx" line="101">

---

## onSetupProfilingClick

The 'onSetupProfilingClick' function is used to track when the user clicks on the 'Set Up Profiling' button and to display the profiling onboarding panel.

```tsx
  // Open the modal on demand
  const onSetupProfilingClick = useCallback(() => {
    trackAnalytics('profiling_views.onboarding', {
      organization,
    });
    SidebarPanelStore.activatePanel(SidebarPanelKey.PROFILING_ONBOARDING);
  }, [organization]);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/profiling/profileGroupProvider.tsx" line="119">

---

## ProfileGroupProvider

The 'ProfileGroupProvider' component imports the profiling data and provides it to the child components through the 'ProfileGroupContext'. The 'useProfileGroup' hook is used to access this data.

```tsx

```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
