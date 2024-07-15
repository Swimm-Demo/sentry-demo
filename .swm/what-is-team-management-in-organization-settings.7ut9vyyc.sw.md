---
title: What is Team Management in Organization Settings
---
Organization teams in Sentry are groups of users within an organization. They are used to manage access to projects and issues within the organization. Each team can have different members and different access rights, which are managed through the 'access' and 'features' properties. The 'access' property is a set of strings representing the access rights of the team, and the 'features' property is a set of strings representing the features available to the team.

The OrganizationTeams function in the 'organizationTeams.tsx' file is the main component for managing teams in an organization. It uses the 'useTeams' hook to fetch the teams from the TeamStore and provides functionality for searching teams, loading more teams, and checking if there are more teams to load. It also checks if the current user has the 'project:admin' access right, which determines if they can create new teams.

The 'teamQuery' state is used to filter the teams based on the user's search input. The 'debouncedSearch' function is used to delay the search action until the user has stopped typing for a certain amount of time, to reduce the number of API calls.

The 'action' constant is a Button component that allows the user to create a new team. It is disabled and shows a tooltip if the user does not have the 'project:admin' access right. When clicked, it opens the 'Create Team' modal.

The 'OrganizationTeamsContainer' function in the 'index.tsx' file is the main entry point for the organization teams settings page. It fetches the access requests for the organization and passes them to the 'OrganizationTeams' component. It also provides a 'handleRemoveAccessRequest' function that removes an access request and updates the teams in the TeamStore.

The 'teamSettings' directory contains the 'TeamSettings' component, which is used to manage the settings of a specific team. It uses the 'useOrganization' hook to fetch the current organization and provides functionality for submitting changes to the team settings and removing the team.

<SwmSnippet path="/static/app/views/settings/organizationTeams/organizationTeams.tsx" line="37">

---

# OrganizationTeams Function

The OrganizationTeams function is the main component for managing teams in an organization. It uses the 'useTeams' hook to fetch the teams from the TeamStore and provides functionality for searching teams, loading more teams, and checking if there are more teams to load. It also checks if the current user has the 'project:admin' access right, which determines if they can create new teams.

```tsx
function OrganizationTeams({
  organization,
  access,
  features,
  requestList,
  onRemoveAccessRequest,
}: Props) {
  const [teamQuery, setTeamQuery] = useState('');
  const {initiallyLoaded} = useTeams({provideUserTeams: true});
  const {teams, onSearch, loadMore, hasMore, fetching} = useTeams();

  if (!organization) {
    return null;
  }
  const canCreateTeams = access.has('project:admin');

  const action = (
    <Button
      priority="primary"
      size="sm"
      disabled={!canCreateTeams}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationTeams/organizationTeams.tsx" line="44">

---

# Team Query

The 'teamQuery' state is used to filter the teams based on the user's search input. The 'debouncedSearch' function is used to delay the search action until the user has stopped typing for a certain amount of time, to reduce the number of API calls.

```tsx
  const [teamQuery, setTeamQuery] = useState('');
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationTeams/organizationTeams.tsx" line="53">

---

# Create Team Button

The 'action' constant is a Button component that allows the user to create a new team. It is disabled and shows a tooltip if the user does not have the 'project:admin' access right. When clicked, it opens the 'Create Team' modal.

```tsx
  const action = (
    <Button
      priority="primary"
      size="sm"
      disabled={!canCreateTeams}
      title={
        !canCreateTeams ? t('You do not have permission to create teams') : undefined
      }
      onClick={() =>
        openCreateTeamModal({
          organization,
        })
      }
      icon={<IconAdd isCircled />}
    >
      {t('Create Team')}
    </Button>
  );
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationTeams/index.tsx" line="1">

---

# OrganizationTeamsContainer Function

The 'OrganizationTeamsContainer' function in the 'index.tsx' file is the main entry point for the organization teams settings page. It fetches the access requests for the organization and passes them to the 'OrganizationTeams' component. It also provides a 'handleRemoveAccessRequest' function that removes an access request and updates the teams in the TeamStore.

```tsx
import {useCallback, useEffect, useMemo} from 'react';
import type {RouteComponentProps} from 'react-router';

import {loadStats} from 'sentry/actionCreators/projects';
import LoadingError from 'sentry/components/loadingError';
import LoadingIndicator from 'sentry/components/loadingIndicator';
import {t} from 'sentry/locale';
import TeamStore from 'sentry/stores/teamStore';
import type {AccessRequest} from 'sentry/types/organization';
import {
  type ApiQueryKey,
  setApiQueryData,
  useApiQuery,
  useQueryClient,
} from 'sentry/utils/queryClient';
import useApi from 'sentry/utils/useApi';
import useOrganization from 'sentry/utils/useOrganization';

import OrganizationTeams from './organizationTeams';

export function OrganizationTeamsContainer(props: RouteComponentProps<{}, {}>) {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationTeams/teamSettings/index.tsx" line="1">

---

# TeamSettings Component

The 'teamSettings' directory contains the 'TeamSettings' component, which is used to manage the settings of a specific team. It uses the 'useOrganization' hook to fetch the current organization and provides functionality for submitting changes to the team settings and removing the team.

```tsx
import {Fragment, useMemo} from 'react';
import type {RouteComponentProps} from 'react-router';
import cloneDeep from 'lodash/cloneDeep';

import {addErrorMessage, addSuccessMessage} from 'sentry/actionCreators/indicator';
import {removeTeam, updateTeamSuccess} from 'sentry/actionCreators/teams';
import {hasEveryAccess} from 'sentry/components/acl/access';
import {Button} from 'sentry/components/button';
import Confirm from 'sentry/components/confirm';
import FieldGroup from 'sentry/components/forms/fieldGroup';
import type {FormProps} from 'sentry/components/forms/form';
import Form from 'sentry/components/forms/form';
import JsonForm from 'sentry/components/forms/jsonForm';
import type {FieldObject} from 'sentry/components/forms/types';
import Panel from 'sentry/components/panels/panel';
import PanelHeader from 'sentry/components/panels/panelHeader';
import SentryDocumentTitle from 'sentry/components/sentryDocumentTitle';
import teamSettingsFields from 'sentry/data/forms/teamSettingsFields';
import {IconDelete} from 'sentry/icons';
import {t, tct} from 'sentry/locale';
import type {Team} from 'sentry/types/organization';
```

---

</SwmSnippet>

# Organization Teams Functions

This section will explain the main functions related to Organization Teams in Sentry.

<SwmSnippet path="/static/app/views/settings/organizationTeams/organizationTeams.tsx" line="37">

---

## OrganizationTeams

The 'OrganizationTeams' function is the main component for managing teams in an organization. It uses the 'useTeams' hook to fetch the teams from the TeamStore and provides functionality for searching teams, loading more teams, and checking if there are more teams to load. It also checks if the current user has the 'project:admin' access right, which determines if they can create new teams.

```tsx
function OrganizationTeams({
  organization,
  access,
  features,
  requestList,
  onRemoveAccessRequest,
}: Props) {
  const [teamQuery, setTeamQuery] = useState('');
  const {initiallyLoaded} = useTeams({provideUserTeams: true});
  const {teams, onSearch, loadMore, hasMore, fetching} = useTeams();

  if (!organization) {
    return null;
  }
  const canCreateTeams = access.has('project:admin');

  const action = (
    <Button
      priority="primary"
      size="sm"
      disabled={!canCreateTeams}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationTeams/index.tsx" line="52">

---

## handleRemoveAccessRequest

The 'handleRemoveAccessRequest' function is used to remove an access request and update the teams in the TeamStore. It is passed as a prop to the 'OrganizationTeams' component.

```tsx
    });
  }, [organization?.slug, api]);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationTeams/teamMembersRow.tsx" line="24">

---

## TeamMembersRow

The 'TeamMembersRow' function is a component that represents a row in the team members list. It receives the team member data as props and provides functionality for removing the member from the team and updating the member's role.

```tsx
function TeamMembersRow({
  organization,
  team,
  member,
  user,
  hasWriteAccess,
  removeMember,
  updateMemberRole,
}: Props) {
  const isSelf = user.email === member.email;

  return (
    <TeamRolesPanelItem key={member.id}>
      <div>
        <IdBadge avatarSize={36} member={member} />
      </div>
      <RoleSelectWrapper>
        <TeamRoleSelect
          disabled={isSelf || !hasWriteAccess}
          organization={organization}
          team={team}
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
