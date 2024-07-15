---
title: Understanding the Compact Select Component
---
Compact Select in the Components directory is a flexible select component with a customizable trigger button. It is designed to handle both single and multiple selection modes. The component is built using TypeScript and leverages React's context API for state management. It provides a series of TypeScript function overloads to properly parse prop types across two dimensions: option value types (number vs string), and selection mode (singular vs multiple).

The Compact Select component is highly configurable, allowing developers to customize its behavior and appearance. It accepts a variety of props, including options for the select component, default values, onChange handlers, and more. It also provides a mechanism to handle disabled options and limit the number of options displayed at a time.

The component uses several utility functions to manage its state and handle user interactions. For example, the `getItemsWithKeys` function is used to assign unique keys to each option, and the `domId` function is used to generate unique DOM IDs for the select trigger. The `toggleOptions` function is used to toggle the selection of all provided options.

The Compact Select component is composed of several sub-components, including `Control`, `List`, and `CompositeSelect`. The `Control` component manages the open state of the select component and provides the context to all children. The `List` component renders a list of selectable options, and the `CompositeSelect` component allows for the creation of composite selectors, where each region functions as a separated, self-contained selectable list.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
