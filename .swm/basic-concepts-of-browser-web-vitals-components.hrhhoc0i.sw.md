---
title: Basic Concepts of Browser Web Vitals Components
---
Components in the Browser section of the sentry-demo repository refer to the building blocks of the web application's user interface. They are primarily written in TypeScript and styled with CSS. These components are used to structure and style the web application's Insights view, specifically the Browser Web Vitals section.

These components include styled div elements, such as LabelContainer, BrowserItem, and SupportedBrowsers, which are used to structure and style parts of the user interface. They also include constants like browserOptions, which is an array of objects representing different browser types.

The components are organized into different files and directories based on their functionality. For example, the charts directory contains components related to displaying charts, and the tables directory contains components for displaying tables.

In addition to these, there are also components like BrowserTypeSelector and WebVitalsDetailPanel that are more complex and contain logic for handling user interactions and displaying data.

<SwmSnippet path="/static/app/views/insights/browser/webVitals/components/webVitalsDetailPanel.tsx" line="160">

---

# WebVitalsDetailPanel Component

The `WebVitalsDetailPanel` component is used to display detailed information about a specific web vital. It provides insights on how improving the performance of a web vital can impact the overall performance score of the application.

```tsx
                "A number rating how impactful a performance improvement on this page would be to your application's [webVital] Performance Score.",
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/browser/webVitals/components/webVitalDescription.tsx" line="51">

---

# WebVitalDescription Component

The `WebVitalDescription` component is used to provide a detailed description of a specific web vital. It helps developers understand what the web vital measures and its importance.

```tsx
    'Largest Contentful Paint (LCP) measures the render time for the largest content to appear in the viewport. This may be in any form from the document object model (DOM), such as images, SVGs, or text blocks. It’s the largest pixel area in the viewport, thus most visually defining. LCP helps developers understand how long it takes to see the main content on the page.'
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/browser/webVitals/components/tables/pagePerformanceTable.tsx" line="181">

---

# PagePerformanceTable Component

The `PagePerformanceTable` component is used to display a table of page performance data. It provides a rating on how improving the performance of a page can impact the overall performance score of the application.

```tsx
                  "A number rating how impactful a performance improvement on this page would be to your application's overall Performance Score."
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/browser/webVitals/components/webVitalMeters.tsx" line="103">

---

# WebVitalMeters Component

The `WebVitalMeters` component is used to provide a link to a resource that explains how performance scores are calculated.

```tsx
                          {t('Find out how performance scores are calculated here.')}
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
