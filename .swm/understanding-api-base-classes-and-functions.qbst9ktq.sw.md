---
title: Understanding API Base Classes and Functions
---
Bases in the Api directory of the sentry-demo repository refers to the base classes and functions that are used across different modules of the API. These base classes and functions provide common functionality that can be inherited or used by other classes and functions in the API. For instance, the `OrganizationEndpoint` class in `organization.py` provides common methods and properties for handling requests related to organizations.

Another example is the `NoProjects` exception defined in `organization.py`. This exception is raised when a specific operation cannot proceed due to the absence of any projects. It's imported and used in various other modules like `organization_events.py`.

The `ProjectPermission` class in `project.py` is another base class that defines the permissions required for accessing project-related endpoints. This class is used in other modules like `group.py` and `event.py` to enforce access control.

In summary, the Bases in the Api directory provide a set of reusable classes and functions that encapsulate common behavior and functionality for handling API requests in the sentry-demo repository.

<SwmSnippet path="/src/sentry/api/bases/organization_events.py" line="18">

---

# Usage of Bases in organization_events.py

Here, the `NoProjects` exception from the bases module is imported and can be used in this file to handle scenarios where an operation cannot proceed due to the absence of any projects.

```python
from sentry.api.bases import NoProjects
from sentry.api.bases.organization import OrganizationEndpoint
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
