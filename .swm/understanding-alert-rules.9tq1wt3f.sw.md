---
title: Understanding Alert Rules
---
Rules in Alerts are a crucial part of the Sentry application. They are used to define the conditions under which alerts are triggered. These conditions can be based on various factors such as the occurrence of certain events, the violation of predefined thresholds, or the status of specific metrics. The rules are highly customizable, allowing developers to fine-tune the alerting mechanism according to their needs.

The rules are defined in the 'ruleForm.tsx' and 'ruleConditionsForm.tsx' files. These files contain various constants and methods that are used to set up and validate the rules. For example, the 'validateActivatedAlerts' method checks if the alert rules are activated and valid.

The 'IssueAlertRule' type in 'textRule.tsx' and the 'AlertRuleDetailsProps' interface in 'ruleDetails.tsx' are used to define the structure of the alert rules. These types and interfaces ensure that the rules are consistent and adhere to the required format.

The 'alertType' constant is used to specify the type of alert that is associated with a rule. This can be used to differentiate between different types of alerts and handle them accordingly.

The 'monitorType' member is used to specify the type of monitor that is associated with a rule. This can be used to differentiate between different types of monitors and handle them accordingly.

The 'hasActivatedAlerts' constant is used to check if the alert rules are activated. This is used to ensure that alerts are only triggered when the rules are active.

<SwmSnippet path="/static/app/views/alerts/rules/metric/ruleForm.tsx" line="1019">

---

# Rule Definition

The 'rule' constant is used to define the structure of a rule. It contains various properties such as 'name', 'query', 'project', 'timeWindow', 'triggers', 'aggregate', 'thresholdType', 'thresholdPeriod', 'comparisonDelta', 'comparisonType', 'resolveThreshold', 'loading', 'eventTypes', 'dataset', and 'alertType'.

```tsx
    const {
      organization,
      ruleId,
      rule,
      onSubmitSuccess,
      router,
      disableProjectSelector,
      eventView,
      location,
    } = this.props;
    const {
      name,
      query,
      project,
      timeWindow,
      triggers,
      aggregate,
      thresholdType,
      thresholdPeriod,
      comparisonDelta,
      comparisonType,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/alerts/rules/metric/ruleForm.tsx" line="254">

---

# Rule Navigation

The 'goBack' method is used to navigate back to the list of rules. It uses the 'router' and 'organization' constants to construct the URL.

```tsx
  goBack() {
    const {router} = this.props;
    const {organization} = this.props;

    router.push(normalizeUrl(`/organizations/${organization.slug}/alerts/rules/`));
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/alerts/rules/metric/details/index.tsx" line="54">

---

# Rule Details

The 'MetricAlertDetails' class is used to display the details of a rule. It fetches the necessary data when the component is mounted and updates it when necessary.

```tsx
class MetricAlertDetails extends Component<Props, State> {
  state: State = {isLoading: false, hasError: false, error: null, selectedIncident: null};

  componentDidMount() {
    const {api, organization} = this.props;

    fetchOrgMembers(api, organization.slug);
    this.fetchData();
    this.trackView();
  }

  componentDidUpdate(prevProps: Props) {
    const prevQuery = pick(prevProps.location.query, ['start', 'end', 'period', 'alert']);
    const nextQuery = pick(this.props.location.query, [
      'start',
      'end',
      'period',
      'alert',
    ]);
    if (
      !isEqual(prevQuery, nextQuery) ||
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/alerts/rules/metric/ruleForm.tsx" line="181">

---

# Rule Validation

The 'getDefaultState' method is used to initialize the state of a rule. It checks if the rule is valid and sets the default values for various properties.

```tsx
  getDefaultState(): State {
    const {rule, location, organization} = this.props;
    const triggersClone = [...rule.triggers];
    const {
      aggregate: _aggregate,
      eventTypes: _eventTypes,
      dataset: _dataset,
      name,
    } = location?.query ?? {};
    const eventTypes = typeof _eventTypes === 'string' ? [_eventTypes] : _eventTypes;

    // Warning trigger is removed if it is blank when saving
    if (triggersClone.length !== 2) {
      triggersClone.push(createDefaultTrigger(AlertRuleTriggerType.WARNING));
    }

    const aggregate = _aggregate ?? rule.aggregate;
    const dataset = _dataset ?? rule.dataset;

    const isErrorMigration =
      this.props.location?.query?.migration === '1' && ruleNeedsErrorMigration(rule);
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
