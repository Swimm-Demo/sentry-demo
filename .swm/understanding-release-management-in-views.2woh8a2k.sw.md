---
title: Understanding Release Management in Views
---
Releases in the 'Views' directory of the sentry-demo repository refer to the specific versions of the software that are prepared for distribution. They are represented as a list in the 'ReleasesList' component, which is a part of the 'Releases' view. This component fetches and displays a list of releases, allowing users to sort and filter them. Each release in the list is represented by a 'Release' object, which includes details such as the version, commit count, and last deployment.

The 'Releases' view also includes a 'ReleaseOverview' component, which provides a detailed view of a specific release. This component fetches and displays detailed information about a release, including its performance metrics and associated issues. It also provides options to sort and filter transactions associated with the release.

In addition to the 'ReleasesList' and 'ReleaseOverview' components, the 'Releases' view includes several utility components and functions that assist in fetching, processing, and displaying release data. These include 'ReleasesRequest', which fetches release data from the API, and 'ReleasesDisplayOptions', which provides options for how releases are displayed.

<SwmSnippet path="/static/app/views/releases/list/index.tsx" line="66">

---

# Release List

The 'ReleasesList' component fetches and displays a list of releases. It allows users to sort and filter the releases, and provides options for how the releases are displayed.

```tsx
type RouteParams = {
  orgId: string;
};

type Props = RouteComponentProps<RouteParams, {}> & {
  api: Client;
  organization: Organization;
  projects: Project[];
  selection: PageFilters;
};

type State = {
  releases: Release[];
} & DeprecatedAsyncView['state'];

class ReleasesList extends DeprecatedAsyncView<Props, State> {
  shouldReload = true;
  shouldRenderBadRequests = true;

  getTitle() {
    return routeTitleGen(t('Releases'), this.props.organization.slug, false);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/releases/detail/overview/index.tsx" line="63">

---

# Release Overview

The 'ReleaseOverview' component provides a detailed view of a specific release. It fetches and displays detailed information about the release, including its performance metrics and associated issues. It also provides options to sort and filter transactions associated with the release.

```tsx
const RELEASE_PERIOD_KEY = 'release';

export enum TransactionsListOption {
  FAILURE_COUNT = 'failure_count',
  TPM = 'tpm',
  SLOW = 'slow',
  SLOW_LCP = 'slow_lcp',
  REGRESSION = 'regression',
  IMPROVEMENT = 'improved',
}

type RouteParams = {
  orgId: string;
  release: string;
};

type Props = RouteComponentProps<RouteParams, {}> & {
  api: Client;
  organization: Organization;
  selection: PageFilters;
};
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/releases/list/releasesRequest.tsx" line="88">

---

# Release Request

The 'ReleasesRequest' component is a utility component that fetches release data from the API. It is used by the 'ReleasesList' and 'ReleaseOverview' components to fetch the data they need to display.

```tsx
  display: ReleasesDisplayOption[];
  location: Location;
  organization: Organization;
  releases: string[];
  selection: PageFilters;
  defaultStatsPeriod?: string;
  disable?: boolean;
  healthStatsPeriod?: HealthStatsPeriodOption;
  releasesReloading?: boolean;
};
type State = {
  errored: boolean;
  loading: boolean;
  statusCountByProjectInPeriod: SessionApiResponse | null;
  statusCountByReleaseInPeriod: SessionApiResponse | null;
  totalCountByProjectIn24h: SessionApiResponse | null;
  totalCountByProjectInPeriod: SessionApiResponse | null;
  totalCountByReleaseIn24h: SessionApiResponse | null;
  totalCountByReleaseInPeriod: SessionApiResponse | null;
};

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/releases/list/releasesRequest.tsx" line="88">

---

# Release Display Options

The 'ReleasesDisplayOption' is a type that provides options for how releases are displayed. It is used by the 'ReleasesList' component to determine how to display the list of releases.

```tsx
  display: ReleasesDisplayOption[];
  location: Location;
  organization: Organization;
  releases: string[];
  selection: PageFilters;
  defaultStatsPeriod?: string;
  disable?: boolean;
  healthStatsPeriod?: HealthStatsPeriodOption;
  releasesReloading?: boolean;
};
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
