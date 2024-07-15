---
title: Basic concepts of Form Components
---
Forms in the Sentry-demo repository refer to a set of components that are used to collect user input for further processing. They are primarily used to control user interaction, data entry, and data validation.

The Form components are built using the FormModel class, which is a MobX-based model that manages the form's state. It provides methods for setting initial data, form options, and resetting the form. It also has computed properties to check if the form has changed or if it's currently saving.

The Form component uses the FormModel to manage its state. It creates a new instance of FormModel if none is provided, sets the initial data and form options, and provides a method to reset the form when it's unmounted.

The FormPanel component is a visual wrapper for form fields. It can be collapsible and its state is managed using React's useState and useCallback hooks. It also sanitizes the title to be used as a query selector.

The FormField components are used to create individual form fields. They are created based on their field configuration and can be disabled. The fields are rendered based on their type.

The FormContext is a React context that provides the FormModel instance and the saveOnBlur option to its children. This allows form fields to interact with the form's state.

<SwmSnippet path="/static/app/components/forms/model.tsx" line="81">

---

# FormModel

FormModel is a class that manages the state of a form. It provides methods for setting initial data, form options, and resetting the form. It also has computed properties to check if the form has changed or if it's currently saving.

```tsx
class FormModel {
  /**
   * Map of field name -> value
   */
  fields: ObservableMap<string, FieldValue> = observable.map();

  /**
   * Errors for individual fields
   * Note we don't keep error in `this.fieldState` so that we can easily
   * See if the form is in an "error" state with the `isError` getter
   */
  errors = new Map();

  /**
   * State of individual fields
   *
   * Map of field name -> object
   */
  fieldState = new Map();

  /**
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/forms/form.tsx" line="83">

---

# Form

The Form component uses the FormModel to manage its state. It creates a new instance of FormModel if none is provided, sets the initial data and form options, and provides a method to reset the form when it's unmounted.

```tsx
function Form({
  'data-test-id': dataTestId,
  allowUndo,
  apiEndpoint,
  apiMethod,
  cancelLabel,
  children,
  className,
  extraButton,
  footerClass,
  footerStyle,
  hideFooter,
  initialData,
  model,
  onCancel,
  onFieldChange,
  onPreSubmit,
  onSubmit,
  onSubmitError,
  onSubmitSuccess,
  preventFormResetOnUnmount,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/forms/jsonForm.tsx" line="120">

---

# FormPanel

The FormPanel component is a visual wrapper for form fields. It can be collapsible and its state is managed using React's useState and useCallback hooks. It also sanitizes the title to be used as a query selector.

```tsx
    initiallyCollapsed?: boolean;
    title?: React.ReactNode;
  }) {
    const shouldDisplayForm = this.shouldDisplayForm(fields);

    if (
      !shouldDisplayForm &&
      !formPanelProps?.renderFooter &&
      !formPanelProps?.renderHeader
    ) {
      return null;
    }

    return (
      <FormPanel
        title={title}
        fields={fields}
        {...formPanelProps}
        initiallyCollapsed={initiallyCollapsed ?? formPanelProps.initiallyCollapsed}
      />
    );
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/forms/formField/index.tsx" line="98">

---

# FormField

The FormField components are used to create individual form fields. They are created based on their field configuration and can be disabled. The fields are rendered based on their type.

```tsx
// XXX(epurkhiser): Many of these props are duplicated in form types. The forms
// interfaces need some serious consolidation

interface BaseProps {
  /**
   * Used to render the actual control
   */
  children: (renderProps) => React.ReactNode;
  /**
   * Name of the field
   */
  name: string;
  // TODO(ts): These are actually props that are needed for some lower
  // component. We should let the rendering component pass these in instead
  defaultValue?: FieldValue;
  formatMessageValue?: boolean | Function;
  /**
   * Transform data when saving on blur.
   */
  getData?: (value: any) => any;
  /**
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/forms/formContext.tsx" line="8">

---

# FormContext

The FormContext is a React context that provides the FormModel instance and the saveOnBlur option to its children. This allows form fields to interact with the form's state.

```tsx
 * These differ from the 'old' forms in that they use mobx observers
 * to update state and expose it via the `FormModel`
 */
export type FormContextData = {
  /**
   * The default value is undefined so that FormField components
   * not within a form context boundary create MockModels based
   * on their props.
   */
  form?: FormModel;
  /**
```

---

</SwmSnippet>

# Form Components Overview

Form Components and their Interactions

<SwmSnippet path="/static/app/components/forms/apiForm.tsx" line="1">

---

## ApiForm Component

The ApiForm component is a form that interacts with an API endpoint. It uses the `useApi` hook to get an instance of the API client, and defines a `handleSubmit` function that makes a request to the specified `apiEndpoint` using the specified `apiMethod`. The form data is passed to the API request, and loading indicators are shown while the request is in progress.

```tsx
import {useCallback} from 'react';

import {addLoadingMessage, clearIndicators} from 'sentry/actionCreators/indicator';
import type {RequestOptions} from 'sentry/api';
import type {FormProps} from 'sentry/components/forms/form';
import Form from 'sentry/components/forms/form';
import {t} from 'sentry/locale';
import useApi from 'sentry/utils/useApi';

type Props = FormProps & {
  apiEndpoint: string;
  apiMethod: string;
  hostOverride?: string;
  onSubmit?: (data: Record<string, any>) => any | void;
};

/**
 * @deprecated
 *
 * DO NOT USE THIS. Prefer using `Form` instead. Form already supports API
 * requests, this is quite old and should be removed
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/forms/controls/selectAsyncControl.tsx" line="14">

---

## SelectAsyncControl Component

The SelectAsyncControl component is a select control that fetches its options from an API endpoint. It uses the `Client` class to make API requests, and stores the results in its state. The `doQuery` function is used to make a request to the specified `url` and update the component's state with the results. The `handleLoadOptions` function is used to load the options when the component is rendered.

```tsx
export type Result = {
  label: string;
  value: string;
};

export interface SelectAsyncControlProps {
  forwardedRef: React.Ref<ReactSelect<GeneralSelectValue>>;
  // TODO(ts): Improve data type
  onQuery: (query: string | undefined) => {};
  onResults: (data: any) => Result[];
  url: string;
  value: ControlProps['value'];
  defaultOptions?: boolean | GeneralSelectValue[];
}

type State = {
  query?: string;
};

/**
 * Performs an API request to `url` to fetch the options
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
