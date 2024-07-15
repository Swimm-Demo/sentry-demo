---
title: Basic Concepts of UI Components in Web Assets
---
Components in the sentry-demo repository refer to reusable pieces of code that are used to build the user interface of the application. They are organized in a hierarchical structure, where each component resides in a specific directory under the 'static/app/components' directory. Each component is a self-contained module that encapsulates the code and resources required for its functionality. For example, the 'charts' directory contains components related to rendering various types of charts, while the 'organizations' directory contains components specific to organization-related functionalities. Components can include TypeScript files (.tsx), which define the component's structure and behavior, and test files (.spec.tsx), which contain tests for the component.

<SwmSnippet path="/static/app/components/dropdownMenu/index.tsx" line="51">

---

# DropdownMenuProps Component

The `DropdownMenuProps` interface defines the properties that the DropdownMenu component expects. These properties control the appearance and behavior of the dropdown menu.

```tsx
interface DropdownMenuProps
  extends Omit<
      DropdownMenuListProps,
      'overlayState' | 'overlayPositionProps' | 'items' | 'children' | 'menuTitle'
    >,
    Pick<
      UseOverlayProps,
      | 'isOpen'
      | 'offset'
      | 'position'
      | 'isDismissable'
      | 'shouldCloseOnBlur'
      | 'shouldCloseOnInteractOutside'
      | 'onInteractOutside'
      | 'onOpenChange'
      | 'preventOverflowOptions'
      | 'flipOptions'
    > {
  /**
   * Items to display inside the dropdown menu. If the item has a `children`
   * prop, it will be rendered as a menu section. If it has a `children` prop
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/selectMembers/index.tsx" line="56">

---

# SelectMembers Component

The `SelectMembers` class is a component that allows you to select either members and/or teams. It maintains its own state and provides several methods for handling user interactions.

```tsx
class SelectMembers extends Component<Props, State> {
  state: State = {
    loading: false,
    inputValue: '',
    options: null,
    memberListLoading: MemberListStore.state.loading,
  };

  componentWillUnmount() {
    this.unlisteners.forEach(listener => {
      if (typeof listener === 'function') {
        listener();
      }
    });
  }

  unlisteners = [
    MemberListStore.listen(
      () => this.setState({memberListLoading: MemberListStore.state.loading}),
      undefined
    ),
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/modals/metricWidgetViewerModal/queries.tsx" line="467">

---

# DebouncedInput Function

The `DebouncedInput` function is a component that wraps an input field and debounces its onChange event. This is useful for inputs that trigger expensive operations such as API calls.

```tsx
// TODO: Move this to a shared component
function DebouncedInput({
  onChange,
  wait = DEFAULT_DEBOUNCE_DURATION,
  ...inputProps
}: InputProps & {wait?: number}) {
  const [value, setValue] = useState<string | number | readonly string[] | undefined>(
    inputProps.value
  );

  const handleChange = useMemo(
    () =>
      debounce((e: React.ChangeEvent<HTMLInputElement>) => {
        onChange?.(e);
      }, wait),
    [onChange, wait]
  );

  return (
    <Input
      {...inputProps}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/forms/fieldGroup/index.tsx" line="13">

---

# FieldGroup Function

The `FieldGroup` function is a component that renders a field, which includes a label, help text, and a form control. It is unconnected to any form state, meaning it does not automatically handle form submission or validation.

```tsx
/**
 * A component to render a Field (i.e. label + help + form "control"),
 * generally inside of a Panel.
 *
 * This is unconnected to any Form state
 */
function FieldGroup({
  className,
  disabled = false,
  inline = true,
  visible = true,
  ...rest
}: FieldGroupProps) {
  const props = {
    inline,
    disabled,
    visible,
    ...rest,
  };

  const {
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
