---
title: Exploring the Admin Interface
---
Admin in the views directory refers to the administrative interface of the Sentry application. It provides a set of views for managing various aspects of the system such as users, organizations, and projects.

The Admin interface is structured into different sections, each represented by a TypeScript file. For instance, 'adminUsers.tsx' handles the display and management of users, while 'adminOrganizations.tsx' is responsible for organization-related operations.

The 'adminLayout.tsx' file serves as the main layout for the admin interface. It uses the 'renderAdminNavigation' function to generate the navigation menu, which includes links to different sections of the admin interface.

Each section of the admin interface, such as Users, Organizations, and Projects, provides a grid view of the respective entities. This grid view is facilitated by the 'ResultGrid' component, which fetches and displays data from the respective endpoints.

The 'adminSettings.tsx' file provides an interface for managing various system settings. It fetches the current settings from the '/internal/options/' endpoint and allows the user to update them.

<SwmSnippet path="/static/app/views/admin/adminUsers.tsx" line="34">

---

# AdminUsers Function

The `AdminUsers` function in `adminUsers.tsx` is responsible for displaying and managing users. It fetches user data from the '/users/' endpoint and displays it in a grid view. The grid includes columns for the username, date joined, and last login. The function also provides a search filter and sorting options.

```tsx
function AdminUsers(props: Props) {
  const columns = [
    <th key="username">User</th>,
    <th key="dateJoined" style={{textAlign: 'center', width: 150}}>
      Joined
    </th>,
    <th key="lastLogin" style={{textAlign: 'center', width: 150}}>
      Last Login
    </th>,
  ];

  return (
    <div>
      <h3>{t('Users')}</h3>
      <ResultGrid
        path="/manage/users/"
        endpoint="/users/"
        method="GET"
        columns={columns}
        columnsForRow={getRow}
        hasSearch
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/admin/adminSettings.tsx" line="88">

---

# AdminSettings Function

The `AdminSettings` function in `adminSettings.tsx` is responsible for managing system settings. It fetches the current settings from the '/internal/options/' endpoint and allows the user to update them. The settings are displayed in a form, with each setting represented by a field.

```tsx
  const initialData = {};
  const fields = {};
  for (const key of optionsAvailable) {
    // TODO(dcramer): we should not be mutating options
    const option = data[key] ?? {field: {}, value: undefined};

    if (option.value === undefined || option.value === '') {
      const defn = getOption(key);
      initialData[key] = defn.defaultValue ? defn.defaultValue() : '';
    } else {
      initialData[key] = option.value;
    }
    fields[key] = getOptionField(key, option.field);
  }

  return (
    <div>
      <h3>{t('Settings')}</h3>

      <Form
        apiMethod="PUT"
```

---

</SwmSnippet>

# AdminOverview Directory

The `adminOverview` directory contains several TypeScript files that provide views for the admin interface. These include `eventChart.tsx` for displaying event data, `apiChart.tsx` for API data, and `index.tsx` as the main entry point for the admin overview.

# Admin Functions

This section provides an overview of the main functions in the admin section of the Sentry application.

<SwmSnippet path="/static/app/views/admin/adminUsers.tsx" line="34">

---

## AdminUsers

The `AdminUsers` function is responsible for rendering the Users section of the admin interface. It fetches data about users from the '/users/' endpoint and displays it in a grid view. The grid includes columns for the username, date joined, and last login.

```tsx
function AdminUsers(props: Props) {
  const columns = [
    <th key="username">User</th>,
    <th key="dateJoined" style={{textAlign: 'center', width: 150}}>
      Joined
    </th>,
    <th key="lastLogin" style={{textAlign: 'center', width: 150}}>
      Last Login
    </th>,
  ];

  return (
    <div>
      <h3>{t('Users')}</h3>
      <ResultGrid
        path="/manage/users/"
        endpoint="/users/"
        method="GET"
        columns={columns}
        columnsForRow={getRow}
        hasSearch
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/admin/adminOrganizations.tsx" line="19">

---

## AdminOrganizations

The `AdminOrganizations` function renders the Organizations section of the admin interface. It fetches data about organizations from the '/organizations/' endpoint and displays it in a grid view.

```tsx
function AdminOrganizations(props: Props) {
  return (
    <div>
      <h3>{t('Organizations')}</h3>
      <ResultGrid
        path="/manage/organizations/"
        endpoint="/organizations/?show=all"
        method="GET"
        columns={[<th key="column-org">Organization</th>]}
        columnsForRow={getRow}
        hasSearch
        sortOptions={[
          ['date', 'Date Joined'],
          ['members', 'Members'],
          ['events', 'Events'],
          ['projects', 'Projects'],
          ['employees', 'Employees'],
        ]}
        defaultSort="date"
        {...props}
      />
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/admin/adminProjects.tsx" line="34">

---

## AdminProjects

The `AdminProjects` function renders the Projects section of the admin interface. It fetches data about projects from the '/projects/' endpoint and displays it in a grid view.

```tsx
function AdminProjects(props: Props) {
  const columns = [
    <th key="name">Project</th>,
    <th key="status" style={{width: 150, textAlign: 'center'}}>
      Status
    </th>,
    <th key="dateCreated" style={{width: 200, textAlign: 'right'}}>
      Created
    </th>,
  ];

  return (
    <div>
      <h3>{t('Projects')}</h3>
      <ResultGrid
        path="/manage/projects/"
        endpoint="/projects/?show=all"
        method="GET"
        columns={columns}
        columnsForRow={getRow}
        hasSearch
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/admin/adminSettings.tsx" line="72">

---

## AdminSettings

The `AdminSettings` function renders the Settings section of the admin interface. It fetches data about system settings from the '/internal/options/' endpoint and allows the user to update them.

```tsx
export default function AdminSettings() {
  const {data, isLoading, isError} = useApiQuery<Record<string, FieldDef>>(
    ['/internal/options/'],
    {
      staleTime: 0,
    }
  );

  if (isError) {
    return <LoadingError />;
  }

  if (isLoading) {
    return <LoadingIndicator />;
  }

  const initialData = {};
  const fields = {};
  for (const key of optionsAvailable) {
    // TODO(dcramer): we should not be mutating options
    const option = data[key] ?? {field: {}, value: undefined};
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/admin/adminEnvironment.tsx" line="23">

---

## AdminEnvironment

The `AdminEnvironment` function renders the Environment section of the admin interface. It fetches data about the environment from the '/internal/environment/' endpoint and displays it.

```tsx
export default function AdminEnvironment() {
  const {data, isLoading, isError} = useApiQuery<Data>(['/internal/environment/'], {
    staleTime: 0,
  });

  if (isError) {
    return <LoadingError />;
  }

  if (isLoading) {
    return <LoadingIndicator />;
  }

  const {version} = ConfigStore.getState();

  return (
    <div>
      <h3>{t('Environment')}</h3>

      {data?.environment ? (
        <dl className="vars">
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/admin/adminQueue.tsx" line="12">

---

## AdminQueue

The `AdminQueue` function renders the Queue section of the admin interface. It fetches data about the queue from the '/internal/queue/tasks/' endpoint and displays it.

```tsx
import PanelHeader from 'sentry/components/panels/panelHeader';
import {t} from 'sentry/locale';
import {useApiQuery} from 'sentry/utils/queryClient';

const TIME_WINDOWS = ['1h', '1d', '1w'] as const;

type TimeWindow = (typeof TIME_WINDOWS)[number];

type State = {
  activeTask: string;
  resolution: string;
  since: number;
  timeWindow: TimeWindow;
};

export default function AdminQueue() {
  const [state, setState] = useState<State>({
    timeWindow: '1w',
    since: new Date().getTime() / 1000 - 3600 * 24 * 7,
    resolution: '1h',
    activeTask: '',
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/admin/adminRelays.tsx" line="13">

---

## AdminRelays

The `AdminRelays` function renders the Relays section of the admin interface. It fetches data about relays from the '/internal/relays/' endpoint and displays it.

```tsx
type Props = RouteComponentProps<{}, {}> & {api: Client};

type State = {
  loading: boolean;
};

type RelayRow = {
  firstSeen: string;
  id: string;
  lastSeen: string;
  publicKey: string;
  relayId: string;
};

class AdminRelays extends Component<Props, State> {
  state: State = {
    loading: false,
  };

  onDelete(key: string) {
    this.setState({loading: true});
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/admin/adminBuffer.tsx" line="3">

---

## AdminBuffer

The `AdminBuffer` function renders the Buffers section of the admin interface. It fetches data about buffers from the '/internal/buffers/' endpoint and displays it.

```tsx
function AdminBuffer() {
  const since = new Date().getTime() / 1000 - 3600 * 24 * 7;

  return (
    <div>
      <h3>Buffers</h3>

      <div className="box">
        <div className="box-header">
          <h4>About</h4>
        </div>

        <div className="box-content with-padding">
          <p>
            Sentry buffers are responsible for making changes to cardinality counters —
            such as an issues event count — as well as updating attributes like{' '}
            <em>last seen</em>. These are flushed on a regularly interval, and are
            directly affected by the queue backlog.
          </p>
        </div>
      </div>
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/admin/adminWarnings.tsx" line="12">

---

## AdminWarnings

The `AdminWarnings` function renders the Warnings section of the admin interface. It fetches data about warnings from the '/internal/warnings/' endpoint and displays it.

```tsx
function AdminWarnings() {
  const {data, isLoading, isError} = useApiQuery<Data>(['/internal/warnings/'], {
    staleTime: 0,
  });

  if (isLoading) {
    return <LoadingIndicator />;
  }

  if (!data || isError) {
    return null;
  }

  const {groups, warnings} = data;

  return (
    <div>
      <h3>{t('System Warnings')}</h3>
      {!warnings && !groups && t('There are no warnings at this time')}

      {groups.map(([groupName, groupedWarnings]) => (
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/admin/adminPackages.tsx" line="13">

---

## AdminPackages

The `AdminPackages` function renders the Packages section of the admin interface. It fetches data about packages from the '/internal/packages/' endpoint and displays it.

```tsx
export default function AdminPackages() {
  const {data, isLoading, isError} = useApiQuery<Data>(['/internal/packages/'], {
    staleTime: 0,
  });

  if (isError) {
    return <LoadingError />;
  }

  if (isLoading) {
    return <LoadingIndicator />;
  }

  return (
    <div>
      <h3>{t('Extensions')}</h3>

      {data?.extensions && data?.extensions.length > 0 ? (
        <dl className="vars">
          {data?.extensions.map(([key, value]) => (
            <Fragment key={key}>
```

---

</SwmSnippet>

# Admin Interface Endpoints

Admin Interface Endpoints

<SwmSnippet path="/static/app/views/admin/adminUsers.tsx" line="48">

---

## User Management Endpoint

The '/users/' endpoint is used in the 'AdminUsers' component to fetch and display a list of all users. The 'ResultGrid' component is used to display the data fetched from this endpoint. The endpoint is hit with a 'GET' request.

```tsx
      <ResultGrid
        path="/manage/users/"
        endpoint="/users/"
        method="GET"
        columns={columns}
        columnsForRow={getRow}
        hasSearch
        filters={{
          status: {
            name: 'Status',
            options: [
              ['active', 'Active'],
              ['disabled', 'Disabled'],
            ],
          },
        }}
        sortOptions={[['date', 'Date Joined']]}
        defaultSort="date"
        {...props}
      />
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/admin/adminOrganizations.tsx" line="23">

---

## Organization Management Endpoint

The '/organizations/' endpoint is used in the 'AdminOrganizations' component to fetch and display a list of all organizations. The 'ResultGrid' component is used to display the data fetched from this endpoint. The endpoint is hit with a 'GET' request.

```tsx
      <ResultGrid
        path="/manage/organizations/"
        endpoint="/organizations/?show=all"
        method="GET"
        columns={[<th key="column-org">Organization</th>]}
        columnsForRow={getRow}
        hasSearch
        sortOptions={[
          ['date', 'Date Joined'],
          ['members', 'Members'],
          ['events', 'Events'],
          ['projects', 'Projects'],
          ['employees', 'Employees'],
        ]}
        defaultSort="date"
        {...props}
      />
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
