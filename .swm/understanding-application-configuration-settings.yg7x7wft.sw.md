---
title: Understanding Application Configuration Settings
---
Settings in the 'Views' directory of the sentry-demo repository refers to the configuration options available for different aspects of the application. These settings are organized into various components, each handling a specific part of the application's configuration.

For instance, the 'components' directory under 'settings' contains various components like 'teamSelect', 'settingsBreadcrumb', 'dataScrubbing', etc. Each of these components represents a specific setting or a group of related settings that the user can configure.

Similarly, the 'project' directory under 'settings' contains settings related to individual projects. These include settings for project filters, remote config, project ownership, and more.

The 'account' directory under 'settings' contains settings related to the user's account. These include settings for notifications, API applications, account security, and more.

Overall, the 'Settings' in 'Views' provide a way to manage and configure various aspects of the application, from user account details to project-specific configurations.

<SwmSnippet path="/static/app/views/settings/organizationGeneralSettings/organizationSettingsForm.tsx" line="33">

---

# Organization Settings

This file contains the form for organization settings. It uses the `location` constant to get the current location and the `access` constant to check if the user has write access to the organization.

```tsx
function OrganizationSettingsForm({initialData, onSave}: Props) {
  const location = useLocation();
  const organization = useOrganization();
  const endpoint = `/organizations/${organization.slug}/`;

  const access = useMemo(() => new Set(organization.access), [organization]);

  const jsonFormSettings = useMemo(
    () => ({
      features: new Set(organization.features),
      access,
      location,
      disabled: !access.has('org:write'),
    }),
    [access, location, organization]
  );

  const forms = useMemo(() => {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/project/projectKeys/details/keySettings.tsx" line="44">

---

# Project Settings

This file contains the settings for project keys. It uses the `api` constant to make API requests and the `handleRemove` function to handle the removal of a key.

```tsx
  data,
  updateData,
}: Props) {
  const api = useApi();

  const {keyId, projectId} = params;
  const apiEndpoint = `/projects/${organization.slug}/${projectId}/keys/${keyId}/`;

  const handleRemove = useCallback(async () => {
    addLoadingMessage(t('Revoking key\u2026'));

    try {
      await api.requestPromise(
        `/projects/${organization.slug}/${projectId}/keys/${keyId}/`,
        {
          method: 'DELETE',
        }
      );

      onRemove();
      addSuccessMessage(t('Revoked key'));
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/components/settingsLayout.tsx" line="35">

---

# Settings Layout

This file contains the layout for the settings. It uses the `toggleNav` function to toggle the visibility of the navigation and the `location` constant to get the current location.

```tsx
  const location = useLocation();

  const toggleNav = useCallback((visible: boolean) => {
    const bodyElement = document.getElementsByTagName('body')[0];

    window.scrollTo?.(0, 0);
    bodyElement.classList[visible ? 'add' : 'remove']('scroll-lock');

    setMobileNavVisible(visible);
    setNavOffsetTop(headerRef.current?.getBoundingClientRect().bottom ?? 0);
  }, []);

  // Close menu when navigating away
  useEffect(() => toggleNav(false), [toggleNav, location.pathname]);

  const {renderNavigation, children, params, routes, route} = props;

  // We want child's view's props
  const childProps = children && isValidElement(children) ? children.props : props;
  const childRoutes = childProps.routes || routes || [];
  const childRoute = childProps.route || route || {};
```

---

</SwmSnippet>

# Endpoints Explanation

Project Performance Settings

<SwmSnippet path="/static/app/views/settings/projectPerformance/projectPerformance.tsx" line="119">

---

## Project Performance Settings

The `getPerformanceIssuesEndpoint` function constructs the endpoint URL for fetching performance issues for a specific project. The endpoint URL is constructed using the organization ID and project ID.

```tsx
  getProjectEndpoint({orgId, projectId}: RouteParams) {
    return `/projects/${orgId}/${projectId}/`;
  }

  getPerformanceIssuesEndpoint({orgId, projectId}: RouteParams) {
    return `/projects/${orgId}/${projectId}/performance-issues/configure/`;
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/projectPerformance/projectPerformance.tsx" line="119">

---

## Project Endpoint

The `getProjectEndpoint` function constructs the endpoint URL for fetching a specific project. The endpoint URL is constructed using the organization ID and project ID.

```tsx
  getProjectEndpoint({orgId, projectId}: RouteParams) {
    return `/projects/${orgId}/${projectId}/`;
  }
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
