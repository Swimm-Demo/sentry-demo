---
title: Introduction to Metrics Management in Project Settings
---
Project metrics in Sentry are numerical values extracted from span attributes that can help track anything about your environment over time. They are located in the Settings section of the project. The metrics are managed through the `ProjectMetrics` and `ProjectMetricsDetails` functions in the `projectMetrics.tsx` and `projectMetricsDetails.tsx` files respectively. These functions use various hooks and utilities to fetch, display, and manage the metrics data. The metrics data can be blocked or unblocked, and this status is managed by the `useBlockMetric` function. The metrics data can also include tags, which are managed by the `useMetricsTags` function.

<SwmSnippet path="/static/app/views/settings/projectMetrics/projectMetrics.tsx" line="31">

---

# ProjectMetrics Function

The `ProjectMetrics` function is responsible for rendering the Metrics page. It uses the `useOrganization` hook to get the current organization, checks if the organization has custom metrics extraction rules, and activates the metrics onboarding sidebar if necessary. It also sets up the settings page header and the metrics table.

```tsx
function ProjectMetrics({project}: Props) {
  const organization = useOrganization();
  const hasExtractionRules = hasCustomMetricsExtractionRules(organization);
  const {activateSidebar} = useMetricsOnboardingSidebar();

  return (
    <Fragment>
      <SentryDocumentTitle title={routeTitleGen(t('Metrics'), project.slug, false)} />
      <SettingsPageHeader
        title={t('Metrics')}
        action={
          !hasExtractionRules && (
            <Button
              priority="primary"
              onClick={() => {
                Sentry.metrics.increment('ddm.add_custom_metric', 1, {
                  tags: {
                    referrer: 'settings',
                  },
                });
                activateSidebar();
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/projectMetrics/projectMetricsDetails.tsx" line="42">

---

# ProjectMetricsDetails Function

The `ProjectMetricsDetails` function is responsible for rendering the details of a specific metric. It uses several hooks and utilities to fetch and manage the metrics data. It also sets up the panel for displaying the metric details.

```tsx
function ProjectMetricsDetails({project, params, organization}: Props) {
  const {mri} = params;

  const projectId = parseInt(project.id, 10);
  const projectIds = [projectId];

  const {
    data: {blockingStatus},
  } = useProjectMetric(mri, projectId);
  const {data: tagsData = []} = useMetricsTags(mri, {projects: projectIds}, false);

  const isBlockedMetric = blockingStatus?.isBlocked ?? false;
  const blockMetricMutation = useBlockMetric(project);
  const {hasAccess} = useAccess({access: ['project:write'], project});

  const {type, name, unit} = parseMRI(mri) ?? {};
  const aggregation = getDefaultAggregation(mri);
  const {data: metricsData, isLoading} = useMetricsQuery(
    [{mri, aggregation, name: 'query'}],
    {
      datetime: {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/metrics/useBlockMetric.tsx" line="30">

---

# useBlockMetric Function

The `useBlockMetric` function is a custom hook that is used to block or unblock a metric. It uses the `useApi` and `useQueryClient` hooks to make a PUT request to the metrics visibility endpoint.

```tsx
export const useBlockMetric = (project: Project) => {
  const api = useApi();
  const {slug} = useOrganization();
  const queryClient = useQueryClient();

  const options = {
    mutationFn: (data: BlockMutationData) => {
      return api.requestPromise(`/projects/${slug}/${project.slug}/metrics/visibility/`, {
        method: 'PUT',
        query: {project: project.id},
        data: {
          metricMri: data.mri,
          project: project.id,
          operationType: data.operationType,
          tags: isTagOp(data) ? data.tags : undefined,
        },
      });
    },
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/metrics/useMetricsTags.tsx" line="51">

---

# useMetricsTags Function

The `useMetricsTags` function is a custom hook that is used to fetch the tags of a metric. It uses the `useApiQuery` hook to make a request to the metrics tags endpoint.

```tsx
export function useMetricsTags(
  mri: MRI | undefined,
  pageFilters: Partial<PageFilters>,
  filterBlockedTags = true,
  blockedTags?: string[]
) {
  const organization = useOrganization();
  const {getTags} = useVirtualMetricsContext();
  const parsedMRI = parseMRI(mri);
  const useCase = parsedMRI?.useCase ?? 'custom';
  const isVirtualMetric = parsedMRI?.type === 'v';

  const tagsQuery = useApiQuery<MetricTag[]>(
    getMetricsTagsQueryKey(organization, mri, pageFilters),
    {
      enabled: !!mri && !isVirtualMetric,
      staleTime: Infinity,
    }
  );

  const metricMeta = useMetricsMeta(pageFilters, [useCase], false, !blockedTags);
```

---

</SwmSnippet>

# Project Metrics Functions

This section will explain the main functions related to project metrics in Sentry.

<SwmSnippet path="/static/app/views/settings/projectMetrics/index.tsx" line="14">

---

## ProjectMetrics

The `ProjectMetrics` function is a container that wraps the actual `ProjectMetrics` component with a feature check. It ensures that the 'custom-metrics' feature is available before rendering the `ProjectMetrics` component.

```tsx
function ProjectMetricsContainer(props: Props) {
  return (
    <Feature features={['custom-metrics']}>
      <ProjectMetrics {...props} />
    </Feature>
  );
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/projectMetrics/projectMetricsDetails.tsx" line="31">

---

## ProjectMetricsDetails

The `ProjectMetricsDetails` function is responsible for displaying the details of a specific metric. It fetches the metric data, handles the blocking and unblocking of the metric, and manages the tags associated with the metric.

```tsx
import SettingsPageHeader from 'sentry/views/settings/components/settingsPageHeader';
import {useAccess} from 'sentry/views/settings/projectMetrics/access';
import {BlockButton} from 'sentry/views/settings/projectMetrics/blockButton';

import {useProjectMetric} from '../../../utils/metrics/useMetricsMeta';

type Props = {
  organization: Organization;
  project: Project;
} & RouteComponentProps<{mri: MRI; projectId: string}, {}>;

function ProjectMetricsDetails({project, params, organization}: Props) {
  const {mri} = params;

  const projectId = parseInt(project.id, 10);
  const projectIds = [projectId];

  const {
    data: {blockingStatus},
  } = useProjectMetric(mri, projectId);
  const {data: tagsData = []} = useMetricsTags(mri, {projects: projectIds}, false);
```

---

</SwmSnippet>

## useBlockMetric

The `useBlockMetric` function is a custom hook that provides functionality for blocking and unblocking a metric. It uses the `useMutation` hook from react-query to send a request to the API when a metric is blocked or unblocked.

## useMetricsTags

The `useMetricsTags` function is a custom hook that fetches the tags associated with a metric. It uses the `useApiQuery` hook to send a request to the API and fetch the tags.

# Project Metrics Endpoints

Project Metrics Endpoints

<SwmSnippet path="/static/app/views/settings/projectMetrics/utils/useMetricsExtractionRules.tsx" line="30">

---

## Metrics Extraction Rules Endpoint

The `/projects/{orgSlug}/{projectId}/metrics/extraction-rules/` endpoint is used to get the metrics extraction rules for a specific project. The `getMetricsExtractionRulesApiKey` function constructs the API key for this endpoint. The `useMetricsExtractionRules` hook uses this API key to fetch the metrics extraction rules.

```tsx
export const getMetricsExtractionRulesApiKey = (
  orgSlug: string,
  projectId: string | number,
  options?: MetricRulesAPIOptions
) => {
  if (Object.keys(options ?? {}).length === 0) {
    // when no options are provided, return only endpoint path as a key
    return [`/projects/${orgSlug}/${projectId}/metrics/extraction-rules/`] as const;
  }

  return [
    `/projects/${orgSlug}/${projectId}/metrics/extraction-rules/`,
    {query: options},
  ] as const;
};
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/projectMetrics/extrapolationField.tsx" line="37">

---

## Project Endpoint

The `/projects/{organization.slug}/{project.slug}/` endpoint is used to update a specific project. In this case, it's used to toggle the extrapolation of metrics for the project. The `handleToggleChange` function is a mutation function that makes a PUT request to this endpoint.

```tsx
      return api.requestPromise(`/projects/${organization.slug}/${project.slug}/`, {
        method: 'PUT',
        data: {
          extrapolateMetrics: value,
        },
      });
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
