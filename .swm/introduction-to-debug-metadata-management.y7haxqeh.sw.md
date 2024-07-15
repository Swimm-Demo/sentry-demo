---
title: Introduction to Debug Metadata Management
---
Debug Meta in the Interfaces directory refers to a set of components and utilities that handle the display and management of debug metadata associated with events in Sentry. This metadata includes information about debug images, their status, and details about image candidates. The Debug Meta components are used to filter, sort, and display this data in a user-friendly format.

The main component, DebugMetaWithRouter, is a React component that manages the state and behavior of the debug metadata interface. It subscribes to the DebugMetaStore, which holds the current filter and search term, and updates its state accordingly. It also provides methods for filtering and searching images, handling changes in filter and search term, and opening and closing the image details modal.

The DebugImageDetails component is used to display detailed information about a specific debug image. It fetches additional debug files from the server and combines them with the existing candidates from the image. The information is then sorted and displayed in a modal.

The utils.tsx file provides utility functions used across the Debug Meta components. These include functions for getting the status weight of an image, combining statuses, getting the file name from a path, normalizing an ID, and determining whether a section should be skipped.

<SwmSnippet path="/static/app/components/events/interfaces/debugMeta/index.tsx" line="73">

---

# DebugMetaWithRouter Component

DebugMetaWithRouter is the main component for managing and displaying debug metadata. It maintains a state that includes the current search term, filter selections, and filtered images. It also provides methods for handling changes in filter and search term, filtering images, and opening and closing the image details modal.

```tsx
class DebugMetaWithRouter extends PureComponent<Props, State> {
  static defaultProps: DefaultProps = {
    data: {images: []},
  };

  state: State = {
    searchTerm: '',
    scrollbarWidth: 0,
    isOpen: false,
    filterOptions: [],
    filterSelections: [],
    filteredImages: [],
    filteredImagesByFilter: [],
    filteredImagesBySearch: [],
  };

  componentDidMount() {
    this.unsubscribeFromDebugMetaStore = DebugMetaStore.listen(
      this.onDebugMetaStoreChange,
      undefined
    );
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/debugMeta/debugImageDetails/index.tsx" line="1">

---

# DebugImageDetails Component

DebugImageDetails is a component used to display detailed information about a specific debug image. It fetches additional debug files from the server and combines them with the existing candidates from the image. The information is then sorted and displayed in a modal.

```tsx
import {Fragment} from 'react';
import {css} from '@emotion/react';
import styled from '@emotion/styled';
import partition from 'lodash/partition';
import sortBy from 'lodash/sortBy';

import {addErrorMessage} from 'sentry/actionCreators/indicator';
import type {ModalRenderProps} from 'sentry/actionCreators/modal';
import {Button, LinkButton} from 'sentry/components/button';
import ButtonBar from 'sentry/components/buttonBar';
import LoadingError from 'sentry/components/loadingError';
import {t} from 'sentry/locale';
import {space} from 'sentry/styles/space';
import type {DebugFile} from 'sentry/types/debugFiles';
import {DebugFileFeature} from 'sentry/types/debugFiles';
import type {Image, ImageCandidate, ImageStatus} from 'sentry/types/debugImage';
import {CandidateDownloadStatus} from 'sentry/types/debugImage';
import type {Event} from 'sentry/types/event';
import type {Organization} from 'sentry/types/organization';
import type {Project} from 'sentry/types/project';
import {displayReprocessEventAction} from 'sentry/utils/displayReprocessEventAction';
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/debugMeta/debugImageDetails/utils.tsx" line="1">

---

# Utility Functions

The utils.tsx file provides utility functions used across the Debug Meta components. These include functions for getting the status weight of an image, combining statuses, getting the file name from a path, normalizing an ID, and determining whether a section should be skipped.

```tsx
export const INTERNAL_SOURCE = 'sentry:project';
export const INTERNAL_SOURCE_LOCATION = 'sentry://project_debug_file/';

```

---

</SwmSnippet>

# Debug Meta Endpoints

Debug Meta Endpoints

<SwmSnippet path="/static/app/components/events/interfaces/debugMeta/debugImageDetails/reprocessAlert.tsx" line="42">

---

## Reprocess Endpoint

This code snippet shows the usage of the `/projects/${orgSlug}/${projSlug}/events/${eventId}/reprocessable/` endpoint. This endpoint is used to check if an event is reprocessable. The response from this endpoint is used to update the state of the `ReprocessableEvent`.

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
