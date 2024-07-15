---
title: Overview of Dynamic Sampling Rules
---
Rules in Dynamic Sampling are a part of Sentry's performance monitoring platform. They are used to manage and control the data sampling rates based on certain conditions or biases. This allows developers to focus on the most relevant data for their needs.

The rules are implemented through various modules and classes such as `RuleType`, `Bias`, `BiasesCombinator`, and others. These components work together to define and apply the rules.

For instance, `RuleType` is a module that defines the type of rule to be applied. `Bias` is a base class for biases that can affect the sampling decision. `BiasesCombinator` is a class that combines different biases.

There are also specific types of biases like `IgnoreHealthChecksBias` and `RecalibrationBias` that are used to adjust the sampling based on specific conditions.

The `apply_dynamic_factor` function is an example of how these rules are applied. It adjusts the sampling rate based on a dynamic factor, ensuring that the sampling rate stays within a certain range.

<SwmSnippet path="/src/sentry/dynamic_sampling/rules/utils.py" line="114">

---

# RuleType

`RuleType` is a module that defines the type of rule to be applied. It is used in the `get_rule_type` function to determine the type of a given rule based on its ID.

```python
def get_rule_type(rule: Rule) -> RuleType | None:
    # Edge case handled naively in which we check if the ID is within the possible bounds. This is done because the
    # latest release rules have ids from 1500 to 1500 + (limit - 1). For example if the limit is 2, we will only have
    # ids: 1500, 1501.
    #
    # This implementation MUST be changed in case we change the logic of rule ids.
    if (
        RESERVED_IDS[RuleType.BOOST_LATEST_RELEASES_RULE]
        <= rule["id"]
        < RESERVED_IDS[RuleType.BOOST_LATEST_RELEASES_RULE] + BOOSTED_RELEASES_LIMIT
    ):
        return RuleType.BOOST_LATEST_RELEASES_RULE
    elif (
        RESERVED_IDS[RuleType.BOOST_LOW_VOLUME_TRANSACTIONS_RULE]
        <= rule["id"]
        < RESERVED_IDS[RuleType.BOOST_LATEST_RELEASES_RULE]
    ):
        return RuleType.BOOST_LOW_VOLUME_TRANSACTIONS_RULE

    return REVERSE_RESERVED_IDS.get(rule["id"], None)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/dynamic_sampling/rules/biases/recalibration_bias.py" line="7">

---

# Bias

`Bias` is a base class for biases that can affect the sampling decision. An example of a specific bias is the `RecalibrationBias` class, which adjusts the overall sampling rate to the desired rate.

```python
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
        # is the identity of the multiplication.
        if adjusted_factor == 1.0:
            return []

        return [
            {
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/dynamic_sampling/rules/biases/boost_low_volume_transactions_bias.py" line="10">

---

# BiasesCombinator

`BiasesCombinator` is a class that combines different biases. The `generate_rules` function in the `boost_low_volume_transactions_bias.py` file is an example of how these biases are combined to generate rules.

```python
    def generate_rules(self, project: Project, base_sample_rate: float) -> list[PolymorphicRule]:
        proj_id = project.id
        org_id = project.organization.id

        transaction_map, base_implicit_rate = get_transactions_resampling_rates(
            org_id=org_id, proj_id=proj_id, default_rate=base_sample_rate
        )

        ret_val: list[Rule] = []

        if len(transaction_map) == 0:
            return ret_val  # no point returning any rules the project rule should take over

        if base_sample_rate == 0:
            return ret_val  # we can't deal without a base_sample_rate

        if base_implicit_rate == 0.0:
            base_implicit_rate = 1.0

        # The implicit rate that we compute is transformed to a factor, so that when the rate is multiplied by the last
        # sample rate rule, the value will be `base_implicit_rate`.
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
