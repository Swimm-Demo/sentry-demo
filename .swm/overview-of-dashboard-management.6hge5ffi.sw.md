---
title: Overview of Dashboard Management
---
Dashboards in Sentry are customizable spaces for visualizing performance data. They are composed of widgets that display various types of data such as issues, releases, and metrics. Dashboards are defined in the `dashboard.tsx` file and can be managed in the `manage/index.tsx` file. The `renderDashboards` method is used to render the dashboards on the screen.

The `Props` type in `dashboard.tsx` and `manage/dashboardList.tsx` files define the properties that the dashboard components receive. These properties include the API client, the dashboard details, and other necessary data for rendering and managing the dashboards.

The `State` type in `dashboard.tsx` and `orgDashboards.tsx` files define the state of the dashboard components. This state includes whether the dashboard is being viewed on a mobile device, the layout of the dashboard, and the selected dashboard.

The `render` method in `dashboard.tsx` is responsible for rendering the dashboard. It filters the widgets based on the organization's features, calculates the column depths for the layout, and renders the widgets and the add widget button if the user has the necessary permissions.

The `dashboards` member in `orgDashboards.tsx` and `manage/dashboardList.tsx` files is an array of dashboard list items. It represents the list of dashboards that are displayed to the user.

The `dashboards` term is also used in various localization files to represent the term 'dashboards' in different languages.

<SwmSnippet path="/static/app/views/dashboards/dashboard.tsx" line="75">

---

# Dashboard Definition

The `Props` type defines the properties that the dashboard components receive. These properties include the API client, the dashboard details, and other necessary data for rendering and managing the dashboards.

```tsx
type Props = {
  api: Client;
  dashboard: DashboardDetails;
  handleAddCustomWidget: (widget: Widget) => void;
  handleUpdateWidgetList: (widgets: Widget[]) => void;
  isEditingDashboard: boolean;
  location: Location;
  /**
   * Fired when widgets are added/removed/sorted.
   */
  onUpdate: (widgets: Widget[]) => void;
  organization: Organization;
  router: InjectedRouter;
  selection: PageFilters;
  widgetLimitReached: boolean;
  handleAddMetricWidget?: (layout?: Widget['layout']) => void;
  isPreview?: boolean;
  newWidget?: Widget;
  onSetNewWidget?: () => void;
  paramDashboardId?: string;
  paramTemplateId?: string;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/dashboards/dashboard.tsx" line="98">

---

# Dashboard State

The `State` type defines the state of the dashboard components. This state includes whether the dashboard is being viewed on a mobile device, the layout of the dashboard, and the selected dashboard.

```tsx
type State = {
  isMobile: boolean;
  layouts: Layouts;
  windowWidth: number;
};

class Dashboard extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    const {dashboard} = props;
    const desktopLayout = getDashboardLayout(dashboard.widgets);
    this.state = {
      isMobile: false,
      layouts: {
        [DESKTOP]: desktopLayout,
        [MOBILE]: getMobileLayout(desktopLayout, dashboard.widgets),
      },
      windowWidth: window.innerWidth,
    };
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/dashboards/dashboard.tsx" line="131">

---

# Dashboard Rendering

The `render` method is responsible for rendering the dashboard. It filters the widgets based on the organization's features, calculates the column depths for the layout, and renders the widgets and the add widget button if the user has the necessary permissions.

```tsx
      !isEqual(
        dashboardLayout.map(pickDefinedStoreKeys),
        state.layouts[DESKTOP].map(pickDefinedStoreKeys)
      )
    ) {
      return {
        ...state,
        layouts: {
          [DESKTOP]: dashboardLayout,
          [MOBILE]: getMobileLayout(dashboardLayout, props.dashboard.widgets),
        },
      };
    }
    return null;
  }

  componentDidMount() {
    const {newWidget} = this.props;
    window.addEventListener('resize', this.debouncedHandleResize);

    // Always load organization tags on dashboards
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/dashboards/orgDashboards.tsx" line="36">

---

# Dashboard List

The `dashboards` member is an array of dashboard list items. It represents the list of dashboards that are displayed to the user.

```tsx
type State = {
  // endpoint response
  dashboards: DashboardListItem[] | null;
  /**
   * The currently selected dashboard.
   */
  selectedDashboard: DashboardDetails | null;
} & DeprecatedAsyncComponent['state'];

class OrgDashboards extends DeprecatedAsyncComponent<Props, State> {
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/locale/he/LC_MESSAGES/django.po" line="2521">

---

# Localization

The term `dashboards` is also used in various localization files to represent the term 'dashboards' in different languages.

```gettext catalog
#: static/app/components/dashboards/issueWidgetQueriesForm.tsx:82
#: static/app/components/dashboards/widgetQueriesForm.tsx:99
#: static/app/components/events/interfaces/breadcrumbs/utils.tsx:112
#: static/app/views/issueList/createSavedSearchModal.tsx:138
#: templates/sentry/partial/interfaces/http_email.html:21
msgid "Query"
msgstr ""

#: static/app/components/events/interfaces/richHttpContent/richHttpContent.tsx:28
#: templates/sentry/partial/interfaces/http_email.html:29
msgid "Fragment"
msgstr ""

#: static/app/components/events/contextSummary/contextSummaryUser.tsx:46
#: templates/sentry/partial/interfaces/user_email.html:14
msgid "ID:"
msgstr ""

#: templates/sentry/partial/interfaces/user_email.html:20
msgid "IP Address:"
msgstr ""
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
