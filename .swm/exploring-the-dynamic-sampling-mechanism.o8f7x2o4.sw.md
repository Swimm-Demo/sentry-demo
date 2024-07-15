---
title: Exploring the Dynamic Sampling Mechanism
---
Dynamic sampling in the main application refers to a set of functionalities that allow for the selective collection of data based on certain criteria. This is achieved through various tasks and utilities found in the `src/sentry/dynamic_sampling` directory. The `dynamic_sampling_task` and `dynamic_sampling_task_with_context` functions, for instance, are decorators that add metrics and context to the functions they wrap, allowing for the monitoring of function execution times and frequency. The `DynamicSamplingLogState` class, on the other hand, is used to accumulate stats about the running of a dynamic sampling function or iterator. The dynamic sampling functionality also involves various models and tasks that handle different aspects of the sampling process.

<SwmSnippet path="/src/sentry/dynamic_sampling/tasks/utils.py" line="49">

---

# Dynamic Sampling Task

The `dynamic_sampling_task` function is a decorator that wraps around a function and adds metrics to it. It counts how many times the function is run and how long it takes to run the function.

```python
def dynamic_sampling_task(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        function_name = func.__name__
        task_name = _compute_task_name(function_name)

        # We will count how many times the function is run.
        metrics.incr(f"{task_name}.start", sample_rate=1.0)
        # We will count how much it takes to run the function.
        with metrics.timer(task_name, sample_rate=1.0):
            return func(*args, **kwargs)

    return _wrapper
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/dynamic_sampling/tasks/task_context.py" line="7">

---

# DynamicSamplingLogState Class

The `DynamicSamplingLogState` class is used to accumulate stats about the running of a dynamic sampling function or iterator. It keeps track of various stats like the number of rows, database calls, iterations, projects, organizations, and execution time.

```python
class DynamicSamplingLogState:
    """
    Stats accumulated about the running of a dynamic sampling function or iterator

    A particular function may not use all stats
    """

    num_rows_total: int = 0
    num_db_calls: int = 0
    num_iterations: int = 0
    num_projects: int = 0
    num_orgs: int = 0
    execution_time: float = 0.0

    def to_dict(self) -> dict[str, int | float]:
        return {
            "numRowsTotal": self.num_rows_total,
            "numDbCalls": self.num_db_calls,
            "numIterations": self.num_iterations,
            "numProjects": self.num_projects,
            "numOrgs": self.num_orgs,
```

---

</SwmSnippet>

# Dynamic Sampling Models

The `src/sentry/dynamic_sampling/models` directory contains various models that handle different aspects of the dynamic sampling process. These models are used to manage and manipulate the data related to dynamic sampling.

# Dynamic Sampling Rules

The `src/sentry/dynamic_sampling/rules` directory contains various rules and helper functions that are used to determine how the dynamic sampling should be performed. These rules are used to control the sampling process based on certain criteria.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
