---
title: Overview of Team Performance Insights
---
Team Insights in the Organization Stats of the Sentry application provides a detailed view of the performance and health of a team's projects. It is a feature that is accessible to the organization and is used to monitor and track the status of different projects associated with a team.

The Team Insights feature is implemented in various components such as 'issues', 'health', and 'controls'. Each of these components provides different insights related to the team's projects. For instance, 'issues' provides insights into the issues faced by the team's projects, 'health' provides insights into the health status of the team's projects, and 'controls' provides the ability to manipulate the view of these insights.

The Team Insights feature uses the 'organization' constant to fetch the organization's data and the 'localStorageKey' constant to store and retrieve the selected team's ID from the local storage. The 'useRouteAnalyticsEventNames' function is used to track the viewing of the Team Insights feature for analytics purposes.

<SwmSnippet path="/static/app/views/organizationStats/teamInsights/index.tsx" line="13">

---

# Team Insights Container

This is the main container for the Team Insights feature. It wraps the children components with the 'Feature' and 'NoProjectMessage' components. The 'Feature' component checks if the 'team-insights' feature is enabled for the organization. The 'NoProjectMessage' component displays a message when there are no projects for the organization.

```tsx
function TeamInsightsContainer({children, organization}: Props) {
  return (
    <Feature organization={organization} features="team-insights">
      <NoProjectMessage organization={organization}>
        {children && isValidElement(children)
          ? cloneElement<any>(children, {
              organization,
            })
          : (children as React.ReactChild)}
      </NoProjectMessage>
    </Feature>
  );
}

export default withOrganization(TeamInsightsContainer);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/organizationStats/teamInsights/issues.tsx" line="30">

---

# Team Insights Issues

This component provides insights into the issues faced by the team's projects. It uses the 'useRouteAnalyticsEventNames' function to track the viewing of the Team Insights feature for analytics purposes. It also uses the 'localStorageKey' constant to retrieve the selected team's ID from the local storage.

```tsx
  const organization = useOrganization();
  const {teams, isLoading, isError} = useUserTeams();

  useRouteAnalyticsEventNames('team_insights.viewed', 'Team Insights: Viewed');

  const query = location?.query ?? {};
  const localStorageKey = `teamInsightsSelectedTeamId:${organization.slug}`;

  let localTeamId: string | null | undefined =
    query.team ?? localStorage.getItem(localStorageKey);
  if (localTeamId && !teams.find(team => team.id === localTeamId)) {
    localTeamId = null;
  }
  const currentTeamId = localTeamId ?? teams[0]?.id;
  const currentTeam = teams.find(team => team.id === currentTeamId) as
    | TeamWithProjects
    | undefined;
  const projects = currentTeam?.projects ?? [];
  const environment = query.environment;

  const {period, start, end, utc} = dataDatetime(query);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/organizationStats/teamInsights/health.tsx" line="30">

---

# Team Insights Health

This component provides insights into the health status of the team's projects. Similar to the 'issues' component, it also uses the 'useRouteAnalyticsEventNames' function and the 'localStorageKey' constant.

```tsx
  const organization = useOrganization();
  const {teams, isLoading, isError} = useUserTeams();

  useRouteAnalyticsEventNames('team_insights.viewed', 'Team Insights: Viewed');

  const query = location?.query ?? {};
  const localStorageKey = `teamInsightsSelectedTeamId:${organization.slug}`;

  let localTeamId: string | null | undefined =
    query.team ?? localStorage.getItem(localStorageKey);
  if (localTeamId && !teams.find(team => team.id === localTeamId)) {
    localTeamId = null;
  }
  const currentTeamId = localTeamId ?? teams[0]?.id;
  const currentTeam = teams.find(team => team.id === currentTeamId) as
    | TeamWithProjects
    | undefined;
  const projects = currentTeam?.projects ?? [];

  const {period, start, end, utc} = dataDatetime(query);

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/organizationStats/teamInsights/controls.tsx" line="64">

---

# Team Insights Controls

This component provides the ability to manipulate the view of the Team Insights. It uses the 'localStorageKey' constant to store the selected team's ID in the local storage when the team is changed.

```tsx
  const theme = useTheme();

  const query = location?.query ?? {};
  const localStorageKey = `teamInsightsSelectedTeamId:${organization.slug}`;

  function handleChangeTeam(teamId: string) {
    localStorage.setItem(localStorageKey, teamId);
    // TODO(workflow): Preserve environment if it exists for the new team
    setStateOnUrl({team: teamId, environment: undefined});
  }
```

---

</SwmSnippet>

# Function Explanations

This section will explain the main functions used in the Team Insights feature of the Sentry application.

<SwmSnippet path="/static/app/views/organizationStats/teamInsights/issues.tsx" line="33">

---

## useRouteAnalyticsEventNames

The `useRouteAnalyticsEventNames` function is used to track the viewing of the Team Insights feature for analytics purposes. It takes two parameters: the event name and the event description.

```tsx
  useRouteAnalyticsEventNames('team_insights.viewed', 'Team Insights: Viewed');

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/organizationStats/teamInsights/issues.tsx" line="30">

---

## useApiQuery

The `useApiQuery` function is used to fetch data from the API. It takes an array as a parameter which includes the endpoint URL and options such as query params. This function is used in various components to fetch the necessary data for the Team Insights feature.

```tsx
  const organization = useOrganization();
  const {teams, isLoading, isError} = useUserTeams();

  useRouteAnalyticsEventNames('team_insights.viewed', 'Team Insights: Viewed');

  const query = location?.query ?? {};
  const localStorageKey = `teamInsightsSelectedTeamId:${organization.slug}`;

  let localTeamId: string | null | undefined =
    query.team ?? localStorage.getItem(localStorageKey);
  if (localTeamId && !teams.find(team => team.id === localTeamId)) {
    localTeamId = null;
  }
  const currentTeamId = localTeamId ?? teams[0]?.id;
  const currentTeam = teams.find(team => team.id === currentTeamId) as
    | TeamWithProjects
    | undefined;
  const projects = currentTeam?.projects ?? [];
  const environment = query.environment;

  const {period, start, end, utc} = dataDatetime(query);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/organizationStats/teamInsights/issues.tsx" line="49">

---

## normalizeDateTimeParams

The `normalizeDateTimeParams` function is used to normalize the DateTime components of the page filters. It takes the query as a parameter and returns an object with the normalized DateTime parameters.

```tsx

  const {period, start, end, utc} = dataDatetime(query);
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
