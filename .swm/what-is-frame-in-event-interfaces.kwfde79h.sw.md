---
title: What is Frame in Event Interfaces
---
In the Sentry-Demo repository, 'Frame' is a type used in various components within the 'Interfaces' directory. It is used to represent a single frame of a stack trace in an event. The 'Frame' type contains information about the source code file, function, and line number where an error occurred, as well as other metadata. It is used in various contexts such as rendering the frame's details, linking the frame to its source code, and displaying the frame in the context of its surrounding source code lines.

The 'Frame' type is used in several components within the 'Interfaces' directory. For example, it is used in the 'Context' component to provide detailed context about an error, including source code, variables, and registers. It is also used in the 'DefaultTitle' component to display information about the frame in the event details page, and in the 'FunctionName' component to display the name of the function where the error occurred.

In addition to being used in individual components, 'Frame' is also a key part of several utility functions. These functions use the 'Frame' type to perform operations such as determining whether a frame has source code context, or generating a link to the source code file where the error occurred.

<SwmSnippet path="/static/app/components/events/interfaces/frame/context.tsx" line="33">

---

# Usage of 'Frame' in Components

'Frame' is used as a prop in the 'Context' component. This component uses the 'Frame' to provide detailed context about an error, including source code, variables, and registers.

```tsx
type Props = {
  components: SentryAppComponent<SentryAppSchemaStacktraceLink>[];
  event: Event;
  frame: Frame;
  registers: {[key: string]: string};
  className?: string;
  emptySourceNotation?: boolean;
  frameMeta?: Record<any, any>;
  hasAssembly?: boolean;
  hasContextRegisters?: boolean;
  hasContextSource?: boolean;
  hasContextVars?: boolean;
  isExpanded?: boolean;
  isFirst?: boolean;
  platform?: PlatformKey;
  registersMeta?: Record<any, any>;
};
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/frame/defaultTitle/index.tsx" line="22">

---

'Frame' is also used in the 'DefaultTitle' component. This component uses the 'Frame' to display information about the frame in the event details page.

```tsx
type Props = {
  frame: Frame;
  platform: PlatformKey;
  /**
   * Is the stack trace being previewed in a hovercard?
   */
  isHoverPreviewed?: boolean;
  isUsedForGrouping?: boolean;
  meta?: Record<any, any>;
};

type GetPathNameOutput = {key: string; value: string; meta?: Meta};

function DefaultTitle({
  frame,
  platform,
  isHoverPreviewed,
  isUsedForGrouping,
  meta,
}: Props) {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/frame/functionName.tsx" line="6">

---

In the 'FunctionName' component, 'Frame' is used to display the name of the function where the error occurred.

```tsx
type Props = {
  frame: Frame;
  className?: string;
  hasHiddenDetails?: boolean;
  meta?: Record<any, any>;
  showCompleteFunctionName?: boolean;
};

export function FunctionName({
  frame,
  showCompleteFunctionName,
  hasHiddenDetails,
  className,
  meta,
  ...props
}: Props) {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/frame/utils.tsx" line="22">

---

# Usage of 'Frame' in Utility Functions

'Frame' is also used in utility functions. For example, the 'getFrameHint' function uses the 'Frame' to generate a hint about the frame, based on its properties.

```tsx
export function getFrameHint(frame: Frame) {
  // returning [hintText, hintIcon]
  const {symbolicatorStatus} = frame;
  const func = frame.function || '<unknown>';
  // Custom color used to match adjacent text.
  const warningIcon = <IconQuestion size="xs" color={'#2c45a8' as any} />;
  const errorIcon = <IconWarning size="xs" color="red300" />;

  if (func.match(/^@objc\s/)) {
    return [t('Objective-C -> Swift shim frame'), warningIcon];
  }
  if (func.match(/^__?hidden#\d+/)) {
    return [t('Hidden function from bitcode build'), errorIcon];
  }
  if (!symbolicatorStatus && func === '<unknown>') {
    // Only render this if the event was not symbolicated.
    return [t('No function name was supplied by the client SDK.'), warningIcon];
  }

  if (
    func === '<unknown>' ||
```

---

</SwmSnippet>

# Understanding Frame Functions

Let's take a closer look at some of the key functions related to the 'Frame' type in the Sentry-Demo repository.

<SwmSnippet path="/static/app/components/events/interfaces/frame/utils.tsx" line="22">

---

## getFrameHint

The `getFrameHint` function is used to provide hints about a frame. It takes a 'Frame' as an argument and returns an array containing a hint text and a hint icon. The function checks various properties of the frame to determine the appropriate hint. For example, it checks if the function name matches certain patterns, or if the symbolicator status indicates a missing symbol or an unknown image.

```tsx
export function getFrameHint(frame: Frame) {
  // returning [hintText, hintIcon]
  const {symbolicatorStatus} = frame;
  const func = frame.function || '<unknown>';
  // Custom color used to match adjacent text.
  const warningIcon = <IconQuestion size="xs" color={'#2c45a8' as any} />;
  const errorIcon = <IconWarning size="xs" color="red300" />;

  if (func.match(/^@objc\s/)) {
    return [t('Objective-C -> Swift shim frame'), warningIcon];
  }
  if (func.match(/^__?hidden#\d+/)) {
    return [t('Hidden function from bitcode build'), errorIcon];
  }
  if (!symbolicatorStatus && func === '<unknown>') {
    // Only render this if the event was not symbolicated.
    return [t('No function name was supplied by the client SDK.'), warningIcon];
  }

  if (
    func === '<unknown>' ||
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/frame/utils.tsx" line="73">

---

## hasContextSource

The `hasContextSource` function checks if a frame has source code context. It takes a 'Frame' as an argument and returns a boolean indicating whether the frame has context. This is determined by checking if the 'context' property of the frame is defined and has a length greater than zero.

```tsx
export function hasContextSource(frame: Frame) {
  return defined(frame.context) && !!frame.context.length;
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/frame/utils.tsx" line="77">

---

## hasContextVars

The `hasContextVars` function checks if a frame has context variables. It takes a 'Frame' as an argument and returns a boolean indicating whether the frame has context variables. This is determined by checking if the 'vars' property of the frame is not an empty object.

```tsx
export function hasContextVars(frame: Frame) {
  return !isEmptyObject(frame.vars || {});
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/frame/utils.tsx" line="85">

---

## hasAssembly

The `hasAssembly` function checks if a frame has assembly information. It takes a 'Frame' and an optional platform as arguments and returns a boolean indicating whether the frame has assembly information. This is determined by checking if the platform is '.NET' and if the 'package' property of the frame is defined.

```tsx
export function hasAssembly(frame: Frame, platform?: string) {
  return (
    isDotnet(getPlatform(frame.platform, platform ?? 'other')) && defined(frame.package)
  );
}
```

---

</SwmSnippet>

# Frame Endpoints

Understanding Frame Endpoints

<SwmSnippet path="/static/app/components/events/interfaces/frame/stacktraceLinkModal.tsx" line="113">

---

## /projects/{organization.slug}/{project.slug}/repo-path-parsing/ Endpoint

This endpoint is used to parse the path of the repository. It is a POST request that sends data related to the source code and the stack trace root. The response from this endpoint is used to create a code mapping configuration.

```tsx
    const parsingEndpoint = `/projects/${organization.slug}/${project.slug}/repo-path-parsing/`;
    try {
      const configData = await api.requestPromise(parsingEndpoint, {
        method: 'POST',
        data: {
          sourceUrl: sourceCodeInput,
          stackPath: filename,
        },
      });
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/frame/stacktraceLinkModal.tsx" line="123">

---

## /organizations/{organization.slug}/code-mappings/ Endpoint

This endpoint is used to create a new code mapping configuration. It is a POST request that sends data related to the source code, stack trace root, and the configuration obtained from the previous endpoint. The response from this endpoint is used to save the stack trace configuration.

```tsx
      const configEndpoint = `/organizations/${organization.slug}/code-mappings/`;
      await api.requestPromise(configEndpoint, {
        method: 'POST',
        data: {
          ...configData,
          projectId: project.id,
          integrationId: configData.integrationId,
        },
      });
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
