---
title: Exploring Network Details
---
Network in the sentry-demo repository refers to the functionality of capturing and displaying network-related information during the replay of events. This is primarily handled through the `NetworkDetails` function, which is responsible for rendering the network details tab in the replay interface.

The `NetworkDetails` function uses the `useUrlParams` utility to manage URL parameters, specifically the 'n_detail_tab' parameter which determines the currently active tab in the network details interface. The function also checks if the necessary props such as 'item' and 'projectId' are available, and if not, it returns null, preventing the component from rendering.

The `NetworkDetailsContent` function is responsible for rendering the content of the network details tab. It uses the `useOrganization` hook to retrieve the current organization, and tracks analytics events when the network tab changes. The content displayed depends on the currently active tab, which is determined by the 'visibleTab' prop.

The `NetworkDetailsTabs` function is responsible for rendering the tabs in the network details interface. It uses the `useUrlParams` utility to manage the 'n_detail_tab' URL parameter, which determines the currently active tab.

The `useNetworkFilters` function is used to manage the filters applied to the network frames displayed in the network details tab. It provides functions to retrieve the available method types, resource types, and status types, and to set the current filters and search term.

<SwmSnippet path="/static/app/views/replays/detail/network/useNetworkFilters.tsx" line="61">

---

# Network Filters

The `useNetworkFilters` function is used to manage the filters applied to the network frames displayed in the network details tab. It provides functions to retrieve the available method types, resource types, and status types, and to set the current filters and search term.

```tsx
function useNetworkFilters({networkFrames}: Options): Return {
  const {setFilter, query} = useFiltersInLocationQuery<FilterFields>();

  const method = useMemo(() => decodeList(query.f_n_method), [query.f_n_method]);
  const status = useMemo(() => decodeList(query.f_n_status), [query.f_n_status]);
  const type = useMemo(() => decodeList(query.f_n_type), [query.f_n_type]);
  const searchTerm = decodeScalar(query.f_n_search, '').toLowerCase();

  // Need to clear Network Details URL params when we filter, otherwise you can
  // get into a state where it is trying to load details for a non fetch/xhr
  // request.
  const setFilterAndClearDetails = useCallback(
    arg => {
      setFilter({
        ...arg,
        n_detail_row: undefined,
        n_detail_tab: undefined,
      });
    },
    [setFilter]
  );
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/replays/detail/network/useSortNetwork.tsx" line="27">

---

# Network Sorting

The `useSortNetwork` function is used to manage the sorting of network frames. It uses the `useUrlParams` utility to manage URL parameters related to sorting, and provides a function to handle sorting based on different fields.

```tsx
function useSortNetwork({items}: Opts) {
  const {getParamValue: getSortAsc, setParamValue: setSortAsc} = useUrlParams(
    's_n_asc',
    DEFAULT_ASC
  );
  const {getParamValue: getSortBy, setParamValue: setSortBy} = useUrlParams(
    's_n_by',
    DEFAULT_BY
  );
  const {setParamValue: setDetailRow} = useUrlParams('n_detail_row', '');

  const sortAsc = getSortAsc();
  const sortBy = getSortBy();

  const sortConfig = useMemo(
    () =>
      ({
        asc: sortAsc === 'true',
        by: sortBy,
        getValue: SortStrategies[sortBy],
      }) as SortConfig,
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/replays/detail/network/networkFilters.tsx" line="9">

---

# Network Frames

`networkFrames` is a prop that contains the network frames to be displayed in the network details tab. It is used in the `NetworkFilters` function to generate the filters for the network frames.

```tsx
  networkFrames: undefined | unknown[];
} & ReturnType<typeof useNetworkFilters>;
```

---

</SwmSnippet>

# Network Functions

This section will cover the main functions related to the network functionality in the sentry-demo repository.

<SwmSnippet path="/static/app/views/replays/detail/network/details/index.tsx" line="19">

---

## NetworkDetails Function

The `NetworkDetails` function is responsible for rendering the network details tab in the replay interface. It uses the `useUrlParams` utility to manage URL parameters, specifically the 'n_detail_tab' parameter which determines the currently active tab in the network details interface. The function also checks if the necessary props such as 'item' and 'projectId' are available, and if not, it returns null, preventing the component from rendering.

```tsx
function NetworkDetails({
  isHeld,
  isSetup,
  item,
  onClose,
  onDoubleClick,
  onMouseDown,
  projectId,
  startTimestampMs,
}: Props) {
  const {getParamValue: getDetailTab} = useUrlParams('n_detail_tab', 'details');

  if (!item || !projectId) {
    return null;
  }

  const visibleTab = getDetailTab() as TabKey;

  return (
    <Fragment>
      <DetailsSplitDivider
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/replays/detail/network/details/content.tsx" line="30">

---

## NetworkDetailsContent Function

The `NetworkDetailsContent` function is responsible for rendering the content of the network details tab. It uses the `useOrganization` hook to retrieve the current organization, and tracks analytics events when the network tab changes. The content displayed depends on the currently active tab, which is determined by the 'visibleTab' prop.

```tsx
  const output = getOutputType(props);

  const organization = useOrganization();
  useEffect(() => {
    trackAnalytics('replay.details-network-tab-changed', {
      is_sdk_setup: isSetup,
      organization,
      output,
      resource_method: getFrameMethod(item),
      resource_status: String(getFrameStatus(item)),
      resource_type: item.op,
      tab: visibleTab,
    });
  }, [isSetup, item, organization, output, visibleTab]);

  switch (visibleTab) {
    case 'request':
      return (
        <OverflowFluidHeight>
          <SectionList>
            <QueryParamsSection {...props} />
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/replays/detail/network/details/tabs.tsx" line="39">

---

## NetworkDetailsTabs Function

The `NetworkDetailsTabs` function is responsible for rendering the tabs in the network details interface. It uses the `useUrlParams` utility to manage the 'n_detail_tab' URL parameter, which determines the currently active tab.

```tsx
          }}
        >
          {label}
        </ListLink>
      ))}
    </ScrollableTabs>
  );
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/replays/detail/network/useNetworkFilters.tsx" line="27">

---

## useNetworkFilters Function

The `useNetworkFilters` function is used to manage the filters applied to the network frames displayed in the network details tab. It provides functions to retrieve the available method types, resource types, and status types, and to set the current filters and search term.

```tsx
};

type Options = {
  networkFrames: SpanFrame[];
};

const UNKNOWN_STATUS = 'unknown';

type Return = {
  getMethodTypes: () => NetworkSelectOption[];
  getResourceTypes: () => NetworkSelectOption[];
  getStatusTypes: () => NetworkSelectOption[];
  items: SpanFrame[];
  searchTerm: string;
  selectValue: string[];
  setFilters: (val: NetworkSelectOption[]) => void;
  setSearchTerm: (searchTerm: string) => void;
};

const FILTERS = {
  method: (item: SpanFrame, method: string[]) =>
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
