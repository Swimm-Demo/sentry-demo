---
title: Getting started with Rule Actions
---
Actions in Sentry's rules system refer to the operations that are performed when a rule is triggered. They are represented by the EventAction class and its subclasses. These actions can range from sending notifications, creating tickets in integrated services, to interacting with plugins and more.

The EventAction class is an abstract base class that defines the structure and behavior of actions in Sentry. It includes methods like 'after' which is executed after a rule matches an event. This method is expected to yield instances of CallbackFuture, which are then passed into a callback function.

The EventAction class is extended by other classes to create specific actions. For example, the IntegrationEventAction class is used for actions that involve integrations with external services.

Actions are instantiated and managed by the instantiate_action function. This function takes a rule and an action, and returns an instance of the action class. If the action class is not registered, it logs a warning and returns None.

The actions are part of the rule data and changes to them are tracked. The [utils.py](http://utils.py) file contains functions to generate a diff of changes when a rule is edited. This includes changes to the actions of the rule.

<SwmSnippet path="/src/sentry/rules/actions/__init__.py" line="1">

---

# EventAction Class

The EventAction class is an abstract base class that defines the structure and behavior of actions in Sentry. It includes methods like 'after' which is executed after a rule matches an event. This method is expected to yield instances of CallbackFuture, which are then passed into a callback function.

```python
from sentry.rules.actions.base import EventAction
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/rules/actions/integrations/base.py" line="21">

---

# IntegrationEventAction Class

The EventAction class is extended by other classes to create specific actions. For example, the IntegrationEventAction class is used for actions that involve integrations with external services.

```python
class IntegrationEventAction(EventAction, abc.ABC):
    """Intermediate abstract class to help DRY some event actions code."""

    @property
    @abc.abstractmethod
    def prompt(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def provider(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def integration_key(self) -> str:
        pass

    def is_enabled(self) -> bool:
        enabled: bool = bool(self.get_integrations())
        return enabled
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/rules/actions/__init__.py" line="1">

---

# Instantiate Action

Actions are instantiated and managed by the instantiate_action function. This function takes a rule and an action, and returns an instance of the action class. If the action class is not registered, it logs a warning and returns None.

```python
from sentry.rules.actions.base import EventAction
from sentry.rules.actions.integrations import IntegrationEventAction
from sentry.rules.actions.integrations.create_ticket import (
    IntegrationNotifyServiceForm,
    TicketEventAction,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/rules/actions/integrations/base.py" line="14">

---

# Rule Changes Tracking

The actions are part of the rule data and changes to them are tracked. The [utils.py](http://utils.py) file contains functions to generate a diff of changes when a rule is edited. This includes changes to the actions of the rule.

```python
from sentry.models.organization import OrganizationStatus
from sentry.models.rule import Rule
from sentry.rules.actions import EventAction

INTEGRATION_KEY = "integration"
```

---

</SwmSnippet>

# Actions in Sentry Rules System

This section provides an overview of the main functions related to actions in the Sentry rules system.

<SwmSnippet path="/src/sentry/rules/actions/base.py" line="35">

---

## EventAction

The EventAction class is an abstract base class that defines the structure and behavior of actions in Sentry. It includes methods like 'after' which is executed after a rule matches an event. This method is expected to yield instances of CallbackFuture, which are then passed into a callback function.

```python
class EventAction(RuleBase, abc.ABC):
    rule_type = "action/event"

    @abc.abstractmethod
    def after(
        self, event: GroupEvent, notification_uuid: str | None = None
    ) -> Generator[CallbackFuture, None, None]:
        """
        Executed after a Rule matches.

        Should yield CallBackFuture instances which will then be passed into
        the given callback.

        See the notification implementation for example usage.


        >>> def after(self, state):
        >>>     yield self.future(self.print_results)
        >>>
        >>> def print_results(self, event, futures):
        >>>     print('Got futures for Event {}'.format(event.id))
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/rules/actions/integrations/base.py" line="21">

---

## IntegrationEventAction

The IntegrationEventAction class is a subclass of EventAction and is used for actions that involve integrations with external services. It includes methods like 'is_enabled', 'get_integration_name', 'get_integrations', 'get_integration_id', and 'get_integration' which are used to interact with the integrated services.

```python
class IntegrationEventAction(EventAction, abc.ABC):
    """Intermediate abstract class to help DRY some event actions code."""

    @property
    @abc.abstractmethod
    def prompt(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def provider(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def integration_key(self) -> str:
        pass

    def is_enabled(self) -> bool:
        enabled: bool = bool(self.get_integrations())
        return enabled
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/rules/actions/sentry_apps/base.py" line="11">

---

## SentryAppEventAction

The SentryAppEventAction class is another subclass of EventAction. It is an abstract class that ensures that actions in SENTRY_APP_ACTIONS have all required methods. It includes abstract methods like 'actionType', 'get_custom_actions', and 'self_validate'.

```python
class SentryAppEventAction(EventAction, abc.ABC):
    """Abstract class to ensure that actions in SENTRY_APP_ACTIONS have all required methods"""

    @property
    @abc.abstractmethod
    def actionType(self) -> str:
        pass

    @abc.abstractmethod
    def get_custom_actions(self, project: Project) -> Sequence[Mapping[str, Any]]:
        pass

    @abc.abstractmethod
    def self_validate(self) -> None:
        pass
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/rules/actions/base.py" line="16">

---

## instantiate_action

The instantiate_action function is used to create an instance of an action class. It takes a rule and an action, and returns an instance of the action class. If the action class is not registered, it logs a warning and returns None.

```python
def instantiate_action(rule: Rule, action, rule_fire_history: RuleFireHistory | None = None):
    from sentry.rules import rules

    action_id = action["id"]
    action_cls = rules.get(action_id)
    if action_cls is None:
        logger.warning("Unregistered action %r", action["id"])
        return None

    action_inst = action_cls(
        rule.project, data=action, rule=rule, rule_fire_history=rule_fire_history
    )
    if not isinstance(action_inst, EventAction):
        logger.warning("Unregistered action %r", action["id"])
        return None

    return action_inst
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/rules/actions/utils.py" line="14">

---

## Action Changes Tracking

The [utils.py](http://utils.py) file contains functions to generate a diff of changes when a rule is edited. This includes changes to the actions of the rule. Functions like 'get_updated_rule_data', 'check_value_changed', 'generate_diff_labels', 'get_frequency_label', 'convert_data', and 'get_changed_data' are used for this purpose.

```python
def get_updated_rule_data(rule: Rule) -> dict[str, Any]:
    rule_data = dict(rule.data)
    if rule.environment_id:
        rule_data["environment_id"] = rule.environment_id
    if rule.owner_user_id or rule.owner_team_id:
        rule_data["owner"] = Actor.from_id(user_id=rule.owner_user_id, team_id=rule.owner_team_id)
    rule_data["label"] = rule.label
    return rule_data


def check_value_changed(
    present_state: dict[str, Any], prior_state: dict[str, Any], key: str, word: str
) -> str | None:
    if present_state.get(key) != prior_state.get(key):
        old_value = prior_state.get(key)
        new_value = present_state.get(key)
        return f"Changed {word} from '{old_value}' to '{new_value}'"
    return None


def generate_diff_labels(
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
