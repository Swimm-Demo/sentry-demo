---
title: Getting Started with Organization Management
---
Organizations in the Sentry-demo project refer to entities that represent a group of users and their associated projects, teams, and settings. They are used to manage access control and permissions across the application.

In the components directory, the 'organization' constant is often used to fetch and manipulate data related to the organization. For instance, it is used to determine if certain features are enabled for the organization, such as 'global-views' or 'open-membership'.

The 'organization' constant is also used to determine the role of the organization, which can be 'owner' or 'manager'. This information is used to control access to certain functionalities within the application.

In the 'PageFilterPinButton' component, the 'organization' member is used to track analytics when a page filter is pinned or unpinned. This helps in understanding user interactions within the organization.

<SwmSnippet path="/static/app/components/organizations/projectPageFilter/index.tsx" line="98">

---

# Usage of 'organization' constant

Here, the 'organization' constant is used to determine if certain features are enabled for the organization, such as 'global-views' or 'open-membership'. It is also used to determine the role of the organization, which can be 'owner' or 'manager'. This information is used to control access to certain functionalities within the application.

```tsx
  const organization = useOrganization();

  const allowMultiple = organization.features.includes('global-views');

  const {projects, initiallyLoaded: projectsLoaded} = useProjects();
  const [memberProjects, otherProjects] = useMemo(
    () => partition(projects, project => project.isMember),
    [projects]
  );

  const showNonMemberProjects = useMemo(() => {
    const {isSuperuser} = ConfigStore.get('user');
    const isOrgAdminOrManager =
      organization.orgRole === 'owner' || organization.orgRole === 'manager';
    const isOpenMembership = organization.features.includes('open-membership');

    return isSuperuser || isOrgAdminOrManager || isOpenMembership;
  }, [organization.orgRole, organization.features]);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/organizations/environmentPageFilter/index.tsx" line="65">

---

# 'organization' in EnvironmentPageFilter

In the 'EnvironmentPageFilter' component, the 'organization' constant is used to fetch and manipulate data related to the organization.

```tsx
  const organization = useOrganization();

  const {projects, initiallyLoaded: projectsLoaded} = useProjects();

  const {
    selection: {projects: projectPageFilterValue, environments: envPageFilterValue},
    isReady: pageFilterIsReady,
    desyncedFilters,
  } = usePageFilters();

  const environments = useMemo<string[]>(() => {
    const isSuperuser = isActiveSuperuser();

    const unsortedEnvironments = projects.flatMap(project => {
      const projectId = parseInt(project.id, 10);
      // Include environments from:
      // - all projects if the user is a superuser
      // - the requested projects
      // - all member projects if 'my projects' (empty list) is selected.
      // - all projects if -1 is the only selected project.
      if (
```

---

</SwmSnippet>

# Usage of 'organization' in Components

This section provides an overview of how the 'organization' constant is used in various components of the sentry-demo project.

<SwmSnippet path="/static/app/components/organizations/projectPageFilter/index.tsx" line="98">

---

## Usage of 'organization' in ProjectPageFilter

In the 'ProjectPageFilter' component, the 'organization' constant is used to determine if certain features are enabled for the organization, such as 'global-views' or 'open-membership'. It is also used to determine the role of the organization, which can be 'owner' or 'manager'. This information is used to control access to certain functionalities within the application.

```tsx
  const organization = useOrganization();

  const allowMultiple = organization.features.includes('global-views');

  const {projects, initiallyLoaded: projectsLoaded} = useProjects();
  const [memberProjects, otherProjects] = useMemo(
    () => partition(projects, project => project.isMember),
    [projects]
  );

  const showNonMemberProjects = useMemo(() => {
    const {isSuperuser} = ConfigStore.get('user');
    const isOrgAdminOrManager =
      organization.orgRole === 'owner' || organization.orgRole === 'manager';
    const isOpenMembership = organization.features.includes('open-membership');

    return isSuperuser || isOrgAdminOrManager || isOpenMembership;
  }, [organization.orgRole, organization.features]);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/organizations/environmentPageFilter/index.tsx" line="65">

---

## Usage of 'organization' in EnvironmentPageFilter

In the 'EnvironmentPageFilter' component, the 'organization' constant is used in several callback functions to manipulate the router and the organization's data.

```tsx
  const organization = useOrganization();

  const {projects, initiallyLoaded: projectsLoaded} = useProjects();

  const {
    selection: {projects: projectPageFilterValue, environments: envPageFilterValue},
    isReady: pageFilterIsReady,
    desyncedFilters,
  } = usePageFilters();

  const environments = useMemo<string[]>(() => {
    const isSuperuser = isActiveSuperuser();

    const unsortedEnvironments = projects.flatMap(project => {
      const projectId = parseInt(project.id, 10);
      // Include environments from:
      // - all projects if the user is a superuser
      // - the requested projects
      // - all member projects if 'my projects' (empty list) is selected.
      // - all projects if -1 is the only selected project.
      if (
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/organizations/pageFilters/container.tsx" line="75">

---

## Usage of 'organization' in PageFiltersContainer

In the 'PageFiltersContainer' component, the 'organization' constant is used to determine if the 'global-views' feature is enabled for the organization. It is also used to initialize the URL state.

```tsx
  const organization = useOrganization();

  const {isReady} = usePageFilters();

  const {projects, initiallyLoaded: projectsLoaded} = useProjects();

  const enforceSingleProject = !organization.features.includes('global-views');

  const specifiedProjects = specificProjectSlugs
    ? projects.filter(project => specificProjectSlugs.includes(project.slug))
    : projects;

  const user = useUser();
  const memberProjects = user.isSuperuser
    ? specifiedProjects
    : specifiedProjects.filter(project => project.isMember);
  const nonMemberProjects = user.isSuperuser
    ? []
    : specifiedProjects.filter(project => !project.isMember);

  const doInitialization = () => {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/organizations/projectPageFilter/menuFooter.tsx" line="27">

---

## Usage of 'organization' in ProjectPageFilterMenuFooter

In the 'ProjectPageFilterMenuFooter' component, the 'organization' constant is used to render certain features based on the organization's settings. It is also used to construct a URL for adding a new project.

```tsx
  const organization = useOrganization();
  const {projects} = useProjects();

  return (
    <Fragment>
      <Feature
        organization={organization}
        features="organizations:global-views"
        hookName="feature-disabled:project-selector-all-projects"
        renderDisabled={false}
      >
        {({renderShowAllButton}: FeatureRenderProps) => {
          // if our hook is adding renderShowAllButton, render that
          if (showNonMemberProjects && renderShowAllButton && projects.length > 1) {
            return renderShowAllButton({
              onButtonClick: () => handleChange([]),
              canShowAllProjects: showNonMemberProjects,
            });
          }

          return null;
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
