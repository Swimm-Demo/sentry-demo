---
title: Introduction to Issue Alert Rule
---
An 'Issue' in the Rules directory of the sentry-demo repository refers to a specific type of alert rule. These rules are designed to trigger alerts when certain conditions are met within the application's error and performance data. The 'Issue' is defined and manipulated in various files within the Rules directory, such as 'issueList.tsx' and 'index.tsx'.

The 'Issue' is represented as a rule object in the codebase. This object contains various properties that define the conditions for the alert, such as 'conditions', 'filters', 'actionMatch', 'filterMatch', 'frequency', and 'name'. These properties are used to determine when and how an alert should be triggered.

The 'Issue' also interacts with other components of the application. For example, it uses the 'useApiQuery' function to fetch group history data, and it uses the 'useOrganization' function to get information about the current organization. It also uses various styled components to define its appearance in the user interface.

In addition to its properties, the 'Issue' also has various methods that manipulate its state and behavior. For example, the 'isRuleStateChange' method checks if there has been a change in the rule's state, and the 'renderRuleName' method renders the rule's name in the user interface.

<SwmSnippet path="/static/app/views/alerts/rules/issue/details/issuesList.tsx" line="22">

---

# Issue Definition

Here we see the 'GroupHistory' type which is used to represent an issue. It contains properties like 'count', 'eventId', 'group', and 'lastTriggered' which are used to define the issue.

```tsx
type GroupHistory = {
  count: number;
  eventId: string;
  group: Group;
  lastTriggered: string;
};
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/alerts/rules/issue/previewIssues.tsx" line="54">

---

# Issue Usage

In this snippet, we see the 'PreviewIssues' function which uses the 'issue' object. It uses properties of the issue like 'conditions', 'filters', 'actionMatch', 'filterMatch', and 'frequency' to determine when and how an alert should be triggered.

```tsx
export function PreviewIssues({members, rule, project}: PreviewIssuesProps) {
  const api = useApi();
  const organization = useOrganization();
  const isMounted = useIsMountedRef();
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [previewError, setPreviewError] = useState<boolean>(false);
  const [previewGroups, setPreviewGroups] = useState<string[]>([]);
  const [previewPage, setPreviewPage] = useState<number>(0);
  const [pageLinks, setPageLinks] = useState<string>('');
  const [issueCount, setIssueCount] = useState<number>(0);
  const endDateRef = useRef<string | null>(null);

  /**
   * If any of this data changes we'll need to re-fetch the preview
   */
  const relevantRuleData = useMemo(
    () =>
      rule
        ? {
            conditions: rule.conditions || [],
            filters: rule.filters || [],
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/alerts/rules/issue/details/issuesList.tsx" line="35">

---

# Issue Interaction with Other Components

In this snippet, we see how the 'Issue' interacts with other components of the application. It uses the 'useApiQuery' function to fetch group history data, and it uses the 'useOrganization' function to get information about the current organization.

```tsx
function AlertRuleIssuesList({project, rule, period, start, end, utc, cursor}: Props) {
  const organization = useOrganization();
  const {
    data: groupHistory,
    getResponseHeader,
    isLoading,
    isError,
    error,
  } = useApiQuery<GroupHistory[]>(
    [
      `/projects/${organization.slug}/${project.slug}/rules/${rule.id}/group-history/`,
      {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/alerts/rules/issue/previewIssues.tsx" line="93">

---

# Issue Methods

Here we see the 'api' constant being used to make a request to the '/rules/preview/' endpoint. This is an example of how the 'Issue' uses various methods to manipulate its state and behavior.

```tsx
      // we currently don't have a way to parse objects from query params, so this method is POST for now
      api
        .requestPromise(`/projects/${organization.slug}/${project.slug}/rules/preview/`, {
```

---

</SwmSnippet>

# Issue Functions

The 'Issue' is represented as a rule object in the codebase. This object contains various properties that define the conditions for the alert, such as 'conditions', 'filters', 'actionMatch', 'filterMatch', 'frequency', and 'name'. These properties are used to determine when and how an alert should be triggered.

<SwmSnippet path="/static/app/views/alerts/rules/issue/details/issuesList.tsx" line="35">

---

## AlertRuleIssuesList

The AlertRuleIssuesList function is used to list the issues related to a specific alert rule. It uses the 'useApiQuery' function to fetch group history data, and it uses the 'useOrganization' function to get information about the current organization.

```tsx
function AlertRuleIssuesList({project, rule, period, start, end, utc, cursor}: Props) {
  const organization = useOrganization();
  const {
    data: groupHistory,
    getResponseHeader,
    isLoading,
    isError,
    error,
  } = useApiQuery<GroupHistory[]>(
    [
      `/projects/${organization.slug}/${project.slug}/rules/${rule.id}/group-history/`,
      {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/alerts/rules/issue/previewIssues.tsx" line="54">

---

## PreviewIssues

The PreviewIssues function is used to preview the issues that would be triggered by a specific alert rule. It uses the 'useApi' function to make API requests, and it uses the 'useOrganization' function to get information about the current organization. It also uses various state variables to manage its state.

```tsx
export function PreviewIssues({members, rule, project}: PreviewIssuesProps) {
  const api = useApi();
  const organization = useOrganization();
  const isMounted = useIsMountedRef();
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [previewError, setPreviewError] = useState<boolean>(false);
  const [previewGroups, setPreviewGroups] = useState<string[]>([]);
  const [previewPage, setPreviewPage] = useState<number>(0);
  const [pageLinks, setPageLinks] = useState<string>('');
  const [issueCount, setIssueCount] = useState<number>(0);
  const endDateRef = useRef<string | null>(null);
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
