---
title: Understanding Debug Image Details in Debug Meta
---
Debug Image Details in Debug Meta refers to the detailed information about a debug image in the Sentry application. It is implemented in the `DebugImageDetails` function in the `index.tsx` file located in the `debugImageDetails` directory. This function receives properties such as the event, organization, project slug, and image, and uses these to fetch and display detailed information about the debug image.

The `DebugImageDetails` function uses the `useApiQuery` hook to fetch debug files related to the image. It then processes these debug files and the image's candidates to generate a sorted list of candidates. Each candidate represents a debug file that matches the debug image. The status of each candidate (e.g., whether it has been applied, has an error, etc.) is also determined during this process.

The `DebugImageDetails` function also defines the layout and style of the debug image details modal. It uses styled components to define the layout and appearance of the modal's content, title, and filename. It also defines the modal's responsive behavior for different screen sizes.

The `DebugImageDetails` function also handles user interactions such as deleting a debug file. When a user clicks the delete button for a debug file, the function sends a DELETE request to the Sentry API to delete the debug file.

The `DebugImageDetails` function also uses other components to display specific parts of the debug image details. For example, it uses the `GeneralInfo` component to display general information about the debug image, and the `Candidates` component to display the list of candidates for the debug image.

<SwmSnippet path="/static/app/components/events/interfaces/debugMeta/debugImageDetails/index.tsx" line="210">

---

## DebugImageDetails Function

The `DebugImageDetails` function is the main function for displaying debug image details. It uses the `useApiQuery` hook to fetch debug files related to the image.

```tsx
  onReprocessEvent,
}: DebugImageDetailsProps) {
  const organization = useOrganization();
  const api = useApi();
  const hasUploadedDebugFiles =
    image?.candidates?.some(candidate => candidate.source === INTERNAL_SOURCE) ?? false;

  const {
    data: debugFiles,
    isLoading,
    isError,
    refetch,
  } = useApiQuery<DebugFile[]>(
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/debugMeta/debugImageDetails/index.tsx" line="223">

---

## Fetching Debug Files

The `useApiQuery` hook is used to fetch debug files related to the image. The debug files are fetched from the Sentry API using the organization slug, project slug, and debug ID of the image.

```tsx
    [
      `/projects/${organization.slug}/${projSlug}/files/dsyms/?debug_id=${image?.debug_id}`,
      {
        query: {
          // FIXME(swatinem): Ideally we should not filter here at all,
          // though Symbolicator does not currently report `bcsymbolmap` and `il2cpp`
          // candidates, and we would thus show bogus "unapplied" entries for those,
          // which would probably confuse people more than not seeing successfully
          // fetched candidates for those two types of files.
          file_formats: [
            'breakpad',
            'macho',
            'elf',
            'pe',
            'pdb',
            'sourcebundle',
            'wasm',
            'portablepdb',
          ],
        },
      },
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/debugMeta/debugImageDetails/index.tsx" line="252">

---

## Processing Debug Files and Candidates

The debug files and the image's candidates are processed to generate a sorted list of candidates. Each candidate represents a debug file that matches the debug image. The status of each candidate is also determined during this process.

```tsx
  const candidates = getCandidates({debugFiles, image, isLoading});
  const baseUrl = api.baseUrl;
  const fileName = getFileName(code_file);
  const haveCandidatesUnappliedDebugFile = candidates.some(
    candidate => candidate.download.status === CandidateDownloadStatus.UNAPPLIED
  );
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/debugMeta/debugImageDetails/index.tsx" line="344">

---

## Defining the Layout and Style

The `DebugImageDetails` function defines the layout and style of the debug image details modal. It uses styled components to define the layout and appearance of the modal's content, title, and filename. It also defines the modal's responsive behavior for different screen sizes.

```tsx
const Content = styled('div')`
  display: grid;
  gap: ${space(3)};
  font-size: ${p => p.theme.fontSizeMedium};
`;

const Title = styled('div')`
  display: grid;
  grid-template-columns: max-content 1fr;
  gap: ${space(1)};
  align-items: center;
  font-size: ${p => p.theme.fontSizeExtraLarge};
  max-width: calc(100% - 40px);
  word-break: break-all;
`;

const FileName = styled('span')`
  font-family: ${p => p.theme.text.familyMono};
`;

const StyledButtonBar = styled(ButtonBar)`
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/debugMeta/debugImageDetails/index.tsx" line="269">

---

## Handling User Interactions

The `DebugImageDetails` function handles user interactions such as deleting a debug file. When a user clicks the delete button for a debug file, the function sends a DELETE request to the Sentry API to delete the debug file.

```tsx
  const handleDelete = async (debugId: string) => {
    try {
      await api.requestPromise(
        `/projects/${organization.slug}/${projSlug}/files/dsyms/?id=${debugId}`,
        {method: 'DELETE'}
      );
      refetch();
    } catch {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/debugMeta/debugImageDetails/index.tsx" line="296">

---

## Using Other Components

The `DebugImageDetails` function uses other components to display specific parts of the debug image details. For example, it uses the `GeneralInfo` component to display general information about the debug image, and the `Candidates` component to display the list of candidates for the debug image.

```tsx
          <GeneralInfo image={image} />
          {hasReprocessWarning && (
            <ReprocessAlert
              api={api}
              orgSlug={organization.slug}
              projSlug={projSlug}
              eventId={event.id}
```

---

</SwmSnippet>

# Debug Image Details Functions

This section will explain the main functions involved in the Debug Image Details functionality.

<SwmSnippet path="/static/app/components/events/interfaces/debugMeta/debugImageDetails/index.tsx" line="203">

---

## DebugImageDetails Function

The `DebugImageDetails` function is the main function responsible for rendering the Debug Image Details modal. It fetches debug files related to the image, processes these files and the image's candidates to generate a sorted list of candidates, and defines the layout and style of the modal. It also handles user interactions such as deleting a debug file.

```tsx
export function DebugImageDetails({
  image,
  projSlug,
  Header,
  Body,
  Footer,
  event,
  onReprocessEvent,
}: DebugImageDetailsProps) {
  const organization = useOrganization();
  const api = useApi();
  const hasUploadedDebugFiles =
    image?.candidates?.some(candidate => candidate.source === INTERNAL_SOURCE) ?? false;

  const {
    data: debugFiles,
    isLoading,
    isError,
    refetch,
  } = useApiQuery<DebugFile[]>(
    [
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/debugMeta/debugImageDetails/index.tsx" line="87">

---

## getCandidates Function

The `getCandidates` function is used within `DebugImageDetails` to process the debug files and the image's candidates. It maps each candidate to a debug file and sorts them based on certain criteria. The result is a sorted list of candidates, each representing a debug file that matches the debug image.

```tsx
  image,
  isLoading,
}: {
  debugFiles: DebugFile[] | undefined;
  image: DebugImageDetailsProps['image'];
  isLoading: boolean;
}) {
  const {candidates = []} = image ?? {};

  if (!debugFiles || isLoading) {
    return candidates;
  }

  const debugFileCandidates = candidates.map(({location, ...candidate}) => ({
    ...candidate,
    location: location?.includes(INTERNAL_SOURCE_LOCATION)
      ? location.split(INTERNAL_SOURCE_LOCATION)[1]
      : location,
  }));

  const candidateLocations = new Set(
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/debugMeta/debugImageDetails/index.tsx" line="217">

---

## useApiQuery Hook

The `useApiQuery` hook is used within `DebugImageDetails` to fetch debug files related to the image. It sends a GET request to the Sentry API and returns the response data, which includes the debug files.

```tsx
  const {
    data: debugFiles,
    isLoading,
    isError,
    refetch,
  } = useApiQuery<DebugFile[]>(
    [
      `/projects/${organization.slug}/${projSlug}/files/dsyms/?debug_id=${image?.debug_id}`,
      {
        query: {
          // FIXME(swatinem): Ideally we should not filter here at all,
          // though Symbolicator does not currently report `bcsymbolmap` and `il2cpp`
          // candidates, and we would thus show bogus "unapplied" entries for those,
          // which would probably confuse people more than not seeing successfully
          // fetched candidates for those two types of files.
          file_formats: [
            'breakpad',
            'macho',
            'elf',
            'pe',
            'pdb',
```

---

</SwmSnippet>

# Debug Image Details API

Debug Image Details API

<SwmSnippet path="/static/app/components/events/interfaces/debugMeta/debugImageDetails/reprocessAlert.tsx" line="42">

---

## Debug Image Details API

The endpoint `/projects/${orgSlug}/${projSlug}/events/${eventId}/reprocessable/` is used to check if an event is reprocessable. The `orgSlug`, `projSlug`, and `eventId` are parameters that specify the organization, project, and event respectively. The endpoint is accessed using the `requestPromise` method of the `api` object, which sends a HTTP request to the endpoint and returns a promise that resolves with the response.

```tsx
      const response = await api.requestPromise(
        `/projects/${orgSlug}/${projSlug}/events/${eventId}/reprocessable/`
      );
      setReprocessableEvent(response);
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
