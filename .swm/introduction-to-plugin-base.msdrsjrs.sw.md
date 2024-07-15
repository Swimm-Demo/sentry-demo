---
title: Introduction to Plugin Base
---
Base in the Plugins directory refers to the foundational classes and functions that are used to build and manage plugins in the Sentry application. It provides the core functionalities that all plugins can inherit and use. This includes the Plugin and Plugin2 classes, which are the primary classes that all plugins extend from. These classes provide a set of methods such as 'enable' and 'set_option' that control the behavior of the plugins.

The 'enable' method is used to activate a plugin. It sets the 'enabled' option to True for a given plugin. The 'set_option' method is used to update the value of an option in the plugin's keyspace. If a project is passed to this method, it will limit the scope to that project's keyspace.

The Base also includes a set of utility functions and classes such as 'PluggableViewMixin', 'Response', and 'default_plugin_config' that are used across different plugins. These utilities provide common functionalities that are shared among different plugins.

<SwmSnippet path="/src/sentry/plugins/base/v1.py" line="29">

---

# Base in Plugin Development

This is the `__new__` method in the Plugin class. It is used to create a new instance of the class. If the class does not have a 'title', 'slug', or 'logger' attribute, it adds them. The 'title' is set to the name of the class, the 'slug' is a lowercased version of the 'title' with spaces replaced by hyphens, and the 'logger' is a logger instance with the name set to 'sentry.plugins.{slug}'.

```python
    def __new__(cls, name, bases, attrs):
        new_cls: type[IPlugin] = type.__new__(cls, name, bases, attrs)  # type: ignore[assignment]
        if IPlugin in bases:
            return new_cls
        if not hasattr(new_cls, "title"):
            new_cls.title = new_cls.__name__
        if not hasattr(new_cls, "slug"):
            new_cls.slug = new_cls.title.replace(" ", "-").lower()
        if "logger" not in attrs:
            new_cls.logger = logging.getLogger(f"sentry.plugins.{new_cls.slug}")
        return new_cls
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/plugins/base/v2.py" line="27">

---

# Base in Plugin2 Development

This is the `__new__` method in the Plugin2 class. It works similarly to the `__new__` method in the Plugin class, but it creates an instance of the Plugin2 class instead.

```python
    def __new__(cls, name, bases, attrs):
        new_cls: type[IPlugin2] = type.__new__(cls, name, bases, attrs)  # type: ignore[assignment]
        if IPlugin2 in bases:
            return new_cls
        if not hasattr(new_cls, "title"):
            new_cls.title = new_cls.__name__
        if not hasattr(new_cls, "slug"):
            new_cls.slug = new_cls.title.replace(" ", "-").lower()
        if not hasattr(new_cls, "logger"):
            new_cls.logger = logging.getLogger(f"sentry.plugins.{new_cls.slug}")
        return new_cls
```

---

</SwmSnippet>

# Base Functions

The 'Base' in the 'sentry' application refers to the foundational classes and functions that are used to build and manage plugins.

<SwmSnippet path="/src/sentry/plugins/base/v1.py" line="29">

---

## **new**

The `__new__` function is a special method in Python that's called when an instance of the class is created. Here, it's used to create a new instance of a plugin class, set its title and slug, and assign a logger to it.

```python
    def __new__(cls, name, bases, attrs):
        new_cls: type[IPlugin] = type.__new__(cls, name, bases, attrs)  # type: ignore[assignment]
        if IPlugin in bases:
            return new_cls
        if not hasattr(new_cls, "title"):
            new_cls.title = new_cls.__name__
        if not hasattr(new_cls, "slug"):
            new_cls.slug = new_cls.title.replace(" ", "-").lower()
        if "logger" not in attrs:
            new_cls.logger = logging.getLogger(f"sentry.plugins.{new_cls.slug}")
        return new_cls
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/plugins/base/v1.py" line="3">

---

## Plugin

The `Plugin` class is the primary class that all plugins extend from. It provides a set of methods that control the behavior of the plugins.

```python
__all__ = ("Plugin",)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/plugins/base/v2.py" line="459">

---

## Plugin2

The `Plugin2` class is similar to the `Plugin` class but it's used for the second version of the plugins.

```python
__all__ = ("Plugin2",)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/plugins/base/structs.py" line="6">

---

## Annotation

The `Annotation` class is used to create an annotation object with a label, url, and description.

```python
class Annotation:
    def __init__(self, label, url=None, description=None):
        self.label = label
        self.url = url
        self.description = description
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/plugins/base/structs.py" line="13">

---

## Notification

The `Notification` class is used to create a notification object with an event and a set of rules.

```python
class Notification:
    def __init__(self, event, rule=None, rules=None):
        if rule and not rules:
            rules = [rule]

        self.event = event
        self.rules = rules or []

    @property
    def rule(self):
        warnings.warn(
            "Notification.rule is deprecated. Switch to Notification.rules.", DeprecationWarning
        )
        return self.rules[0]
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
