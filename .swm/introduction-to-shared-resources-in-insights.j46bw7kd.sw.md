---
title: Introduction to Shared Resources in Insights
---
Common in the Insights directory refers to a set of shared utilities, components, queries, and views that are used across different parts of the Insights feature. These shared resources help in maintaining consistency and reducing code duplication.

The utilities in the common directory provide various functionalities like handling date filters, tracking responses, retry handlers, and more. These utilities are used across different parts of the Insights feature to perform common tasks.

The components in the common directory are reusable UI elements used across the Insights feature. These include tables, charts, panels, and other UI elements.

The queries in the common directory are used to fetch data required by the Insights feature. These queries interact with the backend services to fetch and update data.

The views in the common directory are reusable views or pages used across the Insights feature. These views are composed of the common components and utilities, and are used to display data fetched by the common queries.

<SwmSnippet path="/static/app/views/insights/common/queries/useReleases.tsx" line="18">

---

# Common Utilities

Here, the 'useOrganization' utility from Common is used to get the current organization. This is an example of how utilities in Common are used.

```tsx
  const organization = useOrganization();
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/insights/common/queries/useTransactions.tsx" line="18">

---

# Common Queries

In this example, the 'useDiscoverQuery' from Common is used to fetch data for the Transactions view. This is an example of how queries in Common are used.

```tsx
export function useTransactions(eventIDs: string[], referrer = 'use-transactions') {
  const location = useLocation();
  const {slug} = useOrganization();

  const eventView = EventView.fromNewQueryWithLocation(
    {
      fields: ['id', 'timestamp', 'project.name', 'transaction.duration', 'trace'],
      name: 'Transactions',
      version: 2,
      query: `id:[${eventIDs.join(',')}]`,
    },
    location
  );

  const enabled = Boolean(eventIDs.length);

  const response = useDiscoverQuery({
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
