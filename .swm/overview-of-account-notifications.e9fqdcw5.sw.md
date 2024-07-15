---
title: Overview of Account Notifications
---
Notifications in the Account section of the Sentry-Demo application refer to the system's way of alerting users about specific events or updates. These notifications can be sent via email or through an integration.

The notification settings are managed in the 'notificationSettings.tsx' file. Here, users can customize their notification preferences according to their needs. The settings include options for different types of notifications, such as quota warnings, transaction notifications, and error notifications.

The 'notificationSettingsByType.tsx' file handles the different types of notifications that a user can receive. It maps the types to their respective settings, allowing for a more organized and efficient handling of notifications.

The 'notificationSettingsByEntity.tsx' file manages the notification settings for different entities. This allows users to have different notification preferences for different parts of the application.

The 'isLoading' constant in the 'notificationSettings.tsx' file is used to handle the loading state of the notification settings. This ensures that the user interface remains responsive and informative while the settings are being loaded.

<SwmSnippet path="/static/app/views/settings/account/notifications/notificationSettings.tsx" line="35">

---

# Notification Settings

This is where the notification settings are managed. Users can customize their notification preferences according to their needs.

```tsx
function NotificationSettings({organizations}: NotificationSettingsProps) {
  const checkFeatureFlag = (flag: string) => {
    return organizations.some(org => org.features?.includes(flag));
  };
  const notificationFields = NOTIFICATION_SETTINGS_TYPES.filter(type => {
    const notificationFlag = NOTIFICATION_FEATURE_MAP[type];
    if (Array.isArray(notificationFlag)) {
      return notificationFlag.some(flag => checkFeatureFlag(flag));
    }
    if (notificationFlag) {
      return checkFeatureFlag(notificationFlag);
    }
    return true;
  });

  const renderOneSetting = (type: string) => {
    // TODO(isabella): Once GA, remove this
    const field = NOTIFICATION_SETTING_FIELDS[type];
    if (type === 'quota' && checkFeatureFlag('spend-visibility-notifications')) {
      field.label = t('Spend');
      field.help = t('Notifications that help avoid surprise invoices.');
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/account/notifications/notificationSettingsByType.tsx" line="34">

---

# Notification Types

This file handles the different types of notifications that a user can receive. It maps the types to their respective settings, allowing for a more organized and efficient handling of notifications.

```tsx
import {isGroupedByProject} from './utils';

type Props = {
  notificationType: string; // TODO(steve)? type better
  organizations: Organization[];
} & DeprecatedAsyncComponent['props'];

type State = {
  defaultSettings: DefaultSettings | null;
  identities: Identity[];
  notificationOptions: NotificationOptionsObject[];
  notificationProviders: NotificationProvidersObject[];
  organizationIntegrations: OrganizationIntegration[];
} & DeprecatedAsyncComponent['state'];

const typeMappedChildren = {
  quota: [
    'quotaErrors',
    'quotaTransactions',
    'quotaAttachments',
    'quotaReplays',
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/account/notifications/notificationSettingsByEntity.tsx" line="33">

---

# Notification Entities

This file manages the notification settings for different entities. This allows users to have different notification preferences for different parts of the application.

```tsx
  handleEditNotificationOption: (notificationOption: NotificationOptionsObject) => void;
  handleRemoveNotificationOption: (id: string) => void;
  notificationOptions: NotificationOptionsObject[];
  notificationType: string;
  organizations: Organization[];
}

function NotificationSettingsByEntity({
  entityType,
  handleAddNotificationOption,
  handleEditNotificationOption,
  handleRemoveNotificationOption,
  notificationOptions,
  notificationType,
  organizations,
}: NotificationSettingsByEntityProps) {
  const router = useRouter();
  const [selectedEntityId, setSelectedEntityId] = useState<string | null>(null);
  const [selectedValue, setSelectedValue] = useState<Value | null>(null);

  const customerDomain = ConfigStore.get('customerDomain');
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/account/notifications/notificationSettings.tsx" line="81">

---

# Loading State

The 'isLoading' constant is used to handle the loading state of the notification settings. This ensures that the user interface remains responsive and informative while the settings are being loaded.

```tsx
  // use 0 as stale time because we change the values elsewhere
  const {
    data: initialLegacyData,
    isLoading,
    isError,
    isSuccess,
    refetch,
  } = useApiQuery<{[key: string]: string}>(['/users/me/notifications/'], {
    staleTime: 0,
  });

  return (
    <Fragment>
      <SentryDocumentTitle title={t('Notifications')} />
      <SettingsPageHeader title={t('Notifications')} />
      <TextBlock>
        {t('Personal notifications sent by email or an integration.')}
      </TextBlock>
      {isError && <LoadingError onRetry={refetch} />}
      <PanelNoBottomMargin>
        <PanelHeader>{t('Notification')}</PanelHeader>
```

---

</SwmSnippet>

# Notification Functions

This section will cover the main functions related to notifications in the Sentry-Demo application.

<SwmSnippet path="/static/app/views/settings/account/notifications/notificationSettingsByEntity.tsx" line="31">

---

## Notification Options

The 'NotificationSettingsByEntityProps' interface defines the properties for the 'NotificationSettingsByEntity' function. This includes the 'handleAddNotificationOption', 'handleEditNotificationOption', and 'handleRemoveNotificationOption' functions, which are used to manage notification options.

```tsx
    notificationOption: Omit<NotificationOptionsObject, 'id'>
  ) => void;
  handleEditNotificationOption: (notificationOption: NotificationOptionsObject) => void;
  handleRemoveNotificationOption: (id: string) => void;
  notificationOptions: NotificationOptionsObject[];
  notificationType: string;
  organizations: Organization[];
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/account/notifications/notificationSettingsByEntity.tsx" line="104">

---

## Adding Notification Options

The 'handleAddNotificationOption' function is used to add a new notification option. It takes a 'data' object as a parameter, which includes the type, scopeType, scopeIdentifier, and value of the new notification option.

```tsx
    const data = {
      type: notificationType,
      scopeType: entityType,
      scopeIdentifier: selectedEntityId,
      value: selectedValue,
    };
    setSelectedEntityId(null);
    setSelectedValue(null);
    handleAddNotificationOption(data);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/account/notifications/notificationSettingsByEntity.tsx" line="381">

---

## Editing Notification Options

The 'handleEditNotificationOption' function is used to edit an existing notification option. It takes a 'data' object as a parameter, which includes the id, type, scopeType, scopeIdentifier, and value of the notification option to be edited.

```tsx

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/account/notifications/notificationSettingsByEntity.tsx" line="345">

---

## Removing Notification Options

The 'handleRemoveNotificationOption' function is used to remove an existing notification option. It takes an 'id' as a parameter, which is the id of the notification option to be removed.

```tsx

```

---

</SwmSnippet>

# Notification Endpoints

Notification Settings Management

<SwmSnippet path="/static/app/views/settings/account/notifications/notificationSettingsByType.tsx" line="85">

---

## getEndpoints

The `getEndpoints` function is used to define the endpoints for fetching the notification settings. It uses the `notificationType` prop to determine the type of notifications to fetch.

```tsx
  getEndpoints(): ReturnType<DeprecatedAsyncComponent['getEndpoints']> {
    const {notificationType} = this.props;
    return [
      [
        'notificationOptions',
        `/users/me/notification-options/`,
        {query: getQueryParams(notificationType)},
      ],
      [
        'notificationProviders',
        `/users/me/notification-providers/`,
        {query: getQueryParams(notificationType)},
      ],
      ['identities', `/users/me/identities/`, {query: {provider: 'slack'}}],
      [
        'organizationIntegrations',
        `/users/me/organization-integrations/`,
        {query: {provider: 'slack'}},
      ],
      ['defaultSettings', '/notification-defaults/'],
    ];
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/account/notifications/notificationSettingsByType.tsx" line="354">

---

## handleAddNotificationOption

The `handleAddNotificationOption` function is used to add a new notification option. It makes an API request to add the new option and updates the state with the new option.

```tsx
  handleAddNotificationOption = async (data: Omit<NotificationOptionsObject, 'id'>) => {
    // TODO: add error handling
    const notificationOption = await this.api.requestPromise(
      '/users/me/notification-options/',
      {
        method: 'PUT',
        data,
      }
    );

    this.setState(state => {
      return {
        notificationOptions: [...state.notificationOptions, notificationOption],
      };
    });
  };
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
