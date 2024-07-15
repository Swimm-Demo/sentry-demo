---
title: Exploring Mobile Insights
---
Mobile in Insights refers to the functionality and components that provide mobile-specific insights in the Sentry application. It includes various UI components, data queries, and constants that are used to handle and display mobile-specific data.

The 'MobileCursors' enumerator in 'static/app/views/insights/mobile/screenload/constants.ts' is a part of this functionality. It defines constants for different types of cursors used in the mobile insights view.

The 'MobileSortKeys' enumerator in the same file is another part of this functionality. It defines constants for different types of sort keys used in the mobile insights view.

The 'static/app/views/insights/mobile/ui' directory contains various UI components and views used in the mobile insights view. This includes 'referrers.tsx' and 'settings.ts' files.

The 'static/app/views/insights/mobile/screenload/data' directory contains setup content for the mobile screen load data.

<SwmSnippet path="/static/app/views/insights/mobile/screenload/constants.ts" line="4">

---

# MobileCursors Enumerator

The 'MobileCursors' enumerator defines constants for different types of cursors used in the mobile insights view. These cursors are used to navigate through the data in the mobile insights view.

```typescript
export enum MobileCursors {
  SPANS_TABLE = 'spansCursor',
  SCREENS_TABLE = 'screensCursor',
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/mobile/ui/settings.ts" line="3">

---

# Mobile UI Settings

The 'settings.ts' file in the 'mobile/ui' directory contains constants for the module title and base URL of the mobile insights view. These constants are used to configure the UI of the mobile insights view.

```typescript
export const MODULE_TITLE = t('Mobile UI');
export const BASE_URL = 'mobile/ui';
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
