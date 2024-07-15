---
title: Overview of Relay Key Management
---
The Organization Relay in the Sentry application is a feature that allows the organization to manage their Relay keys. It is located under the Settings of the application. The Relay keys are used to authenticate and authorize requests from external Relays to the Sentry application.

The Relay keys are managed through a user interface in the Settings. This interface allows the user to add, edit, and delete Relay keys. The user interface is disabled if the organization does not have write access.

The Relay keys are stored in the organization object and are updated using the RelayWrapper component. The RelayWrapper component uses the useApiQuery hook to fetch the Relay usage data from the `/organizations/${orgSlug}/relay_usage/` endpoint.

The RelayWrapper component also provides functionality to open a modal for adding a new Relay key. This is done using the handleOpenAddDialog function which opens the Add modal and updates the Relay keys on successful submission.

The RelayWrapper component also provides functionality to delete a Relay key. This is done using the handleDeleteRelay function which sends a PUT request to the `/organizations/${orgSlug}/` endpoint with the updated list of Relay keys.

The RelayUsageList component is used to display the list of Relay keys and their usage. It uses the useApiQuery hook to fetch the Relay usage data from the `/organizations/${orgSlug}/relay_usage/` endpoint.

<SwmSnippet path="/static/app/views/settings/organizationRelay/relayWrapper.tsx" line="29">

---

# RelayWrapper Component

The RelayWrapper component is responsible for managing the Relay keys. It uses the useApiQuery hook to fetch the Relay usage data from the `/organizations/${orgSlug}/relay_usage/` endpoint. It also provides functionality to open a modal for adding a new Relay key and to delete a Relay key.

```tsx
export function RelayWrapper() {
  const organization = useOrganization();
  const api = useApi();
  const [relays, setRelays] = useState<Relay[]>(organization.trustedRelays);

  const disabled = !organization.access.includes('org:write');

  const handleOpenAddDialog = useCallback(() => {
    openModal(modalProps => (
      <Add
        {...modalProps}
        savedRelays={relays}
        api={api}
        orgSlug={organization.slug}
        onSubmitSuccess={response => {
          addSuccessMessage(t('Successfully added Relay public key'));
          setRelays(response.trustedRelays);
        }}
      />
    ));
  }, [relays, api, organization.slug]);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationRelay/relayWrapper.tsx" line="36">

---

# handleOpenAddDialog Function

The handleOpenAddDialog function is used to open the Add modal. This function is called when the user wants to add a new Relay key. On successful submission, the Relay keys are updated.

```tsx
  const handleOpenAddDialog = useCallback(() => {
    openModal(modalProps => (
      <Add
        {...modalProps}
        savedRelays={relays}
        api={api}
        orgSlug={organization.slug}
        onSubmitSuccess={response => {
          addSuccessMessage(t('Successfully added Relay public key'));
          setRelays(response.trustedRelays);
        }}
      />
    ));
  }, [relays, api, organization.slug]);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationRelay/relayWrapper.tsx" line="139">

---

# handleDeleteRelay Function

The handleDeleteRelay function is used to delete a Relay key. This function sends a PUT request to the `/organizations/${orgSlug}/` endpoint with the updated list of Relay keys.

```tsx
  const handleDeleteRelay = useCallback(
    async (publicKey: string) => {
      const trustedRelays = relays
        .filter(relay => relay.publicKey !== publicKey)
        .map(relay => omit(relay, ['created', 'lastModified']));

      try {
        const response = await api.requestPromise(`/organizations/${orgSlug}/`, {
          method: 'PUT',
          data: {trustedRelays},
        });
        addSuccessMessage(t('Successfully deleted Relay public key'));
        onRelaysChange(response.trustedRelays);
      } catch {
        addErrorMessage(t('An unknown error occurred while deleting Relay public key'));
      }
    },
    [relays, api, orgSlug, onRelaysChange]
  );
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationRelay/relayWrapper.tsx" line="92">

---

# RelayUsageList Component

The RelayUsageList component is used to display the list of Relay keys and their usage. It uses the useApiQuery hook to fetch the Relay usage data from the `/organizations/${orgSlug}/relay_usage/` endpoint.

```tsx
function RelayUsageList({
  relays,
  orgSlug,
  disabled,
  api,
  onRelaysChange,
}: {
  api: ReturnType<typeof useApi>;
  disabled: boolean;
  onRelaysChange: (relays: Relay[]) => void;
  orgSlug: Organization['slug'];
  relays: Relay[];
}) {
  const {isLoading, isError, refetch, data} = useApiQuery<RelayActivity[]>(
    [`/organizations/${orgSlug}/relay_usage/`],
    {
      staleTime: 0,
      retry: false,
      enabled: relays.length > 0,
    }
  );
```

---

</SwmSnippet>

# Organization Relay Functions

The Organization Relay in Sentry is a feature that allows the organization to manage their Relay keys. It is located under the Settings of the application. The Relay keys are used to authenticate and authorize requests from external Relays to the Sentry application.

<SwmSnippet path="/static/app/views/settings/organizationRelay/relayWrapper.tsx" line="29">

---

## RelayWrapper

The RelayWrapper component is responsible for managing the state of the Relay keys in the organization. It uses the useApi hook to make API requests and the useState hook to manage the state of the Relay keys. It also provides functionality to open a modal for adding a new Relay key and to delete a Relay key.

```tsx
export function RelayWrapper() {
  const organization = useOrganization();
  const api = useApi();
  const [relays, setRelays] = useState<Relay[]>(organization.trustedRelays);

  const disabled = !organization.access.includes('org:write');

  const handleOpenAddDialog = useCallback(() => {
    openModal(modalProps => (
      <Add
        {...modalProps}
        savedRelays={relays}
        api={api}
        orgSlug={organization.slug}
        onSubmitSuccess={response => {
          addSuccessMessage(t('Successfully added Relay public key'));
          setRelays(response.trustedRelays);
        }}
      />
    ));
  }, [relays, api, organization.slug]);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationRelay/list/index.tsx" line="20">

---

## RelayUsageList

The RelayUsageList component is used to display the list of Relay keys and their usage. It uses the useApiQuery hook to fetch the Relay usage data from the `/organizations/${orgSlug}/relay_usage/` endpoint. It also provides functionality to open a modal for editing a Relay key and to delete a Relay key.

```tsx
function List({relays, relayActivities, onRefresh, onDelete, onEdit, disabled}: Props) {
  const orderedRelays = orderBy(relays, relay => relay.created, ['desc']);

  const relaysByPublicKey = getRelaysByPublicKey(orderedRelays, relayActivities);

  const renderCardContent = (activities: Array<RelayActivity>) => {
    if (!activities.length) {
      return <WaitingActivity onRefresh={onRefresh} disabled={disabled} />;
    }

    return <ActivityList activities={activities} />;
  };

  return (
    <div>
      {Object.keys(relaysByPublicKey).map(relayByPublicKey => {
        const {name, description, created, activities} =
          relaysByPublicKey[relayByPublicKey];
        return (
          <div key={relayByPublicKey}>
            <CardHeader
```

---

</SwmSnippet>

# Organization Relay Endpoints

Organization Relay Endpoints

<SwmSnippet path="/static/app/views/settings/organizationRelay/modals/modalManager.tsx" line="139">

---

## /organizations/${orgSlug}/ Endpoint

This endpoint is used to update the trusted Relays of an organization. It is a PUT request that requires the updated list of trusted Relays as data.

```tsx
      const response = await api.requestPromise(`/organizations/${orgSlug}/`, {
        method: 'PUT',
        data: {trustedRelays},
      });
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationRelay/relayWrapper.tsx" line="106">

---

## /organizations/${orgSlug}/relay_usage/ Endpoint

This endpoint is used to fetch the Relay usage data for an organization. It is a GET request that returns a list of Relay activities.

```tsx
    [`/organizations/${orgSlug}/relay_usage/`],
    {
      staleTime: 0,
      retry: false,
      enabled: relays.length > 0,
    }
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
