---
title: Getting Started with Event-Based Conditions
---
Conditions in the Sentry-Demo repository refer to the set of rules that determine how and when certain actions should be triggered. They are represented by the EventCondition class, which is an abstract base class for all event-based conditions.

These conditions are used throughout the codebase to handle different types of events. For instance, there are specific conditions for when an event reappears, when an event is first seen, when an event frequency reaches a certain threshold, and so on.

Each specific condition is defined in its own Python file and they all inherit from the EventCondition base class. This structure allows for a high degree of modularity and flexibility in defining new conditions.

The EventCondition class is part of the sentry.rules.conditions module, which is located in the src/sentry/rules/conditions directory. This module contains all the different conditions that can be applied to events.

<SwmSnippet path="/src/sentry/rules/conditions/base.py" line="1">

---

# EventCondition Base Class

The EventCondition class is the base class for all event-based conditions. It is imported in all the files where specific conditions are defined.

```python
import abc
from collections.abc import Sequence
from datetime import datetime
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/rules/conditions/reappeared_event.py" line="5">

---

# Specific Conditions

This is an example of a specific condition. The ReappearedEventCondition class inherits from the EventCondition base class and defines the condition for when an event reappears.

```python
from sentry.models.activity import Activity
from sentry.rules import EventState
from sentry.rules.conditions.base import EventCondition
from sentry.types.activity import ActivityType
from sentry.types.condition_activity import ConditionActivity, ConditionActivityType
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/rules/conditions/__init__.py" line="1">

---

# Conditions Module

The sentry.rules.conditions module, located in the src/sentry/rules/conditions directory, contains all the different conditions that can be applied to events.

```python
from .base import *  # NOQA

```

---

</SwmSnippet>

# Functions of Conditions

This section will cover the main functions of the conditions in Sentry-Demo, focusing on the LevelCondition and EveryEventCondition classes.

<SwmSnippet path="/src/sentry/rules/conditions/level.py" line="27">

---

## LevelCondition

The `LevelCondition` class is used to check the level of an event. It has a method `_passes` that checks if the level of the event matches the desired level based on the match type (equal, greater or equal, less or equal). The `passes` method uses `_passes` to determine if the condition is met for a given event.

```python
class LevelCondition(EventCondition):
    id = "sentry.rules.conditions.level.LevelCondition"
    form_cls = LevelEventForm
    label = "The event's level is {match} {level}"
    form_fields = {
        "level": {"type": "choice", "choices": list(LEVEL_CHOICES.items())},
        "match": {"type": "choice", "choices": list(MATCH_CHOICES.items())},
    }

    def _passes(self, level_name: str) -> bool:
        desired_level_raw = self.get_option("level")
        desired_match = self.get_option("match")

        if not (desired_level_raw and desired_match):
            return False

        desired_level = int(desired_level_raw)
        # Fetch the event level from the tags since event.level is
        # event.group.level which may have changed
        try:
            level: int = LOG_LEVELS_MAP[level_name]
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/rules/conditions/every_event.py" line="6">

---

## EveryEventCondition

The `EveryEventCondition` class represents a condition that passes for every event. It has a `passes` method that always returns True, meaning this condition will always be met for any event.

```python
class EveryEventCondition(EventCondition):
    id = "sentry.rules.conditions.every_event.EveryEventCondition"
    label = "The event occurs"

    def passes(self, event: GroupEvent, state: EventState) -> bool:
        return True

    def is_enabled(self) -> bool:
        return False
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
