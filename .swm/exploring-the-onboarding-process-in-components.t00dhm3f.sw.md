---
title: Exploring the Onboarding Process in Components
---
Onboarding in the components directory of the sentry-demo repository refers to the process of setting up and configuring the Sentry platform for a new user or project. This process is facilitated through a series of steps and instructions that guide the user through the installation, configuration, and verification of the Sentry SDK in their project.

The onboarding process begins with the `OnboardingLayout` function in the `onboardingLayout.tsx` file. This function sets up the layout for the onboarding process, including the introduction, steps, and next steps. It uses various hooks and functions to fetch necessary data such as the organization details, platform options, and source package registries.

The `OnboardingLayout` function also uses the `useCurrentProjectState` function from the `useCurrentProjectState.tsx` file to manage the state of the current project during the onboarding process. This function fetches the current project details and updates the state based on the user's actions.

The `OnboardingLayout` function then renders the onboarding steps using the `Step` component. Each step is defined in the `Docs` type in the `types.ts` file and includes instructions for installing, configuring, and verifying the Sentry SDK.

The onboarding process also includes the selection of platform options, which are fetched from the URL using the `useUrlPlatformOptions` function from the `platformOptionsControl.tsx` file. These options are then passed to the `PlatformOptionsControl` component for display.

Finally, the `OnboardingLayout` function renders the next steps after the onboarding process, which are also defined in the `Docs` type. These steps provide the user with further actions to take after completing the onboarding process.

<SwmSnippet path="/static/app/components/onboarding/gettingStartedDoc/onboardingLayout.tsx" line="48">

---

# Onboarding Layout

The `OnboardingLayout` function sets up the layout for the onboarding process, including the introduction, steps, and next steps. It uses various hooks and functions to fetch necessary data such as the organization details, platform options, and source package registries.

```tsx
export function OnboardingLayout({
  cdn,
  docsConfig,
  dsn,
  platformKey,
  projectId,
  projectSlug,
  activeProductSelection = EMPTY_ARRAY,
  newOrg,
  configType = 'onboarding',
}: OnboardingLayoutProps) {
  const organization = useOrganization();
  const {isLoading: isLoadingRegistry, data: registryData} =
    useSourcePackageRegistries(organization);
  const selectedOptions = useUrlPlatformOptions(docsConfig.platformOptions);
  const {platformOptions} = docsConfig;

  const {introduction, steps, nextSteps} = useMemo(() => {
    const doc = docsConfig[configType] ?? docsConfig.onboarding;

    const docParams: DocsParams<any> = {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/onboarding/gettingStartedDoc/utils/useCurrentProjectState.tsx" line="18">

---

# Current Project State

The `useCurrentProjectState` function is used within the `OnboardingLayout` function to manage the state of the current project during the onboarding process. This function fetches the current project details and updates the state based on the user's actions.

```tsx
function useCurrentProjectState({
  currentPanel,
  targetPanel,
  onboardingPlatforms,
  allPlatforms,
}: Props) {
  const params = useParams<{projectId?: string}>();
  const projectSlug = params.projectId;
  const {projects, initiallyLoaded: projectsLoaded} = useProjects();
  const {selection, isReady} = useLegacyStore(PageFiltersStore);
  const [currentProject, setCurrentProject] = useState<Project | undefined>(undefined);

  const isActive = currentPanel === targetPanel;

  // Projects with onboarding instructions
  const projectsWithOnboarding = projects.filter(
    p => p.platform && onboardingPlatforms.includes(p.platform)
  );

  const [supportedProjects, unsupportedProjects] = useMemo(() => {
    return partition(projects, p => p.platform && allPlatforms.includes(p.platform));
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/onboarding/gettingStartedDoc/types.ts" line="82">

---

# Onboarding Steps

The `Docs` type in the `types.ts` file defines the steps for the onboarding process. Each step includes instructions for installing, configuring, and verifying the Sentry SDK.

```typescript
export interface Docs<PlatformOptions extends BasePlatformOptions = BasePlatformOptions> {
  onboarding: OnboardingConfig<PlatformOptions>;
  crashReportOnboarding?: OnboardingConfig<PlatformOptions>;
  customMetricsOnboarding?: OnboardingConfig<PlatformOptions>;
  feedbackOnboardingCrashApi?: OnboardingConfig<PlatformOptions>;
  feedbackOnboardingNpm?: OnboardingConfig<PlatformOptions>;
  platformOptions?: PlatformOptions;
  replayOnboardingJsLoader?: OnboardingConfig<PlatformOptions>;
  replayOnboardingNpm?: OnboardingConfig<PlatformOptions>;
}

export type ConfigType =
  | 'onboarding'
  | 'feedbackOnboardingNpm'
  | 'feedbackOnboardingCrashApi'
  | 'crashReportOnboarding'
  | 'replayOnboardingNpm'
  | 'replayOnboardingJsLoader'
  | 'customMetricsOnboarding';
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/onboarding/gettingStartedDoc/onboardingLayout.tsx" line="62">

---

# Platform Options

The `OnboardingLayout` function fetches platform options from the URL using the `useUrlPlatformOptions` function. These options are then passed to the `PlatformOptionsControl` component for display.

```tsx
  const selectedOptions = useUrlPlatformOptions(docsConfig.platformOptions);
  const {platformOptions} = docsConfig;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/onboarding/gettingStartedDoc/utils/feedbackOnboarding.tsx" line="78">

---

# Next Steps

The `OnboardingLayout` function also renders the next steps after the onboarding process, which are defined in the `Docs` type. These steps provide the user with further actions to take after completing the onboarding process.

```tsx
  verify: () => [],
  nextSteps: () => [],
};
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
