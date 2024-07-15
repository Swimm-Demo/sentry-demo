---
title: Understanding Event Contexts
---
In the Sentry demo repository, 'Contexts' refer to additional contextual data associated with an Event. This data can be related to the app, device, OS, or even the user. The 'Contexts' are used to provide more detailed information about the state of the system or the environment when the event occurred. This can be particularly useful for debugging purposes.

The 'Contexts' are organized in a hierarchical structure within the 'Events' directory. Each type of context (app, device, user, etc.) has its own dedicated sub-directory under the 'contexts' directory. Each of these sub-directories contains the necessary files to handle the specific type of context data.

The 'EventContexts' function in 'index.tsx' is a key part of handling 'Contexts'. It retrieves the 'contexts' and 'sdk' from the event, and uses the 'contexts' to determine if the OpenTelemetry (otel) SDK is being used. If it is, it sets certain attributes on the root span of the Sentry transaction associated with the event.

The 'ContextDataSection' function in 'contextDataSection.tsx' is responsible for rendering the context data associated with an event. It uses the 'getOrderedContextItems' function to retrieve the context items in a specific order, and then maps over these items to render a 'ContextCard' for each item.

The 'ContextCard' function in 'contextCard.tsx' is used to render a single context item. It takes in the type, alias, and value of the context item, as well as the event, group, and project associated with the context item.

The 'utils.tsx' file contains the 'CONTEXT_TYPES' constant, which maps context types to their corresponding context data handlers. These handlers are responsible for processing the context data of their respective types.

<SwmSnippet path="/static/app/components/events/contexts/index.tsx" line="71">

---

# EventContexts Function

The 'EventContexts' function in 'index.tsx' is a key part of handling 'Contexts'. It retrieves the 'contexts' and 'sdk' from the event, and uses the 'contexts' to determine if the OpenTelemetry (otel) SDK is being used. If it is, it sets certain attributes on the root span of the Sentry transaction associated with the event.

```tsx
export function EventContexts({event, group}: Props) {
  const {projects} = useProjects();
  const project = projects.find(p => p.id === event.projectID);
  const {contexts, sdk} = event;

  const usingOtel = useCallback(() => contexts.otel !== undefined, [contexts.otel]);

  useEffect(() => {
    const span = Sentry.getActiveSpan();
    if (usingOtel() && span) {
      const rootSpan = Sentry.getRootSpan(span);
      rootSpan.setAttribute('otel_event', true);
      rootSpan.setAttribute('otel_sdk', sdk?.name);
      rootSpan.setAttribute('otel_sdk_version', sdk?.version);
    }
  }, [usingOtel, sdk]);

  return <ContextDataSection event={event} group={group} project={project} />;
}
```

---

</SwmSnippet>

# ContextDataSection Function

The 'ContextDataSection' function in 'contextDataSection.tsx' is responsible for rendering the context data associated with an event. It uses the 'getOrderedContextItems' function to retrieve the context items in a specific order, and then maps over these items to render a 'ContextCard' for each item.

# ContextCard Function

The 'ContextCard' function in 'contextCard.tsx' is used to render a single context item. It takes in the type, alias, and value of the context item, as well as the event, group, and project associated with the context item.

<SwmSnippet path="/static/app/components/events/contexts/utils.tsx" line="94">

---

# CONTEXT_TYPES Constant

The 'utils.tsx' file contains the 'CONTEXT_TYPES' constant, which maps context types to their corresponding context data handlers. These handlers are responsible for processing the context data of their respective types.

```tsx
const CONTEXT_TYPES = {
  default: DefaultContext,
  app: AppEventContext,
  device: DeviceEventContext,
  memory_info: MemoryInfoEventContext,
  browser: BrowserEventContext,
  os: OperatingSystemEventContext,
  unity: UnityEventContext,
  runtime: RuntimeEventContext,
  user: UserEventContext,
  gpu: GPUEventContext,
  trace: TraceEventContext,
  threadpool_info: ThreadPoolInfoEventContext,
  state: StateEventContext,
  profile: ProfileEventContext,
  replay: ReplayEventContext,
  // 'redux.state' will be replaced with more generic context called 'state'
  'redux.state': ReduxContext,
  // 'ThreadPool Info' will be replaced with 'threadpool_info' but
  // we want to keep it here for now so it works for existing versions
  'ThreadPool Info': ThreadPoolInfoEventContext,
```

---

</SwmSnippet>

# Context Handling Functions

This section will cover the main functions related to handling 'Contexts' in the Sentry demo repository.

<SwmSnippet path="/static/app/components/events/contexts/index.tsx" line="71">

---

## EventContexts

The 'EventContexts' function retrieves the 'contexts' and 'sdk' from the event, and uses the 'contexts' to determine if the OpenTelemetry (otel) SDK is being used. If it is, it sets certain attributes on the root span of the Sentry transaction associated with the event.

```tsx
export function EventContexts({event, group}: Props) {
  const {projects} = useProjects();
  const project = projects.find(p => p.id === event.projectID);
  const {contexts, sdk} = event;

  const usingOtel = useCallback(() => contexts.otel !== undefined, [contexts.otel]);

  useEffect(() => {
    const span = Sentry.getActiveSpan();
    if (usingOtel() && span) {
      const rootSpan = Sentry.getRootSpan(span);
      rootSpan.setAttribute('otel_event', true);
      rootSpan.setAttribute('otel_sdk', sdk?.name);
      rootSpan.setAttribute('otel_sdk_version', sdk?.version);
    }
  }, [usingOtel, sdk]);

  return <ContextDataSection event={event} group={group} project={project} />;
}
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/contexts/contextDataSection.tsx" line="19">

---

## ContextDataSection

The 'ContextDataSection' function is responsible for rendering the context data associated with an event. It uses the 'getOrderedContextItems' function to retrieve the context items in a specific order, and then maps over these items to render a 'ContextCard' for each item.

```tsx
export default function ContextDataSection({
  event,
  group,
  project,
}: ContextDataSectionProps) {
  const cards = getOrderedContextItems(event).map(
    ({alias, type, value: contextValue}) => (
      <ContextCard
        key={alias}
        type={type}
        alias={alias}
        value={contextValue}
        event={event}
        group={group}
        project={project}
      />
    )
  );

  return (
    <EventDataSection
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/contexts/contextCard.tsx" line="74">

---

## ContextCard

The 'ContextCard' function is used to render a single context item. It takes in the type, alias, and value of the context item, as well as the event, group, and project associated with the context item.

```tsx
export default function ContextCard({
  alias,
  event,
  type,
  project,
  value = {},
}: ContextCardProps) {
  const location = useLocation();
  const organization = useOrganization();
  if (isEmptyObject(value)) {
    return null;
  }
  const meta = getContextMeta(event, type === 'default' ? alias : type);

  const contextItems = getFormattedContextData({
    event,
    contextValue: value,
    contextType: type,
    organization,
    project,
    location,
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
