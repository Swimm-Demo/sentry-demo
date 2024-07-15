---
title: Exploring the Relocation Feature
---
Relocation in the views directory of the sentry-demo repository refers to a feature that allows users to move their data from one location to another. This is implemented in the `relocation.tsx` file, which contains various styled components and constants that define the behavior and appearance of the relocation feature.

The `relocation.tsx` file contains several constants such as `headerView`, `backButtonView`, `contentView`, and `errView`. These constants are used to define different views or parts of the relocation feature. For example, `headerView` defines the header part of the relocation page, `backButtonView` defines the back button, `contentView` defines the main content of the page, and `errView` is used to display an error message if there's an issue with the relocation process.

The `relocation.tsx` file also contains styled components that define the appearance of the relocation feature. These components use styled-components, a library that allows you to write CSS in your JavaScript, to define the styles. For example, `Container` is a styled component that defines a flex container with specific padding, background color, and other styles.

The `relocation` directory also contains a `components` subdirectory, which contains additional components used in the relocation feature. These components are used to break down the relocation feature into smaller, more manageable parts.

The `relocation` directory also contains other files such as `uploadBackup.tsx`, `encryptBackup.tsx`, `getStarted.tsx`, `publicKey.tsx`, and `inProgress.tsx`. These files define different steps or parts of the relocation process. For example, `uploadBackup.tsx` defines the step where users upload their backup, and `encryptBackup.tsx` defines the step where the backup is encrypted.

<SwmSnippet path="/static/app/views/relocation/relocation.tsx" line="345">

---

# Relocation Components

The `relocation.tsx` file contains several styled components that define the appearance of the relocation feature. These components use styled-components, a library that allows you to write CSS in your JavaScript, to define the styles. For example, `Container` is a styled component that defines a flex container with specific padding, background color, and other styles.

```tsx
const Container = styled('div')`
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  background: #faf9fb;
  padding: 120px ${space(3)};
  width: 100%;
  margin: 0 auto;

  p,
  a {
    line-height: 1.6;
  }
`;

const Header = styled('header')`
  background: ${p => p.theme.background};
  padding-left: ${space(4)};
  padding-right: ${space(4)};
  position: sticky;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/relocation/relocation.tsx" line="39">

---

# Relocation Steps

The `getRelocationOnboardingSteps` function defines the different steps of the relocation process. Each step is represented by an object with properties such as `id`, `title`, `Component`, and `cornerVariant`. The `Component` property refers to the component that is displayed for that step.

```tsx
function getRelocationOnboardingSteps(): StepDescriptor[] {
  return [
    {
      id: 'get-started',
      title: t('Get Started'),
      Component: GetStarted,
      cornerVariant: 'top-left',
    },
    {
      id: 'public-key',
      title: t("Save Sentry's public key to your machine"),
      Component: PublicKey,
      cornerVariant: 'top-left',
    },
    {
      id: 'encrypt-backup',
      title: t('Encrypt backup'),
      Component: EncryptBackup,
      cornerVariant: 'top-left',
    },
    {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/relocation/relocation.tsx" line="104">

---

# Fetching Existing Relocation

The `fetchExistingRelocation` function is used to fetch the existing relocation data from the server. It sets the `existingRelocationState` to `LoadingState.FETCHING` and then makes a GET request to the `/relocations/` endpoint for each region. The responses are then flattened and sorted by the `dateAdded` property. The UUID of the relocation with the status `IN_PROGRESS` or `PAUSE` is then stored in `existingRelocationUUID`.

```tsx
  const fetchExistingRelocation = useCallback(() => {
    setExistingRelocationState(LoadingState.FETCHING);
    return Promise.all(
      regions.map(region =>
        api.requestPromise(`/relocations/`, {
          method: 'GET',
          host: region.url,
        })
      )
    )
      .then(responses => {
        const response = responses.flat(1);
        response.sort((a, b) => {
          return (
            new Date(a.dateAdded || 0).getTime() - new Date(b.dateAdded || 0).getTime()
          );
        });
        const existingRelocationUUID =
          response.find(
```

---

</SwmSnippet>

# Relocation Functions

This section will explain the main functions involved in the relocation feature of the Sentry application.

<SwmSnippet path="/static/app/views/relocation/relocation.tsx" line="39">

---

## getRelocationOnboardingSteps

The `getRelocationOnboardingSteps` function defines the steps involved in the relocation process. Each step is represented as an object with an id, title, and a Component that renders the step. The steps include 'get-started', 'public-key', 'encrypt-backup', 'upload-backup', and 'in-progress'.

```tsx
function getRelocationOnboardingSteps(): StepDescriptor[] {
  return [
    {
      id: 'get-started',
      title: t('Get Started'),
      Component: GetStarted,
      cornerVariant: 'top-left',
    },
    {
      id: 'public-key',
      title: t("Save Sentry's public key to your machine"),
      Component: PublicKey,
      cornerVariant: 'top-left',
    },
    {
      id: 'encrypt-backup',
      title: t('Encrypt backup'),
      Component: EncryptBackup,
      cornerVariant: 'top-left',
    },
    {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/relocation/relocation.tsx" line="80">

---

## RelocationOnboarding

The `RelocationOnboarding` function is a React component that orchestrates the relocation process. It uses the `getRelocationOnboardingSteps` function to get the steps of the process, and maintains the state of the process, including the current step, the existing relocation state, and the public keys. It also defines functions to fetch existing relocations and public keys, and to navigate to different steps.

```tsx
function RelocationOnboarding(props: Props) {
  const {
    params: {step: stepId},
  } = props;
  const onboardingSteps = getRelocationOnboardingSteps();
  const stepObj = onboardingSteps.find(({id}) => stepId === id);
  const stepIndex = onboardingSteps.findIndex(({id}) => stepId === id);
  const api = useApi();
  const regions = ConfigStore.get('regions');
  const [existingRelocationState, setExistingRelocationState] = useState(
    LoadingState.FETCHING
  );
  const [existingRelocation, setExistingRelocation] = useState('');
  const [publicKeys, setPublicKeys] = useState(new Map<string, string>());
  const [publicKeysState, setPublicKeysState] = useState(LoadingState.FETCHING);
  const [relocationState, setRelocationState] = useSessionStorage<RelocationState>(
    'relocationOnboarding',
    {
      orgSlugs: '',
      regionUrl: '',
      promoCode: '',
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
