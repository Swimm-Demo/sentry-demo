---
title: Exploring the Performance Landing View
---
Landing in the Performance section refers to the initial view or starting point for performance data visualization. It's where different types of performance data views are managed and rendered.

The 'Landing' component uses several constants to manage the display of performance data. These constants include 'landingDisplay', 'showOnboarding', 'projects', and 'location'.

'landingDisplay' determines the type of performance data view to be displayed. It's derived from the 'paramLandingDisplay' or defaults to 'defaultLandingDisplayForProjects'.

'showOnboarding' is a boolean that determines whether to display the onboarding view. It's true when the 'onboardingProject' is not undefined.

'projects' and 'location' are used to fetch and display the relevant performance data.

The 'Landing' component also uses styled components like 'SearchContainerWithFilter' and 'SearchContainerWithFilterAndMetrics' to apply specific styles to the performance data view.

<SwmSnippet path="/static/app/views/performance/landing/utils.tsx" line="26">

---

# LandingDisplay Type

The 'LandingDisplay' type is used to define the structure of the landing display object. It includes a 'field' that represents the type of the landing display and a 'label' that represents the display name of the landing display.

```tsx
type LandingDisplay = {
  field: LandingDisplayField;
  label: string;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/landing/utils.tsx" line="38">

---

# LandingDisplay Constants

'LANDING_DISPLAYS' is an array of objects that define the different types of landing displays available. Each object in the array is of type 'LandingDisplay'.

```tsx

// TODO Abdullah Khan: Remove code for Web Vitals tab in performance landing
// page when new starfish web vitals module is mature.
export const LANDING_DISPLAYS = [
  {
    label: t('All Transactions'),
    field: LandingDisplayField.ALL,
  },
  {
    label: t('Frontend'),
    field: LandingDisplayField.FRONTEND_OTHER,
  },
  {
    label: t('Backend'),
    field: LandingDisplayField.BACKEND,
  },
  {
    label: t('Mobile'),
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/landing/utils.tsx" line="79">

---

# LandingDisplay Selection

The 'getLandingDisplayFromParam' and 'getDefaultDisplayForPlatform' functions are used to determine the landing display to be used. The 'getLandingDisplayFromParam' function retrieves the landing display from the location query parameters. The 'getDefaultDisplayForPlatform' function retrieves the default landing display for the given platform.

```tsx
export function getLandingDisplayFromParam(location: Location) {
  const landingField = decodeScalar(location?.query?.landingDisplay);

  const display = LANDING_DISPLAYS.find(({field}) => field === landingField);
  return display;
}

export function getDefaultDisplayForPlatform(projects: Project[], eventView?: EventView) {
  const defaultDisplayField = getDefaultDisplayFieldForPlatform(projects, eventView);

  const defaultDisplay = LANDING_DISPLAYS.find(
    ({field}) => field === defaultDisplayField
  );
  return defaultDisplay || LANDING_DISPLAYS[0];
}

export function getCurrentLandingDisplay(
  location: Location,
  projects: Project[],
  eventView?: EventView
): LandingDisplay {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/landing/index.tsx" line="88">

---

# Landing Component

The 'PerformanceLanding' function is the main component for the landing page. It uses the 'landingDisplay', 'showOnboarding', 'projects', and 'location' constants to manage and display the performance data. It also uses styled components like 'SearchContainerWithFilter' and 'SearchContainerWithFilterAndMetrics' to apply specific styles to the performance data view.

```tsx
  const {teams, initiallyLoaded} = useTeams({provideUserTeams: true});

  const hasMounted = useRef(false);
  const paramLandingDisplay = getLandingDisplayFromParam(location);
  const defaultLandingDisplayForProjects = getDefaultDisplayForPlatform(
    projects,
    eventView
  );
  const landingDisplay = paramLandingDisplay ?? defaultLandingDisplayForProjects;
  const showOnboarding = onboardingProject !== undefined;

  useEffect(() => {
    if (hasMounted.current) {
      browserHistory.replace({
        pathname: location.pathname,
        query: {
          ...location.query,
          landingDisplay: undefined,
        },
      });
    }
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
