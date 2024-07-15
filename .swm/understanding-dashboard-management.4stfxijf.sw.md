---
title: Understanding Dashboard Management
---
In the Dashboards of the Sentry application, 'Manage' refers to the functionality that allows users to handle their dashboards. This includes creating, deleting, and duplicating dashboards. The `DashboardList` function in `dashboardList.tsx` is central to this functionality. It provides a list of dashboards and options to manipulate them. For instance, the `handleDelete` function is used to delete a dashboard, and the `handleDuplicate` function is used to create a copy of an existing dashboard.

The `onAdd` function in `index.tsx` is used to add a new dashboard. It calls the `createDashboard` function, which sends a POST request to the server to create a new dashboard. After the dashboard is successfully created, a success message is displayed to the user.

The `onAction` function in `dashboardList.tsx` is used to open a confirmation modal when a user attempts to delete a dashboard. If the user confirms the action, the `handleDelete` function is called to delete the dashboard.

The `dashboards` member in `dashboardList.tsx` and `index.tsx` holds the list of dashboards that the user can manage. This list is fetched from the server and displayed to the user.

<SwmSnippet path="/static/app/views/dashboards/manage/index.spec.tsx" line="69">

---

# Dashboard Management

This line of code displays a message to the user when they don't have any projects to manage. It's part of the 'Manage' functionality that ensures users have at least one project to use the view.

```tsx
      screen.getByText('You need at least one project to use this view')
```

---

</SwmSnippet>

# Dashboard Management

Dashboard Management APIs

<SwmSnippet path="/static/app/views/dashboards/manage/dashboardList.tsx" line="65">

---

## Dashboard Creation

The `handleDuplicate` function is used to create a copy of an existing dashboard. It first fetches the details of the dashboard to be duplicated, then creates a new dashboard with these details. The new dashboard is then sent to the server via a POST request to the '/organizations/org-slug/dashboards/' endpoint.

```tsx
  async function handleDuplicate(dashboard: DashboardListItem) {
    try {
      const dashboardDetail = await fetchDashboard(api, organization.slug, dashboard.id);
      const newDashboard = cloneDashboard(dashboardDetail);
      newDashboard.widgets.map(widget => (widget.id = undefined));
      await createDashboard(api, organization.slug, newDashboard, true);
      trackAnalytics('dashboards_manage.duplicate', {
        organization,
        dashboard_id: parseInt(dashboard.id, 10),
      });
      onDashboardsChange();
      addSuccessMessage(t('Dashboard duplicated'));
    } catch (e) {
      addErrorMessage(t('Error duplicating Dashboard'));
    }
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/dashboards/manage/dashboardList.tsx" line="50">

---

## Dashboard Deletion

The `handleDelete` function is used to delete a dashboard. It sends a DELETE request to the '/organizations/org-slug/dashboards/2/' endpoint, where '2' is the ID of the dashboard to be deleted.

```tsx
  function handleDelete(dashboard: DashboardListItem) {
    deleteDashboard(api, organization.slug, dashboard.id)
      .then(() => {
        trackAnalytics('dashboards_manage.delete', {
          organization,
          dashboard_id: parseInt(dashboard.id, 10),
        });
        onDashboardsChange();
        addSuccessMessage(t('Dashboard deleted'));
      })
      .catch(() => {
        addErrorMessage(t('Error deleting Dashboard'));
      });
  }
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
