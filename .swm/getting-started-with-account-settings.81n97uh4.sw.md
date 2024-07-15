---
title: Getting started with Account Settings
---
The 'Account' in the Settings of Sentry-demo refers to the user's account settings. It provides various functionalities for users to manage their account details, security settings, and notifications. The account settings layout is rendered using the 'AccountSettingsLayout' class, which fetches and displays the organization details associated with the account.

The 'AccountSettingsNavigation' function is used to navigate through different sections of the account settings. It uses the 'getConfiguration' function to get the navigation objects for the settings, which include 'Account Details', 'Security', 'Notifications', and 'Email Addresses'.

The 'AccountIdentities' function in 'accountIdentities.tsx' file is used to manage the identities associated with the account. It provides functionalities to disconnect an identity, and sort identities based on their categories and names.

<SwmSnippet path="/static/app/views/settings/account/accountDetails.tsx" line="40">

---

# Account Details

The 'AccountDetails' function is used to fetch and display the user's account details. It uses the 'useApiQuery' function to fetch the user's data from the 'USER_ENDPOINT'. The user's data is then displayed using the 'JsonForm' component.

```tsx
function AccountDetails() {
  const organization = useOrganization({allowNull: true});
  const queryClient = useQueryClient();
  const {
    data: user,
    isLoading,
    isError,
    refetch,
  } = useApiQuery<User>(USER_ENDPOINT_QUERY_KEY, {staleTime: 0});

  if (isLoading) {
    return (
      <Fragment>
        <SettingsPageHeader title={t('Account Details')} />
        <LoadingIndicator />
      </Fragment>
    );
  }

  if (isError) {
    return <LoadingError onRetry={refetch} />;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/account/accountAuthorizations.tsx" line="33">

---

# Account Authorizations

The 'AccountAuthorizations' class is used to manage the authorizations of the user's account. It fetches the authorizations data from the '/api-authorizations/' endpoint and provides a method to revoke an authorization.

```tsx
class AccountAuthorizations extends DeprecatedAsyncView<Props, State> {
  getEndpoints(): ReturnType<DeprecatedAsyncView['getEndpoints']> {
    return [['data', '/api-authorizations/']];
  }

  getTitle() {
    return 'Approved Applications';
  }

  handleRevoke = authorization => {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/account/accountClose.tsx" line="56">

---

# Account Close

The 'AccountClose' function is used to handle the closing of the user's account. It fetches the organizations associated with the user's account and provides a method to remove the account and its associated organizations.

```tsx
function AccountClose() {
  const api = useApi();

  const [organizations, setOrganizations] = useState<OwnedOrg[]>([]);
  const [orgsToRemove, setOrgsToRemove] = useState<Set<string>>(new Set());
  const [isLoading, setIsLoading] = useState(true);

  // Load organizations from all regions.
  useEffect(() => {
    setIsLoading(true);
    fetchOrganizations(api, {owner: 1}).then((response: OwnedOrg[]) => {
      const singleOwnerOrgs = response
        .filter(item => item.singleOwner)
        .map(item => item.organization.slug);

      setOrgsToRemove(new Set(singleOwnerOrgs));
      setOrganizations(response);
      setIsLoading(false);
    });
  }, [api]);

```

---

</SwmSnippet>

# Account Settings Endpoints

Account Settings in Sentry-demo

<SwmSnippet path="/static/app/views/settings/account/accountSecurity/accountSecurityWrapper.tsx" line="11">

---

## /users/me/authenticators/ Endpoint

The '/users/me/authenticators/' endpoint is used to manage the authenticators of the current user. It is used in the 'AccountSecurityWrapper' component to fetch the list of authenticators, disable an authenticator, and regenerate backup codes.

```tsx
const ENDPOINT = '/users/me/authenticators/';

type Props = {
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/account/accountEmails.tsx" line="31">

---

## /users/me/emails/ Endpoint

The '/users/me/emails/' endpoint is used to manage the emails of the current user. It is used in the 'AccountEmails' component to fetch the list of emails, add a new email, and remove an existing email.

```tsx

function AccountEmails() {
  const handleSubmitSuccess: FormProps['onSubmitSuccess'] = (_change, model, id) => {
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
