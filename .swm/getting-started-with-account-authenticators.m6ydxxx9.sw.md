---
title: Getting started with Account Authenticators
---
Account security in the Sentry demo application is primarily handled through the use of authenticators. These are defined in the 'accountSecurityDetails.tsx' and 'accountSecurityEnroll.tsx' files. Authenticators are used to verify the identity of a user, providing an additional layer of security beyond just username and password.

The 'Props' type in 'accountSecurityDetails.tsx' and 'accountSecurityWrapper.tsx' files defines the properties that are passed into the account security components. These properties include actions such as regenerating backup codes and deleting disabled accounts, which are crucial for maintaining account security.

The 'State' type in 'accountSecurityDetails.tsx' and 'accountSecurityWrapper.tsx' files represents the state of the account security components. This includes information about the authenticator and user emails, which are essential for managing account security.

The 'isEnrolled' constant is used to check if an authenticator is active for a user's account. If the authenticator is active, it means the user has set up an additional layer of security for their account.

The 'date' member in 'accountSecurityDetails.tsx' is used to display the date when a particular security event occurred. This can be useful for users to track their account activity and spot any unusual behavior.

The 'getTitle' method in 'accountSecurityEnroll.tsx' is used to set the title of the account security page. This helps users understand the purpose of the page.

<SwmSnippet path="/static/app/views/settings/account/accountSecurity/accountSecurityDetails.tsx" line="51">

---

# Authenticators

The 'State' type represents the state of the account security components. This includes information about the authenticator, which is essential for managing account security.

```tsx
type State = {
  authenticator: Authenticator | null;
} & DeprecatedAsyncView['state'];
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/account/accountSecurity/accountSecurityDetails.tsx" line="46">

---

# Account Security Properties

The 'Props' type defines the properties that are passed into the account security components. These properties include actions such as regenerating backup codes, which are crucial for maintaining account security.

```tsx
type Props = {
  deleteDisabled: boolean;
  onRegenerateBackupCodes: () => void;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/account/accountSecurity/accountSecurityEnroll.tsx" line="305">

---

# Account Security Actions

The 'handleSubmit' function handles the submission of the 2FA form. This is a crucial part of the account security process as it verifies the user's identity.

```tsx
  };

  handleSubmit: FormProps['onSubmit'] = data => {
    const id = this.state.authenticator?.id;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/account/accountSecurity/accountSecurityEnroll.tsx" line="62">

---

# Account Security Fields

The 'getFields' function retrieves additional form fields based on the 2FA method. This allows the form to adapt based on the chosen 2FA method, providing a flexible and user-friendly interface for account security.

```tsx
/**
 * Retrieve additional form fields (or modify ones) based on 2fa method
 */
const getFields = ({
  authenticator,
  hasSentCode,
  sendingCode,
  onSmsReset,
  onU2fTap,
}: GetFieldsOpts): null | FieldObject[] => {
  const {form} = authenticator;

  if (!form) {
    return null;
  }

  if (authenticator.id === 'totp') {
    return [
      () => (
        <CodeContainer key="qrcode">
          <StyledQRCode
```

---

</SwmSnippet>

# Account Security Endpoints

Account Security Endpoints

<SwmSnippet path="/static/app/views/settings/account/accountSecurity/accountSecurityEnroll.tsx" line="169">

---

## Authenticator Endpoint

The `authenticatorEndpoint` is used to get the URL for the user's authenticators. This endpoint is used to manage the user's authenticators.

```tsx
  get authenticatorEndpoint() {
    return `/users/me/authenticators/${this.props.params.authId}/`;
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/account/accountSecurity/accountSecurityEnroll.tsx" line="173">

---

## Enroll Endpoint

The `enrollEndpoint` is used to get the URL for enrolling a new authenticator. This endpoint is used when the user wants to add a new authenticator to their account.

```tsx
  get enrollEndpoint() {
    return `${this.authenticatorEndpoint}enroll/`;
  }
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
