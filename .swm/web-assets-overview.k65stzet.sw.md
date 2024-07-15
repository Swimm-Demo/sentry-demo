---
title: Web Assets Overview
---
Web Assets in Sentry-Demo refer to the static files that are used in the application. These include images, stylesheets, and JavaScript files. They are crucial for the visual aspects and functionality of the application.

The assets are used in various parts of the application. For instance, in the 'integrations.tsx' file, there is a member called 'assets' which is an array of URLs. These URLs likely point to various static files that are used in the application.

In the 'webVitalDescription.tsx' file, there are constants that map to descriptions of various web vitals. These vitals are performance metrics that are crucial for understanding the loading performance of the web assets.

The 'settings.ts' file contains a constant called 'BASE_URL' which is set to 'browser/assets'. This suggests that there is a dedicated route in the application for serving web assets.

In the 'utils.ts' file, there is a function called 'getContext' which is used to get the rendering context of a canvas. This is likely used for rendering graphical web assets.

<SwmSnippet path="/static/app/types/integrations.tsx" line="460">

---

# Usage of Web Assets

In the 'integrations.tsx' file, there is a member called 'assets' which is an array of URLs. These URLs likely point to various static files that are used in the application.

```tsx
  assets: Array<{url: string}>;
  canDisable: boolean;
  // TODO(ts)
  contexts: any[];
  doc: string;
  featureDescriptions: IntegrationFeature[];
  features: string[];
  hasConfiguration: boolean;
  id: string;
  isDeprecated: boolean;
  isHidden: boolean;
  isTestable: boolean;
  metadata: any;
  name: string;
  shortName: string;
  slug: string;
  status: string;
  type: string;
  altIsSentryApp?: boolean;
  author?: {name: string; url: string};
  deprecationDate?: string;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/browser/webVitals/components/webVitalDescription.tsx" line="30">

---

# Web Vitals and Web Assets

In the 'webVitalDescription.tsx' file, there are constants that map to descriptions of various web vitals. These vitals are performance metrics that are crucial for understanding the loading performance of the web assets.

```tsx
  webVital: WebVitals;
  score?: number;
  value?: string;
};

const WEB_VITAL_FULL_NAME_MAP = {
  cls: t('Cumulative Layout Shift'),
  fcp: t('First Contentful Paint'),
  inp: t('Interaction to Next Paint'),
  lcp: t('Largest Contentful Paint'),
  ttfb: t('Time to First Byte'),
};

const VITAL_DESCRIPTIONS: Partial<Record<WebVital, string>> = {
  [WebVital.FCP]: t(
    'First Contentful Paint (FCP) measures the amount of time the first content takes to render in the viewport. Like FP, this could also show up in any form from the document object model (DOM), such as images, SVGs, or text blocks.'
  ),
  [WebVital.CLS]: t(
    'Cumulative Layout Shift (CLS) is the sum of individual layout shift scores for every unexpected element shift during the rendering process. Imagine navigating to an article and trying to click a link before the page finishes loading. Before your cursor even gets there, the link may have shifted down due to an image rendering. Rather than using duration for this Web Vital, the CLS score represents the degree of disruptive and visually unstable shifts.'
  ),
  [WebVital.LCP]: t(
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/browser/resources/settings.ts" line="8">

---

# Serving of Web Assets

The 'settings.ts' file contains a constant called 'BASE_URL' which is set to 'browser/assets'. This suggests that there is a dedicated route in the application for serving web assets.

```typescript
export const BASE_URL = 'browser/assets'; // Name of the data shown (singular)
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/profiling/gl/utils.ts" line="283">

---

# Rendering of Web Assets

In the 'utils.ts' file, there is a function called 'getContext' which is used to get the rendering context of a canvas. This is likely used for rendering graphical web assets.

```typescript
export function getContext(
  canvas: HTMLCanvasElement,
  context: 'webgl'
): WebGLRenderingContext;
export function getContext(canvas: HTMLCanvasElement, context: string): RenderingContext {
  const ctx =
    context === 'webgl'
      ? canvas.getContext(context, {antialias: false})
      : canvas.getContext(context);
  if (!ctx) {
    throw new Error(`Could not get context ${context}`);
  }
  return ctx;
}
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
