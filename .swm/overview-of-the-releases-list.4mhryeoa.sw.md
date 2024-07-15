---
title: Overview of the Releases List
---
The 'List' in the 'Releases' section of the sentry-demo repository refers to the display of all the releases in a structured format. It is implemented in the 'ReleasesList' class in the 'index.tsx' file within the 'releases/list' directory. The 'List' provides a comprehensive view of all the releases, including their details such as the date of creation, total sessions, active users, crash-free users, and more. The 'List' also allows for sorting and filtering of the releases based on various parameters like date, build number, semantic version, etc., enhancing the user's ability to navigate and manage the releases.

The 'List' also includes a 'ReleasesDropdown' component that allows users to select and view specific releases. The 'ReleasesRequest' component fetches the data for the releases, and the 'ReleasesPromo' component provides promotional information about the releases. The 'List' also includes a 'ReleasesDisplayOption' component that allows users to choose how the releases are displayed.

The 'List' is styled using styled-components, a CSS-in-JS library, which allows for dynamic styling based on props and themes. The styling is responsive, adapting to different screen sizes for an optimal viewing experience across various devices.

<SwmSnippet path="/static/app/views/releases/list/index.tsx" line="616">

---

# List Styling

The 'List' is styled using styled-components, a CSS-in-JS library, which allows for dynamic styling based on props and themes. The styling is responsive, adapting to different screen sizes for an optimal viewing experience across various devices.

```tsx
const AlertText = styled('div')`
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  gap: ${space(2)};

  > *:nth-child(1) {
    flex: 1;
  }
  flex-direction: column;
  @media (min-width: ${p => p.theme.breakpoints.medium}) {
    flex-direction: row;
  }
`;

const ReleasesPageFilterBar = styled(PageFilterBar)`
  margin-bottom: ${space(2)};
`;

const SortAndFilterWrapper = styled('div')`
  display: grid;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/releases/list/index.tsx" line="87">

---

# List Data Fetching

The 'getEndpoints' method in the 'ReleasesList' class is responsible for fetching the data for the releases. It constructs a query with parameters like 'project', 'environment', 'cursor', 'query', 'sort', etc., and makes a request to the '/organizations/{organization.slug}/releases/' endpoint.

```tsx
  }

  getEndpoints(): ReturnType<DeprecatedAsyncView['getEndpoints']> {
    const {organization, location} = this.props;
    const {statsPeriod} = location.query;
    const activeSort = this.getSort();
    const activeStatus = this.getStatus();

    const query = {
      ...pick(location.query, ['project', 'environment', 'cursor', 'query', 'sort']),
      summaryStatsPeriod: statsPeriod,
      per_page: 20,
      flatten: activeSort === ReleasesSortOption.DATE ? 0 : 1,
      adoptionStages: 1,
      status:
        activeStatus === ReleasesStatusOption.ARCHIVED
          ? ReleaseStatus.ARCHIVED
          : ReleaseStatus.ACTIVE,
    };

    const endpoints: ReturnType<DeprecatedAsyncView['getEndpoints']> = [
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/releases/list/index.tsx" line="158">

---

# List Display Options

The 'getDisplay' method in the 'ReleasesList' class determines how the releases are displayed. It checks the 'display' query parameter and returns the corresponding 'ReleasesDisplayOption'.

```tsx
  getDisplay(): ReleasesDisplayOption {
    const {display} = this.props.location.query;

    switch (display) {
      case ReleasesDisplayOption.USERS:
        return ReleasesDisplayOption.USERS;
      default:
        return ReleasesDisplayOption.SESSIONS;
    }
```

---

</SwmSnippet>

# Functions in Releases List

In this section, we will discuss the main functions used in the 'List' of the 'Releases' section.

<SwmSnippet path="/static/app/views/releases/list/index.tsx" line="141">

---

## getSort

The `getSort` function is used to determine the sorting option for the releases. It checks if the sort option exists in the `ReleasesSortOption` enumeration. If it does, it returns the sort option; otherwise, it defaults to sorting by date.

```tsx
  getSort(): ReleasesSortOption {
    const {environments} = this.props.selection;
    const {sort} = this.props.location.query;

    // Require 1 environment for date adopted
    if (sort === ReleasesSortOption.ADOPTION && environments.length !== 1) {
      return ReleasesSortOption.DATE;
    }

    const sortExists = Object.values(ReleasesSortOption).includes(sort);
    if (sortExists) {
      return sort;
    }

    return ReleasesSortOption.DATE;
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/releases/list/index.tsx" line="158">

---

## getDisplay

The `getDisplay` function is used to determine the display option for the releases. It checks the `display` query parameter in the location query. If it's set to 'users', it returns the 'users' display option; otherwise, it defaults to the 'sessions' display option.

```tsx
  getDisplay(): ReleasesDisplayOption {
    const {display} = this.props.location.query;

    switch (display) {
      case ReleasesDisplayOption.USERS:
        return ReleasesDisplayOption.USERS;
      default:
        return ReleasesDisplayOption.SESSIONS;
    }
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/releases/list/index.tsx" line="188">

---

## getSelectedProjectSlugs

The `getSelectedProjectSlugs` function is used to get the slugs of the selected projects. It reduces the projects array to a list of slugs of the selected projects.

```tsx
  getSelectedProjectSlugs(): string[] {
    const {selection, projects} = this.props;
    const projIdSet = new Set(selection.projects);

    return projects.reduce((result: string[], proj) => {
      if (projIdSet.has(Number(proj.id))) {
        result.push(proj.slug);
      }
      return result;
    }, []);
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/releases/list/index.tsx" line="213">

---

## handleSortBy

The `handleSortBy` function is a handler for the sort by event. It updates the location query with the new sort option.

```tsx
  handleSortBy = (sort: string) => {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/releases/list/index.tsx" line="222">

---

## handleDisplay

The `handleDisplay` function is a handler for the display event. It updates the location query with the new display option.

```tsx
  handleDisplay = (display: string) => {
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
