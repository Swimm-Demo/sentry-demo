---
title: Understanding Form Fields
---
Fields in the sentry-demo repository refer to the different types of input fields that can be used in forms. These fields are used to capture user input in various forms throughout the application. They are implemented as React components and are located in the 'forms/fields' directory.

Each field type has its own specific properties and behaviors. For example, the 'TableField' component represents a table where each row can be considered a field. It has properties like 'addButtonText' for customizing the text of the add button, and 'allowEmpty' to specify whether the table can have empty fields.

There are various types of fields available such as 'NumberField', 'TextField', 'SelectField', and 'FileField' among others. Each of these fields is used for capturing specific types of user input. For instance, 'NumberField' is used for numerical input, 'TextField' for textual input, 'SelectField' for selecting an option from a list, and 'FileField' for file uploads.

The 'name' property is common to all fields and is used to identify the field in the form data. The 'model' property is also common to all fields and represents the form model that the field belongs to.

The 'onChange' and 'onBlur' event handlers are used to handle user interactions with the fields. The 'onChange' handler is triggered when the field's value changes, while the 'onBlur' handler is triggered when the field loses focus.

<SwmSnippet path="/static/app/components/forms/fields/inputField.tsx" line="65">

---

# InputField Component

The `InputField` component is a base field that is generally not used within the Form itself. It takes a `field` prop which is a function that returns a React node. If no `field` prop is provided, it defaults to the `defaultField` function. The `hideControlState` prop can be used to hide the control state of the field.

```tsx
/**
 * InputField should be thought of as a "base" field, and generally not used
 * within the Form itself.
 */
function InputField({field = defaultField, hideControlState, ...props}: InputFieldProps) {
  return (
    <FormField {...props} hideControlState flexibleControlStateSize>
      {({children: _children, ...otherFieldProps}) =>
        field({...otherFieldProps, hideControlState})
      }
    </FormField>
  );
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/forms/fields/accessibility.spec.tsx" line="27">

---

# Field Accessibility

This file contains tests to ensure that all fields have appropriate aria attributes for accessibility. It also contains a list of fields that are still missing accessibility check tests.

```tsx
describe('Field accessibility', function () {
  it('has appropriate aria attributes on all fields', async function () {
    // TODO(epurkhiser): The following fields are sill missing accessibility
    // check tests:
    //
    // - ChoiceMapper
    // - ProjectMapperField
    // - SentryProjectSelectorField
    // - TableField
    // - DatePickerField
    // - DateTimeField
    // - FileField

    // TODO(epurkhiser): It would be really nice if we could enforce that every
    // field that exists in `components/forms/fields/*` has a proper
    // accessibility test here.

    const model = new FormModel();

    render(
      <Form model={model}>
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/forms/fields/selectField.tsx" line="136">

---

# SelectField Component

The `SelectField` component is a type of field that allows the user to select an option from a dropdown list. It has a `styles` prop that can be used to customize its appearance.

```tsx
                ),
              }}
              styles={{
                control: provided => ({
                  ...provided,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/forms/fields/fileField.tsx" line="55">

---

# FileField Component

The `FileField` component is a type of field that allows the user to select a file. It has a `name` prop that identifies the field in the form data.

```tsx
      }: {
        children: React.ReactNode;
        model: FormModel;
        name: string;
        onChange: (value, event?: React.FormEvent<HTMLInputElement>) => void;
      }) => {
        return (
          <InputGroup>
            <InputGroup.LeadingItems disablePointerEvents>
              <FileName hasFile={!!fileName}>
                {fileName || t('No file selected')}
              </FileName>
            </InputGroup.LeadingItems>
            <FileInput
              {...omit(fieldProps, 'value', 'onBlur', 'onKeyDown')}
              type="file"
              name={name}
              accept={accept?.join(', ')}
              onChange={e => handleFile(model, name, onChange, e)}
            />
            {!hideControlState && (
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/forms/fields/inputField.tsx" line="31">

---

# DefaultField Function

The `defaultField` function is used to create a default input field. It takes several props including `onChange`, `onBlur`, `onKeyDown`, `model`, `name`, and `hideControlState`. These props are used to handle user interactions with the field and to link the field to the form model.

```tsx
function defaultField({
  onChange,
  onBlur,
  onKeyDown,
  model,
  name,
  hideControlState,
  ...rest
}: {
  model: FormModel;
  name: string;
  onBlur: OnEvent;
  onChange: OnEvent;
  onKeyDown: OnEvent;
  hideControlState?: boolean;
}) {
  return (
    <InputGroup>
      <InputGroup.Input
        onBlur={e => onBlur(e.target.value, e)}
        onKeyDown={e => onKeyDown((e.target as any).value, e)}
```

---

</SwmSnippet>

# Field Types

This section provides an overview of the main field types used in forms in the application.

<SwmSnippet path="/static/app/components/forms/fields/tableField.tsx" line="41">

---

## TableField

The 'TableField' component represents a table where each row can be considered a field. It has properties like 'addButtonText' for customizing the text of the add button, and 'allowEmpty' to specify whether the table can have empty fields. The 'saveChanges' function is used to save the changes made to the table.

```tsx
export default class TableField extends Component<InputFieldProps> {
  static defaultProps = DEFAULT_PROPS;

  hasValue = value => defined(value) && !isEmptyObject(value);

  renderField = (props: RenderProps) => {
    const {
      onChange,
      onBlur,
      addButtonText,
      columnLabels,
      columnKeys,
      disabled: rawDisabled,
      allowEmpty,
      confirmDeleteMessage,
    } = props;

    const mappedKeys = columnKeys || [];
    const emptyValue = mappedKeys.reduce((a, v) => ({...a, [v]: null}), {id: ''});

    const valueIsEmpty = this.hasValue(props.value);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/forms/fields/selectField.tsx" line="68">

---

## SelectField

The 'SelectField' component represents a dropdown select field. It has properties like 'choices' for specifying the options in the dropdown, and 'disabled' to specify whether the field is disabled. The 'isArray' function is used to check if the provided value is an array.

```tsx
> {
  static defaultProps = {
    allowClear: false,
    allowEmpty: false,
    placeholder: '--',
    escapeMarkup: true,
    multiple: false,
    small: false,
    formatMessageValue: (value, props) =>
      (getChoices(props).find(choice => choice[0] === value) || [null, value])[1],
  };

  handleChange = (
    onBlur: InputFieldProps['onBlur'],
    onChange: InputFieldProps['onChange'],
    optionObj: ValueType<OptionType, boolean>
  ) => {
    let value: any = undefined;

    // If optionObj is empty, then it probably means that the field was "cleared"
    if (!optionObj) {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/forms/fields/inputField.tsx" line="69">

---

## InputField

The 'InputField' component represents a basic input field. It has properties like 'field' for specifying the field type, and 'hideControlState' to specify whether the control state should be hidden. The 'defaultField' function is used to render the default field.

```tsx
function InputField({field = defaultField, hideControlState, ...props}: InputFieldProps) {
  return (
    <FormField {...props} hideControlState flexibleControlStateSize>
      {({children: _children, ...otherFieldProps}) =>
        field({...otherFieldProps, hideControlState})
      }
    </FormField>
  );
}
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
