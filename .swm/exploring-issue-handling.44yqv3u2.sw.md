---
title: Exploring Issue Handling
---
Issues in the main application of Sentry-demo refer to the errors or exceptions that are captured and tracked by the Sentry system. They are represented by the 'Issue' class and related classes in the 'sentry.issues' module. These classes provide the structure and methods for handling and manipulating issue data.

The 'Issue' class and related classes are defined in various files within the 'sentry.issues' module. For example, the 'IssueOccurrence' class in 'issue_occurrence.py' represents a specific occurrence of an issue, separate from an 'Event'. An 'Event' may have 0-M 'IssueOccurrences' associated with it, and each 'IssueOccurrence' is associated with one 'Event'.

The 'sentry.issues' module also includes services for handling issues, such as the 'issue_service' defined in 'services/issue/service.py'. These services provide functionality for operations on issues, such as creating, updating, and deleting issues.

In addition, the 'sentry.issues' module includes algorithms for forecasting and escalating issues, as seen in 'escalating_issues_alg.py' and '[ongoing.py](http://ongoing.py)'. These algorithms help in predicting future issue occurrences and escalating issues based on certain conditions.

<SwmSnippet path="/src/sentry/issues/issue_occurrence.py" line="67">

---

# IssueOccurrence Class

The 'IssueOccurrence' class represents a specific occurrence of an issue, separate from an 'Event'. An 'Event' may have 0-M 'IssueOccurrences' associated with it, and each 'IssueOccurrence' is associated with one 'Event'.

```python
class IssueOccurrence:
    """
    A class representing a specific occurrence of an issue. Separate to an `Event`. An `Event` may
    have 0-M `IssueOccurrences` associated with it, and each `IssueOccurrence` is associated with
    one `Event`.

    Longer term, we might change this relationship so that each `IssueOccurrence` is the primary
    piece of data that is passed around. It would have an `Event` associated with it.
    """

    id: str
    project_id: int
    # Event id pointing to an event in nodestore
    event_id: str
    fingerprint: Sequence[str]
    issue_title: str
    # Exact format not decided yet, but this will be a string regardless
    subtitle: str
    resource_id: str | None
    # Extra context around how the problem was detected. Used to display grouping information on
    # the issue details page, and will be available for use in UI customizations.
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/issues/services/issue/service.py" line="1">

---

# Issue Services

The 'sentry.issues' module includes services for handling issues, such as the 'issue_service'. These services provide functionality for operations on issues, such as creating, updating, and deleting issues.

```python
# Please do not use
#     from __future__ import annotations
# in modules such as this one where hybrid cloud data models or service classes are
# defined, because we want to reflect on type annotations and avoid forward references.


from abc import abstractmethod

from sentry.hybridcloud.rpc.resolvers import ByOrganizationId, ByOrganizationSlug, ByRegionName
from sentry.hybridcloud.rpc.service import RpcService, regional_rpc_method
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/issues/escalating_issues_alg.py" line="8">

---

# Issue Algorithms

The 'sentry.issues' module includes algorithms for forecasting and escalating issues. These algorithms help in predicting future issue occurrences and escalating issues based on certain conditions.

```python
class IssueForecast(TypedDict):
    forecasted_date: str
    forecasted_value: int


class GroupCount(TypedDict):
    intervals: list[str]
    data: list[int]


# standard values if no parameters are passed
@dataclass
class ThresholdVariables:
    std_multiplier: int = 5
    min_spike_multiplier: int = 5
    max_spike_multiplier: int = 8
    min_bursty_multiplier: int = 2
    max_bursty_multiplier: int = 5


standard_version = ThresholdVariables()
```

---

</SwmSnippet>

# Issue Handling Functions

This section discusses the main functions related to issues in the Sentry-demo application.

<SwmSnippet path="/src/sentry/issues/issue_occurrence.py" line="67">

---

## IssueOccurrence

The 'IssueOccurrence' class represents a specific occurrence of an issue. It includes various attributes such as the issue's ID, project ID, event ID, fingerprint, issue title, and more. It also includes methods for converting the occurrence data to a dictionary and creating an 'IssueOccurrence' instance from a dictionary.

```python
class IssueOccurrence:
    """
    A class representing a specific occurrence of an issue. Separate to an `Event`. An `Event` may
    have 0-M `IssueOccurrences` associated with it, and each `IssueOccurrence` is associated with
    one `Event`.

    Longer term, we might change this relationship so that each `IssueOccurrence` is the primary
    piece of data that is passed around. It would have an `Event` associated with it.
    """

    id: str
    project_id: int
    # Event id pointing to an event in nodestore
    event_id: str
    fingerprint: Sequence[str]
    issue_title: str
    # Exact format not decided yet, but this will be a string regardless
    subtitle: str
    resource_id: str | None
    # Extra context around how the problem was detected. Used to display grouping information on
    # the issue details page, and will be available for use in UI customizations.
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/issues/services/issue/service.py" line="58">

---

## issue_service

The 'issue_service' is an instance of the 'IssueService' class, which provides functionality for operations on issues, such as creating, updating, and deleting issues.

```python
issue_service = IssueService.create_delegation()
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/issues/escalating_issues_alg.py" line="31">

---

## generate_issue_forecast

The 'generate_issue_forecast' function is used to calculate daily issue spike limits, given an input dataset from snuba. It uses various statistical measures such as the average and standard deviation of the timeseries data to calculate the forecast.

```python
def generate_issue_forecast(
    data: GroupCount, start_time: datetime, alg_params: ThresholdVariables = standard_version
) -> list[IssueForecast]:
    """
    Calculates daily issue spike limits, given an input dataset from snuba.

    For issues with at least 14 days of history, we combine a weighted average of the last
    7 days of hourly data with the observed variance over that time interval. We double the
    weight if historical observation falls on the same day of week to incorporate daily seasonality.
    The overall multiplier is calibrated to 5 standard deviations, although it is
    truncated to [5, 8] to avoid poor results in a timeseries with very high
    or low variance.
    In addition, we also calculate the cv (coefficient of variance) of the timeseries the past week, which is the ratio of the
    standard deviation over the average. This is to get an understanding of how high or low the variance
    is relative to the data. The CV is then placed into an exponential equation that outputs
    a multiplier inversely related to how high the cv is. The multiplier is bounded between 2 and 5. The
    ceilings for the next week are all the same - which is the maximum number of events in an hour over the
    past week multiplied by this multiplier. This calculation is to account for bursty issues or those that
    have a very high variance.
    The final spike limit for each hour is set to the max of the bursty limit bound or the calculated limit.
    :param data: Dict of Snuba query results - hourly data over past 7 days
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
