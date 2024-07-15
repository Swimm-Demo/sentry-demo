---
title: Understanding Performance Monitoring in Components
---
Performance in the components directory of the sentry-demo project refers to the monitoring and tracking of how well the application's components are functioning. It involves the analysis of various metrics related to the components' execution and response times, resource usage, and overall efficiency.

The 'waterfall' subdirectory within the 'performance' directory contains several TypeScript (tsx) files. These files are used to create a waterfall chart, a form of visualization that helps in understanding the performance of different components in a sequence or a process. Each row in the waterfall chart represents a component, and the length of the row signifies the duration of its execution.

The 'utils.tsx' file contains utility functions that are used across the waterfall chart for calculations and data manipulations related to performance metrics. The 'types.tsx' file defines the TypeScript types used in the waterfall chart. The 'constants.tsx' file defines constant values used across the waterfall chart.

The remaining tsx files ('messageRow.tsx', 'miniHeader.tsx', 'row.tsx', 'rowBar.tsx', 'treeConnector.tsx', 'rowDetails.tsx', 'rowTitle.tsx', 'rowDivider.tsx') are component files that define the structure and behavior of different parts of the waterfall chart.

# Waterfall Chart

The 'waterfall' subdirectory within the 'performance' directory contains several TypeScript (tsx) files. These files are used to create a waterfall chart, a form of visualization that helps in understanding the performance of different components in a sequence or a process.

# Utility Functions

The 'utils.tsx' file contains utility functions that are used across the waterfall chart for calculations and data manipulations related to performance metrics.

# TypeScript Types

The 'types.tsx' file defines the TypeScript types used in the waterfall chart.

# Constant Values

The 'constants.tsx' file defines constant values used across the waterfall chart.

# Component Files

The remaining tsx files ('messageRow.tsx', 'miniHeader.tsx', 'row.tsx', 'rowBar.tsx', 'treeConnector.tsx', 'rowDetails.tsx', 'rowTitle.tsx', 'rowDivider.tsx') are component files that define the structure and behavior of different parts of the waterfall chart.

# Performance Functions

Performance functions in the sentry-demo project

<SwmSnippet path="/static/app/components/performance/waterfall/utils.tsx" line="1">

---

## Utility Functions

The 'utils.tsx' file contains utility functions that are used across the waterfall chart for calculations and data manipulations related to performance metrics.

```tsx
import type {Theme} from '@emotion/react';
import Color from 'color';

import type {DurationDisplay} from 'sentry/components/performance/waterfall/types';
import {CHART_PALETTE} from 'sentry/constants/chartPalette';
import {space} from 'sentry/styles/space';

import type {SpanBarType} from './constants';
import {getSpanBarColours} from './constants';

export const getBackgroundColor = ({
  showStriping,
  showDetail,
  theme,
}: {
  theme: Theme;
  showDetail?: boolean;
  showStriping?: boolean;
}) => {
  if (showDetail) {
    return theme.textColor;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/performance/waterfall/row.tsx" line="1">

---

## Component Files

The 'row.tsx' file is an example of the component files that define the structure and behavior of different parts of the waterfall chart. Each row in the waterfall chart represents a component, and the length of the row signifies the duration of its execution.

```tsx
import {Fragment} from 'react';
import styled from '@emotion/styled';

import {ROW_HEIGHT} from 'sentry/components/performance/waterfall/constants';
import {getBackgroundColor} from 'sentry/components/performance/waterfall/utils';
import {useReplayContext} from 'sentry/components/replays/replayContext';
import toPercent from 'sentry/utils/number/toPercent';
import useCurrentHoverTime from 'sentry/utils/replays/playback/providers/useCurrentHoverTime';

interface RowProps extends React.HTMLAttributes<HTMLDivElement> {
  cursor?: 'pointer' | 'default';
  showBorder?: boolean;
  visible?: boolean;
}

export const Row = styled('div')<RowProps>`
  display: ${p => (p.visible ? 'block' : 'none')};
  border-top: ${p => (p.showBorder ? `1px solid ${p.theme.border}` : null)};
  margin-top: ${p => (p.showBorder ? '-1px' : null)}; /* to prevent offset on toggle */
  position: relative;
  overflow: hidden;
```

---

</SwmSnippet>

# Performance Monitoring Endpoints

Performance Monitoring Endpoints

<SwmSnippet path="/static/app/components/performance/searchBar.tsx" line="63">

---

## Performance Monitoring Endpoints

The endpoint `/organizations/${organization.slug}/events/` is used to fetch event data related to a specific organization. The data fetched from this endpoint is used to populate the search results in the performance monitoring feature. The search results include transaction data which is used to monitor the performance of different components of the application.

```tsx

  const projectIdStrings = (eventView.project as Readonly<number>[])?.map(String);

  const handleSearchChange = query => {
    setSearchString(query);

    if (query.length === 0) {
      onSearch('');
    }

    if (query.length < 3) {
      setSearchResults([]);
      closeDropdown();
      return;
    }

    openDropdown();
    getSuggestedTransactions(query);
  };

  const handleKeyDown = (event: React.KeyboardEvent) => {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/performance/teamKeyTransactionsManager.tsx" line="85">

---

## Team Key Transactions Endpoint

The `fetchTeamKeyTransactions` function is used to fetch key transaction data for a team. This data is used to monitor the performance of key transactions executed by a team. The function makes a request to an endpoint which is not explicitly defined in the context, but it's likely to be an endpoint related to team key transactions.

```tsx
  async fetchData() {
    const {api, organization, selectedTeams, selectedProjects} = this.props;
    const keyFetchID = Symbol('keyFetchID');
    this.setState({isLoading: true, keyFetchID});

    let teamKeyTransactions: TeamKeyTransactions = [];
    let error: string | null = null;

    try {
      teamKeyTransactions = await fetchTeamKeyTransactions(
        api,
        organization.slug,
        selectedTeams,
        selectedProjects
      );
    } catch (err) {
      error = err.responseJSON?.detail ?? t('Error fetching team key transactions');
    }

    this.setState({
      isLoading: false,
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
