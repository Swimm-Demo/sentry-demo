---
title: Introduction to Project Ownership Management
---
Project ownership in Sentry is a mechanism that allows you to control who is responsible for specific parts of your application. It is implemented through the use of ownership rules, which are defined in the 'ProjectOwnership' component. These rules can be set to associate certain files or paths in your codebase with specific teams or users, who will then be notified when errors occur in those areas.

The 'SelectOwners' component is used to manage the assignment of owners to a project. It provides an interface for selecting owners from a list of available teams and users. The 'getTeamsNotInProject' function is used to filter out teams that are already assigned to the project.

The 'OwnerInput' component is used to input ownership rules. These rules are then saved using the 'handleOwnershipSave' function in the 'ProjectOwnership' component.

The 'CodeOwnerFileTable' component displays a list of codeowner files being used for the project. Codeowners are another way of defining ownership in a project, typically through a CODEOWNERS file in your repository.

<SwmSnippet path="/static/app/views/settings/project/projectOwnership/index.tsx" line="79">

---

# ProjectOwnership Component

The 'handleOwnershipSave' function is used to save the ownership rules. It takes an 'IssueOwnership' object as a parameter, which represents the ownership rules, and updates the state of the 'ProjectOwnership' component with these rules.

```tsx
  handleOwnershipSave = (ownership: IssueOwnership) => {
    this.setState(prevState => ({
      ...prevState,
      ownership,
    }));
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/project/projectOwnership/selectOwners.tsx" line="201">

---

# SelectOwners Component

The 'handleAddTeamToProject' function is used to add a team to a project. It takes a 'team' object as a parameter, which represents the team to be added. The function makes an API call to add the team to the project and updates the state of the 'SelectOwners' component accordingly.

```tsx
  async handleAddTeamToProject(team) {
    const {api, organization, project, value} = this.props;
    // Copy old value
    const oldValue = [...value];

    // Optimistic update
    this.props.onChange([...this.props.value, this.createMentionableTeam(team)]);

    try {
      // Try to add team to project
      // Note: we can't close select menu here because we have to wait for ProjectsStore to update first
      // The reason for this is because we have little control over `react-select`'s `AsyncSelect`
      // We can't control when `handleLoadOptions` gets called, but it gets called when select closes, so
      // wait for store to update before closing the menu. Otherwise, we'll have stale items in the select menu
      await addTeamToProject(api, organization.slug, project.slug, team);
    } catch (err) {
      // Unable to add team to project, revert select menu value
      this.props.onChange(oldValue);
      this.closeSelectMenu();
    }
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/project/projectOwnership/ownerInput.tsx" line="35">

---

# OwnerInput Component

The 'OwnerInput' component is used to input ownership rules. It has a 'project' prop, which represents the project for which the ownership rules are being defined, and an 'onSave' prop, which is a function that is called when the ownership rules are saved.

```tsx
  project: Project;
  onSave?: (ownership: IssueOwnership) => void;
} & typeof defaultProps;

type State = {
  error: null | {
    raw: string[];
  };
  hasChanges: boolean;
  text: string | null;
};

class OwnerInput extends Component<Props, State> {
  static defaultProps = defaultProps;

  state: State = {
    hasChanges: false,
    text: null,
    error: null,
  };
```

---

</SwmSnippet>

# Project Ownership Functions

This section will explain the main functions related to project ownership in Sentry.

<SwmSnippet path="/static/app/views/settings/project/projectOwnership/selectOwners.tsx" line="173">

---

## getTeamsNotInProject

The 'getTeamsNotInProject' function is used to filter out teams that are already assigned to the project. It retrieves all teams from the TeamStore and excludes those that are already in the project. The result is a list of teams that are not yet assigned to the project.

```tsx
  getTeamsNotInProject(teamsInProject: Owner[] = []) {
    const teams = TeamStore.getAll() || [];
    const excludedTeamIds = teamsInProject.map(({actor}) => actor.id);

    return teams
      .filter(team => !excludedTeamIds.includes(team.id))
      .map(this.createUnmentionableTeam);
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/project/projectOwnership/index.tsx" line="79">

---

## handleOwnershipSave

The 'handleOwnershipSave' function is used to save the ownership rules. When a user saves the ownership rules, this function is called. It updates the state of the 'ProjectOwnership' component with the new ownership rules.

```tsx
  handleOwnershipSave = (ownership: IssueOwnership) => {
    this.setState(prevState => ({
      ...prevState,
      ownership,
    }));
    closeModal();
  };
```

---

</SwmSnippet>

# Project Ownership Endpoints

Project Ownership Endpoints

<SwmSnippet path="/static/app/views/settings/project/projectOwnership/ownerInput.tsx" line="78">

---

## Project Ownership Endpoint

This endpoint is used to update the ownership rules for a project. The PUT method is used to update the data, which includes the raw text of the ownership rules.

```tsx
      {
        method: 'PUT',
        data: {raw: text || ''},
      }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/project/projectOwnership/addCodeOwnerModal.tsx" line="84">

---

## Codeowners Endpoint

This endpoint is used to fetch a codeowners file for a specific code mapping. The GET method is used to retrieve the data, which includes the raw text of the codeowners file.

```tsx
      const data: CodeownersFile = await this.api.requestPromise(
        `/organizations/${organization.slug}/code-mappings/${codeMappingId}/codeowners/`,
        {
          method: 'GET',
        }
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
