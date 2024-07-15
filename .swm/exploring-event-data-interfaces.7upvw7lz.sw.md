---
title: Exploring Event Data Interfaces
---
Interfaces in the Events directory of the Sentry-demo repository refer to the various types of data that can be associated with an event. These interfaces are organized into different subdirectories such as 'request', 'frame', 'crons', 'spans', 'csp', 'threads', and 'uptime', each representing a different aspect of an event. For instance, the 'request' interface deals with HTTP request data associated with an event, while the 'frame' interface handles data related to individual frames in a stack trace. Each interface contains various TypeScript files (.tsx) that define the structure and functionality of that particular interface.

These interfaces are used to structure and categorize the data associated with an event, making it easier to process and analyze. They also provide a way to handle different types of data in a consistent manner, as each interface defines a standard set of operations that can be performed on the data it represents. This modular approach allows for greater flexibility and maintainability in the codebase.

<SwmSnippet path="/static/app/components/events/interfaces/keyValueList/index.tsx" line="16">

---

# Props Interface in KeyValueList

This is an example of an interface named 'Props' in the KeyValueList component. It defines properties such as 'data', 'longKeys', 'onClick', and 'shouldSort', which are used to handle key-value list data associated with an event.

```tsx
  data?: KeyValueListData;
  longKeys?: boolean;
  onClick?: () => void;
  shouldSort?: boolean;
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/frame/contextLine.tsx" line="9">

---

# Props Interface in ContextLine

This is another example of an interface named 'Props', this time in the ContextLine component. It defines properties such as 'isActive', 'line', 'children', and 'coverage', which are used to handle context line data in a frame of a stack trace.

```tsx
interface Props {
  isActive: boolean;
  line: [lineNo: number, content: string];
  children?: React.ReactNode;
  coverage?: Coverage | '';
}
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
