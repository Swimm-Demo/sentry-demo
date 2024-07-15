---
title: Exploring Event Handling in Components
---
In the sentry-demo repository, 'Events' refer to the data structures that capture and encapsulate the details of an occurrence in the system. They are used to track errors, performance issues, and other significant incidents within the application. The 'Events' are represented as objects with various properties and methods that provide context about the event, such as the organization, project, and group associated with the event, as well as whether the event is shared or not.

The 'EventEntries' component in the 'events' directory is a key part of handling events in the application. It takes in an 'Event' object as a prop and uses it to render different components based on the event's properties. For example, if the event is not available, it renders a 'Latest Event Not Available' message. If the event has user feedback or tags, it renders the corresponding components with the relevant data.

The 'Event' object is also used in various other components within the 'events' directory. For instance, in the 'EventContexts' component, it is used to get the context metadata and display the known and unknown context data. In the 'EventEntries' component, it is used to partition the entries for replay and render different sections of the event details.

In summary, 'Events' in the sentry-demo repository are crucial for tracking and displaying detailed information about significant occurrences in the system. They are used extensively across various components within the 'events' directory to render the appropriate data and functionality based on the event's properties.

<SwmSnippet path="/static/app/components/events/eventEntries.tsx" line="54">

---

# EventEntries Component

The 'EventEntries' component in the 'events' directory is a key part of handling events in the application. It takes in an 'Event' object as a prop and uses it to render different components based on the event's properties. For example, if the event is not available, it renders a 'Latest Event Not Available' message. If the event has user feedback or tags, it renders the corresponding components with the relevant data.

```tsx
function EventEntries({
  organization,
  project,
  event,
  group,
  className,
  isShare = false,
  showTagSummary = true,
}: Props) {
  const orgSlug = organization.slug;
  const projectSlug = project.slug;
  const orgFeatures = organization?.features ?? [];

  if (!event) {
    return (
      <LatestEventNotAvailable>
        <h3>{t('Latest Event Not Available')}</h3>
      </LatestEventNotAvailable>
    );
  }

```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/contexts/utils.tsx" line="432">

---

# EventContexts Component

In the 'EventContexts' component, the 'Event' object is used to get the context metadata and display the known and unknown context data.

```tsx
}: {
  contextType: string;
  contextValue: any;
  event: Event;
  location: Location;
  organization: Organization;
  project?: Project;
}): KeyValueListData {
  const meta = getContextMeta(event, contextType);

  if (KNOWN_PLATFORM_CONTEXTS.has(contextType)) {
    return [
      ...getKnownPlatformContextData({platform: contextType, data: contextValue, meta}),
      ...getUnknownPlatformContextData({platform: contextType, data: contextValue, meta}),
    ];
  }

  switch (contextType) {
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
