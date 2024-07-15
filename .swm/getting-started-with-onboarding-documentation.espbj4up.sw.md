---
title: Getting started with Onboarding Documentation
---
The 'Getting started doc' in the Onboarding section of the Sentry-demo repository refers to the documentation and code snippets provided to guide new users in setting up and configuring Sentry for their specific platform. This documentation is dynamically loaded based on the user's selected platform and project settings.

<SwmSnippet path="/static/app/components/onboarding/gettingStartedDoc/utils/useLoadGettingStarted.tsx" line="24">

---

The 'useLoadGettingStarted' function is responsible for loading the appropriate getting started documentation based on the user's selected platform and project settings.

```tsx
  projSlug,
}: Props): {
  cdn: string | undefined;
  docs: Docs<any> | null;
  dsn: string | undefined;
  isError: boolean;
  isLoading: boolean;
  refetch: () => void;
} {
  const [module, setModule] = useState<undefined | 'none' | {default: Docs<any>}>(
    undefined
  );

  const projectKeys = useProjectKeys({orgSlug, projSlug});

  const platformPath = getPlatformPath(platform);

  useEffect(() => {
    async function getGettingStartedDoc() {
      if (
        (productType === 'replay' && !replayPlatforms.includes(platform.id)) ||
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/onboarding/gettingStartedDoc/step.tsx" line="11">

---

The 'Step' component represents a single step in the getting started guide. Each step has a type, which can be 'install', 'configure', or 'verify', and a corresponding title.

```tsx
export enum StepType {
  INSTALL = 'install',
  CONFIGURE = 'configure',
  VERIFY = 'verify',
}

export const StepTitle = {
  [StepType.INSTALL]: t('Install'),
  [StepType.CONFIGURE]: t('Configure SDK'),
  [StepType.VERIFY]: t('Verify'),
};
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/onboarding/gettingStartedDoc/onboardingLayout.tsx" line="48">

---

The 'OnboardingLayout' component is responsible for rendering the entire getting started guide. It uses the 'docsConfig' prop to determine which steps to display and in what order.

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

<SwmSnippet path="/static/app/components/onboarding/gettingStartedDoc/utils/useLoadGettingStarted.tsx" line="42">

---

# Loading the Getting Started Doc

The `getGettingStartedDoc` function is responsible for loading the appropriate getting started documentation based on the user's platform and product type. If the platform does not support the selected product type, the function sets the module to 'none'. Otherwise, it attempts to import the relevant documentation from the `sentry/gettingStartedDocs` directory.

```tsx
    async function getGettingStartedDoc() {
      if (
        (productType === 'replay' && !replayPlatforms.includes(platform.id)) ||
        (productType === 'feedback' && !feedbackOnboardingPlatforms.includes(platform.id))
      ) {
        setModule('none');
        return;
      }

      try {
        const mod = await import(
          /* webpackExclude: /.spec/ */
          `sentry/gettingStartedDocs/${platformPath}`
        );
        setModule(mod);
      } catch (err) {
        setModule(undefined);
        Sentry.captureException(err);
      }
    }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/onboarding/gettingStartedDoc/step.tsx" line="196">

---

# Displaying the Getting Started Doc

The `Step` component is responsible for displaying the loaded getting started documentation. It takes in various props such as title, type, configurations, additional info, description, and whether the step is optional. Based on these props, it renders the appropriate UI elements.

```tsx
export function Step({
  title,
  type,
  configurations,
  additionalInfo,
  description,
  isOptional = false,
  codeHeader,
}: StepProps) {
  const [showOptionalConfig, setShowOptionalConfig] = useState(false);

  const config = (
    <Fragment>
      {description && <Description>{description}</Description>}

      {!!configurations?.length && (
        <Configurations>
          {configurations.map((configuration, index) => {
            if (configuration.configurations) {
              return (
                <Fragment key={index}>
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/onboarding/gettingStartedDoc/utils/useLoadGettingStarted.tsx" line="57">

---

# Error Handling

In case of an error while loading the getting started documentation, the `getGettingStartedDoc` function sets the module to undefined and captures the exception using Sentry's `captureException` function.

```tsx
      } catch (err) {
        setModule(undefined);
        Sentry.captureException(err);
      }
```

---

</SwmSnippet>

# Getting Started Doc Functions

Let's take a closer look at the main functions involved in loading and displaying the 'Getting started doc'.

<SwmSnippet path="/static/app/components/onboarding/gettingStartedDoc/utils/useLoadGettingStarted.tsx" line="20">

---

## useLoadGettingStarted

The `useLoadGettingStarted` function is a custom React hook that loads the getting started documentation for a specific platform. It takes an object of properties including the platform, product type, organization slug, and project slug. It returns an object containing the documentation, DSN, CDN, loading state, error state, and a refetch function.

```tsx
export function useLoadGettingStarted({
  platform,
  productType,
  orgSlug,
  projSlug,
}: Props): {
  cdn: string | undefined;
  docs: Docs<any> | null;
  dsn: string | undefined;
  isError: boolean;
  isLoading: boolean;
  refetch: () => void;
} {
  const [module, setModule] = useState<undefined | 'none' | {default: Docs<any>}>(
    undefined
  );

  const projectKeys = useProjectKeys({orgSlug, projSlug});

  const platformPath = getPlatformPath(platform);

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/onboarding/gettingStartedDoc/utils/useLoadGettingStarted.tsx" line="42">

---

## getGettingStartedDoc

The `getGettingStartedDoc` function is an asynchronous function that is used within the `useLoadGettingStarted` hook. It checks if the selected platform supports the selected product type and then attempts to import the corresponding getting started documentation. If the import is successful, it sets the module state to the imported module. If an error occurs during the import, it captures the exception using Sentry's `captureException` function.

```tsx
    async function getGettingStartedDoc() {
      if (
        (productType === 'replay' && !replayPlatforms.includes(platform.id)) ||
        (productType === 'feedback' && !feedbackOnboardingPlatforms.includes(platform.id))
      ) {
        setModule('none');
        return;
      }

      try {
        const mod = await import(
          /* webpackExclude: /.spec/ */
          `sentry/gettingStartedDocs/${platformPath}`
        );
        setModule(mod);
      } catch (err) {
        setModule(undefined);
        Sentry.captureException(err);
      }
    }
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
