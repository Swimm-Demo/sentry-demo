---
title: What are Data Scrubbing Modals
---
Modals in Data Scrubbing are used to manage the creation and editing of data scrubbing rules. They are implemented as React components and are responsible for rendering the user interface and handling user interactions.

The `Modal` component in `modal.tsx` is a generic modal component that accepts props such as `title`, `onSave`, `content`, and `disabled`. It renders the modal's header, body, and footer, and handles the 'Save' and 'Cancel' actions.

The `ModalManager` component in `modalManager.tsx` is a higher-level component that manages the state and behavior of the modal. It handles form validation, loading of source suggestions, and saving of new rules.

The `Add` and `Edit` components in `add.tsx` and `edit.tsx` respectively, use the `ModalManager` to implement the specific functionality for adding and editing data scrubbing rules. They define the modal's title and the behavior for getting new rules.

<SwmSnippet path="/static/app/views/settings/components/dataScrubbing/modals/modal.tsx" line="15">

---

# Modal Component

The `Modal` component is a generic modal component that accepts props such as `title`, `onSave`, `content`, and `disabled`. It renders the modal's header, body, and footer, and handles the 'Save' and 'Cancel' actions.

```tsx
function Modal({
  title,
  onSave,
  content,
  disabled,
  Header,
  Body,
  Footer,
  closeModal,
}: Props) {
  return (
    <Fragment>
      <Header closeButton>
        <h5>{title}</h5>
      </Header>
      <Body>{content}</Body>
      <Footer>
        <ButtonBar gap={1.5}>
          <Button onClick={closeModal}>{t('Cancel')}</Button>
          <Button onClick={onSave} disabled={disabled} priority="primary">
            {t('Save Rule')}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/components/dataScrubbing/modals/modalManager.tsx" line="48">

---

# ModalManager Component

The `ModalManager` component is a higher-level component that manages the state and behavior of the modal. It handles form validation, loading of source suggestions, and saving of new rules.

```tsx
class ModalManager extends Component<Props, State> {
  state = this.getDefaultState();

  componentDidMount() {
    this.handleValidateForm();
  }

  componentDidUpdate(_prevProps: Props, prevState: State) {
    if (!isEqual(prevState.values, this.state.values)) {
      this.handleValidateForm();
    }

    if (prevState.eventId.value !== this.state.eventId.value) {
      this.loadSourceSuggestions();
    }
    if (prevState.eventId.status !== this.state.eventId.status) {
      saveToSourceGroupData(this.state.eventId, this.state.sourceSuggestions);
    }
  }

  getDefaultState(): Readonly<State> {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/components/dataScrubbing/modals/add.tsx" line="5">

---

# Add and Edit Components

The `Add` component uses the `ModalManager` to implement the specific functionality for adding data scrubbing rules. It defines the modal's title and the behavior for getting new rules.

```tsx
import ModalManager from './modalManager';

type ModalManagerProps = ModalManager['props'];
type Props = Omit<ModalManagerProps, 'title' | 'initialValues' | 'onGetNewRules'>;

function Add({savedRules, ...props}: Props) {
  const handleGetNewRules = (
    values: Parameters<ModalManagerProps['onGetNewRules']>[0]
  ) => {
    return [...savedRules, {...values, id: savedRules.length}] as Array<Rule>;
  };

  return (
    <ModalManager
      {...props}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/components/dataScrubbing/modals/edit.tsx" line="5">

---

Similarly, the `Edit` component uses the `ModalManager` to implement the specific functionality for editing data scrubbing rules. It also defines the modal's title and the behavior for getting new rules.

```tsx
import ModalManager from './modalManager';

type ModalManagerProps = ModalManager['props'];
type Props = Omit<ModalManagerProps, 'title' | 'initialValues' | 'onGetNewRules'> & {
  rule: Rule;
};

function Edit({savedRules, rule, ...props}: Props) {
  const handleGetNewRules = (
    values: Parameters<ModalManagerProps['onGetNewRules']>[0]
  ) => {
    const updatedRule = {...values, id: rule.id};

    const newRules = savedRules.map(savedRule => {
      if (savedRule.id === updatedRule.id) {
        return updatedRule;
      }
      return savedRule;
    }) as Array<Rule>;

    return newRules;
```

---

</SwmSnippet>

# Modal Functions

This section will cover the main functions related to modals in the Sentry application.

<SwmSnippet path="/static/app/views/settings/components/dataScrubbing/modals/modal.tsx" line="15">

---

## Modal

The `Modal` function is a React component that renders a modal dialog. It accepts props such as `title`, `onSave`, `content`, and `disabled` to customize the modal's appearance and behavior.

```tsx
function Modal({
  title,
  onSave,
  content,
  disabled,
  Header,
  Body,
  Footer,
  closeModal,
}: Props) {
  return (
    <Fragment>
      <Header closeButton>
        <h5>{title}</h5>
      </Header>
      <Body>{content}</Body>
      <Footer>
        <ButtonBar gap={1.5}>
          <Button onClick={closeModal}>{t('Cancel')}</Button>
          <Button onClick={onSave} disabled={disabled} priority="primary">
            {t('Save Rule')}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/components/dataScrubbing/modals/modalManager.tsx" line="48">

---

## ModalManager

The `ModalManager` class is a higher-level component that manages the state and behavior of the modal. It handles form validation, loading of source suggestions, and saving of new rules.

```tsx
class ModalManager extends Component<Props, State> {
  state = this.getDefaultState();

  componentDidMount() {
    this.handleValidateForm();
  }

  componentDidUpdate(_prevProps: Props, prevState: State) {
    if (!isEqual(prevState.values, this.state.values)) {
      this.handleValidateForm();
    }

    if (prevState.eventId.value !== this.state.eventId.value) {
      this.loadSourceSuggestions();
    }
    if (prevState.eventId.status !== this.state.eventId.status) {
      saveToSourceGroupData(this.state.eventId, this.state.sourceSuggestions);
    }
  }

  getDefaultState(): Readonly<State> {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/components/dataScrubbing/modals/add.tsx" line="10">

---

## Add

The `Add` function is a React component that uses the `ModalManager` to implement the specific functionality for adding data scrubbing rules. It defines the modal's title and the behavior for getting new rules.

```tsx
function Add({savedRules, ...props}: Props) {
  const handleGetNewRules = (
    values: Parameters<ModalManagerProps['onGetNewRules']>[0]
  ) => {
    return [...savedRules, {...values, id: savedRules.length}] as Array<Rule>;
  };

  return (
    <ModalManager
      {...props}
      savedRules={savedRules}
      title={t('Add an advanced data scrubbing rule')}
      onGetNewRules={handleGetNewRules}
    />
  );
}

export default Add;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/components/dataScrubbing/modals/edit.tsx" line="12">

---

## Edit

The `Edit` function is a React component that uses the `ModalManager` to implement the specific functionality for editing data scrubbing rules. It defines the modal's title and the behavior for getting new rules.

```tsx
function Edit({savedRules, rule, ...props}: Props) {
  const handleGetNewRules = (
    values: Parameters<ModalManagerProps['onGetNewRules']>[0]
  ) => {
    const updatedRule = {...values, id: rule.id};

    const newRules = savedRules.map(savedRule => {
      if (savedRule.id === updatedRule.id) {
        return updatedRule;
      }
      return savedRule;
    }) as Array<Rule>;

    return newRules;
  };

  return (
    <ModalManager
      {...props}
      savedRules={savedRules}
      title={t('Edit an advanced data scrubbing rule')}
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
