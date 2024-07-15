---
title: Delving into Sentrys Testing Suite and QA Practices
---
This document will cover the topic of testing in `.spec.tsx` files and how code quality assurance is maintained in the project. We'll cover:

1. What's being tested in the `.spec.tsx` files
2. How is code quality assurance maintained in the project.

<SwmSnippet path="/static/app/components/replays/utils.spec.tsx" line="16">

---

# What's being tested in the `.spec.tsx` files

This file contains a series of tests for the `countColumns` function. The function is tested with different inputs to ensure it behaves as expected in various scenarios.

```tsx
describe('countColumns', () => {
  it('should divide 27s by 2700px to find twentyseven 1s columns, with some fraction remaining', () => {
    // 2700 allows for up to 27 columns at 100px wide.
    // That is what we'd need if we were to render at `1s` granularity, so we can.
    const width = 2700;

    const duration = 27 * SECOND;
    const minWidth = 100;
    const {timespan, cols, remaining} = countColumns(duration, width, minWidth);

    expect(timespan).toBe(1 * SECOND);
    expect(cols).toBe(27);
    expect(remaining).toBe(0);
  });

  it('should divide 27s by 2699px to find five 5s columns, with some fraction remaining', () => {
    // 2699px allows for up to 26 columns at 100px wide, with 99px leftover.
    // That is less than the 27 cols we'd need if we were to render at `1s` granularity.
    // So instead we get 5 cols (wider than 100px) at 5s granularity, and some extra space is remaining.
    const width = 2699;

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/content.spec.tsx" line="16">

---

This file contains tests for the Performance Content component. It verifies that the component renders correctly and behaves as expected under different conditions.

```tsx
const FEATURES = ['performance-view'];

function WrappedComponent({router}) {
  return (
    <MEPSettingProvider>
      <PerformanceContent router={router} location={router.location} />
    </MEPSettingProvider>
  );
}

function initializeData(projects, query, features = FEATURES) {
  const organization = OrganizationFixture({
    features,
  });
  const initialData = initializeOrg({
    projects,
    organization,
    router: {
      location: {
        pathname: '/test',
        query: query || {},
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/traceDetails/content.spec.tsx" line="9">

---

This file contains tests for the Trace Details Content component. It verifies that the component renders correctly and behaves as expected under different conditions.

```tsx
const SAMPLE_ERROR_DATA = {
  data: [
    {id: '1', level: 'error', title: 'Test error 1', project: 'sentry'},
    {id: '2', level: 'fatal', title: 'Test error 2', project: 'sentry'},
  ],
};

const initializeData = () => {
  const data = _initializeData({
    features: ['performance-view', 'trace-view'],
  });

  act(() => ProjectsStore.loadInitialData(data.projects));
  return data;
};

describe('TraceDetailsContent', () => {
  describe('Without Transactions', () => {
    beforeEach(() => {
      MockApiClient.addMockResponse({
        url: '/organizations/org-slug/events/',
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/api.spec.tsx" line="9">

---

# How is code quality assurance maintained in the project

This file contains tests for the API client. It verifies that the client behaves as expected under different conditions, ensuring the quality of the API interactions in the project.

```tsx
jest.unmock('sentry/api');

describe('api', function () {
  let api;

  beforeEach(function () {
    api = new MockApiClient();
  });

  describe('Client', function () {
    describe('cancel()', function () {
      it('should abort any open XHR requests', function () {
        const abort1 = jest.fn();
        const abort2 = jest.fn();

        const req1 = new Request(new Promise(() => null), {
          abort: abort1,
        } as any);
        const req2 = new Request(new Promise(() => null), {abort: abort2} as any);

        api.activeRequests = {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/projectDebugFiles/sources/builtInRepositories.spec.tsx" line="8">

---

This file contains tests for the Built-in Repositories settings. It verifies that the settings render correctly and behave as expected under different conditions.

```tsx
describe('Built-in Repositories', function () {
  const api = new MockApiClient();
  const {project, organization} = initializeOrg();

  const builtinSymbolSourceOptions = BuiltInSymbolSourcesFixture();
  const builtinSymbolSources = ['ios', 'microsoft', 'android'];

  it('renders', function () {
    render(
      <BuiltInRepositories
        api={api}
        organization={organization}
        project={project}
        builtinSymbolSourceOptions={builtinSymbolSourceOptions}
        builtinSymbolSources={builtinSymbolSources}
      />
    );

    // Section Title
    expect(screen.queryAllByText('Built-in Repositories')).toHaveLength(2);

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/commandLine.spec.tsx" line="6">

---

This file contains a test for the CommandLine component. It verifies that the component renders correctly.

```tsx
  it('renders', () => {
    const children = 'sentry devserver --workers';
    render(<CommandLine>{children}</CommandLine>);
    expect(screen.getByText(children)).toBeInTheDocument();
  });
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/releases/detail/utils.spec.tsx" line="12">

---

This file contains tests for the utility functions used in the Releases detail view. It verifies that these functions behave as expected under different conditions.

```tsx
  describe('generateReleaseMarkLines', () => {
    const {created, adopted, unadopted} = releaseMarkLinesLabels;
    const {router} = initializeOrg();
    const release = ReleaseFixture();
    const project = release.projects[0];

    it('generates "Created" markline', () => {
      const marklines = generateReleaseMarkLines(
        release,
        project,
        lightTheme,
        router.location
      );

      expect(marklines.map(markline => markline.seriesName)).toEqual([created]);
    });

    it('generates also Adoption marklines if exactly one env is selected', () => {
      const marklines = generateReleaseMarkLines(release, project, lightTheme, {
        ...router.location,
        query: {environment: 'prod'},
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="follow-up"><sup>Powered by [Swimm](/)</sup></SwmMeta>
