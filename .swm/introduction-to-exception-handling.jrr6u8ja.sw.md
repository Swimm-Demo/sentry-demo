---
title: Introduction to Exception Handling
---
In the sentry-demo repository, an Exception refers to a specific type of error or issue that has occurred within the application. It is a key part of the error tracking and performance monitoring functionality provided by Sentry. The Exception is captured and processed by Sentry's SDKs and then sent to the Sentry server for further analysis and tracking.

The Exception is represented in the codebase as an object with various properties that provide information about the error. This includes details such as the type of error, the message associated with the error, the stack trace, and any additional data related to the error.

The Exception is used in various parts of the codebase, particularly within the 'Crash Content' component. This component is responsible for displaying detailed information about an error event, including the Exception details. The Exception data is used to populate various parts of the UI, providing developers with valuable insights into the nature of the error.

The Exception also plays a crucial role in the handling of error events. When an error occurs, an Exception is created and processed by Sentry's SDKs. This includes capturing the stack trace, which provides a snapshot of the application's state at the time of the error, and any additional data related to the error. This information is then sent to the Sentry server for further analysis and tracking.

<SwmSnippet path="/static/app/components/events/interfaces/crashContent/exception/relatedExceptions.tsx" line="25">

---

# Exception Object

The Exception is represented in the codebase as an object with various properties that provide information about the error. This includes details such as the type of error, the message associated with the error, the stack trace, and any additional data related to the error.

```tsx
  exception: ExceptionValue;
  link: boolean;
  onExceptionClick: (exceptionId: number) => void;
};
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/crashContent/exception/relatedExceptions.tsx" line="146">

---

# Exception Handling

The Exception also plays a crucial role in the handling of error events. When an error occurs, an Exception is created and processed by Sentry's SDKs. This information is then sent to the Sentry server for further analysis and tracking.

```tsx
export function RelatedExceptions({
  allExceptions,
  mechanism,
  newestFirst,
  onExceptionClick,
}: ExceptionGroupContextProps) {
  if (!mechanism || !mechanism.is_exception_group) {
    return null;
  }

  const parentException = allExceptions.find(
    exc => exc.mechanism?.exception_id === mechanism.parent_id
  );
  const exception = allExceptions.find(
    exc => exc.mechanism?.exception_id === mechanism.exception_id
  );
  const childExceptions = allExceptions.filter(
    exc => exc.mechanism?.parent_id === mechanism.exception_id
  );

  if (newestFirst) {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/crashContent/exception/relatedExceptions.tsx" line="87">

---

# Exception Display

The Exception data is used to populate various parts of the UI, providing developers with valuable insights into the nature of the error.

```tsx
function ExceptionTreeItem({
  exception,
  level,
  firstChild,
  link = true,
  onExceptionClick,
}: ExceptionTreeItemProps) {
  return (
    <TreeItem level={level} data-test-id="exception-tree-item">
      {level > 0 && <TreeChildLine firstChild={firstChild} />}
      <Circle />
      <ExceptionLink
        exception={exception}
        link={link}
        onExceptionClick={onExceptionClick}
      />
    </TreeItem>
  );
}
```

---

</SwmSnippet>

# Exception Handling Functions

Let's explore the main functions related to Exception handling in Sentry.

<SwmSnippet path="/static/app/components/events/interfaces/crashContent/exception/relatedExceptions.tsx" line="38">

---

## getExceptionName Function

The `getExceptionName` function is used to get the name of an exception. It checks if the exception type is defined, and if so, it returns the exception value. If the exception value is not defined, it returns 'Exception'.

```tsx
function getExceptionName(exception: ExceptionValue) {
  if (exception.type) {
    return exception.value ? `${exception.type}: ${exception.value}` : exception.type;
  }

  return exception.value ?? t('Exception');
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/crashContent/exception/relatedExceptions.tsx" line="62">

---

## toggleException Function

The `toggleException` function is used to toggle the visibility of an exception. It takes an exceptionId as a parameter and toggles the visibility of the exception with that id in the collapsedExceptions state.

```tsx
        setTimeout(() => {
          const linkedElement = document.getElementById(`exception-${exceptionId}`);
          linkedElement?.scrollIntoView?.({behavior: 'smooth'});
        }, 0);
      }}
    >
      {exceptionName}
    </Button>
  );
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/crashContent/exception/relatedExceptions.tsx" line="72">

---

## expandException Function

The `expandException` function is used to expand an exception. It takes an exceptionId as a parameter and sets the visibility of the parent exception group of the exception with that id to false in the collapsedExceptions state.

```tsx

function TreeChildLine({firstChild}: {firstChild?: boolean}) {
  return (
    <TreeChildLineSvg
      viewBox="0 0 10 24"
      stroke="currentColor"
      width="10px"
      height="24px"
    >
      <line x1="0" y1={firstChild ? 10 : 0} x2="0" y2="24" />
      <line x1="0" y1="24" x2="10" y2="24" />
    </TreeChildLineSvg>
  );
}
```

---

</SwmSnippet>

# Exception Endpoints

Endpoints related to Exception handling

<SwmSnippet path="/static/app/components/events/interfaces/crashContent/exception/rawContent.tsx" line="59">

---

## Apple Crash Report Endpoint

This endpoint is used to fetch the Apple crash report for a specific event. The endpoint URL is constructed using the organization slug, project slug, and event ID. The type of the report (original or minified) is also specified as a query parameter.

```tsx
  getAppleCrashReportEndpoint(organization: Organization) {
    const {type, projectSlug, eventId} = this.props;

    const minified = type === 'minified';
    return `/projects/${organization.slug}/${projectSlug}/events/${eventId}/apple-crash-report?minified=${minified}`;
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/crashContent/exception/useSourceMapDebug.tsx" line="74">

---

## Source Map Debug Endpoint

This endpoint is used to fetch the source map debug information for a specific event. The endpoint URL is constructed using the organization slug, project slug, and event ID. Additional query parameters are used to specify the frame index and exception index.

```tsx
const sourceMapDebugQuery = ({
  orgSlug,
  projectSlug,
  eventId,
  frameIdx,
  exceptionIdx,
}: UseSourceMapDebugProps): ApiQueryKey => [
  `/projects/${orgSlug}/${projectSlug}/events/${eventId}/source-map-debug/`,
  {
    query: {
      frame_idx: `${frameIdx}`,
      exception_idx: `${exceptionIdx}`,
    },
  },
];
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
