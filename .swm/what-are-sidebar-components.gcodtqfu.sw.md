---
title: What are Sidebar Components
---
The Sidebar in the Components directory of the sentry-demo repository refers to a set of React components that collectively build the sidebar interface of the application. It includes various elements such as navigation items, panels, badges, and tooltips. The sidebar is designed to be responsive and its appearance changes based on the application's state and the user's actions.

The SidebarItem component, for instance, represents an individual item in the sidebar. It can be active or inactive, and it can contain an icon, a label, and optional badges. The component's appearance and behavior are determined by various properties, such as whether it's nested, whether it's in a floating accordion, and whether it's a main item.

The SidebarPanel component is another key part of the sidebar. It represents a panel that can be displayed when a sidebar item is clicked. The panel can contain a title and a body, and it can be hidden by clicking outside of it. The panel's position and size are determined by various properties, such as whether the sidebar is collapsed and the orientation of the panel.

The sidebar also includes various styled components, such as SidebarItemWrapper, SidebarItemIcon, and SidebarItemLabel, which are used to style the sidebar items. These components use styled-components, a library that allows you to write CSS in your JavaScript, to define their styles.

<SwmSnippet path="/static/app/components/sidebar/sidebarItem.tsx" line="122">

---

# SidebarItem Component

The SidebarItem component represents an individual item in the sidebar. It can be active or inactive, and it can contain an icon, a label, and optional badges. The component's appearance and behavior are determined by various properties, such as whether it's nested, whether it's in a floating accordion, and whether it's a main item.

```tsx
function SidebarItem({
  id,
  href,
  to,
  search,
  icon,
  label,
  badge,
  active,
  exact,
  hasPanel,
  isNew,
  isBeta,
  isAlpha,
  collapsed,
  className,
  orientation,
  isNewSeenKeySuffix,
  onClick,
  trailingItems,
  variant,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/sidebar/sidebarPanel.tsx" line="63">

---

# SidebarPanel Component

The SidebarPanel component represents a panel that can be displayed when a sidebar item is clicked. The panel can contain a title and a body, and it can be hidden by clicking outside of it. The panel's position and size are determined by various properties, such as whether the sidebar is collapsed and the orientation of the panel.

```tsx
function SidebarPanel({
  orientation,
  collapsed,
  hidePanel,
  title,
  children,
  ...props
}: Props): React.ReactElement {
  const portalEl = useRef<HTMLDivElement>(getSidebarPortal());

  const panelCloseHandler = useCallback(
    (evt: MouseEvent) => {
      if (!(evt.target instanceof Element)) {
        return;
      }

      if (portalEl.current.contains(evt.target)) {
        return;
      }

      // If we are in Sandbox, don't hide panel when the modal is clicked (before the email is added)
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/sidebar/sidebarItem.tsx" line="359">

---

# Styled Components

The sidebar includes various styled components, such as SidebarItemWrapper, SidebarItemIcon, and SidebarItemLabel, which are used to style the sidebar items. These components use styled-components, a library that allows you to write CSS in your JavaScript, to define their styles.

```tsx
const StyledSidebarItem = styled(Link, {
  shouldForwardProp: p => typeof p === 'string' && isPropValid(p),
})`
  display: flex;
  color: ${p => (p.isInFloatingAccordion ? p.theme.gray400 : 'inherit')};
  position: relative;
  cursor: pointer;
  font-size: 15px;
  height: ${p => (p.isInFloatingAccordion ? '35px' : '30px')};
  flex-shrink: 0;
  border-radius: ${p => p.theme.borderRadius};
  transition: none;

  &:before {
    display: block;
    content: '';
    position: absolute;
    top: 4px;
    left: calc(-${space(2)} - 1px);
    bottom: 6px;
    width: 5px;
```

---

</SwmSnippet>

# Sidebar Functionality

This section will cover the main functions related to the sidebar functionality of the sentry-demo application.

<SwmSnippet path="/static/app/components/sidebar/sidebarItem.tsx" line="122">

---

## SidebarItem

The SidebarItem function represents an individual item in the sidebar. It takes a set of properties that determine its appearance and behavior, such as whether it's active, whether it's nested, and whether it's in a floating accordion. The function uses these properties to render the appropriate elements and apply the appropriate styles.

```tsx
function SidebarItem({
  id,
  href,
  to,
  search,
  icon,
  label,
  badge,
  active,
  exact,
  hasPanel,
  isNew,
  isBeta,
  isAlpha,
  collapsed,
  className,
  orientation,
  isNewSeenKeySuffix,
  onClick,
  trailingItems,
  variant,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/sidebar/sidebarPanel.tsx" line="63">

---

## SidebarPanel

The SidebarPanel function represents a panel that can be displayed when a sidebar item is clicked. The panel can contain a title and a body, and it can be hidden by clicking outside of it. The function uses a set of properties to determine the panel's position and size, such as whether the sidebar is collapsed and the orientation of the panel.

```tsx
function SidebarPanel({
  orientation,
  collapsed,
  hidePanel,
  title,
  children,
  ...props
}: Props): React.ReactElement {
  const portalEl = useRef<HTMLDivElement>(getSidebarPortal());

  const panelCloseHandler = useCallback(
    (evt: MouseEvent) => {
      if (!(evt.target instanceof Element)) {
        return;
      }

      if (portalEl.current.contains(evt.target)) {
        return;
      }

      // If we are in Sandbox, don't hide panel when the modal is clicked (before the email is added)
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/sidebar/sidebarAccordion.tsx" line="12">

---

## SidebarAccordion

The SidebarAccordion function represents a collapsible section of the sidebar. It can contain multiple sidebar items, and it can be expanded or collapsed by the user. The function uses a set of properties to determine its appearance and behavior, such as whether it's initially expanded.

```tsx
import {Button} from 'sentry/components/button';
import {Chevron} from 'sentry/components/chevron';
import {Overlay} from 'sentry/components/overlay';
import {ExpandedContext} from 'sentry/components/sidebar/expandedContextProvider';
import {t} from 'sentry/locale';
import {space} from 'sentry/styles/space';
import {useLocalStorageState} from 'sentry/utils/useLocalStorageState';
import useMedia from 'sentry/utils/useMedia';
import useOnClickOutside from 'sentry/utils/useOnClickOutside';
import useRouter from 'sentry/utils/useRouter';

import type {SidebarItemProps} from './sidebarItem';
import SidebarItem, {isItemActive} from './sidebarItem';

type SidebarAccordionProps = SidebarItemProps & {
  children?: React.ReactNode;
  initiallyExpanded?: boolean;
};

function SidebarAccordion({
  children,
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
