---
title: Basic Concepts of Project Setup Process
---
Project installation in the Sentry Demo repository refers to the process of setting up a new project within the Sentry platform. This process is handled within the 'projectInstall' directory, which contains various components and views that guide the user through the project creation process. The 'createProject.tsx' file, for instance, contains the logic for creating a new project, including setting the project name, selecting the platform, and setting up alert rules. The 'platform.tsx' file, on the other hand, handles the selection of the platform for the project, providing a list of all available platforms and setting up the selected platform for the project. The 'newProject.tsx' file is the entry point for the project creation process, rendering the 'CreateProject' component.

<SwmSnippet path="/static/app/views/projectInstall/createProject.tsx" line="1">

---

# Project Creation

This file contains the logic for creating a new project, including setting the project name, selecting the platform, and setting up alert rules.

```tsx
import {useCallback, useContext, useMemo, useState} from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import omit from 'lodash/omit';
import startCase from 'lodash/startCase';
import {PlatformIcon} from 'platformicons';

import {addErrorMessage, addSuccessMessage} from 'sentry/actionCreators/indicator';
import {openModal} from 'sentry/actionCreators/modal';
import Access from 'sentry/components/acl/access';
import {Alert} from 'sentry/components/alert';
import {Button} from 'sentry/components/button';
import Input from 'sentry/components/input';
import * as Layout from 'sentry/components/layouts/thirds';
import ExternalLink from 'sentry/components/links/externalLink';
import List from 'sentry/components/list';
import ListItem from 'sentry/components/list/listItem';
import {SupportedLanguages} from 'sentry/components/onboarding/frameworkSuggestionModal';
import type {Platform} from 'sentry/components/platformPicker';
import PlatformPicker from 'sentry/components/platformPicker';
import {useProjectCreationAccess} from 'sentry/components/projects/useProjectCreationAccess';
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/projectInstall/platform.tsx" line="1">

---

# Platform Selection

This file handles the selection of the platform for the project. It provides a list of all available platforms and sets up the selected platform for the project.

```tsx
import {Fragment, useCallback, useContext, useEffect, useMemo, useState} from 'react';
import type {RouteComponentProps} from 'react-router';
import styled from '@emotion/styled';
import omit from 'lodash/omit';

import Feature from 'sentry/components/acl/feature';
import {Alert} from 'sentry/components/alert';
import {Button} from 'sentry/components/button';
import ButtonBar from 'sentry/components/buttonBar';
import NotFound from 'sentry/components/errors/notFound';
import HookOrDefault from 'sentry/components/hookOrDefault';
import {SdkDocumentation} from 'sentry/components/onboarding/gettingStartedDoc/sdkDocumentation';
import type {ProductSolution} from 'sentry/components/onboarding/productSelection';
import {platformProductAvailability} from 'sentry/components/onboarding/productSelection';
import {
  performance as performancePlatforms,
  replayPlatforms,
} from 'sentry/data/platformCategories';
import type {Platform} from 'sentry/data/platformPickerCategories';
import platforms from 'sentry/data/platforms';
import {t} from 'sentry/locale';
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/projectInstall/newProject.tsx" line="1">

---

# Project Installation Entry Point

This file is the entry point for the project creation process. It renders the 'CreateProject' component, which kicks off the project creation process.

```tsx
import styled from '@emotion/styled';

import SentryDocumentTitle from 'sentry/components/sentryDocumentTitle';
import {space} from 'sentry/styles/space';

import {CreateProject} from './createProject';

function NewProject() {
  return (
    <SentryDocumentTitle>
      <Container>
        <div className="container">
          <Content>
            <CreateProject />
          </Content>
        </div>
      </Container>
    </SentryDocumentTitle>
  );
}

```

---

</SwmSnippet>

# Project Installation Functions

This section will explain the main functions involved in the project installation process in the Sentry Demo repository.

<SwmSnippet path="/static/app/views/projectInstall/createProject.tsx" line="47">

---

## CreateProject Function

The CreateProject function is responsible for creating a new project. It uses the useApi, useOrganization, useLocation, and useTeams hooks to get necessary data and context. It also sets up local state for the project name, platform, and team using the useState hook. The function also handles the submission of the project creation form, making a POST request to the appropriate endpoint to create the new project.

```tsx
function CreateProject() {
  const api = useApi();
  const organization = useOrganization();
  const location = useLocation();
  const gettingStartedWithProjectContext = useContext(GettingStartedWithProjectContext);
  const {teams} = useTeams();

  const autoFill =
    location.query.referrer === 'getting-started' &&
    location.query.project === gettingStartedWithProjectContext.project?.id;

  const accessTeams = teams.filter((team: Team) => team.access.includes('team:admin'));

  useRouteAnalyticsEventNames(
    'project_creation_page.viewed',
    'Project Create: Creation page viewed'
  );

  const [projectName, setProjectName] = useState(
    autoFill ? gettingStartedWithProjectContext.project?.name : ''
  );
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/projectInstall/platform.tsx" line="54">

---

## ProjectInstallPlatform Function

The ProjectInstallPlatform function is responsible for handling the selection of the platform for the project. It uses the useOrganization and useProjects hooks to get necessary data. It also sets up local state for the current platform, showLoaderOnboarding, and products using the useState hook. The function also makes use of the useApiQuery hook to fetch project alert rules.

```tsx
export function ProjectInstallPlatform({location, params}: Props) {
  const organization = useOrganization();
  const gettingStartedWithProjectContext = useContext(GettingStartedWithProjectContext);

  const isSelfHosted = ConfigStore.get('isSelfHosted');
  const isSelfHostedErrorsOnly = ConfigStore.get('isSelfHostedErrorsOnly');

  const {projects, initiallyLoaded} = useProjects({
    slugs: [params.projectId],
    orgId: organization.slug,
  });

  const loadingProjects = !initiallyLoaded;
  const project = !loadingProjects
    ? projects.find(proj => proj.slug === params.projectId)
    : undefined;

  const currentPlatformKey = project?.platform ?? 'other';
  const currentPlatform = allPlatforms.find(p => p.id === currentPlatformKey);

  const [showLoaderOnboarding, setShowLoaderOnboarding] = useState(
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
