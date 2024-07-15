---
title: Introduction to the Discover Feature
---
Discover in the Views directory refers to a feature in Sentry that allows users to explore and investigate their data. It provides a flexible query builder to create custom queries, visualize data in various ways, and dive deep into event details. The Discover feature is implemented across multiple files and components within the Views directory.

<SwmSnippet path="/static/app/views/discover/index.tsx" line="14">

---

The DiscoverContainer component in this file is a key part of the Discover feature. It checks if the user has access to the Discover feature and renders the appropriate content.

```tsx
function DiscoverContainer({organization, children}: Props) {
  function renderNoAccess() {
    return (
      <Layout.Page withPadding>
        <Alert type="warning">{t("You don't have access to this feature")}</Alert>
      </Layout.Page>
    );
  }

  return (
    <Feature
      features="discover-basic"
      organization={organization}
      hookName="feature-disabled:discover2-page"
      renderDisabled={renderNoAccess}
    >
      <NoProjectMessage organization={organization}>{children}</NoProjectMessage>
    </Feature>
  );
}

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/utils.tsx" line="167">

---

The getPrebuiltQueries function in this file is used to generate a set of predefined queries for the Discover feature. These queries are used to provide users with a starting point for exploring their data.

```tsx
export function getPrebuiltQueries(organization: Organization) {
  const views = [...ALL_VIEWS];
  if (organization.features.includes('performance-view')) {
    // insert transactions queries at index 2
    views.splice(2, 0, ...TRANSACTION_VIEWS);
    views.push(...WEB_VITALS_VIEWS);
  }

  return views;
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/homepage.tsx" line="22">

---

The HomepageQueryAPI component in this file is responsible for fetching the saved queries for the Discover homepage. It also handles the logic for updating the URL with the selected query parameters.

```tsx
type Props = {
  api: Client;
  loading: boolean;
  location: Location;
  organization: Organization;
  router: InjectedRouter;
  selection: PageFilters;
  setSavedQuery: (savedQuery: SavedQuery) => void;
};

type HomepageQueryState = DeprecatedAsyncComponent['state'] & {
  savedQuery?: SavedQuery | null;
  starfishResult?: null;
};

class HomepageQueryAPI extends DeprecatedAsyncComponent<Props, HomepageQueryState> {
  shouldReload = true;

  componentDidUpdate(_, prevState) {
    const hasFetchedSavedQuery = !prevState.savedQuery && this.state.savedQuery;
    const hasInitiallyLoaded = prevState.loading && !this.state.loading;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/results.tsx" line="79">

---

The Results component in this file is responsible for fetching and displaying the results of a query in the Discover feature. It handles the logic for updating the query parameters, fetching the data, and rendering the results.

```tsx
type Props = {
  api: Client;
  loading: boolean;
  location: Location;
  organization: Organization;
  router: InjectedRouter;
  selection: PageFilters;
  setSavedQuery: (savedQuery?: SavedQuery) => void;
  isHomepage?: boolean;
  savedQuery?: SavedQuery;
};

type State = {
  confirmedQuery: boolean;
  error: string;
  errorCode: number;
  eventView: EventView;
  needConfirmation: boolean;
  showTags: boolean;
  tips: string[];
  totalValues: null | number;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/index.tsx" line="1">

---

# DiscoverContainer Component

The DiscoverContainer component is the main entry point for the Discover feature. It checks if the user has access to the Discover feature and if not, it displays a warning message. If the user has access, it renders the children components within the NoProjectMessage component.

```tsx
import Feature from 'sentry/components/acl/feature';
import {Alert} from 'sentry/components/alert';
import * as Layout from 'sentry/components/layouts/thirds';
import NoProjectMessage from 'sentry/components/noProjectMessage';
import {t} from 'sentry/locale';
import type {Organization} from 'sentry/types/organization';
import withOrganization from 'sentry/utils/withOrganization';

type Props = {
  children: React.ReactNode;
  organization: Organization;
};

function DiscoverContainer({organization, children}: Props) {
  function renderNoAccess() {
    return (
      <Layout.Page withPadding>
        <Alert type="warning">{t("You don't have access to this feature")}</Alert>
      </Layout.Page>
    );
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/utils.tsx" line="744">

---

# getTargetForTransactionSummaryLink Function

The getTargetForTransactionSummaryLink function is a utility function used in the Discover feature. It takes in a data row, organization, projects, next view, and location as parameters and returns a target for the transaction summary link. This function is used to navigate to the transaction summary page from the Discover page.

```tsx
export function getTargetForTransactionSummaryLink(
  dataRow: EventData,
  organization: Organization,
  projects?: Project[],
  nextView?: EventView,
  location?: Location
) {
  let projectID: string | string[] | undefined;
  const filterProjects = location?.query.project;

  if (typeof filterProjects === 'string' && filterProjects !== '-1') {
    // Project selector in discover has just one selected project
    projectID = filterProjects;
  } else {
    const projectMatch = projects?.find(
      project =>
        project.slug && [dataRow['project.name'], dataRow.project].includes(project.slug)
    );
    projectID = projectMatch ? [projectMatch.id] : undefined;
  }

```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
