---
title: Introduction to Data Table in Discover
---
In the Discover section of the Sentry application, the 'Table' is a key component that fetches and handles the pagination of data. It is defined in the 'Table' class within the 'index.tsx' file. The 'Table' class maintains its state, which includes information about loading status, error messages, and fetched data.

The 'Table' class uses various methods to manage its state and data. For instance, the 'fetchData' method is used to retrieve data based on the current event view and API payload. The 'didViewChange' and 'shouldRefetchData' methods are used to determine if the view has changed or if data should be refetched.

The 'Table' class passes the fetched data to the 'TableView' component, which is responsible for rendering the table. The 'TableView' component is defined in the 'tableView.tsx' file. It uses the data from the 'Table' class to generate new EventView objects for actions like resizing columns.

The 'TableView' component also handles the rendering of individual cells within the table. It uses various methods, such as '\_renderGridHeaderCell' and '\_renderGridBodyCell', to render header and body cells respectively. These methods take into account the type of data to be displayed and apply appropriate formatting and styling.

The 'Table' and 'TableView' components are styled using styled-components, a CSS-in-JS library. The styling is defined in the same files as the components themselves. For instance, the 'Container' styled component in 'index.tsx' sets the minimum width of the 'Table' component.

<SwmSnippet path="/static/app/views/discover/table/index.tsx" line="60">

---

# Table Class

The 'Table' class is defined here. It maintains its state, which includes information about loading status, error messages, and fetched data. The 'fetchData' method is used to retrieve data based on the current event view and API payload.

```tsx
class Table extends PureComponent<TableProps, TableState> {
  state: TableState = {
    isLoading: true,
    tableFetchID: undefined,
    error: null,

    pageLinks: null,
    tableData: null,
    prevView: null,
  };

  componentDidMount() {
    this.fetchData();
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/table/tableView.tsx" line="102">

---

# TableView Component

The 'TableView' component is defined here. It uses the data from the 'Table' class to generate new EventView objects for actions like resizing columns. It also handles the rendering of individual cells within the table using methods like '\_renderGridHeaderCell' and '\_renderGridBodyCell'.

```tsx
function TableView(props: TableViewProps) {
  const {projects} = useProjects();
  const routes = useRoutes();
  const replayLinkGenerator = generateReplayLink(routes);

  /**
   * Updates a column on resizing
   */
  function _resizeColumn(
    columnIndex: number,
    nextColumn: TableColumn<keyof TableDataRow>
  ) {
    const {location, eventView} = props;

    const newWidth = nextColumn.width ? Number(nextColumn.width) : COL_WIDTH_UNDEFINED;
    const nextEventView = eventView.withResizedColumn(columnIndex, newWidth);

    pushEventViewToLocation({
      location,
      nextEventView,
      extraQuery: pickRelevantLocationQueryStrings(location),
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/table/tableView.tsx" line="686">

---

# Styling

The 'Table' and 'TableView' components are styled using styled-components, a CSS-in-JS library. The styling is defined in the same files as the components themselves.

```tsx
const PrependHeader = styled('span')`
  color: ${p => p.theme.subText};
`;

const StyledTooltip = styled(Tooltip)`
  display: initial;
  max-width: max-content;
`;

export const StyledLink = styled(Link)`
  & div {
    display: inline;
  }
`;

export const TransactionLink = styled(Link)`
  ${p => p.theme.overflowEllipsis}
`;

const StyledIcon = styled(IconStack)`
  vertical-align: middle;
```

---

</SwmSnippet>

# Table Functionality

This section will explain the main functions used in the Table functionality of the Sentry application.

<SwmSnippet path="/static/app/views/discover/table/index.tsx" line="105">

---

## fetchData

The 'fetchData' method is used to retrieve data based on the current event view and API payload. It is called when the component mounts and whenever the view changes or data needs to be refetched.

```tsx
  fetchData = () => {
    const {
      eventView,
      organization,
      location,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/table/index.tsx" line="88">

---

## didViewChange

The 'didViewChange' method is used to determine if the view has changed. It compares the current and previous API payloads to make this determination.

```tsx
    const {prevView} = this.state;
    const thisAPIPayload = this.props.eventView.getEventsAPIPayload(this.props.location);
    if (prevView === null) {
      return true;
    }
    const otherAPIPayload = prevView.getEventsAPIPayload(this.props.location);

    return !isAPIPayloadSimilar(thisAPIPayload, otherAPIPayload);
  };
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/table/index.tsx" line="98">

---

## shouldRefetchData

The 'shouldRefetchData' method is used to determine if data should be refetched. It compares the current and previous API payloads to make this determination.

```tsx
  shouldRefetchData = (prevProps: TableProps): boolean => {
    const thisAPIPayload = this.props.eventView.getEventsAPIPayload(this.props.location);
    const otherAPIPayload = prevProps.eventView.getEventsAPIPayload(prevProps.location);

    return !isAPIPayloadSimilar(thisAPIPayload, otherAPIPayload);
  };
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/table/tableView.tsx" line="110">

---

## \_resizeColumn

The '\_resizeColumn' method is used to resize a column in the table. It takes the column index and the next column as parameters, calculates the new width, and generates a new EventView object with the resized column.

```tsx
  function _resizeColumn(
    columnIndex: number,
    nextColumn: TableColumn<keyof TableDataRow>
  ) {
    const {location, eventView} = props;

    const newWidth = nextColumn.width ? Number(nextColumn.width) : COL_WIDTH_UNDEFINED;
    const nextEventView = eventView.withResizedColumn(columnIndex, newWidth);

    pushEventViewToLocation({
      location,
      nextEventView,
      extraQuery: pickRelevantLocationQueryStrings(location),
    });
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/table/tableView.tsx" line="246">

---

## \_renderGridHeaderCell

The '\_renderGridHeaderCell' method is used to render a header cell in the table. It takes a column as a parameter and returns a React node.

```tsx
  function _renderGridHeaderCell(
    column: TableColumn<keyof TableDataRow>
  ): React.ReactNode {
    const {eventView, location, tableData} = props;
    const tableMeta = tableData?.meta;

    const align = fieldAlignment(column.name, column.type, tableMeta);
    const field = {field: column.key as string, width: column.width};
    function generateSortLink(): LocationDescriptorObject | undefined {
      if (!tableMeta) {
        return undefined;
      }

      const nextEventView = eventView.sortOnField(field, tableMeta);
      const queryStringObject = nextEventView.generateQueryStringObject();
      // Need to pull yAxis from location since eventView only stores 1 yAxis field at time
      queryStringObject.yAxis = decodeList(location.query.yAxis);

      return {
        ...location,
        query: queryStringObject,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/table/tableView.tsx" line="296">

---

## \_renderGridBodyCell

The '\_renderGridBodyCell' method is used to render a body cell in the table. It takes a column, a data row, a row index, and a column index as parameters, and returns a React node.

```tsx
  function _renderGridBodyCell(
    column: TableColumn<keyof TableDataRow>,
    dataRow: TableDataRow,
    rowIndex: number,
    columnIndex: number
  ): React.ReactNode {
    const {isFirstPage, eventView, location, organization, tableData, isHomepage} = props;

    if (!tableData || !tableData.meta) {
      return dataRow[column.key];
    }

    const columnKey = String(column.key);
    const fieldRenderer = getFieldRenderer(columnKey, tableData.meta, false);

    const display = eventView.getDisplayMode();
    const isTopEvents =
      display === DisplayModes.TOP5 || display === DisplayModes.DAILYTOP5;

    const topEvents = eventView.topEvents ? parseInt(eventView.topEvents, 10) : TOP_N;
    const count = Math.min(tableData?.data?.length ?? topEvents, topEvents);
```

---

</SwmSnippet>

# Table Data Management

Table Data Fetching and Pagination

<SwmSnippet path="/static/app/views/discover/table/index.tsx" line="60">

---

## Table Class

The 'Table' class is defined here. It maintains its state, which includes information about loading status, error messages, and fetched data.

```tsx
class Table extends PureComponent<TableProps, TableState> {
  state: TableState = {
    isLoading: true,
    tableFetchID: undefined,
    error: null,

    pageLinks: null,
    tableData: null,
    prevView: null,
  };
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/table/index.tsx" line="105">

---

## Fetching Data

The 'fetchData' method is used to retrieve data based on the current event view and API payload. The data is fetched from the '/organizations/${organization.slug}/events/' endpoint.

```tsx
  fetchData = () => {
    const {
      eventView,
      organization,
      location,
      setError,
      confirmedQuery,
      setTips,
      setSplitDecision,
    } = this.props;

    if (!eventView.isValid() || !confirmedQuery) {
      return;
    }
    this.setState({prevView: eventView});

    // note: If the eventView has no aggregates, the endpoint will automatically add the event id in
    // the API payload response

    const url = `/organizations/${organization.slug}/events/`;
    const tableFetchID = Symbol('tableFetchID');
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/table/index.tsx" line="87">

---

## Checking for View Changes

The 'didViewChange' method is used to determine if the view has changed. It compares the current API payload with the previous one.

```tsx
  didViewChange = (): boolean => {
    const {prevView} = this.state;
    const thisAPIPayload = this.props.eventView.getEventsAPIPayload(this.props.location);
    if (prevView === null) {
      return true;
    }
    const otherAPIPayload = prevView.getEventsAPIPayload(this.props.location);

    return !isAPIPayloadSimilar(thisAPIPayload, otherAPIPayload);
  };
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/table/index.tsx" line="98">

---

## Checking for Data Refetch

The 'shouldRefetchData' method is used to determine if data should be refetched. It compares the current API payload with the previous one.

```tsx
  shouldRefetchData = (prevProps: TableProps): boolean => {
    const thisAPIPayload = this.props.eventView.getEventsAPIPayload(this.props.location);
    const otherAPIPayload = prevProps.eventView.getEventsAPIPayload(prevProps.location);

    return !isAPIPayloadSimilar(thisAPIPayload, otherAPIPayload);
  };
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
