---
title: Basic Concepts of Mobile Screenload Performance
---
Screenload in the Mobile section of the Sentry-Demo repository refers to the process of loading and rendering screens in a mobile application. It is a crucial aspect of the application's performance and user experience.

The Screenload module is designed to provide insights into the performance of screen loading in mobile applications. It includes various components, views, and data setups to facilitate the tracking and analysis of screen load performance.

The Screenload module uses various constants and functions to manage and display data. For instance, the `PageloadModule` function is used to render the main page of the Screenload module, and the `hasModuleData` constant is used to determine if there is any data available for the module.

The Screenload module also includes a variety of components, such as tables, charts, and selectors, which are used to display and interact with the screen load data. These components are organized in a structured manner within the Screenload directory.

In addition to the components, the Screenload module also includes various views, such as the `screenloadLandingPage` and `screenLoadSpansPage`, which are used to display different aspects of the screen load data.

Overall, the Screenload module provides a comprehensive toolset for monitoring and analyzing screen load performance in mobile applications, helping developers identify and address performance issues.

<SwmSnippet path="/static/app/views/insights/mobile/screenload/views/screenloadLandingPage.tsx" line="34">

---

# PageloadModule Function

The `PageloadModule` function is the main function in the Screenload module. It uses various constants such as `organization`, `onboardingProject`, `hasModuleData`, and `isProjectCrossPlatform` to manage and display data related to screen load performance.

```tsx
export function PageloadModule() {
  const organization = useOrganization();
  const onboardingProject = useOnboardingProject();
  const hasModuleData = useHasFirstSpan(ModuleName.SCREEN_LOAD);
  const {isProjectCrossPlatform} = useCrossPlatformProject();

  const crumbs = useModuleBreadcrumbs('screen_load');

  return (
    <Layout.Page>
      <PageAlertProvider>
        <Layout.Header>
          <Layout.HeaderContent>
            <Breadcrumbs crumbs={crumbs} />
            <HeaderWrapper>
              <Layout.Title>
                {MODULE_TITLE}
                <PageHeadingQuestionTooltip
                  docsUrl={MODULE_DOC_LINK}
                  title={MODULE_DESCRIPTION}
                />
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/mobile/screenload/components/tables/screenLoadSpansTable.tsx" line="60">

---

# ScreenLoadSpansTable Component

The `ScreenLoadSpansTable` component is used to display a table of screen load spans. It uses the `moduleURL` constant to generate URLs for the spans.

```tsx
  primaryRelease,
  secondaryRelease,
}: Props) {
  const moduleURL = useModuleURL('screen_load');
  const location = useLocation();
  const {selection} = usePageFilters();
  const organization = useOrganization();
  const cursor = decodeScalar(location.query?.[MobileCursors.SPANS_TABLE]);
  const {isProjectCrossPlatform, selectedPlatform} = useCrossPlatformProject();

  const spanOp = decodeScalar(location.query[SpanMetricsField.SPAN_OP]) ?? '';
  const {hasTTFD, isLoading: hasTTFDLoading} = useTTFDConfigured([
    `transaction:"${transaction}"`,
  ]);

  const queryStringPrimary = useMemo(() => {
    const searchQuery = new MutableSearch([
      'transaction.op:ui.load',
      `transaction:${transaction}`,
      'has:span.description',
      ...(spanOp
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/mobile/screenload/components/tables/screensTable.tsx" line="46">

---

# ScreensTable Component

The `ScreensTable` component is used to display a table of screens. It uses the `moduleURL` constant to generate URLs for the screens.

```tsx
export function ScreensTable({data, eventView, isLoading, pageLinks, onCursor}: Props) {
  const moduleURL = useModuleURL('screen_load');
  const location = useLocation();
  const organization = useOrganization();
  const {primaryRelease, secondaryRelease} = useReleaseSelection();
  const {project} = useCrossPlatformProject();
  const eventViewColumns = eventView.getColumns();

  const ttidColumnNamePrimaryRelease = `avg_if(measurements.time_to_initial_display,release,${primaryRelease})`;
  const ttidColumnNameSecondaryRelease = `avg_if(measurements.time_to_initial_display,release,${secondaryRelease})`;
  const ttfdColumnNamePrimaryRelease = `avg_if(measurements.time_to_full_display,release,${primaryRelease})`;
  const ttfdColumnNameSecondaryRelease = `avg_if(measurements.time_to_full_display,release,${secondaryRelease})`;
  const countColumnName = `count()`;

  const columnNameMap = {
    transaction: t('Screen'),
    [ttidColumnNamePrimaryRelease]: t('AVG TTID (%s)', PRIMARY_RELEASE_ALIAS),
    [ttidColumnNameSecondaryRelease]: t('AVG TTID (%s)', SECONDARY_RELEASE_ALIAS),
    [ttfdColumnNamePrimaryRelease]: t('AVG TTFD (%s)', PRIMARY_RELEASE_ALIAS),
    [ttfdColumnNameSecondaryRelease]: t('AVG TTFD (%s)', SECONDARY_RELEASE_ALIAS),
    [countColumnName]: t('Total Count'),
```

---

</SwmSnippet>

# Screenload Functions

This section will explain the main functions of the Screenload module, including PageloadModule, ScreenLoadSpans, ScreenLoadEventSamples, and ScreensTable.

<SwmSnippet path="/static/app/views/insights/mobile/screenload/views/screenloadLandingPage.tsx" line="34">

---

## PageloadModule

The `PageloadModule` function is used to render the main page of the Screenload module. It uses various hooks and constants to manage the state and data of the module.

```tsx
export function PageloadModule() {
  const organization = useOrganization();
  const onboardingProject = useOnboardingProject();
  const hasModuleData = useHasFirstSpan(ModuleName.SCREEN_LOAD);
  const {isProjectCrossPlatform} = useCrossPlatformProject();

  const crumbs = useModuleBreadcrumbs('screen_load');

  return (
    <Layout.Page>
      <PageAlertProvider>
        <Layout.Header>
          <Layout.HeaderContent>
            <Breadcrumbs crumbs={crumbs} />
            <HeaderWrapper>
              <Layout.Title>
                {MODULE_TITLE}
                <PageHeadingQuestionTooltip
                  docsUrl={MODULE_DOC_LINK}
                  title={MODULE_DESCRIPTION}
                />
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/mobile/screenload/views/screenLoadSpansPage.tsx" line="54">

---

## ScreenLoadSpans

The `ScreenLoadSpans` function is used to display the spans of the screen load. It uses various hooks and constants to manage the state and data of the spans.

```tsx
function ScreenLoadSpans() {
  const location = useLocation<Query>();
  const organization = useOrganization();
  const router = useRouter();
  const {isProjectCrossPlatform} = useCrossPlatformProject();

  const crumbs = useModuleBreadcrumbs('screen_load');

  const {
    spanGroup,
    primaryRelease,
    secondaryRelease,
    transaction: transactionName,
    spanDescription,
  } = location.query;

  return (
    <Layout.Page>
      <PageAlertProvider>
        <Layout.Header>
          <Layout.HeaderContent>
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/mobile/screenload/components/eventSamples.tsx" line="33">

---

## ScreenLoadEventSamples

The `ScreenLoadEventSamples` function is used to display the event samples of the screen load. It uses various hooks and constants to manage the state and data of the event samples.

```tsx
export function ScreenLoadEventSamples({
  cursorName,
  transaction,
  release,
  sortKey,
  showDeviceClassSelector,
}: Props) {
  const location = useLocation();
  const {selection} = usePageFilters();
  const {primaryRelease} = useReleaseSelection();
  const cursor = decodeScalar(location.query?.[cursorName]);
  const {selectedPlatform: platform, isProjectCrossPlatform} = useCrossPlatformProject();

  const deviceClass = decodeScalar(location.query['device.class']);

  const searchQuery = useMemo(() => {
    const mutableQuery = new MutableSearch([
      'transaction.op:ui.load',
      `transaction:${transaction}`,
      `release:${release}`,
    ]);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/mobile/screenload/components/tables/screensTable.tsx" line="46">

---

## ScreensTable

The `ScreensTable` function is used to display a table of the screens. It uses various hooks and constants to manage the state and data of the table.

```tsx
export function ScreensTable({data, eventView, isLoading, pageLinks, onCursor}: Props) {
  const moduleURL = useModuleURL('screen_load');
  const location = useLocation();
  const organization = useOrganization();
  const {primaryRelease, secondaryRelease} = useReleaseSelection();
  const {project} = useCrossPlatformProject();
  const eventViewColumns = eventView.getColumns();

  const ttidColumnNamePrimaryRelease = `avg_if(measurements.time_to_initial_display,release,${primaryRelease})`;
  const ttidColumnNameSecondaryRelease = `avg_if(measurements.time_to_initial_display,release,${secondaryRelease})`;
  const ttfdColumnNamePrimaryRelease = `avg_if(measurements.time_to_full_display,release,${primaryRelease})`;
  const ttfdColumnNameSecondaryRelease = `avg_if(measurements.time_to_full_display,release,${secondaryRelease})`;
  const countColumnName = `count()`;

  const columnNameMap = {
    transaction: t('Screen'),
    [ttidColumnNamePrimaryRelease]: t('AVG TTID (%s)', PRIMARY_RELEASE_ALIAS),
    [ttidColumnNameSecondaryRelease]: t('AVG TTID (%s)', SECONDARY_RELEASE_ALIAS),
    [ttfdColumnNamePrimaryRelease]: t('AVG TTFD (%s)', PRIMARY_RELEASE_ALIAS),
    [ttfdColumnNameSecondaryRelease]: t('AVG TTFD (%s)', SECONDARY_RELEASE_ALIAS),
    [countColumnName]: t('Total Count'),
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
