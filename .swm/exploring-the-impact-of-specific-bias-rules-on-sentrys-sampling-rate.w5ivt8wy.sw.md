---
title: Exploring the Impact of Specific Bias Rules on Sentrys Sampling Rate
---
This document will cover the role and functionality of the 'IgnoreHealthChecksBias' and 'RecalibrationBias' classes in the sentry-demo repository. We'll cover:

1. The purpose of the 'IgnoreHealthChecksBias' class
2. How 'IgnoreHealthChecksBias' affects the sampling rate
3. The purpose of the 'RecalibrationBias' class
4. How 'RecalibrationBias' affects the sampling rate.

<SwmSnippet path="/src/sentry/dynamic_sampling/rules/biases/ignore_health_checks_bias.py" line="12">

---

# IgnoreHealthChecksBias

The 'IgnoreHealthChecksBias' class generates rules that adjust the base sample rate by a factor defined in 'IGNORE_HEALTH_CHECKS_FACTOR'. This adjustment is applied to transactions that match the 'HEALTH_CHECK_GLOBS' condition.

```python
class IgnoreHealthChecksBias(Bias):
    def generate_rules(self, project: Project, base_sample_rate: float) -> list[PolymorphicRule]:
        return [
            {
                "samplingValue": {
                    "type": "sampleRate",
                    "value": base_sample_rate / IGNORE_HEALTH_CHECKS_FACTOR,
                },
                "type": "transaction",
                "condition": {
                    "op": "or",
                    "inner": [
                        {
                            "op": "glob",
                            "name": "event.transaction",
                            "value": HEALTH_CHECK_GLOBS,
                        }
                    ],
                },
                "id": RESERVED_IDS[RuleType.IGNORE_HEALTH_CHECKS_RULE],
            }
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/dynamic_sampling/rules/biases/ignore_health_checks_bias.py" line="4">

---

'IGNORE_HEALTH_CHECKS_FACTOR' is the factor by which the base sample rate is divided in the 'IgnoreHealthChecksBias' class.

```python
    IGNORE_HEALTH_CHECKS_FACTOR,
    RESERVED_IDS,
    PolymorphicRule,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/dynamic_sampling/rules/biases/recalibration_bias.py" line="1">

---

# RecalibrationBias

The 'RecalibrationBias' class generates rules that adjust the sampling rate based on the 'adjusted_factor' obtained from the 'get_adjusted_factor' function. This adjustment is applied to all traces.

```python
from sentry.dynamic_sampling.rules.biases.base import Bias
from sentry.dynamic_sampling.rules.utils import RESERVED_IDS, PolymorphicRule, RuleType
from sentry.dynamic_sampling.tasks.helpers.recalibrate_orgs import get_adjusted_factor
from sentry.models.project import Project


class RecalibrationBias(Bias):
    """
    Correction bias that tries to bring the overall sampling rate for the organisation to the
    desired sampling rate.

    Various biases boost and shrink different transactions in order to obtain an appropriate
    number of samples from all areas of the application, doing this changes the overall sampling
    rate from the desired sampling rate, this bias tries to rectify the overall organisation sampling
    rate and bring it to the desired sampling rate,it uses the previous interval rate to figure out
    how this should be done.
    """

    def generate_rules(self, project: Project, base_sample_rate: float) -> list[PolymorphicRule]:
        adjusted_factor = get_adjusted_factor(project.organization.id)
        # We don't want to generate any rule in case the factor is 1.0 since we should multiply the factor and 1.0
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="follow-up"><sup>Powered by [Swimm](/)</sup></SwmMeta>
