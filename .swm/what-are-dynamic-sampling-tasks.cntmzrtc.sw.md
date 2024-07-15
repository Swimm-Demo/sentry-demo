---
title: What are Dynamic Sampling Tasks
---
Tasks in the context of Dynamic Sampling in Sentry are functions that are decorated with either the `dynamic_sampling_task` or `dynamic_sampling_task_with_context` decorators. These decorators are used to wrap the task functions and add additional functionality such as metrics tracking.

The `dynamic_sampling_task` decorator wraps the function, computes a task name based on the function name, and increments a metric counter each time the function is run. It also measures the execution time of the function.

The `dynamic_sampling_task_with_context` decorator does the same as `dynamic_sampling_task`, but it also provides a context to the function it wraps. This context contains the task name and a maximum task execution time.

These tasks are used in various modules of the dynamic sampling feature, such as recalibrating organizations, boosting low volume projects, and sliding window calculations.

<SwmSnippet path="/src/sentry/dynamic_sampling/tasks/utils.py" line="26">

---

# Task Creation

The `_compute_task_name` function is used to compute the name of the task based on the function name. This name is used for metrics tracking.

```python
def _compute_task_name(function_name: str) -> str:
    return f"sentry.tasks.dynamic_sampling.{function_name}"
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/dynamic_sampling/tasks/task_context.py" line="63">

---

# Task Context

The `TaskContext` class is used to store information about a running task, such as its name, the amount of time it is allowed to run, and stats about its operation. It also manages multiple named timers for tracking the execution time of functions.

```python
class TaskContext:
    """
    Keeps information about a running task

    * the name
    * the amount of time is allowed to run (until a TimeoutError should be emitted)
    * stats about the task operation (how many items it has processed) used for logging
    * keeps a Timers object that manages multiple named timers for tracking execution time of functions.
    """

    name: str
    num_seconds: float
    context_data: dict[str, DynamicSamplingLogState] | None = None

    def __post_init__(self):
        # always override
        self.expiration_time = time.monotonic() + self.num_seconds
        if self.context_data is None:
            self.context_data = {}
        self.timers = Timers()

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/dynamic_sampling/tasks/common.py" line="77">

---

# Task Execution

The `wrapped` function is an example of a task execution. It checks if the task has exceeded its maximum execution time, gets the timer for the task, and executes the task function. It also updates the execution time of the task in the task context.

```python
        def wrapped(context: TaskContext, *args, **kwargs):
            if time.monotonic() > context.expiration_time:
                raise TimeoutException(context)
            timer = context.get_timer(func_name)
            with timer:
                state = context.get_function_state(func_name)
                val = inner(state, *args, **kwargs)
                state.execution_time = timer.current()
                context.set_function_state(func_name, state)
                return val
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
