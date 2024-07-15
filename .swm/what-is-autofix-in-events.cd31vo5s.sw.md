---
title: What is Autofix in Events
---
Autofix in Events refers to a feature that automatically attempts to fix errors identified in the event data. It is implemented as a React component in the `static/app/components/events/autofix` directory. The main component, `Autofix`, uses several hooks and components to manage and display the autofix process.

The `useAiAutofix` hook is used to manage the autofix process. It uses the `useApi` hook to make API requests and the `useApiQuery` hook to fetch data. The `autofixData` constant, which is derived from the API response, holds the current state of the autofix process.

The `Autofix` component uses the `autofixData` to determine what to display. If `autofixData` is present, it displays an `AutofixCard` with the current autofix data. If not, it displays an `AutofixBanner` indicating that autofix can be triggered.

The `useAutofixSetup` hook is used to check if the necessary conditions for starting the autofix process are met. It makes an API request to the `/issues/${groupId}/autofix/setup/` endpoint and checks several conditions, such as whether the integration is set up, whether AI consent is given, and whether the codebase is indexed.

<SwmSnippet path="/static/app/components/events/autofix/index.tsx" line="15">

---

# Autofix Function

This is the main Autofix function. It uses the `useAiAutofix` hook to manage the autofix process and the `useAutofixSetup` hook to check if the necessary conditions for starting the autofix process are met. The `autofixData` constant holds the current state of the autofix process, which is used to determine what to display.

```tsx
export function Autofix({event, group}: Props) {
  const {autofixData, triggerAutofix, reset} = useAiAutofix(group, event);

  const {canStartAutofix} = useAutofixSetup({
    groupId: group.id,
  });

  useRouteAnalyticsParams({
    autofix_status: autofixData?.status ?? 'none',
  });

  return (
    <ErrorBoundary mini>
      <div>
        {autofixData ? (
          <AutofixCard data={autofixData} onRetry={reset} groupId={group.id} />
        ) : (
          <AutofixBanner
            groupId={group.id}
            projectId={group.project.id}
            triggerAutofix={triggerAutofix}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/autofix/useAutofix.tsx" line="16">

---

# useAiAutofix Hook

The `useAiAutofix` hook is used to manage the autofix process. It uses the `useApi` hook to make API requests and the `useApiQuery` hook to fetch data.

```tsx

export type AutofixResponse = {
  autofix: AutofixData | null;
};

const POLL_INTERVAL = 2500;

export const makeAutofixQueryKey = (groupId: string): ApiQueryKey => [
  `/issues/${groupId}/autofix/`,
];

const makeInitialAutofixData = (): AutofixResponse => ({
  autofix: {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/autofix/useAutofixSetup.tsx" line="37">

---

# useAutofixSetup Hook

The `useAutofixSetup` hook is used to check if the necessary conditions for starting the autofix process are met. It makes an API request to the `/issues/${groupId}/autofix/setup/` endpoint and checks several conditions, such as whether the integration is set up, whether AI consent is given, and whether the codebase is indexed.

```tsx
export function useAutofixSetup(
  {groupId}: {groupId: string},
  options: Omit<UseApiQueryOptions<AutofixSetupResponse, RequestError>, 'staleTime'> = {}
) {
  const queryData = useApiQuery<AutofixSetupResponse>(makeAutofixSetupQueryKey(groupId), {
    enabled: Boolean(groupId),
    staleTime: 0,
    retry: false,
    ...options,
  });

  return {
    ...queryData,
    canStartAutofix: Boolean(
      queryData.data?.integration.ok &&
        queryData.data?.genAIConsent.ok &&
```

---

</SwmSnippet>

# Autofix Functions and Components

This section will explain the main functions and components used in the Autofix feature of the Sentry application.

<SwmSnippet path="/static/app/components/events/autofix/useAutofix.tsx" line="15">

---

## useAiAutofix

The `useAiAutofix` hook is used to manage the autofix process. It uses the `useApi` hook to make API requests and the `useApiQuery` hook to fetch data. The `autofixData` constant, which is derived from the API response, holds the current state of the autofix process.

```tsx
import useApi from 'sentry/utils/useApi';

export type AutofixResponse = {
  autofix: AutofixData | null;
};

const POLL_INTERVAL = 2500;

export const makeAutofixQueryKey = (groupId: string): ApiQueryKey => [
  `/issues/${groupId}/autofix/`,
];

const makeInitialAutofixData = (): AutofixResponse => ({
  autofix: {
    status: 'PROCESSING',
    run_id: '',
    steps: [
      {
        type: AutofixStepType.DEFAULT,
        id: '1',
        index: 0,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/autofix/useAutofixSetup.tsx" line="37">

---

## useAutofixSetup

The `useAutofixSetup` hook is used to check if the necessary conditions for starting the autofix process are met. It makes an API request to the `/issues/${groupId}/autofix/setup/` endpoint and checks several conditions, such as whether the integration is set up, whether AI consent is given, and whether the codebase is indexed.

```tsx
export function useAutofixSetup(
  {groupId}: {groupId: string},
  options: Omit<UseApiQueryOptions<AutofixSetupResponse, RequestError>, 'staleTime'> = {}
) {
  const queryData = useApiQuery<AutofixSetupResponse>(makeAutofixSetupQueryKey(groupId), {
    enabled: Boolean(groupId),
    staleTime: 0,
    retry: false,
    ...options,
  });

  return {
    ...queryData,
    canStartAutofix: Boolean(
      queryData.data?.integration.ok &&
        queryData.data?.genAIConsent.ok &&
        queryData.data?.codebaseIndexing.ok
    ),
    canCreatePullRequests: Boolean(queryData.data?.githubWriteIntegration.ok),
  };
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/autofix/index.tsx" line="15">

---

## Autofix

The `Autofix` component uses the `autofixData` to determine what to display. If `autofixData` is present, it displays an `AutofixCard` with the current autofix data. If not, it displays an `AutofixBanner` indicating that autofix can be triggered.

```tsx
export function Autofix({event, group}: Props) {
  const {autofixData, triggerAutofix, reset} = useAiAutofix(group, event);

  const {canStartAutofix} = useAutofixSetup({
    groupId: group.id,
  });

  useRouteAnalyticsParams({
    autofix_status: autofixData?.status ?? 'none',
  });

  return (
    <ErrorBoundary mini>
      <div>
        {autofixData ? (
          <AutofixCard data={autofixData} onRetry={reset} groupId={group.id} />
        ) : (
          <AutofixBanner
            groupId={group.id}
            projectId={group.project.id}
            triggerAutofix={triggerAutofix}
```

---

</SwmSnippet>

# Autofix Endpoints

Understanding Autofix Endpoints

<SwmSnippet path="/static/app/components/events/autofix/useAutofix.tsx" line="24">

---

## `/issues/${groupId}/autofix/` Endpoint

This endpoint is used to get the current state of the autofix process for a specific issue. The `groupId` parameter in the URL is used to specify the issue. The `useAutofixData` hook uses this endpoint to fetch the current autofix data.

```tsx
  `/issues/${groupId}/autofix/`,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/autofix/autofixInputField.tsx" line="28">

---

## `/issues/${groupId}/autofix/update/` Endpoint

This endpoint is used to update the autofix process for a specific issue. The `groupId` parameter in the URL is used to specify the issue. The `useAutofixUserInstruction` hook uses this endpoint to send user instructions to the autofix process.

```tsx
      return api.requestPromise(`/issues/${groupId}/autofix/update/`, {
        method: 'POST',
        data: {
          run_id: runId,
          payload: {
            type: 'instruction',
            content: {
              type: 'text',
              text: params.instruction,
            },
          },
        },
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
