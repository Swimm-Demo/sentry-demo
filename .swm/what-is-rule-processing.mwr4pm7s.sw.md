---
title: What is Rule Processing
---
Rules in the Sentry application are a set of conditions and actions that are applied to events. They are used to automate responses to specific types of events. For instance, a rule can be set to notify a developer when an event of a certain level occurs.

The 'apply' function in the '[processor.py](http://processor.py)' file is a key part of rule processing. It applies rules to unresolved issues. The function fetches rules, checks if they are snoozed, and applies them if they are not.

The 'apply_delayed' function in the 'delayed_processing.py' file is another important part of rule processing. It fetches rules, groups, and events from the Redis buffer, evaluates the 'slow' conditions in a bulk snuba query, and fires them if they pass.

The 'RuleBase' class in the '[base.py](http://base.py)' file is the base class for all rules. It provides methods for getting rule options, validating forms, rendering labels, and more.

The 'EventState' class in the '[base.py](http://base.py)' file encapsulates the state of an event when a rule is applied. It includes information about whether the event is new, a regression, has reappeared, and more.

The 'EventAction' class in the 'actions/base.py' file is the base class for all rule actions. It provides methods for executing actions after a rule matches.

The 'LevelCondition' class in the 'conditions/level.py' file is a rule condition that checks the level of an event. It provides methods for checking if an event passes the condition and rendering the condition label.

<SwmSnippet path="/src/sentry/rules/processing/processor.py" line="393">

---

# Applying Rules

The 'apply' function is a key part of rule processing. It applies rules to unresolved issues. The function fetches rules, checks if they are snoozed, and applies them if they are not.

```python
    def apply(
        self,
    ) -> Collection[tuple[Callable[[GroupEvent, Sequence[RuleFuture]], None], list[RuleFuture]]]:
        # we should only apply rules on unresolved issues
        if not self.event.group.is_unresolved():
            return {}.values()

        self.grouped_futures.clear()
        rules = self.get_rules()
        snoozed_rules = RuleSnooze.objects.filter(rule__in=rules, user_id=None).values_list(
            "rule", flat=True
        )
        rule_statuses = bulk_get_rule_status(rules, self.group, self.project)
        for rule in rules:
            if rule.id not in snoozed_rules:
                self.apply_rule(rule, rule_statuses[rule.id])

        return self.grouped_futures.values()
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/rules/processing/delayed_processing.py" line="407">

---

# Delayed Rule Application

The 'apply_delayed' function is another important part of rule processing. It fetches rules, groups, and events from the Redis buffer, evaluates the 'slow' conditions in a bulk snuba query, and fires them if they pass.

```python
def apply_delayed(project_id: int, *args: Any, **kwargs: Any) -> None:
    """
    Grab rules, groups, and events from the Redis buffer, evaluate the "slow" conditions in a bulk snuba query, and fire them if they pass
    """
    # STEP 1: Fetch the rulegroup_to_event_data mapping for the project from redis
    project = Project.objects.get_from_cache(id=project_id)
    rulegroup_to_event_data = buffer.backend.get_hash(
        model=Project, field={"project_id": project.id}
    )
    logger.info(
        "delayed_processing.rulegroupeventdata",
        extra={"rulegroupdata": rulegroup_to_event_data, "project_id": project_id},
    )

    # STEP 2: Map each rule to the groups that must be checked for that rule.
    rules_to_groups = get_rules_to_groups(rulegroup_to_event_data)

    # STEP 3: Fetch the Rule models we need to check
    alert_rules_qs = Rule.objects.filter(id__in=list(rules_to_groups.keys()))
    snoozed_rules = set(
        RuleSnooze.objects.filter(rule__in=alert_rules_qs, user_id=None).values_list(
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/rules/base.py" line="16">

---

# Rule Base Class

The 'RuleBase' class is the base class for all rules. It provides methods for getting rule options, validating forms, rendering labels, and more.

```python
from sentry.types.rules import RuleFuture

if TYPE_CHECKING:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/rules/base.py" line="204">

---

# Event State

The 'EventState' class encapsulates the state of an event when a rule is applied. It includes information about whether the event is new, a regression, has reappeared, and more.

```python

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/rules/actions/base.py" line="14">

---

# Rule Actions

The 'EventAction' class is the base class for all rule actions. It provides methods for executing actions after a rule matches.

```python


def instantiate_action(rule: Rule, action, rule_fire_history: RuleFireHistory | None = None):
    from sentry.rules import rules

    action_id = action["id"]
    action_cls = rules.get(action_id)
    if action_cls is None:
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/rules/conditions/level.py" line="81">

---

# Level Condition

The 'LevelCondition' class is a rule condition that checks the level of an event. It provides methods for checking if an event passes the condition and rendering the condition label.

```python
            return self._passes(level)
        except (TypeError, KeyError):
            return False

```

---

</SwmSnippet>

# Rules Endpoints

Endpoints related to Rules

<SwmSnippet path="/src/sentry/rules/history/endpoints/project_rule_group_history.py" line="58">

---

## ProjectRuleGroupHistoryIndexEndpoint

The `ProjectRuleGroupHistoryIndexEndpoint` is a GET endpoint that retrieves the group firing history for an issue alert. It takes the organization ID, project ID, and issue rule ID as parameters. The endpoint fetches the rule groups paginated and returns a response with the serialized results.

```python
class ProjectRuleGroupHistoryIndexEndpoint(RuleEndpoint):
    publish_status = {
        "GET": ApiPublishStatus.EXPERIMENTAL,
    }

    @extend_schema(
        operation_id="Retrieve a Group Firing History for an Issue Alert",
        parameters=[
            GlobalParams.ORG_ID_OR_SLUG,
            GlobalParams.PROJECT_ID_OR_SLUG,
            IssueAlertParams.ISSUE_RULE_ID,
        ],
        responses={
            200: RuleGroupHistorySerializer,
            401: RESPONSE_UNAUTHORIZED,
            403: RESPONSE_FORBIDDEN,
            404: RESPONSE_NOT_FOUND,
        },
    )
    def get(self, request: Request, project: Project, rule: Rule) -> Response:
        per_page = self.get_per_page(request)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/rules/history/endpoints/project_rule_stats.py" line="41">

---

## ProjectRuleStatsIndexEndpoint

The `ProjectRuleStatsIndexEndpoint` is a GET endpoint that retrieves firing stats for an issue alert rule for a given time range. It takes the organization ID, project ID, and issue rule ID as parameters. The endpoint fetches rule hourly stats and returns a response with the serialized results.

```python
class ProjectRuleStatsIndexEndpoint(RuleEndpoint):
    publish_status = {
        "GET": ApiPublishStatus.EXPERIMENTAL,
    }

    @extend_schema(
        operation_id="Retrieve Firing Starts for an Issue Alert Rule for a Given Time Range.",
        parameters=[
            GlobalParams.ORG_ID_OR_SLUG,
            GlobalParams.PROJECT_ID_OR_SLUG,
            IssueAlertParams.ISSUE_RULE_ID,
        ],
        responses={
            200: TimeSeriesValueSerializer,
            401: RESPONSE_UNAUTHORIZED,
            403: RESPONSE_FORBIDDEN,
            404: RESPONSE_NOT_FOUND,
        },
    )
    def get(self, request: Request, project: Project, rule: Rule) -> Response:
        """
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
