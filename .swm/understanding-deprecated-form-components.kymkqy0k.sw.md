---
title: Understanding Deprecated Form Components
---
Deprecatedforms in the Components directory refers to a collection of form-related components that are no longer recommended for use in the codebase. These components are marked as deprecated, indicating that they may be removed in future updates and should be avoided in new development. The Deprecatedforms include various types of form fields such as InputField, BooleanField, TextField, and others. Each of these components has its own functionality and purpose. For instance, the InputField is a base class for creating form input fields, while the BooleanField is used for creating checkbox fields.

The Deprecatedforms also include a Form component, which is a class that handles form state and provides methods for form submission and field value changes. It uses the FormContext to provide form state and methods to its child components. The Form component is used in conjunction with the form field components to create complete forms.

Despite being deprecated, these components are still used in various parts of the codebase. However, it's recommended to use the newer form components for any new development. The deprecated forms and fields are kept for backward compatibility and will be removed once all instances of their usage are replaced with the newer components.

# SelectAsyncField Endpoint

SelectAsyncField Component and its Endpoint

<SwmSnippet path="/static/app/components/deprecatedforms/selectAsyncField.spec.tsx" line="5">

---

## SelectAsyncField Component

The SelectAsyncField component is a part of the Deprecatedforms. It is a form field that fetches its options asynchronously from a specified URL endpoint.

```tsx
import SelectAsyncField from 'sentry/components/deprecatedforms/selectAsyncField';
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/deprecatedforms/selectAsyncField.spec.tsx" line="21">

---

## Endpoint for SelectAsyncField

The endpoint for the SelectAsyncField component is defined in the defaultProps object. The 'url' property specifies the endpoint from which the component fetches its options.

```tsx
    url: '/foo/bar/',
    name: 'fieldName',
    label: 'Select me',
  };
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
