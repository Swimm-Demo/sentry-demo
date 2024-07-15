---
title: Introduction to Release Overview
---
The 'Overview' in the sentry-demo repository refers to a comprehensive summary of the release details. It is primarily implemented in the 'ReleaseOverview' class in the 'index.tsx' file located in the 'static/app/views/releases/detail/overview' directory. This class is responsible for rendering the release details page, which includes information such as the release version, the number of failures, transactions per minute (TPM), and other performance metrics. The 'Overview' also includes various methods to handle changes in the release details, such as restoring a project, changing the transactions list sort order, and changing the date.

The 'Overview' also includes a sidebar, which is a separate component that displays additional details about the release. This includes the project release details, commit author breakdown, release stats, and other related information. These components are located in the 'static/app/views/releases/detail/overview/sidebar' directory.

Another important part of the 'Overview' is the 'ReleaseComparisonChart', which is a set of components used to display a comparison chart of the release events and sessions. These components are located in the 'static/app/views/releases/detail/overview/releaseComparisonChart' directory.

<SwmSnippet path="/static/app/views/releases/detail/overview/index.tsx" line="85">

---

# ReleaseOverview Class

The 'ReleaseOverview' class is responsible for rendering the release details page. It includes various methods to handle changes in the release details, such as restoring a project, changing the transactions list sort order, and changing the date.

```tsx
class ReleaseOverview extends DeprecatedAsyncView<Props> {
  getTitle() {
    const {params, organization} = this.props;
    return routeTitleGen(
      t('Release %s', formatVersion(params.release)),
      organization.slug,
      false
    );
  }

  handleRestore = async (project: ReleaseProject, successCallback: () => void) => {
    const {params, organization} = this.props;

    try {
      await restoreRelease(new Client(), {
        orgSlug: organization.slug,
        projectSlug: project.slug,
        releaseVersion: params.release,
      });
      successCallback();
    } catch {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/releases/detail/overview/index.tsx" line="392">

---

# Titles Constant

The 'titles' constant is used to define the titles of the columns in the transactions list. The titles change based on the selected sort option.

```tsx
          const titles =
            selectedSort.value !== TransactionsListOption.SLOW_LCP
              ? [t('transaction'), t('failure_count()'), t('tpm()'), t('p50()')]
              : [t('transaction'), t('failure_count()'), t('tpm()'), t('p75(lcp)')];
```

---

</SwmSnippet>

# Sidebar Components

The 'Overview' also includes a sidebar, which is a separate component that displays additional details about the release. This includes the project release details, commit author breakdown, release stats, and other related information. These components are located in the 'static/app/views/releases/detail/overview/sidebar' directory.

# ReleaseComparisonChart Components

Another important part of the 'Overview' is the 'ReleaseComparisonChart', which is a set of components used to display a comparison chart of the release events and sessions. These components are located in the 'static/app/views/releases/detail/overview/releaseComparisonChart' directory.

# Overview Functions

The 'Overview' functions are responsible for rendering the release details page, which includes information such as the release version, the number of failures, transactions per minute (TPM), and other performance metrics.

<SwmSnippet path="/static/app/views/releases/detail/overview/index.tsx" line="375">

---

## hasDiscover

The `hasDiscover` function checks if the organization has the 'discover-basic' feature. This is used to determine whether to display the 'Discover' tab in the UI.

```tsx
          releaseBounds,
        }) => {
          const {commitCount, version} = release;
          const hasDiscover = organization.features.includes('discover-basic');
          const hasPerformance = organization.features.includes('performance-view');
          const hasReleaseComparisonPerformance = organization.features.includes(
            'release-comparison-performance'
          );
          const {environments} = selection;
          const performanceType = platformToPerformanceType([project], [project.id]);
          const {selectedSort, sortOptions} = getTransactionsListSort(location);
          const releaseEventView = this.getReleaseEventView(
            version,
            project.id,
            selectedSort,
            releaseBounds
          );
          const titles =
            selectedSort.value !== TransactionsListOption.SLOW_LCP
              ? [t('transaction'), t('failure_count()'), t('tpm()'), t('p50()')]
              : [t('transaction'), t('failure_count()'), t('tpm()'), t('p75(lcp)')];
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/releases/detail/overview/index.tsx" line="380">

---

## environments

The `environments` function retrieves the environments from the selection. This is used to filter the release details based on the selected environment.

```tsx
          const hasReleaseComparisonPerformance = organization.features.includes(
            'release-comparison-performance'
          );
          const {environments} = selection;
          const performanceType = platformToPerformanceType([project], [project.id]);
          const {selectedSort, sortOptions} = getTransactionsListSort(location);
          const releaseEventView = this.getReleaseEventView(
            version,
            project.id,
            selectedSort,
            releaseBounds
          );
          const titles =
            selectedSort.value !== TransactionsListOption.SLOW_LCP
              ? [t('transaction'), t('failure_count()'), t('tpm()'), t('p50()')]
              : [t('transaction'), t('failure_count()'), t('tpm()'), t('p75(lcp)')];
          const releaseTrendView = this.getReleaseTrendView(
            version,
            project.id,
            releaseMeta.released,
            releaseBounds
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/releases/detail/overview/index.tsx" line="392">

---

## titles

The `titles` function determines the titles for the release details based on the selected sort value. This is used to customize the headers of the release details table.

```tsx
          const titles =
            selectedSort.value !== TransactionsListOption.SLOW_LCP
              ? [t('transaction'), t('failure_count()'), t('tpm()'), t('p50()')]
              : [t('transaction'), t('failure_count()'), t('tpm()'), t('p75(lcp)')];
          const releaseTrendView = this.getReleaseTrendView(
            version,
            project.id,
            releaseMeta.released,
            releaseBounds
          );
          const allReleasesPerformanceView = this.getAllReleasesPerformanceView(
            project.id,
            performanceType,
            releaseBounds
          );
          const releasePerformanceView = this.getReleasePerformanceView(
            version,
            project.id,
            performanceType,
            releaseBounds
          );
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/releases/detail/overview/index.tsx" line="423">

---

## organization

The `organization` function retrieves the organization details. This is used to fetch the sessions data for the release details.

```tsx
          const sessionsRequestProps: Omit<SessionsRequest['props'], 'children'> = {
            api,
            organization,
            field: [
              SessionFieldWithOperation.USERS,
              SessionFieldWithOperation.SESSIONS,
              SessionFieldWithOperation.DURATION,
            ],
            groupBy: ['session.status'],
            ...getReleaseParams({location, releaseBounds}),
            shouldFilterSessionsInTimeWindow: true,
          };

          const defaultDateTimeSelected = !period && !start && !end;

          const releaseBoundsLabel =
            releaseBounds.type === 'clamped'
              ? t('Clamped Release Period')
              : t('Entire Release Period');

          return (
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
