---
title: Understanding the 'put' Function and Its Flow
---
<SwmSnippet path="/src/sentry/api/endpoints/internal/feature_flags.py" line="35">

---

# Understanding the 'put' Function

The `put` function is the starting point of the flow. It is responsible for handling HTTP PUT requests. It checks if the Sentry instance is self-hosted, then retrieves the feature flags from the request data. It opens a configuration file, updates the feature flags in the file, and then calls the `configure` function.

```python
    def put(self, request: Request) -> Response:
        if not settings.SENTRY_SELF_HOSTED:
            return Response("You are not self-hosting Sentry.", status=403)

        data = request.data.keys()
        valid_feature_flags = [flag for flag in data if SENTRY_EARLY_FEATURES.get(flag, False)]
        _, py, yml = discover_configs()
        # Open the file for reading and writing
        with open(py, "r+") as file:
            lines = file.readlines()
            # print(lines)
            for valid_flag in valid_feature_flags:
                match_found = False
                new_string = (
                    f'\nSENTRY_FEATURES["{valid_flag}"]={request.data.get(valid_flag,False)}\n'
                )
                # Search for the string match and update lines
                for i, line in enumerate(lines):
                    if valid_flag in line:
                        match_found = True
                        lines[i] = new_string
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/runner/settings.py" line="53">

---

# The 'configure' Function

The `configure` function is called by the `put` function. It sets up the environment given two different config files. It checks if the files exist, sets up the environment variables, and then calls the `initialize_app` function.

```python
def configure(
    ctx: click.Context | None, py: str, yaml: str | None, skip_service_validation: bool = False
) -> None:
    """
    Given the two different config files, set up the environment.

    NOTE: Will only execute once, so it's safe to call multiple times.
    """
    global __installed
    if __installed:
        return

    # Make sure that our warnings are always displayed.
    warnings.filterwarnings("default", "", Warning, r"^sentry")

    # Add in additional mimetypes that are useful for our static files
    # which aren't common in default system registries
    import mimetypes

    for type, ext in (
        ("application/json", "map"),
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/runner/initializer.py" line="306">

---

# The 'initialize_app' Function

The `initialize_app` function is called by the `configure` function. It sets up the application, validates the settings, and then calls the `validate_snuba` and `configure_sdk` functions.

```python
def initialize_app(config: dict[str, Any], skip_service_validation: bool = False) -> None:
    settings = config["settings"]

    # Just reuse the integration app for Single Org / Self-Hosted as
    # it doesn't make much sense to use 2 separate apps for SSO and
    # integration.
    if settings.SENTRY_SINGLE_ORGANIZATION:
        options_mapper.update(
            {
                "github-app.client-id": "GITHUB_APP_ID",
                "github-app.client-secret": "GITHUB_API_SECRET",
            }
        )

    bootstrap_options(settings, config["options"])

    logging.raiseExceptions = settings.DEBUG

    configure_structlog()

    # Commonly setups don't correctly configure themselves for production envs
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/runner/initializer.py" line="620">

---

# The 'validate_snuba' Function

The `validate_snuba` function is called by the `initialize_app` function. It checks if the Snuba service is correctly configured and raises an error if it is not.

```python
def validate_snuba() -> None:
    """
    Make sure everything related to Snuba is in sync.

    This covers a few cases:

    * When you have features related to Snuba, you must also
      have Snuba fully configured correctly to continue.
    * If you have Snuba specific search/tagstore/tsdb backends,
      you must also have a Snuba compatible eventstream backend
      otherwise no data will be written into Snuba.
    * If you only have Snuba related eventstream, yell that you
      probably want the other backends otherwise things are weird.
    """
    if not settings.DEBUG:
        return

    has_all_snuba_required_backends = (
        settings.SENTRY_SEARCH
        in (
            "sentry.search.snuba.EventsDatasetSnubaSearchBackend",
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/client.py" line="119">

---

# The 'put' Function

The 'put' function is a method in the client class that makes a PUT request. It's a wrapper around the 'request' method, specifying 'PUT' as the HTTP method.

```python
    def put(self, *args, **kwargs):
        return self.request("PUT", *args, **kwargs)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/metrics.py" line="101">

---

# The 'incr' Function

The 'incr' function is used to increment a metric. It takes a key, an optional instance, optional tags, an amount to increment by, and a sample rate. If the metrics system hasn't started yet, it starts it and then puts the metric increment in a queue.

```python
    def incr(
        self,
        key: str,
        instance: str | None = None,
        tags: Tags | None = None,
        amount: int = 1,
        sample_rate: float = settings.SENTRY_METRICS_SAMPLE_RATE,
    ) -> None:
        if not self._started:
            self._start()
        self.q.put((key, instance, tags, amount, sample_rate))
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/sdk.py" line="237">

---

# The 'patch_transport_for_instrumentation' Function

The 'patch_transport_for_instrumentation' function is used to patch transport functions to add metrics. It takes a transport and a transport name, patches the '\_send_request' method of the transport to increment a metric before sending the request, and then returns the patched transport.

```python
# Patches transport functions to add metrics to improve resolution around events sent to our ingest.
# Leaving this in to keep a permanent measurement of sdk requests vs ingest.
def patch_transport_for_instrumentation(transport, transport_name):
    _send_request = transport._send_request
    if _send_request:

        def patched_send_request(*args, **kwargs):
            metrics.incr(f"internal.sent_requests.{transport_name}.events")
            return _send_request(*args, **kwargs)

        transport._send_request = patched_send_request
    return transport
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/sdk.py" line="275">

---

# The 'configure_sdk' Function

The 'configure_sdk' function is used to configure the Sentry SDK. It defines a 'MultiplexingTransport' class with methods for capturing envelopes and events, recording lost events, checking health, and flushing. It also defines a '\_capture_anything' method that sends events to Sentry.

```python
def configure_sdk():
    """
    Setup and initialize the Sentry SDK.
    """
    sdk_options, dsns = _get_sdk_options()

    internal_project_key = get_project_key()

    if dsns.sentry4sentry:
        transport = make_transport(get_options(dsn=dsns.sentry4sentry, **sdk_options))
        sentry4sentry_transport = patch_transport_for_instrumentation(transport, "upstream")
    else:
        sentry4sentry_transport = None

    if dsns.sentry_saas:
        transport = make_transport(get_options(dsn=dsns.sentry_saas, **sdk_options))
        sentry_saas_transport = patch_transport_for_instrumentation(transport, "relay")
    elif settings.IS_DEV and not settings.SENTRY_USE_RELAY:
        sentry_saas_transport = None
    elif internal_project_key and internal_project_key.dsn_private:
        transport = make_transport(get_options(dsn=internal_project_key.dsn_private, **sdk_options))
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/sdk.py" line="256">

---

# The '\_get_sdk_options' Function

The '\_get_sdk_options' function is used to get the options for the Sentry SDK. It copies the SDK configuration from the settings, sets some options, and gets the DSNs for Sentry and Relay from the configuration.

```python
def _get_sdk_options() -> tuple[SdkConfig, Dsns]:
    sdk_options = settings.SENTRY_SDK_CONFIG.copy()
    sdk_options["send_client_reports"] = True
    sdk_options["traces_sampler"] = traces_sampler
    sdk_options["before_send_transaction"] = before_send_transaction
    sdk_options["before_send"] = before_send
    sdk_options["release"] = (
        f"backend@{sdk_options['release']}" if "release" in sdk_options else None
    )

    # Modify SENTRY_SDK_CONFIG in your deployment scripts to specify your desired DSN
    dsns = Dsns(
        sentry4sentry=sdk_options.pop("dsn", None),
        sentry_saas=sdk_options.pop("relay_dsn", None),
    )

    return sdk_options, dsns
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/client.py" line="119">

---

# Understanding the 'put' flow

The 'put' function is a method in the client class that makes a PUT request. It's a part of the HTTP client interface and is used to update a resource on the server.

```python
    def put(self, *args, **kwargs):
        return self.request("PUT", *args, **kwargs)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/sdk.py" line="334">

---

# \_capture_anything function

The '\_capture_anything' function is a part of the Sentry SDK. It's responsible for capturing events, errors, and transactions and sending them to Sentry. It also handles metrics and sampling.

```python
        def _capture_anything(self, method_name, *args, **kwargs):
            # Sentry4Sentry (upstream) should get the event first because
            # it is most isolated from the sentry installation.
            if sentry4sentry_transport:
                metrics.incr("internal.captured.events.upstream")
                # TODO(mattrobenolt): Bring this back safely.
                # from sentry import options
                # install_id = options.get('sentry:install-id')
                # if install_id:
                #     event.setdefault('tags', {})['install-id'] = install_id
                s4s_args = args
                # We want to control whether we want to send metrics at the s4s upstream.
                if (
                    not settings.SENTRY_SDK_UPSTREAM_METRICS_ENABLED
                    and method_name == "capture_envelope"
                ):
                    args_list = list(args)
                    envelope = args_list[0]
                    # We filter out all the statsd envelope items, which contain custom metrics sent by the SDK.
                    # unless we allow them via a separate sample rate.
                    safe_items = [
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/metrics.py" line="101">

---

# incr function

The 'incr' function is used to increment a metric. It's used within the '\_capture_anything' function to increment internal metrics related to captured and uncaptured events.

```python
    def incr(
        self,
        key: str,
        instance: str | None = None,
        tags: Tags | None = None,
        amount: int = 1,
        sample_rate: float = settings.SENTRY_METRICS_SAMPLE_RATE,
    ) -> None:
        if not self._started:
            self._start()
        self.q.put((key, instance, tags, amount, sample_rate))
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/services.py" line="44">

---

# copy function

The 'copy' function is used to create a copy of the current context. This is useful when you want to modify the context for a specific operation without affecting the original context.

```python
    def copy(self) -> Context:
        return Context(self.request, self.backends.copy())
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/frame/context.tsx" line="66">

---

# Context function

The 'Context' function is a React component that renders the context of a frame in the Sentry UI. It displays source code, variables, registers, and assembly related to the frame.

```tsx
function Context({
  hasContextVars = false,
  hasContextSource = false,
  hasContextRegisters = false,
  isExpanded = false,
  hasAssembly = false,
  emptySourceNotation = false,
  registers,
  frame,
  event,
  className,
  frameMeta,
  registersMeta,
  platform,
}: Props) {
  const organization = useOrganization();

  const {projects} = useProjects();
  const project = useMemo(
    () => projects.find(p => p.id === event.projectID),
    [projects, event]
```

---

</SwmSnippet>

```mermaid
graph TD;
subgraph src/sentry/runner
  put:::mainFlowStyle --> configure:::mainFlowStyle
end
subgraph src/sentry/runner
  configure:::mainFlowStyle --> initialize_app:::mainFlowStyle
end
subgraph src/sentry/runner
  initialize_app:::mainFlowStyle --> validate_snuba
end
subgraph src/sentry/utils
  initialize_app:::mainFlowStyle --> configure_sdk:::mainFlowStyle
end
subgraph src/sentry/utils
  configure_sdk:::mainFlowStyle --> patch_transport_for_instrumentation
end
subgraph src/sentry/utils
  configure_sdk:::mainFlowStyle --> incr
end
subgraph src/sentry/utils
  configure_sdk:::mainFlowStyle --> _get_sdk_options
end
subgraph src/sentry/utils
  configure_sdk:::mainFlowStyle --> _capture_anything:::mainFlowStyle
end
subgraph src/sentry/utils
  _capture_anything:::mainFlowStyle --> incr
end
subgraph src/sentry/utils
  _capture_anything:::mainFlowStyle --> copy:::mainFlowStyle
end
subgraph static/app
  copy:::mainFlowStyle --> Context:::mainFlowStyle
end
subgraph static/app
  Context:::mainFlowStyle --> useProjects
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
subgraph src/sentry/runner
  put:::mainFlowStyle --> configure:::mainFlowStyle
end
subgraph src/sentry/runner
  configure:::mainFlowStyle --> initialize_app:::mainFlowStyle
end
subgraph src/sentry/runner
  initialize_app:::mainFlowStyle --> validate_snuba
end
subgraph src/sentry
  initialize_app:::mainFlowStyle --> configure_sdk:::mainFlowStyle
end
subgraph src/sentry
  configure_sdk:::mainFlowStyle --> zrm0a[...]
end
subgraph src/sentry/runner
  validate_snuba --> add
end

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

<SwmSnippet path="/src/sentry/api/endpoints/internal/feature_flags.py" line="35">

---

# The `put` Function

The `put` function is the starting point of the flow. It is responsible for handling HTTP PUT requests. It checks if the Sentry instance is self-hosted, then retrieves the feature flags from the request data. It opens a configuration file, updates the feature flags in the file, and then calls the `configure` function.

```python
    def put(self, request: Request) -> Response:
        if not settings.SENTRY_SELF_HOSTED:
            return Response("You are not self-hosting Sentry.", status=403)

        data = request.data.keys()
        valid_feature_flags = [flag for flag in data if SENTRY_EARLY_FEATURES.get(flag, False)]
        _, py, yml = discover_configs()
        # Open the file for reading and writing
        with open(py, "r+") as file:
            lines = file.readlines()
            # print(lines)
            for valid_flag in valid_feature_flags:
                match_found = False
                new_string = (
                    f'\nSENTRY_FEATURES["{valid_flag}"]={request.data.get(valid_flag,False)}\n'
                )
                # Search for the string match and update lines
                for i, line in enumerate(lines):
                    if valid_flag in line:
                        match_found = True
                        lines[i] = new_string
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/runner/settings.py" line="53">

---

# The `configure` Function

The `configure` function is called by the `put` function. It sets up the environment given two different config files. It checks if the files exist, sets up the environment variables, and then calls the `initialize_app` function.

```python
def configure(
    ctx: click.Context | None, py: str, yaml: str | None, skip_service_validation: bool = False
) -> None:
    """
    Given the two different config files, set up the environment.

    NOTE: Will only execute once, so it's safe to call multiple times.
    """
    global __installed
    if __installed:
        return

    # Make sure that our warnings are always displayed.
    warnings.filterwarnings("default", "", Warning, r"^sentry")

    # Add in additional mimetypes that are useful for our static files
    # which aren't common in default system registries
    import mimetypes

    for type, ext in (
        ("application/json", "map"),
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/runner/initializer.py" line="306">

---

# The `initialize_app` Function

The `initialize_app` function is called by the `configure` function. It sets up the application, validates the settings, and then calls the `validate_snuba` and `configure_sdk` functions.

```python
def initialize_app(config: dict[str, Any], skip_service_validation: bool = False) -> None:
    settings = config["settings"]

    # Just reuse the integration app for Single Org / Self-Hosted as
    # it doesn't make much sense to use 2 separate apps for SSO and
    # integration.
    if settings.SENTRY_SINGLE_ORGANIZATION:
        options_mapper.update(
            {
                "github-app.client-id": "GITHUB_APP_ID",
                "github-app.client-secret": "GITHUB_API_SECRET",
            }
        )

    bootstrap_options(settings, config["options"])

    logging.raiseExceptions = settings.DEBUG

    configure_structlog()

    # Commonly setups don't correctly configure themselves for production envs
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/runner/initializer.py" line="620">

---

# The `validate_snuba` Function

The `validate_snuba` function is called by the `initialize_app` function. It checks if the Snuba service is correctly configured and raises an error if it is not.

```python
def validate_snuba() -> None:
    """
    Make sure everything related to Snuba is in sync.

    This covers a few cases:

    * When you have features related to Snuba, you must also
      have Snuba fully configured correctly to continue.
    * If you have Snuba specific search/tagstore/tsdb backends,
      you must also have a Snuba compatible eventstream backend
      otherwise no data will be written into Snuba.
    * If you only have Snuba related eventstream, yell that you
      probably want the other backends otherwise things are weird.
    """
    if not settings.DEBUG:
        return

    has_all_snuba_required_backends = (
        settings.SENTRY_SEARCH
        in (
            "sentry.search.snuba.EventsDatasetSnubaSearchBackend",
```

---

</SwmSnippet>

Now, lets zoom into this section of the flow:

```mermaid
graph TD;
subgraph src/sentry/utils
  configure_sdk:::mainFlowStyle --> patch_transport_for_instrumentation
end
subgraph src/sentry/utils
  configure_sdk:::mainFlowStyle --> incr
end
subgraph src/sentry/utils
  configure_sdk:::mainFlowStyle --> _get_sdk_options
end
subgraph src/sentry/utils
  configure_sdk:::mainFlowStyle --> _capture_anything:::mainFlowStyle
end
subgraph src/sentry/utils
  _capture_anything:::mainFlowStyle --> 3l5wh[...]
end
subgraph src/sentry/api/client.py
  incr --> put
end
subgraph src/sentry/utils
  patch_transport_for_instrumentation --> incr
end

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

<SwmSnippet path="/src/sentry/api/client.py" line="119">

---

# The 'put' Function

The 'put' function is a method in the client class that makes a PUT request. It's a wrapper around the 'request' method, specifying 'PUT' as the HTTP method.

```python
    def put(self, *args, **kwargs):
        return self.request("PUT", *args, **kwargs)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/metrics.py" line="101">

---

# The 'incr' Function

The 'incr' function is used to increment a metric. It takes a key, an optional instance, optional tags, an amount to increment by, and a sample rate. If the metrics system hasn't started yet, it starts it and then puts the metric increment in a queue.

```python
    def incr(
        self,
        key: str,
        instance: str | None = None,
        tags: Tags | None = None,
        amount: int = 1,
        sample_rate: float = settings.SENTRY_METRICS_SAMPLE_RATE,
    ) -> None:
        if not self._started:
            self._start()
        self.q.put((key, instance, tags, amount, sample_rate))
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/sdk.py" line="237">

---

# The 'patch_transport_for_instrumentation' Function

The 'patch_transport_for_instrumentation' function is used to patch transport functions to add metrics. It takes a transport and a transport name, patches the '\_send_request' method of the transport to increment a metric before sending the request, and then returns the patched transport.

```python
# Patches transport functions to add metrics to improve resolution around events sent to our ingest.
# Leaving this in to keep a permanent measurement of sdk requests vs ingest.
def patch_transport_for_instrumentation(transport, transport_name):
    _send_request = transport._send_request
    if _send_request:

        def patched_send_request(*args, **kwargs):
            metrics.incr(f"internal.sent_requests.{transport_name}.events")
            return _send_request(*args, **kwargs)

        transport._send_request = patched_send_request
    return transport
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/sdk.py" line="275">

---

# The 'configure_sdk' Function

The 'configure_sdk' function is used to configure the Sentry SDK. It defines a 'MultiplexingTransport' class with methods for capturing envelopes and events, recording lost events, checking health, and flushing. It also defines a '\_capture_anything' method that sends events to Sentry.

```python
def configure_sdk():
    """
    Setup and initialize the Sentry SDK.
    """
    sdk_options, dsns = _get_sdk_options()

    internal_project_key = get_project_key()

    if dsns.sentry4sentry:
        transport = make_transport(get_options(dsn=dsns.sentry4sentry, **sdk_options))
        sentry4sentry_transport = patch_transport_for_instrumentation(transport, "upstream")
    else:
        sentry4sentry_transport = None

    if dsns.sentry_saas:
        transport = make_transport(get_options(dsn=dsns.sentry_saas, **sdk_options))
        sentry_saas_transport = patch_transport_for_instrumentation(transport, "relay")
    elif settings.IS_DEV and not settings.SENTRY_USE_RELAY:
        sentry_saas_transport = None
    elif internal_project_key and internal_project_key.dsn_private:
        transport = make_transport(get_options(dsn=internal_project_key.dsn_private, **sdk_options))
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/sdk.py" line="256">

---

# The '\_get_sdk_options' Function

The '\_get_sdk_options' function is used to get the options for the Sentry SDK. It copies the SDK configuration from the settings, sets some options, and gets the DSNs for Sentry and Relay from the configuration.

```python
def _get_sdk_options() -> tuple[SdkConfig, Dsns]:
    sdk_options = settings.SENTRY_SDK_CONFIG.copy()
    sdk_options["send_client_reports"] = True
    sdk_options["traces_sampler"] = traces_sampler
    sdk_options["before_send_transaction"] = before_send_transaction
    sdk_options["before_send"] = before_send
    sdk_options["release"] = (
        f"backend@{sdk_options['release']}" if "release" in sdk_options else None
    )

    # Modify SENTRY_SDK_CONFIG in your deployment scripts to specify your desired DSN
    dsns = Dsns(
        sentry4sentry=sdk_options.pop("dsn", None),
        sentry_saas=sdk_options.pop("relay_dsn", None),
    )

    return sdk_options, dsns
```

---

</SwmSnippet>

Now, lets zoom into this section of the flow:

```mermaid
graph TD;
subgraph src/sentry/utils
  _capture_anything:::mainFlowStyle --> incr
end
subgraph src/sentry/utils
  _capture_anything:::mainFlowStyle --> copy:::mainFlowStyle
end
subgraph static/app/components/events/interfaces/frame/context.tsx
  copy:::mainFlowStyle --> Context:::mainFlowStyle
end
subgraph src/sentry/api/client.py
  incr --> put
end

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

<SwmSnippet path="/src/sentry/api/client.py" line="119">

---

# Understanding the 'put' flow

The 'put' function is a method in the client class that makes a PUT request. It's a part of the HTTP client interface and is used to update a resource on the server.

```python
    def put(self, *args, **kwargs):
        return self.request("PUT", *args, **kwargs)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/sdk.py" line="334">

---

# \_capture_anything function

The '\_capture_anything' function is a part of the Sentry SDK. It's responsible for capturing events, errors, and transactions and sending them to Sentry. It also handles metrics and sampling.

```python
        def _capture_anything(self, method_name, *args, **kwargs):
            # Sentry4Sentry (upstream) should get the event first because
            # it is most isolated from the sentry installation.
            if sentry4sentry_transport:
                metrics.incr("internal.captured.events.upstream")
                # TODO(mattrobenolt): Bring this back safely.
                # from sentry import options
                # install_id = options.get('sentry:install-id')
                # if install_id:
                #     event.setdefault('tags', {})['install-id'] = install_id
                s4s_args = args
                # We want to control whether we want to send metrics at the s4s upstream.
                if (
                    not settings.SENTRY_SDK_UPSTREAM_METRICS_ENABLED
                    and method_name == "capture_envelope"
                ):
                    args_list = list(args)
                    envelope = args_list[0]
                    # We filter out all the statsd envelope items, which contain custom metrics sent by the SDK.
                    # unless we allow them via a separate sample rate.
                    safe_items = [
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/metrics.py" line="101">

---

# incr function

The 'incr' function is used to increment a metric. It's used within the '\_capture_anything' function to increment internal metrics related to captured and uncaptured events.

```python
    def incr(
        self,
        key: str,
        instance: str | None = None,
        tags: Tags | None = None,
        amount: int = 1,
        sample_rate: float = settings.SENTRY_METRICS_SAMPLE_RATE,
    ) -> None:
        if not self._started:
            self._start()
        self.q.put((key, instance, tags, amount, sample_rate))
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/utils/services.py" line="44">

---

# copy function

The 'copy' function is used to create a copy of the current context. This is useful when you want to modify the context for a specific operation without affecting the original context.

```python
    def copy(self) -> Context:
        return Context(self.request, self.backends.copy())
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/components/events/interfaces/frame/context.tsx" line="66">

---

# Context function

The 'Context' function is a React component that renders the context of a frame in the Sentry UI. It displays source code, variables, registers, and assembly related to the frame.

```tsx
function Context({
  hasContextVars = false,
  hasContextSource = false,
  hasContextRegisters = false,
  isExpanded = false,
  hasAssembly = false,
  emptySourceNotation = false,
  registers,
  frame,
  event,
  className,
  frameMeta,
  registersMeta,
  platform,
}: Props) {
  const organization = useOrganization();

  const {projects} = useProjects();
  const project = useMemo(
    () => projects.find(p => p.id === event.projectID),
    [projects, event]
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
