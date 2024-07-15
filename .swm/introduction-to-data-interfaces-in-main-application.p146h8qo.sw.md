---
title: Introduction to Data Interfaces in Main Application
---
Interfaces in the main application are structured representations of data, which may render differently than the default metadata in an event. They are defined as classes with various properties and methods that manipulate the data they hold. The 'Interface' class in 'src/sentry/interfaces/base.py' is the base class for all other interfaces in the application.

The 'Interface' class has properties like 'score', 'display_score', 'ephemeral', 'grouping_variants', and 'datapath'. It also has methods for getting the path of the interface, checking equality of two instances, getting and setting state, and converting the interface to Python and JSON formats among others.

There are also specific types of interfaces in the application, like the 'Spans' interface in 'src/sentry/interfaces/spans.py'. This interface contains a list of 'Span' interfaces and has methods to convert the interface to Python and JSON formats.

Interfaces are used throughout the application in various ways. For example, they are used in 'src/sentry/mediators/mediator.py' to define the main functions of mediators, in 'src/sentry/issues/event.schema.json' to describe the Sentry SDK and its configuration, and in 'src/sentry/utils/json.py' to deal with empty containers and missing values.

<SwmSnippet path="/src/sentry/interfaces/base.py" line="61">

---

# Base Interface

The 'Interface' class in 'src/sentry/interfaces/base.py' is the base class for all other interfaces in the application. It has properties like 'score', 'display_score', 'ephemeral', 'grouping_variants', and 'datapath'. It also has methods for getting the path of the interface, checking equality of two instances, getting and setting state, and converting the interface to Python and JSON formats among others.

```python
class Interface:
    """
    An interface is a structured representation of data, which may
    render differently than the default ``extra`` metadata in an event.
    """

    score = 0
    display_score: ClassVar[int | None] = None
    ephemeral = False
    grouping_variants = ["default"]
    datapath = None

    def __init__(self, **data):
        self._data = data or {}

    @classproperty
    def path(cls):
        """The 'path' of the interface which is the root key in the data."""
        return cls.__name__.lower()

    @classproperty
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/interfaces/spans.py" line="50">

---

# Spans Interface

The 'Spans' interface in 'src/sentry/interfaces/spans.py' is an example of a specific type of interface. This interface contains a list of 'Span' interfaces and has methods to convert the interface to Python and JSON formats.

```python
class Spans(Interface):
    """
    Contains a list of Span interfaces
    """

    display_score = 1950
    score = 1950
    path = "spans"

    @classmethod
    def to_python(cls, data, **kwargs):
        spans = [Span.to_python_subpath(data, [i], **kwargs) for i, span in enumerate(data)]
        return super().to_python({"spans": spans}, **kwargs)

    def __iter__(self):
        return iter(self.spans)

    def to_json(self):
        return [span.to_json() for span in self]
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/mediators/mediator.py" line="72">

---

# Usage of Interfaces

Interfaces are used throughout the application in various ways. For example, they are used in 'src/sentry/mediators/mediator.py' to define the main functions of mediators.

```python
    Interface:
        Mediators have two main functions you should be aware of.
```

---

</SwmSnippet>

# Interface and Spans

This section will cover the 'Interface' and 'Spans' classes, which are part of the interfaces in the Sentry application.

<SwmSnippet path="/src/sentry/interfaces/base.py" line="61">

---

## Interface

The 'Interface' class in 'src/sentry/interfaces/base.py' is the base class for all other interfaces in the application. It has properties like 'score', 'display_score', 'ephemeral', 'grouping_variants', and 'datapath'. It also has methods for getting the path of the interface, checking equality of two instances, getting and setting state, and converting the interface to Python and JSON formats among others.

```python
class Interface:
    """
    An interface is a structured representation of data, which may
    render differently than the default ``extra`` metadata in an event.
    """

    score = 0
    display_score: ClassVar[int | None] = None
    ephemeral = False
    grouping_variants = ["default"]
    datapath = None

    def __init__(self, **data):
        self._data = data or {}

    @classproperty
    def path(cls):
        """The 'path' of the interface which is the root key in the data."""
        return cls.__name__.lower()

    @classproperty
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/interfaces/spans.py" line="50">

---

## Spans

The 'Spans' interface in 'src/sentry/interfaces/spans.py' contains a list of 'Span' interfaces and has methods to convert the interface to Python and JSON formats. It is used to store context specific information, such as the details of a specific span in a trace of a transaction.

```python
class Spans(Interface):
    """
    Contains a list of Span interfaces
    """

    display_score = 1950
    score = 1950
    path = "spans"

    @classmethod
    def to_python(cls, data, **kwargs):
        spans = [Span.to_python_subpath(data, [i], **kwargs) for i, span in enumerate(data)]
        return super().to_python({"spans": spans}, **kwargs)

    def __iter__(self):
        return iter(self.spans)

    def to_json(self):
        return [span.to_json() for span in self]
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
