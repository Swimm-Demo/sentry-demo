---
title: Getting Started with the Plugin System
---
Plugins in Sentry are modules that extend the functionality of the application. They are managed by the PluginManager, which provides methods to register and unregister plugins. Plugins can be enabled or disabled for specific projects, and this is managed through the 'enable' and 'set_option' methods in the Plugin base classes. The 'enable' method sets the 'enabled' option to True, while 'set_option' updates the value of an option in the plugin's keyspace. The configuration of plugins is handled by the 'configure' method, which uses the 'default_plugin_config' function. This function uses the plugin's configuration form to update the plugin's options.

There are two versions of the Plugin base class, v1 and v2, which have slightly different methods and properties. For example, the 'get_conf_form' method in v2 can return different forms depending on whether a project is specified or not. The 'default_plugin_options' function is used to get the initial values for the configuration form, and it uses methods like 'get_conf_form' and 'get_conf_key' from the Plugin base class.

Some plugins are hidden, as specified by the HIDDEN_PLUGINS constant. These plugins are not visible in the user interface. An example of a specific plugin is the WebHooksPlugin, which triggers outgoing HTTP POST requests from Sentry. This plugin, like others, is registered using the 'register' method of the PluginManager.

<SwmSnippet path="/src/sentry/plugins/base/__init__.py" line="10">

---

# Plugin Registration

Plugins are registered using the 'register' method of the PluginManager. The PluginManager is accessed through the 'plugins' constant.

```python
plugins = PluginManager()
register = plugins.register
unregister = plugins.unregister
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/plugins/base/v2.py" line="164">

---

# Plugin Enabling

Plugins are enabled for a specific project using the 'enable' method. This method sets the 'enabled' option to True.

```python
    def enable(self, project=None, user=None):
        """Enable the plugin."""
        self.set_option("enabled", True, project, user)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/plugins/base/v2.py" line="439">

---

# Plugin Configuration

The configuration of plugins is handled by the 'configure' method. This method uses the 'default_plugin_config' function to update the plugin's options based on its configuration form.

```python
        """

    def configure(self, project, request):
        """Configures the plugin."""
        return default_plugin_config(self, project, request)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/plugins/base/v2.py" line="114">

---

# Hidden Plugins

Some plugins are hidden, as specified by the HIDDEN_PLUGINS constant. These plugins are not visible in the user interface.

```python
    def is_hidden(self):
        """
        Should this plugin be hidden in the UI

        We use this to hide plugins as they are replaced with integrations.
        """
        return self.slug in HIDDEN_PLUGINS
```

---

</SwmSnippet>

# Plugin Endpoints

Understanding Plugin Endpoints

<SwmSnippet path="/src/sentry/plugins/endpoints.py" line="14">

---

## PluginProjectEndpoint

The `PluginProjectEndpoint` class is a custom endpoint for handling HTTP requests related to a project in a plugin. It defines methods for handling GET and POST requests. The `_handle` method is used to process the request using the appropriate view from the plugin.

```python
class PluginProjectEndpoint(ProjectEndpoint):
    plugin = None
    view = None

    def _handle(self, request: Request, project, *args, **kwargs):
        if self.view is None:
            return Response(status=405)
        return self.view(request, project, *args, **kwargs)

    def get(self, request: Request, project, *args, **kwargs) -> Response:
        return self._handle(request, project, *args, **kwargs)

    def post(self, request: Request, project, *args, **kwargs) -> Response:
        return self._handle(request, project, *args, **kwargs)

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/plugins/endpoints.py" line="37">

---

## PluginGroupEndpoint

The `PluginGroupEndpoint` class is a custom endpoint for handling HTTP requests related to a group in a plugin. Similar to `PluginProjectEndpoint`, it defines methods for handling GET and POST requests. The `_handle` method is used to process the request using the appropriate view from the plugin.

```python
@region_silo_endpoint
class PluginGroupEndpoint(GroupEndpoint):
    publish_status = {
        "GET": ApiPublishStatus.PRIVATE,
        "POST": ApiPublishStatus.PRIVATE,
    }
    plugin = None
    view = None

    def _handle(self, request: Request, group, *args, **kwargs):
        if self.view is None:
            return Response(status=405)

        GroupMeta.objects.populate_cache([group])

        return self.view(request, group, *args, **kwargs)

    def get(self, request: Request, group, *args, **kwargs) -> Response:
        return self._handle(request, group, *args, **kwargs)

    def post(self, request: Request, group, *args, **kwargs) -> Response:
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
