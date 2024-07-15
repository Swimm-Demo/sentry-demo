---
title: Exploring the Trace Details Drawer
---
The Trace Drawer in the New Trace Details section is a component that provides a detailed view of a trace. It is a part of the performance monitoring feature of Sentry. The drawer can be resized and positioned in different layouts such as bottom, left, or right. It contains various styled components like tabs, buttons, and indicators. The drawer's content is dynamic and depends on the trace data fetched from the server.

The Trace Drawer uses a set of properties defined in the TraceDrawerProps type. These properties include the manager, metaResults, replayRecord, rootEventResults, scheduler, trace, traceEventView, traceGridRef, traceType, and traces. These properties provide the necessary data and functionality for the Trace Drawer to operate.

The Trace Drawer also includes a set of styled components defined using the styled-components library. These components include the ResizeableHandle, PanelWrapper, SmallerChevronIcon, TabsHeightContainer, TabsLayout, TabsContainer, TabActions, TabSeparator, TabLayoutControlItem, Tab, TabButtonIndicator, TabButton, Content, TabIconButton, ContentWrapper, PinButton, StyledIconPin, and others. These components are used to build the visual structure of the Trace Drawer.

The Trace Drawer uses a state management system to handle its internal state. This state includes the current layout, whether the drawer is minimized, the current tab, and other preferences. The state is managed using the useTraceState and useTraceStateDispatch hooks.

The Trace Drawer also includes a set of event handlers for user interactions. These handlers include functions for clicking on tabs, minimizing the drawer, scrolling to a node, and others. These handlers are used to update the state of the Trace Drawer and trigger necessary side effects.

<SwmSnippet path="/static/app/views/performance/newTraceDetails/traceDrawer/traceDrawer.tsx" line="60">

---

# TraceDrawerProps

The Trace Drawer uses a set of properties defined in the TraceDrawerProps type. These properties include the manager, metaResults, replayRecord, rootEventResults, scheduler, trace, traceEventView, traceGridRef, traceType, and traces. These properties provide the necessary data and functionality for the Trace Drawer to operate.

```tsx
type TraceDrawerProps = {
  manager: VirtualizedViewManager;
  metaResults: TraceMetaQueryResults;
  onScrollToNode: (node: TraceTreeNode<TraceTree.NodeValue>) => void;
  onTabScrollToNode: (node: TraceTreeNode<TraceTree.NodeValue>) => void;
  replayRecord: ReplayRecord | null;
  rootEventResults: UseApiQueryResult<EventTransaction, RequestError>;
  scheduler: TraceScheduler;
  trace: TraceTree;
  traceEventView: EventView;
  traceGridRef: HTMLElement | null;
  traceType: TraceType;
  traces: TraceSplitResults<TraceFullDetailed> | null;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/newTraceDetails/traceDrawer/traceDrawer.tsx" line="618">

---

# Styled Components

The Trace Drawer also includes a set of styled components defined using the styled-components library. These components include the ResizeableHandle, PanelWrapper, SmallerChevronIcon, TabsHeightContainer, TabsLayout, TabsContainer, TabActions, TabSeparator, TabLayoutControlItem, Tab, TabButtonIndicator, TabButton, Content, TabIconButton, ContentWrapper, PinButton, StyledIconPin, and others. These components are used to build the visual structure of the Trace Drawer.

```tsx
const ResizeableHandle = styled('div')<{
  layout: 'drawer bottom' | 'drawer left' | 'drawer right';
}>`
  width: ${p => (p.layout === 'drawer bottom' ? '100%' : '12px')};
  height: ${p => (p.layout === 'drawer bottom' ? '12px' : '100%')};
  cursor: ${p => (p.layout === 'drawer bottom' ? 'ns-resize' : 'ew-resize')};
  position: absolute;
  top: ${p => (p.layout === 'drawer bottom' ? '-6px' : 0)};
  left: ${p =>
    p.layout === 'drawer bottom' ? 0 : p.layout === 'drawer right' ? '-6px' : 'initial'};
  right: ${p => (p.layout === 'drawer left' ? '-6px' : 0)};

  z-index: 1;
`;

const PanelWrapper = styled('div')<{
  layout: 'drawer bottom' | 'drawer left' | 'drawer right';
}>`
  grid-area: drawer;
  display: flex;
  flex-direction: column;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/newTraceDetails/traceDrawer/traceDrawer.tsx" line="79">

---

# State Management

The Trace Drawer uses a state management system to handle its internal state. This state includes the current layout, whether the drawer is minimized, the current tab, and other preferences. The state is managed using the useTraceState and useTraceStateDispatch hooks.

```tsx
  const traceState = useTraceState();
  const traceDispatch = useTraceStateDispatch();
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/performance/newTraceDetails/traceDrawer/traceDrawer.tsx" line="248">

---

# Event Handlers

The Trace Drawer also includes a set of event handlers for user interactions. These handlers include functions for clicking on tabs, minimizing the drawer, scrolling to a node, and others. These handlers are used to update the state of the Trace Drawer and trigger necessary side effects.

```tsx
  const onMinimizeClick = useCallback(() => {
    traceAnalytics.trackDrawerMinimize(organization);
    traceDispatch({
      type: 'minimize drawer',
      payload: !traceState.preferences.drawer.minimized,
    });
    if (!traceState.preferences.drawer.minimized) {
      onResize(0, 0, true, true);
      size.current = drawerOptions.min;
    } else {
      if (drawerOptions.initialSize === 0) {
        const userPreference =
          traceStateRef.current.preferences.drawer.sizes[
            traceStateRef.current.preferences.layout
          ];

        const {width, height} = props.traceGridRef?.getBoundingClientRect() ?? {
          width: 0,
          height: 0,
        };
        const containerSize =
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
