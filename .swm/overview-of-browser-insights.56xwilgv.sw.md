---
title: Overview of Browser Insights
---
In the Insights section of the sentry-demo project, 'Browser' refers to a set of functionalities and components that provide insights into web vitals and resources related to different types of browsers. It includes various utilities, components, and views that help in analyzing and visualizing the performance of web applications on different browsers.

The 'Browser' functionality is primarily used to filter and sort resources, and to provide a detailed overview of web vitals. It includes components for charts, tables, and selectors, and utilities for sorting, decoding query parameters, and calculating performance scores.

The 'Browser' functionality also includes an enumerator called 'BrowserType' which is used to specify the type of browser. This enumerator is used in various queries and components to filter and sort data based on the type of browser.

<SwmSnippet path="/static/app/views/insights/browser/webVitals/utils/queryParameterDecoders/browserType.tsx" line="5">

---

# BrowserType Enumerator

The 'BrowserType' enumerator is used to specify the type of browser. It includes options for different browsers like Chrome, Safari, Firefox, etc.

```tsx
export enum BrowserType {
  ALL = '',
  CHROME = 'Chrome',
  SAFARI = 'Safari',
  FIREFOX = 'Firefox',
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/browser/webVitals/components/browserTypeSelector.tsx" line="30">

---

# Browser Options

The 'browserOptions' constant is an array of objects, each representing a different browser type. It is used in the 'BrowserTypeSelector' component to provide options for filtering.

```tsx
const browserOptions = [
  {
    value: BrowserType.CHROME,
    label: optionToLabel('chrome', 'Chrome'),
    textValue: 'Chrome',
  },
  {
    value: BrowserType.SAFARI,
    label: optionToLabel('safari', 'Safari'),
    textValue: 'Safari',
  },
  {
    value: BrowserType.FIREFOX,
    label: optionToLabel('firefox', 'Firefox'),
    textValue: 'Firefox',
  },
  {value: BrowserType.OPERA, label: optionToLabel('opera', 'Opera'), textValue: 'Opera'},
  {value: BrowserType.EDGE, label: optionToLabel('edge', 'Edge'), textValue: 'Edge'},
  {
    value: BrowserType.CHROME_MOBILE,
    label: optionToLabel('chrome', 'Chrome Mobile'),
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/browser/webVitals/components/browserTypeSelector.tsx" line="75">

---

# BrowserTypeSelector Component

The 'BrowserTypeSelector' component uses the 'browserOptions' to provide a dropdown menu for selecting the type of browser. The selected options are then used to filter the data.

```tsx
export default function BrowserTypeSelector() {
  const organization = useOrganization();
  const location = useLocation();

  const value = decodeList(location.query[SpanIndexedField.BROWSER_NAME]);

  return (
    <CompactSelect
      triggerProps={{prefix: t('Browser Type')}}
      multiple
      clearable
      value={value}
      triggerLabel={value.length === 0 ? 'All' : undefined}
      menuTitle={'Filter Browsers'}
      options={browserOptions ?? []}
      onChange={(selectedOptions: SelectOption<string>[]) => {
        trackAnalytics('insight.vital.select_browser_value', {
          organization,
          browsers: selectedOptions.map(v => v.value),
        });

```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
