---
title: Understanding FlamegraphTreeTable
---
<SwmSnippet path="/static/app/components/profiling/flamegraph/flamegraphDrawer/flamegraphTreeTable.tsx" line="58">

---

# FlamegraphTreeTable

The `FlamegraphTreeTable` function is a component that renders a table representation of a flamegraph. It takes in various properties such as the tree structure, expanded nodes, and callbacks for user interactions. It uses the `useVirtualizedTree` hook to manage the state of the table, including sorting, scrolling, and node expansion.

```tsx
export function FlamegraphTreeTable({
  tree,
  expanded,
  referenceNode,
  canvasPoolManager,
  canvasScheduler,
  getFrameColor,
  recursion,
  flamegraph,
  onBottomUpClick,
  onTopDownClick,
}: FlamegraphTreeTableProps) {
  const [scrollContainerRef, setFixedScrollContainerRef] =
    useState<HTMLDivElement | null>(null);
  const [dynamicScrollContainerRef, setDynamicScrollContainerRef] =
    useState<HTMLDivElement | null>(null);

  const [sort, setSort] = useState<'total weight' | 'self weight' | 'name'>(
    'total weight'
  );
  const [direction, setDirection] = useState<'asc' | 'desc'>('desc');
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/profiling/hooks/useVirtualizedTree/useVirtualizedTree.tsx" line="125">

---

# useVirtualizedTree

`useVirtualizedTree` is a custom hook that manages the state of a virtualized tree structure. It handles actions such as scrolling, clicking, and expanding tree nodes. It also manages the rendering of rows in the tree.

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

`renderRow` is a method that renders a row in the table. It takes in the row data, row index, column order, and table metadata. It maps over the column order to render each cell in the row. It also handles cell actions such as clicking and hovering.

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

`handleCellAction` is a function that handles actions performed on a cell in the table. It takes in the row data and the column. Depending on the action, it updates the query and navigates to a new view.

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

`getResultsViewUrlTarget` is a method that generates the URL target for the results view. It takes in the organization slug and a boolean indicating whether it's the homepage. It returns an object containing the pathname and query parameters.

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

`generateQueryStringObject` is a method that generates a query string object from the event view. It includes fields such as id, name, field, sort, environment, project, query, yAxis, dataset, display, topEvents, and interval.

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

The `generateExpandedConditions` function is called within `getExpandedResults`. It generates additional conditions based on the fields in an EventView and a data row or event.

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

The `getYAxisOptions` method is called within `getYAxis`. It returns a list of yAxis options based on the aggregate fields in the EventView.

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
  FlamegraphTreeTable:::mainFlowStyle --> useVirtualizedTree:::mainFlowStyle
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
  FlamegraphTreeTable:::mainFlowStyle --> useVirtualizedTree:::mainFlowStyle
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
  getExpandedResults:::mainFlowStyle --> 1sop6[...]
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

<SwmSnippet path="/static/app/components/profiling/flamegraph/flamegraphDrawer/flamegraphTreeTable.tsx" line="58">

---

# FlamegraphTreeTable

The `FlamegraphTreeTable` function is a component that renders a table representation of a flamegraph. It takes in various properties such as the tree structure, expanded nodes, and callbacks for user interactions. It uses the `useVirtualizedTree` hook to manage the state of the table, including sorting, scrolling, and node expansion.

```tsx
export function FlamegraphTreeTable({
  tree,
  expanded,
  referenceNode,
  canvasPoolManager,
  canvasScheduler,
  getFrameColor,
  recursion,
  flamegraph,
  onBottomUpClick,
  onTopDownClick,
}: FlamegraphTreeTableProps) {
  const [scrollContainerRef, setFixedScrollContainerRef] =
    useState<HTMLDivElement | null>(null);
  const [dynamicScrollContainerRef, setDynamicScrollContainerRef] =
    useState<HTMLDivElement | null>(null);

  const [sort, setSort] = useState<'total weight' | 'self weight' | 'name'>(
    'total weight'
  );
  const [direction, setDirection] = useState<'asc' | 'desc'>('desc');
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/utils/profiling/hooks/useVirtualizedTree/useVirtualizedTree.tsx" line="125">

---

# useVirtualizedTree

`useVirtualizedTree` is a custom hook that manages the state of a virtualized tree structure. It handles actions such as scrolling, clicking, and expanding tree nodes. It also manages the rendering of rows in the tree.

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

`renderRow` is a method that renders a row in the table. It takes in the row data, row index, column order, and table metadata. It maps over the column order to render each cell in the row. It also handles cell actions such as clicking and hovering.

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

`handleCellAction` is a function that handles actions performed on a cell in the table. It takes in the row data and the column. Depending on the action, it updates the query and navigates to a new view.

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

`getResultsViewUrlTarget` is a method that generates the URL target for the results view. It takes in the organization slug and a boolean indicating whether it's the homepage. It returns an object containing the pathname and query parameters.

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

`generateQueryStringObject` is a method that generates a query string object from the event view. It includes fields such as id, name, field, sort, environment, project, query, yAxis, dataset, display, topEvents, and interval.

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

# FlamegraphTreeTable Flow

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

The `generateExpandedConditions` function is called within `getExpandedResults`. It generates additional conditions based on the fields in an EventView and a data row or event.

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

The `getYAxisOptions` method is called within `getYAxis`. It returns a list of yAxis options based on the aggregate fields in the EventView.

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
