---
title: Getting started with Crash Details
---
Crash content in the Sentry demo repository refers to the detailed information about an error or exception that occurred in the application. It is part of the event interfaces and is used to provide developers with a comprehensive view of the error, including the stack trace, exception details, and other relevant data.

The Crash Content is primarily handled in the 'CrashContent' function in the 'crashContent/index.tsx' file. This function checks if an exception or a stacktrace is present in the event data. Depending on the type of data available, it either renders the 'ExceptionContent' or the 'StackTraceContent'.

The 'ExceptionContent' and 'StackTraceContent' components are responsible for rendering the detailed view of the exception or stack trace respectively. They are located in the 'crashContent/exception' and 'crashContent/stackTrace' directories.

The 'RawContent' component in the 'crashContent/exception/rawContent.tsx' file is responsible for fetching and displaying the raw crash report for native exceptions. It uses the 'fetchAppleCrashReport' method to fetch the crash report from the server.

The 'fetchAppleCrashReport' method uses the 'requestPromise' function from the 'api.tsx' file to make an API request to the server. It updates the component's state with the fetched crash report or any errors that occurred during the fetch.

<SwmSnippet path="/static/app/components/events/interfaces/crashContent/index.tsx" line="22">

---

# CrashContent Function

The 'CrashContent' function checks if an exception or a stacktrace is present in the event data. Depending on the type of data available, it either renders the 'ExceptionContent' or the 'StackTraceContent'.

```tsx
export function CrashContent({
  event,
  stackView,
  stackType,
  newestFirst,
  projectSlug,
  groupingCurrentLevel,
  hasHierarchicalGrouping,
  exception,
  stacktrace,
}: Props) {
  if (exception) {
    return (
      <ExceptionContent
        stackType={stackType}
        stackView={stackView}
        projectSlug={projectSlug}
        newestFirst={newestFirst}
        event={event}
        values={exception.values}
        groupingCurrentLevel={groupingCurrentLevel}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/crashContent/exception/content.tsx" line="1">

---

# ExceptionContent and StackTraceContent Components

The 'ExceptionContent' component is responsible for rendering the detailed view of the exception. It is located in the 'crashContent/exception' directory.

```tsx
import {useState} from 'react';
import styled from '@emotion/styled';

import {Button} from 'sentry/components/button';
import ErrorBoundary from 'sentry/components/errorBoundary';
import {StacktraceBanners} from 'sentry/components/events/interfaces/crashContent/exception/banners/stacktraceBanners';
import {
  prepareSourceMapDebuggerFrameInformation,
  useSourceMapDebuggerData,
} from 'sentry/components/events/interfaces/crashContent/exception/useSourceMapDebuggerData';
import {renderLinksInText} from 'sentry/components/events/interfaces/crashContent/exception/utils';
import {getStacktracePlatform} from 'sentry/components/events/interfaces/utils';
import {AnnotatedText} from 'sentry/components/events/meta/annotatedText';
import {Tooltip} from 'sentry/components/tooltip';
import {tct, tn} from 'sentry/locale';
import {space} from 'sentry/styles/space';
import type {ExceptionType, Project} from 'sentry/types';
import type {Event, ExceptionValue} from 'sentry/types/event';
import {StackType} from 'sentry/types/stacktrace';
import {defined} from 'sentry/utils';

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/crashContent/stackTrace/content.tsx" line="1">

---

The 'StackTraceContent' component is responsible for rendering the detailed view of the stack trace. It is located in the 'crashContent/stackTrace' directory.

```tsx
import {cloneElement, Fragment, useState} from 'react';
import styled from '@emotion/styled';

import GuideAnchor from 'sentry/components/assistant/guideAnchor';
import type {FrameSourceMapDebuggerData} from 'sentry/components/events/interfaces/sourceMapsDebuggerModal';
import Panel from 'sentry/components/panels/panel';
import {t} from 'sentry/locale';
import type {Frame, Organization, PlatformKey} from 'sentry/types';
import type {Event} from 'sentry/types/event';
import type {StackTraceMechanism, StacktraceType} from 'sentry/types/stacktrace';
import {defined} from 'sentry/utils';
import withOrganization from 'sentry/utils/withOrganization';

import type {DeprecatedLineProps} from '../../frame/deprecatedLine';
import DeprecatedLine from '../../frame/deprecatedLine';
import {
  findImageForAddress,
  getHiddenFrameIndices,
  getLastFrameIndex,
  isRepeatedFrame,
  parseAddress,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/crashContent/exception/rawContent.tsx" line="25">

---

# RawContent Component and fetchAppleCrashReport Method

The 'RawContent' component is responsible for fetching and displaying the raw crash report for native exceptions. It uses the 'fetchAppleCrashReport' method to fetch the crash report from the server.

```tsx
} & Pick<ExceptionType, 'values'>;

type State = {
  crashReport: string;
  error: boolean;
  loading: boolean;
};

class RawContent extends Component<Props, State> {
  state: State = {
    loading: false,
    error: false,
    crashReport: '',
  };

  componentDidMount() {
    if (this.isNative()) {
      this.fetchAppleCrashReport();
    }
  }

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/api.tsx" line="656">

---

The 'fetchAppleCrashReport' method uses the 'requestPromise' function from the 'api.tsx' file to make an API request to the server. It updates the component's state with the fetched crash report or any errors that occurred during the fetch.

```tsx
  requestPromise<IncludeAllArgsType extends boolean>(
    path: string,
    {
      includeAllArgs,
      ...options
    }: {includeAllArgs?: IncludeAllArgsType} & Readonly<RequestOptions> = {}
  ): Promise<IncludeAllArgsType extends true ? ApiResult : any> {
    // Create an error object here before we make any async calls so that we
    // have a helpful stack trace if it errors
    //
    // This *should* get logged to Sentry only if the promise rejection is not handled
    // (since SDK captures unhandled rejections). Ideally we explicitly ignore rejection
    // or handle with a user friendly error message
    const preservedError = new Error('API Request Error');

    return new Promise((resolve, reject) =>
      this.request(path, {
        ...options,
        preservedError,
        success: (data, textStatus, resp) => {
          if (includeAllArgs) {
```

---

</SwmSnippet>

# Crash Content Endpoints

Understanding Crash Content Endpoints

<SwmSnippet path="/static/app/components/events/interfaces/crashContent/exception/rawContent.tsx" line="59">

---

## Apple Crash Report Endpoint

The `getAppleCrashReportEndpoint` function constructs the endpoint URL for fetching an Apple crash report. The URL includes the organization slug, project slug, and event ID. The type of the report (original or minified) is also included as a query parameter.

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

The `sourceMapDebugQuery` function constructs the endpoint URL for fetching source map debug information. The URL includes the organization slug, project slug, and event ID. The frame index and exception index are also included as query parameters.

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
