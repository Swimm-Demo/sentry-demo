---
title: Understanding AggregateFlamegraphTreeTable
---
<SwmSnippet path="/static/app/components/profiling/flamegraph/aggregateFlamegraphTreeTable.tsx" line="111">

---

# AggregateFlamegraphTreeTable

The `AggregateFlamegraphTreeTable` function is the starting point of the flow. It is responsible for rendering the flamegraph tree table. It uses several hooks and local states to manage the flamegraph's state, such as the current view, the root nodes, the tree, the color map, and the sort function. It also defines the `fixedRenderRow` and `dynamicRenderRow` callbacks, which are used to render each row of the flamegraph tree table.

```tsx
export function AggregateFlamegraphTreeTable({
  expanded,
  recursion,
  frameFilter,
}: AggregateFlamegraphTreeTableProps) {
  const dispatch = useDispatchFlamegraphState();
  const profiles = useFlamegraphProfiles();
  const profileGroup = useProfileGroup();
  const flamegraph = useFlamegraph();
  const theme = useFlamegraphTheme();
  const referenceNode = flamegraph.root;

  const [treeView, setTreeView] = useLocalStorageState<'bottom up' | 'top down'>(
    'profiling-aggregate-call-tree-view',
    'bottom up'
  );

  const rootNodes = useMemo(() => {
    return flamegraph.root.children;
  }, [flamegraph.root.children]);

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/profiling/hooks/useVirtualizedTree/useVirtualizedTree.tsx" line="125">

---

# useVirtualizedTree

The `useVirtualizedTree` hook is used to manage the state of the virtualized tree. It provides several functionalities such as handling scrolling, clicking, mouse movement, sorting changes, and node expansion. It also provides the `handleRowClick`, `handleRowMouseEnter`, `handleExpandTreeNode`, `handleRowKeyDown`, and `handleScrollTo` callbacks, which are used in the `AggregateFlamegraphTreeTable` function to handle user interactions.

```tsx
export function useVirtualizedTree<T extends TreeLike>(
  props: UseVirtualizedTreeProps<T>
) {
  const onScrollToNode = props.onScrollToNode;
  const theme = useTheme();
  const clickedGhostRowRef = useRef<HTMLDivElement | null>(null);
  const hoveredGhostRowRef = useRef<HTMLDivElement | null>(null);

  const [state, dispatch] = useReducer(VirtualizedTreeReducer, {
    scrollTop: 0,
    roots: props.tree,
    selectedNodeIndex: props.initialSelectedNodeIndex ?? null,
    overscroll: props.overscroll ?? DEFAULT_OVERSCROLL_ITEMS,
    scrollHeight: getMaxScrollHeight(props.scrollContainer),
  });

  const [tree, setTree] = useState(() => {
    const initialTree =
      props.virtualizedTree ||
      VirtualizedTree.fromRoots(props.tree, props.expanded, props.skipFunction);

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/discover/transactionsTable.tsx" line="114">

---

# renderRow

The `renderRow` method is used to render each row of the transactions table. It takes a row of data, the row index, the column order, and the table metadata as arguments. It then maps over the column order to render each cell in the row. It also handles cell actions, which can be triggered by user interactions.

```tsx
  renderRow(
    row: TableDataRow,
    rowIndex: number,
    columnOrder: TableColumn<React.ReactText>[],
    tableMeta: MetaType
  ): React.ReactNode[] {
    const {
      eventView,
      organization,
      location,
      generateLink,
      handleCellAction,
      titles,
      useAggregateAlias,
      referrer,
    } = this.props;
    const fields = eventView.getFields();

    if (titles?.length) {
      // Slice to match length of given titles
      columnOrder = columnOrder.slice(0, titles.length);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/table/tableView.tsx" line="526">

---

# handleCellAction

The `handleCellAction` function is used to handle actions on a cell in the table. Depending on the action, it may modify the query, update the view, or navigate to a new page. It uses the `getExpandedResults` function to drill down into each distinct value and get a count for each value.

```tsx
  function handleCellAction(
    dataRow: TableDataRow,
    column: TableColumn<keyof TableDataRow>
  ) {
    return (action: Actions, value: React.ReactText) => {
      const {eventView, organization, location, tableData, isHomepage} = props;

      const query = new MutableSearch(eventView.query);

      let nextView = eventView.clone();
      trackAnalytics('discover_v2.results.cellaction', {
        organization,
        action,
      });

      switch (action) {
        case Actions.RELEASE: {
          const maybeProject = projects.find(project => {
            return project.slug === dataRow.project;
          });

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/discover/eventView.tsx" line="1190">

---

# getResultsViewUrlTarget

The `getResultsViewUrlTarget` method is used to generate the URL target for the results view. It takes the organization slug and a boolean indicating whether the current page is the homepage as arguments. It returns an object containing the pathname and the query string object.

```tsx
  getResultsViewUrlTarget(
    slug: string,
    isHomepage: boolean = false
  ): {pathname: string; query: Query} {
    const target = isHomepage ? 'homepage' : 'results';
    return {
      pathname: normalizeUrl(`/organizations/${slug}/discover/${target}/`),
      query: this.generateQueryStringObject(),
    };
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/discover/eventView.tsx" line="672">

---

# generateQueryStringObject

The `generateQueryStringObject` method is used to generate a query string object from the current event view. It includes fields such as id, name, field, widths, sort, environment, project, query, yAxis, dataset, display, topEvents, and interval.

```tsx
  generateQueryStringObject(): Query {
    const output = {
      id: this.id,
      name: this.name,
      field: this.getFields(),
      widths: this.getWidths(),
      sort: encodeSorts(this.sorts),
      environment: this.environment,
      project: this.project,
      query: this.query,
      yAxis: this.yAxis || this.getYAxis(),
      dataset: this.dataset,
      display: this.display,
      topEvents: this.topEvents,
      interval: this.interval,
    };

    for (const field of EXTERNAL_QUERY_STRING_KEYS) {
      if (this[field]?.length) {
        output[field] = this[field];
      }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/utils.tsx" line="262">

---

# getExpandedResults

The `getExpandedResults` function is the starting point of the flow. It converts an aggregated query into one that does not have aggregates. It also applies additional conditions defined in `additionalConditions` and generates conditions based on the `dataRow` parameter and the current fields in the `eventView`.

```tsx
export function getExpandedResults(
  eventView: EventView,
  additionalConditions: Record<string, string>,
  dataRow?: TableDataRow | Event
): EventView {
  const fieldSet = new Set();
  // Expand any functions in the resulting column, and dedupe the result.
  // Mark any column as null to remove it.
  const expandedColumns: (Column | null)[] = eventView.fields.map((field: Field) => {
    const exploded = explodeFieldString(field.field, field.alias);
    const column = exploded.kind === 'function' ? drilldownAggregate(exploded) : exploded;

    if (
      // if expanding the function failed
      column === null ||
      // the new column is already present
      fieldSet.has(column.field) ||
      // Skip aggregate equations, their functions will already be added so we just want to remove it
      isAggregateEquation(field.field)
    ) {
      return null;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/discover/eventView.tsx" line="971">

---

# withDeletedColumn

The `withDeletedColumn` method is called within `getExpandedResults`. It removes a column from the EventView and adjusts the sort keys and yAxis accordingly.

```tsx
  withDeletedColumn(columnIndex: number, tableMeta: MetaType | undefined): EventView {
    // Disallow removal of the orphan column, and check for out-of-bounds
    if (this.fields.length <= 1 || this.fields.length <= columnIndex || columnIndex < 0) {
      return this;
    }

    // ensure tableMeta is non-empty
    tableMeta = validateTableMeta(tableMeta);

    // delete the column
    const newEventView = this.clone();
    const fields = [...newEventView.fields];
    fields.splice(columnIndex, 1);
    newEventView.fields = fields;

    // Ensure there is at least one auto width column
    // To ensure a well formed table results.
    const hasAutoIndex = fields.find(field => field.width === COL_WIDTH_UNDEFINED);
    if (!hasAutoIndex) {
      newEventView.fields[0].width = COL_WIDTH_UNDEFINED;
    }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/utils.tsx" line="423">

---

# generateExpandedConditions

The `generateExpandedConditions` function is also called within `getExpandedResults`. It creates additional conditions based on the fields in an EventView and a dataRow/event.

```tsx
function generateExpandedConditions(
  eventView: EventView,
  additionalConditions: Record<string, string>,
  dataRow?: TableDataRow | Event
): string {
  const parsedQuery = new MutableSearch(eventView.query);

  // Remove any aggregates from the search conditions.
  // otherwise, it'll lead to an invalid query result.
  for (const key in parsedQuery.filters) {
    const column = explodeFieldString(key);
    if (column.kind === 'function') {
      parsedQuery.removeFilter(key);
    }
  }

  const conditions: Record<string, string | string[]> = Object.assign(
    {},
    additionalConditions,
    generateAdditionalConditions(eventView, dataRow)
  );
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/discover/eventView.tsx" line="877">

---

# withUpdatedColumn

The `withUpdatedColumn` method is called twice within `getExpandedResults`. It updates a column in the EventView and adjusts the sort keys and yAxis accordingly.

```tsx
  withUpdatedColumn(
    columnIndex: number,
    updatedColumn: Column,
    tableMeta: MetaType | undefined
  ): EventView {
    const columnToBeUpdated = this.fields[columnIndex];
    const fieldAsString = generateFieldAsString(updatedColumn);

    const updateField = columnToBeUpdated.field !== fieldAsString;
    if (!updateField) {
      return this;
    }

    // ensure tableMeta is non-empty
    tableMeta = validateTableMeta(tableMeta);

    const newEventView = this.clone();

    const updatedField: Field = {
      field: fieldAsString,
      width: COL_WIDTH_UNDEFINED,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/discover/eventView.tsx" line="1319">

---

# getYAxis

The `getYAxis` method is called within `withUpdatedColumn` and `withDeletedColumn`. It returns the current selected yAxis if it is one of the items in yAxisOptions, otherwise it returns the default option.

```tsx
  getYAxis(): string {
    const yAxisOptions = this.getYAxisOptions();

    const yAxis = this.yAxis;
    const defaultOption = yAxisOptions[0].value;

    if (!yAxis) {
      return defaultOption;
    }

    // ensure current selected yAxis is one of the items in yAxisOptions
    const result = yAxisOptions.findIndex(
      (option: SelectValue<string>) => option.value === yAxis
    );

    if (result >= 0) {
      return typeof yAxis === 'string' ? yAxis : yAxis[0];
    }

    return defaultOption;
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/discover/eventView.tsx" line="1300">

---

# getYAxisOptions

The `getYAxisOptions` method is called within `getYAxis`. It returns a list of yAxis options that are either aggregates that are graphable or aggregate equations.

```tsx
  getYAxisOptions(): SelectValue<string>[] {
    // Make option set and add the default options in.
    return uniqBy(
      this.getAggregateFields()
        // Only include aggregates that make sense to be graphable (eg. not string or date)
        .filter(
          (field: Field) =>
            isLegalYAxisType(aggregateOutputType(field.field)) ||
            isAggregateEquation(field.field)
        )
        .map((field: Field) => ({
          label: isEquation(field.field) ? getEquation(field.field) : field.field,
          value: field.field,
        }))
        .concat(CHART_AXIS_OPTIONS),
      'value'
    );
  }
```

---

</SwmSnippet>

```mermaid
graph TD;
subgraph static/app/utils
 AggregateFlamegraphTreeTable:::mainFlowStyle --> useVirtualizedTree:::mainFlowStyle
end
subgraph static/app/components
 useVirtualizedTree:::mainFlowStyle --> renderRow:::mainFlowStyle
end
subgraph static/app/views/discover
 renderRow:::mainFlowStyle --> handleCellAction:::mainFlowStyle
end
subgraph static/app/utils
 handleCellAction:::mainFlowStyle --> getResultsViewUrlTarget
end
subgraph static/app/views/discover
 handleCellAction:::mainFlowStyle --> getExpandedResults:::mainFlowStyle
end
subgraph static/app/views/discover
 getExpandedResults:::mainFlowStyle --> 8sw4y[...]
end
subgraph static/app/utils
 getResultsViewUrlTarget --> generateQueryStringObject
end

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

```mermaid
graph TD;
subgraph static/app/utils
  AggregateFlamegraphTreeTable:::mainFlowStyle --> useVirtualizedTree:::mainFlowStyle
end
subgraph static/app/components
  useVirtualizedTree:::mainFlowStyle --> renderRow:::mainFlowStyle
end
subgraph static/app/views/discover
  renderRow:::mainFlowStyle --> handleCellAction:::mainFlowStyle
end
subgraph static/app/utils
  handleCellAction:::mainFlowStyle --> getResultsViewUrlTarget
end
subgraph static/app/views/discover
  handleCellAction:::mainFlowStyle --> getExpandedResults:::mainFlowStyle
end
subgraph static/app/utils
  getExpandedResults:::mainFlowStyle --> withDeletedColumn
end
subgraph static/app/views/discover
  getExpandedResults:::mainFlowStyle --> generateExpandedConditions
end
subgraph static/app/utils
  getExpandedResults:::mainFlowStyle --> withUpdatedColumn:::mainFlowStyle
end
subgraph static/app/utils
  withUpdatedColumn:::mainFlowStyle --> getYAxis:::mainFlowStyle
end
subgraph static/app/utils
  getYAxis:::mainFlowStyle --> getYAxisOptions:::mainFlowStyle
end

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

# Flow drill down

First, we'll zoom into this section of the flow:

```mermaid
graph TD;
subgraph static/app/utils
  AggregateFlamegraphTreeTable:::mainFlowStyle --> useVirtualizedTree:::mainFlowStyle
end
subgraph static/app/components
  useVirtualizedTree:::mainFlowStyle --> renderRow:::mainFlowStyle
end
subgraph static/app/views/discover
  renderRow:::mainFlowStyle --> handleCellAction:::mainFlowStyle
end
subgraph static/app/utils
  handleCellAction:::mainFlowStyle --> getResultsViewUrlTarget
end
subgraph static/app/views/discover
  handleCellAction:::mainFlowStyle --> getExpandedResults:::mainFlowStyle
end
subgraph static/app/views/discover
  getExpandedResults:::mainFlowStyle --> 8sw4y[...]
end
subgraph static/app/utils
  getResultsViewUrlTarget --> generateQueryStringObject
end

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

<SwmSnippet path="/static/app/components/profiling/flamegraph/aggregateFlamegraphTreeTable.tsx" line="111">

---

# AggregateFlamegraphTreeTable

The `AggregateFlamegraphTreeTable` function is the starting point of the flow. It is responsible for rendering the flamegraph tree table. It uses several hooks and local states to manage the flamegraph's state, such as the current view, the root nodes, the tree, the color map, and the sort function. It also defines the `fixedRenderRow` and `dynamicRenderRow` callbacks, which are used to render each row of the flamegraph tree table.

```tsx
export function AggregateFlamegraphTreeTable({
  expanded,
  recursion,
  frameFilter,
}: AggregateFlamegraphTreeTableProps) {
  const dispatch = useDispatchFlamegraphState();
  const profiles = useFlamegraphProfiles();
  const profileGroup = useProfileGroup();
  const flamegraph = useFlamegraph();
  const theme = useFlamegraphTheme();
  const referenceNode = flamegraph.root;

  const [treeView, setTreeView] = useLocalStorageState<'bottom up' | 'top down'>(
    'profiling-aggregate-call-tree-view',
    'bottom up'
  );

  const rootNodes = useMemo(() => {
    return flamegraph.root.children;
  }, [flamegraph.root.children]);

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/profiling/hooks/useVirtualizedTree/useVirtualizedTree.tsx" line="125">

---

# useVirtualizedTree

The `useVirtualizedTree` hook is used to manage the state of the virtualized tree. It provides several functionalities such as handling scrolling, clicking, mouse movement, sorting changes, and node expansion. It also provides the `handleRowClick`, `handleRowMouseEnter`, `handleExpandTreeNode`, `handleRowKeyDown`, and `handleScrollTo` callbacks, which are used in the `AggregateFlamegraphTreeTable` function to handle user interactions.

```tsx
export function useVirtualizedTree<T extends TreeLike>(
  props: UseVirtualizedTreeProps<T>
) {
  const onScrollToNode = props.onScrollToNode;
  const theme = useTheme();
  const clickedGhostRowRef = useRef<HTMLDivElement | null>(null);
  const hoveredGhostRowRef = useRef<HTMLDivElement | null>(null);

  const [state, dispatch] = useReducer(VirtualizedTreeReducer, {
    scrollTop: 0,
    roots: props.tree,
    selectedNodeIndex: props.initialSelectedNodeIndex ?? null,
    overscroll: props.overscroll ?? DEFAULT_OVERSCROLL_ITEMS,
    scrollHeight: getMaxScrollHeight(props.scrollContainer),
  });

  const [tree, setTree] = useState(() => {
    const initialTree =
      props.virtualizedTree ||
      VirtualizedTree.fromRoots(props.tree, props.expanded, props.skipFunction);

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/discover/transactionsTable.tsx" line="114">

---

# renderRow

The `renderRow` method is used to render each row of the transactions table. It takes a row of data, the row index, the column order, and the table metadata as arguments. It then maps over the column order to render each cell in the row. It also handles cell actions, which can be triggered by user interactions.

```tsx
  renderRow(
    row: TableDataRow,
    rowIndex: number,
    columnOrder: TableColumn<React.ReactText>[],
    tableMeta: MetaType
  ): React.ReactNode[] {
    const {
      eventView,
      organization,
      location,
      generateLink,
      handleCellAction,
      titles,
      useAggregateAlias,
      referrer,
    } = this.props;
    const fields = eventView.getFields();

    if (titles?.length) {
      // Slice to match length of given titles
      columnOrder = columnOrder.slice(0, titles.length);
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/table/tableView.tsx" line="526">

---

# handleCellAction

The `handleCellAction` function is used to handle actions on a cell in the table. Depending on the action, it may modify the query, update the view, or navigate to a new page. It uses the `getExpandedResults` function to drill down into each distinct value and get a count for each value.

```tsx
  function handleCellAction(
    dataRow: TableDataRow,
    column: TableColumn<keyof TableDataRow>
  ) {
    return (action: Actions, value: React.ReactText) => {
      const {eventView, organization, location, tableData, isHomepage} = props;

      const query = new MutableSearch(eventView.query);

      let nextView = eventView.clone();
      trackAnalytics('discover_v2.results.cellaction', {
        organization,
        action,
      });

      switch (action) {
        case Actions.RELEASE: {
          const maybeProject = projects.find(project => {
            return project.slug === dataRow.project;
          });

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/discover/eventView.tsx" line="1190">

---

# getResultsViewUrlTarget

The `getResultsViewUrlTarget` method is used to generate the URL target for the results view. It takes the organization slug and a boolean indicating whether the current page is the homepage as arguments. It returns an object containing the pathname and the query string object.

```tsx
  getResultsViewUrlTarget(
    slug: string,
    isHomepage: boolean = false
  ): {pathname: string; query: Query} {
    const target = isHomepage ? 'homepage' : 'results';
    return {
      pathname: normalizeUrl(`/organizations/${slug}/discover/${target}/`),
      query: this.generateQueryStringObject(),
    };
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/discover/eventView.tsx" line="672">

---

# generateQueryStringObject

The `generateQueryStringObject` method is used to generate a query string object from the current event view. It includes fields such as id, name, field, widths, sort, environment, project, query, yAxis, dataset, display, topEvents, and interval.

```tsx
  generateQueryStringObject(): Query {
    const output = {
      id: this.id,
      name: this.name,
      field: this.getFields(),
      widths: this.getWidths(),
      sort: encodeSorts(this.sorts),
      environment: this.environment,
      project: this.project,
      query: this.query,
      yAxis: this.yAxis || this.getYAxis(),
      dataset: this.dataset,
      display: this.display,
      topEvents: this.topEvents,
      interval: this.interval,
    };

    for (const field of EXTERNAL_QUERY_STRING_KEYS) {
      if (this[field]?.length) {
        output[field] = this[field];
      }
```

---

</SwmSnippet>

Now, lets zoom into this section of the flow:

```mermaid
graph TD;
subgraph static/app
  getExpandedResults:::mainFlowStyle --> withDeletedColumn
end
subgraph static/app
  getExpandedResults:::mainFlowStyle --> generateExpandedConditions
end
subgraph static/app
  getExpandedResults:::mainFlowStyle --> withUpdatedColumn:::mainFlowStyle
end
subgraph static/app
  withUpdatedColumn:::mainFlowStyle --> getYAxis:::mainFlowStyle
end
subgraph static/app
  generateExpandedConditions --> generateAdditionalConditions
end
subgraph static/app
  getYAxis:::mainFlowStyle --> getYAxisOptions:::mainFlowStyle
end

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

<SwmSnippet path="/static/app/views/discover/utils.tsx" line="262">

---

# AggregateFlamegraphTreeTable Flow

The `getExpandedResults` function is the starting point of the flow. It converts an aggregated query into one that does not have aggregates. It also applies additional conditions defined in `additionalConditions` and generates conditions based on the `dataRow` parameter and the current fields in the `eventView`.

```tsx
export function getExpandedResults(
  eventView: EventView,
  additionalConditions: Record<string, string>,
  dataRow?: TableDataRow | Event
): EventView {
  const fieldSet = new Set();
  // Expand any functions in the resulting column, and dedupe the result.
  // Mark any column as null to remove it.
  const expandedColumns: (Column | null)[] = eventView.fields.map((field: Field) => {
    const exploded = explodeFieldString(field.field, field.alias);
    const column = exploded.kind === 'function' ? drilldownAggregate(exploded) : exploded;

    if (
      // if expanding the function failed
      column === null ||
      // the new column is already present
      fieldSet.has(column.field) ||
      // Skip aggregate equations, their functions will already be added so we just want to remove it
      isAggregateEquation(field.field)
    ) {
      return null;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/discover/eventView.tsx" line="971">

---

The `withDeletedColumn` method is called within `getExpandedResults`. It removes a column from the EventView and adjusts the sort keys and yAxis accordingly.

```tsx
  withDeletedColumn(columnIndex: number, tableMeta: MetaType | undefined): EventView {
    // Disallow removal of the orphan column, and check for out-of-bounds
    if (this.fields.length <= 1 || this.fields.length <= columnIndex || columnIndex < 0) {
      return this;
    }

    // ensure tableMeta is non-empty
    tableMeta = validateTableMeta(tableMeta);

    // delete the column
    const newEventView = this.clone();
    const fields = [...newEventView.fields];
    fields.splice(columnIndex, 1);
    newEventView.fields = fields;

    // Ensure there is at least one auto width column
    // To ensure a well formed table results.
    const hasAutoIndex = fields.find(field => field.width === COL_WIDTH_UNDEFINED);
    if (!hasAutoIndex) {
      newEventView.fields[0].width = COL_WIDTH_UNDEFINED;
    }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/discover/utils.tsx" line="423">

---

The `generateExpandedConditions` function is also called within `getExpandedResults`. It creates additional conditions based on the fields in an EventView and a dataRow/event.

```tsx
function generateExpandedConditions(
  eventView: EventView,
  additionalConditions: Record<string, string>,
  dataRow?: TableDataRow | Event
): string {
  const parsedQuery = new MutableSearch(eventView.query);

  // Remove any aggregates from the search conditions.
  // otherwise, it'll lead to an invalid query result.
  for (const key in parsedQuery.filters) {
    const column = explodeFieldString(key);
    if (column.kind === 'function') {
      parsedQuery.removeFilter(key);
    }
  }

  const conditions: Record<string, string | string[]> = Object.assign(
    {},
    additionalConditions,
    generateAdditionalConditions(eventView, dataRow)
  );
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/discover/eventView.tsx" line="877">

---

The `withUpdatedColumn` method is called twice within `getExpandedResults`. It updates a column in the EventView and adjusts the sort keys and yAxis accordingly.

```tsx
  withUpdatedColumn(
    columnIndex: number,
    updatedColumn: Column,
    tableMeta: MetaType | undefined
  ): EventView {
    const columnToBeUpdated = this.fields[columnIndex];
    const fieldAsString = generateFieldAsString(updatedColumn);

    const updateField = columnToBeUpdated.field !== fieldAsString;
    if (!updateField) {
      return this;
    }

    // ensure tableMeta is non-empty
    tableMeta = validateTableMeta(tableMeta);

    const newEventView = this.clone();

    const updatedField: Field = {
      field: fieldAsString,
      width: COL_WIDTH_UNDEFINED,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/discover/eventView.tsx" line="1319">

---

The `getYAxis` method is called within `withUpdatedColumn` and `withDeletedColumn`. It returns the current selected yAxis if it is one of the items in yAxisOptions, otherwise it returns the default option.

```tsx
  getYAxis(): string {
    const yAxisOptions = this.getYAxisOptions();

    const yAxis = this.yAxis;
    const defaultOption = yAxisOptions[0].value;

    if (!yAxis) {
      return defaultOption;
    }

    // ensure current selected yAxis is one of the items in yAxisOptions
    const result = yAxisOptions.findIndex(
      (option: SelectValue<string>) => option.value === yAxis
    );

    if (result >= 0) {
      return typeof yAxis === 'string' ? yAxis : yAxis[0];
    }

    return defaultOption;
  }
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/discover/eventView.tsx" line="1300">

---

The `getYAxisOptions` method is called within `getYAxis`. It returns a list of yAxis options that are either aggregates that are graphable or aggregate equations.

```tsx
  getYAxisOptions(): SelectValue<string>[] {
    // Make option set and add the default options in.
    return uniqBy(
      this.getAggregateFields()
        // Only include aggregates that make sense to be graphable (eg. not string or date)
        .filter(
          (field: Field) =>
            isLegalYAxisType(aggregateOutputType(field.field)) ||
            isAggregateEquation(field.field)
        )
        .map((field: Field) => ({
          label: isEquation(field.field) ? getEquation(field.field) : field.field,
          value: field.field,
        }))
        .concat(CHART_AXIS_OPTIONS),
      'value'
    );
  }
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
