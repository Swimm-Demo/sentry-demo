---
title: Understanding Alerts Management
---
Alerts in Sentry are used to notify users when certain conditions are met. They are defined in the 'alerts' directory, which contains various subdirectories and files that handle different aspects of alerts. The 'index.tsx' file is the main entry point for the alerts functionality, where the AlertsContainer component is defined. This component is responsible for rendering the children components and passing down necessary props.

The 'alerts' directory also contains several utility functions and constants used across different components. For instance, 'getMetricRuleDiscoverUrl.tsx' and 'getIncidentDiscoverUrl.tsx' are used to generate URLs for metric rules and incidents respectively. The 'constants.tsx' file defines constant values used in the alerts functionality.

The 'list' subdirectory contains components related to displaying a list of alerts. For example, 'header.tsx' defines the header of the alerts list, and 'onboarding.tsx' handles the onboarding process for new users. The 'onLoadAllEndpointsSuccess' function in 'incidents/index.tsx' is used to handle the successful loading of all endpoints, and it checks whether the user has configured alert rules or seen the welcome prompt.

The 'rules' subdirectory contains components and utilities related to alert rules. For instance, 'utils.tsx' provides utility functions for alert rules. The 'metric' subdirectory within 'rules' contains components specific to metric alert rules. The 'checkMetricAlertCompatiablity' function in 'incompatibleAlertQuery.tsx' checks whether a given event view is compatible with metric alert rules.

The 'builder' subdirectory contains components used in the alert rule creation process. For example, 'projectProvider.tsx' provides the project context to its children components, and 'builderBreadCrumbs.tsx' defines the breadcrumbs for the alert rule builder.

The 'wizard' subdirectory contains components for the alert creation wizard. It includes various utility functions and components to handle user interactions during the alert creation process.

<SwmSnippet path="/static/app/views/alerts/list/rules/alertRulesList.tsx" line="65">

---

# Alert Rules

The `AlertRulesList` function is the main component for displaying a list of alert rules. It uses various hooks and functions to fetch and manage alert rules, handle user interactions, and render the UI. It also uses the `router` object to navigate between different views.

```tsx
function AlertRulesList() {
  const location = useLocation();
  const router = useRouter();
  const api = useApi();
  const queryClient = useQueryClient();
  const organization = useOrganization();

  useRouteAnalyticsEventNames('alert_rules.viewed', 'Alert Rules: Viewed');
  useRouteAnalyticsParams({
    sort: Array.isArray(location.query.sort)
      ? location.query.sort.join(',')
      : location.query.sort,
  });

  // Fetch alert rules
  const {
    data: ruleListResponse = [],
    refetch,
    getResponseHeader,
    isLoading,
    isError,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/alerts/wizard/index.tsx" line="43">

---

# Alert Wizard

The `AlertWizard` function is used to handle the alert creation process. It maintains the `alertOption` state, which represents the type of the alert being created. The `handleChangeAlertOption` function is used to update this state.

```tsx
const DEFAULT_ALERT_OPTION = 'issues';

function AlertWizard({organization, params, location, projectId}: AlertWizardProps) {
  const [alertOption, setAlertOption] = useState<AlertType>(
    location.query.alert_option in AlertWizardAlertNames
      ? location.query.alert_option
      : DEFAULT_ALERT_OPTION
  );
  const projectSlug = params.projectId ?? projectId;

  const handleChangeAlertOption = (option: AlertType) => {
    setAlertOption(option);
  };

  function renderCreateAlertButton() {
    let metricRuleTemplate: Readonly<WizardRuleTemplate> | undefined =
      AlertWizardRuleTemplates[alertOption];
    const isMetricAlert = !!metricRuleTemplate;
    const isTransactionDataset = metricRuleTemplate?.dataset === Dataset.TRANSACTIONS;

    if (
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/alerts/rules/issue/index.tsx" line="420">

---

# Alert Configuration

The `refetchConfigs` method is used to fetch the latest alert configuration from the server. It makes an API request to fetch the configuration and updates the component's state with the received data.

```tsx
  refetchConfigs() {
    const {organization} = this.props;
    const {project} = this.state;

    this.api
      .requestPromise(
        `/projects/${organization.slug}/${project.slug}/rules/configuration/`
      )
      .then(response => this.setState({configs: response}))
      .catch(() => {
        // No need to alert user if this fails, can use existing data
      });
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/alerts/rules/metric/ruleForm.tsx" line="602">

---

# Alert Validation

The `validateActivatedAlerts` method is used to validate the alert configuration. It checks whether the alert type is 'ACTIVATED' and whether the activation condition and time window are defined.

```tsx
  validateActivatedAlerts() {
    const {organization} = this.props;
    const {monitorType, activationCondition, timeWindow} = this.state;

    const hasActivatedAlerts = organization.features.includes('activated-alert-rules');
    return (
      !hasActivatedAlerts ||
      monitorType !== MonitorType.ACTIVATED ||
      (activationCondition !== undefined && timeWindow)
    );
  }
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
