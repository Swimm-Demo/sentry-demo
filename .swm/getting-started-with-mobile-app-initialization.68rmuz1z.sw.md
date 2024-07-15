---
title: Getting Started with Mobile App Initialization
---
App starts in the mobile context of the Sentry demo refers to the initialization and startup process of a mobile application. This process involves setting up necessary configurations, preparing the application's state, and navigating to the initial screen. The process is handled by various components and functions within the 'appStarts' directory.

The 'AppStartup' function in 'appStartup.tsx' plays a crucial role in this process. It sets up various constants and variables such as 'appStartType', 'version', 'primaryRelease', and 'router' which are used throughout the application's startup process.

The 'appStartType' constant, for example, is used to determine the type of app start (cold or warm) and is used in various other components and functions. Similarly, 'version' is used to specify the version of the dataset being used, and 'primaryRelease' is used to handle release selections.

The 'router' constant is used to handle navigation within the application, and 'location' is used to get the current location of the application. The 'isLoading' constant is used to handle loading states during the startup process.

The 'PageWithProviders' function in 'appStartsLandingPage.tsx' is another important part of the app start process. It returns the 'InitializationModule' wrapped in 'ModulePageProviders', which sets up the necessary providers for the application.

<SwmSnippet path="/static/app/views/insights/mobile/appStarts/components/appStartup.tsx" line="46">

---

# AppStartup Function

The 'AppStartup' function sets up various constants and variables such as 'appStartType', 'version', 'primaryRelease', and 'router' which are used throughout the application's startup process.

```tsx
function AppStartup({additionalFilters, chartHeight}: Props) {
  const theme = useTheme();
  const pageFilter = usePageFilters();
  const {selection} = pageFilter;
  const location = useLocation();
  const organization = useOrganization();
  const {query: locationQuery} = location;

  const {
    primaryRelease,
    secondaryRelease,
    isLoading: isReleasesLoading,
  } = useReleaseSelection();
  const {truncatedPrimaryRelease, truncatedSecondaryRelease} = useTruncatedReleaseNames();
  const {isProjectCrossPlatform, selectedPlatform} = useCrossPlatformProject();

  const router = useRouter();

  const appStartType =
    decodeScalar(location.query[SpanMetricsField.APP_START_TYPE]) ?? COLD_START_TYPE;

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/mobile/appStarts/views/appStartsLandingPage.tsx" line="25">

---

# PageWithProviders Function

The 'PageWithProviders' function returns the 'InitializationModule' wrapped in 'ModulePageProviders', which sets up the necessary providers for the application.

```tsx
function PageWithProviders() {
  return (
    <ModulePageProviders moduleName="app_start" features="insights-initial-modules">
      <InitializationModule />
    </ModulePageProviders>
  );
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/mobile/appStarts/components/appStartup.tsx" line="47">

---

# Constants and Variables

'appStartType', 'version', 'primaryRelease', and 'router' are some of the constants and variables set up in the 'AppStartup' function. They play a crucial role in the application's startup process.

```tsx
  const theme = useTheme();
  const pageFilter = usePageFilters();
  const {selection} = pageFilter;
  const location = useLocation();
  const organization = useOrganization();
  const {query: locationQuery} = location;

  const {
    primaryRelease,
    secondaryRelease,
    isLoading: isReleasesLoading,
  } = useReleaseSelection();
  const {truncatedPrimaryRelease, truncatedSecondaryRelease} = useTruncatedReleaseNames();
  const {isProjectCrossPlatform, selectedPlatform} = useCrossPlatformProject();

  const router = useRouter();

  const appStartType =
    decodeScalar(location.query[SpanMetricsField.APP_START_TYPE]) ?? COLD_START_TYPE;

  const query = new MutableSearch([
```

---

</SwmSnippet>

# App Start Functions

This section discusses the main functions involved in the app start process in the Sentry demo.

<SwmSnippet path="/static/app/views/insights/mobile/appStarts/components/appStartup.tsx" line="46">

---

## AppStartup

The 'AppStartup' function sets up various constants and variables such as 'appStartType', 'version', 'primaryRelease', and 'router' which are used throughout the application's startup process. The 'appStartType' constant, for example, is used to determine the type of app start (cold or warm) and is used in various other components and functions. Similarly, 'version' is used to specify the version of the dataset being used, and 'primaryRelease' is used to handle release selections. The 'router' constant is used to handle navigation within the application, and 'location' is used to get the current location of the application. The 'isLoading' constant is used to handle loading states during the startup process.

```tsx
function AppStartup({additionalFilters, chartHeight}: Props) {
  const theme = useTheme();
  const pageFilter = usePageFilters();
  const {selection} = pageFilter;
  const location = useLocation();
  const organization = useOrganization();
  const {query: locationQuery} = location;

  const {
    primaryRelease,
    secondaryRelease,
    isLoading: isReleasesLoading,
  } = useReleaseSelection();
  const {truncatedPrimaryRelease, truncatedSecondaryRelease} = useTruncatedReleaseNames();
  const {isProjectCrossPlatform, selectedPlatform} = useCrossPlatformProject();

  const router = useRouter();

  const appStartType =
    decodeScalar(location.query[SpanMetricsField.APP_START_TYPE]) ?? COLD_START_TYPE;

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/mobile/appStarts/views/appStartsLandingPage.tsx" line="25">

---

## PageWithProviders

The 'PageWithProviders' function returns the 'InitializationModule' wrapped in 'ModulePageProviders', which sets up the necessary providers for the application. This function is an important part of the app start process.

```tsx
function PageWithProviders() {
  return (
    <ModulePageProviders moduleName="app_start" features="insights-initial-modules">
      <InitializationModule />
    </ModulePageProviders>
  );
}
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
