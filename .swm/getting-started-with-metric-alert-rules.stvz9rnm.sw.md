---
title: Getting started with Metric Alert Rules
---
In the context of the sentry-demo repository, a 'Metric' in 'Rules' refers to a specific type of alert rule that is based on a statistical value, known as an aggregate, that is computed from the events fired by the application. This aggregate could be any numerical property derived from the events, such as count, average, sum, etc.

The 'Metric' rule is defined in various parts of the codebase, including the 'metricChart.tsx', 'relatedIssues.tsx', 'ruleForm.tsx', and 'types.tsx' files. It is used to specify the conditions under which an alert should be triggered.

The 'Metric' rule is also used in the 'duplicate.tsx' file, where it is used to create a duplicate of an existing metric alert rule. This is useful when you want to create a new rule that is similar to an existing one.

In the 'sidebar.tsx' file, the 'Metric' rule is used to display the details of a specific rule in the sidebar. This includes information such as the aggregate used, the time window, and the environment.

The 'Metric' rule is also used in the 'metricChartOption.tsx' file, where it is used to generate the options for the metric chart. This includes information such as the timeseries data, the rule, and the incidents.

<SwmSnippet path="/static/app/views/alerts/rules/metric/details/metricChart.tsx" line="500">

---

# Metric in metricChart.tsx

In the 'metricChart.tsx' file, the 'Metric' rule is used to specify the conditions under which an alert should be triggered. This includes information such as the aggregate used, the time window, and the environment.

```tsx
  render() {
    const {
      api,
      rule,
      organization,
      timePeriod,
      project,
      interval,
      query,
      location,
      isOnDemandAlert,
      selectedIncident,
    } = this.props;
    const {aggregate, timeWindow, environment, dataset} = rule;

    // Fix for 7 days * 1m interval being over the max number of results from events api
    // 10k events is the current max
    if (
      timePeriod.usingPeriod &&
      timePeriod.period === TimePeriod.SEVEN_DAYS &&
      interval === '1m'
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/alerts/rules/metric/details/metricHistoryActivation.tsx" line="13">

---

# Metric in metricHistoryActivation.tsx

In the 'metricHistoryActivation.tsx' file, the 'Metric' rule is used to display the details of a specific rule in the sidebar. This includes information such as the aggregate used, the time window, and the environment.

```tsx
type MetricHistoryActivationProps = {
  activationActivity: ActivationTriggerActivity;
  organization: Organization;
};

export default function MetricHistoryActivation({
  activationActivity,
  organization,
}: MetricHistoryActivationProps) {
  let trigger;
  let activator;
  switch (activationActivity.conditionType) {
    case String(ActivationConditionType.RELEASE_CREATION):
      activator = (
        <GlobalSelectionLink
          to={{
            pathname: `/organizations/${
              organization.slug
            }/releases/${encodeURIComponent(activationActivity.activator)}/`,
          }}
        >
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/alerts/rules/metric/details/metricHistory.tsx" line="23">

---

# Metric in metricHistory.tsx

In the 'metricHistory.tsx' file, the 'Metric' rule is used to sort and filter incidents based on their activities.

```tsx
function MetricHistory({incidents}: Props) {
  const organization = useOrganization();
  const sortedActivity = useMemo(() => {
    const filteredIncidents = (incidents ?? []).filter(
      incident => incident.activities?.length
    );
    const activationTriggers: ActivationTriggerActivity[] = [];
    // NOTE: disabling start/finish trigger rows for now until we've determined whether its
    // valuable during EA

    // activations?.forEach(activation => {
    //   activationTriggers.push({
    //     type: ActivationTrigger.ACTIVATED,
    //     activator: activation.activator,
    //     conditionType: activation.conditionType,
    //     dateCreated: activation.dateCreated,
    //   });
    //   if (activation.isComplete) {
    //     activationTriggers.push({
    //       type: ActivationTrigger.FINISHED,
    //       activator: activation.activator,
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
