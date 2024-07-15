---
title: Introduction to Metrics Consumers
---
Consumers in Sentry metrics are components that process incoming data. They are responsible for handling and processing the metrics data that is sent to Sentry. This includes batching up individual messages, tracking batches of messages, and flushing the batches when they reach a certain size or after a certain amount of time.

The consumers use various classes and methods to perform their tasks. For instance, the `MetricsBatchBuilder` class is used to batch up individual messages into a list, which will later be the payload for the big outer message that gets passed through to the `ParallelTransformStep`. The `BatchMessages` class is the first processing step in the `MetricsConsumerStrategyFactory`. It keeps track of a batch of messages and flushes the batch when it reaches capacity.

The `MessageProcessor` is another important component in the consumers. It is responsible for processing the messages. The `SimpleProduceStep` is used in the multi-process environment of the consumers.

<SwmSnippet path="/src/sentry/sentry_metrics/consumers/indexer/batch.py" line="123">

---

# MetricsBatchBuilder

The `MetricsBatchBuilder` class is used to batch up individual messages into a list, which will later be the payload for the big outer message that gets passed through to the `ParallelTransformStep`.

```python
        1. Check the header to see if the use case ID is disabled
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_metrics/consumers/indexer/batch.py" line="454">

---

# BatchMessages

The `BatchMessages` class is the first processing step in the `MetricsConsumerStrategyFactory`. It keeps track of a batch of messages and flushes the batch when it reaches capacity.

```python
                    # Metrics don't support gauges (which use dicts), so assert value type
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_metrics/consumers/indexer/processing.py" line="60">

---

# MessageProcessor

The `MessageProcessor` is another important component in the consumers. It is responsible for processing the messages.

```python
        Get the tags validator function for the current use case.
        """
        if self._config.use_case_id == UseCaseKey.RELEASE_HEALTH:
            return ReleaseHealthTagsValidator().is_allowed
        else:
            return GenericMetricsTagsValidator().is_allowed

    def __get_schema_validator(self) -> Callable[[str, IngestMetric], None]:
        """
        Get the schema validator function for the current use case.
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/sentry_metrics/consumers/indexer/routing_producer.py" line="69">

---

# SimpleProduceStep

The `SimpleProduceStep` is used in the multi-process environment of the consumers.

```python
        specific use case.
```

---

</SwmSnippet>

# Functions of Consumers

This section discusses the main functions of Consumers in Sentry metrics.

<SwmSnippet path="/src/sentry/replays/lib/consumer.py" line="10">

---

## MetricsBatchBuilder

The `MetricsBatchBuilder` class is used to batch up individual messages into a list, which will later be the payload for the big outer message that gets passed through to the `ParallelTransformStep`.

```python
class LogExceptionStep(ProcessingStrategy[TPayload]):
    def __init__(
        self,
        message: str,
        logger: logging.Logger,
        next_step: ProcessingStrategy[TPayload],
    ) -> None:
        self.__exception_message = message
        self.__next_step = next_step
        self.__closed = False
        self.__logger = logger
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/replays/lib/consumer.py" line="30">

---

## BatchMessages

The `BatchMessages` class is the first processing step in the `MetricsConsumerStrategyFactory`. It keeps track of a batch of messages and flushes the batch when it reaches capacity.

```python
            self.__logger.exception(self.__exception_message)

    def poll(self) -> None:
        try:
            self.__next_step.poll()
        except Exception:
            self.__logger.exception(self.__exception_message)

    def close(self) -> None:
        self.__closed = True

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/replays/lib/consumer.py" line="50">

---

## MessageProcessor

The `MessageProcessor` is another important component in the consumers. It is responsible for processing the messages.

```python

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/replays/lib/consumer.py" line="70">

---

## SimpleProduceStep

The `SimpleProduceStep` is used in the multi-process environment of the consumers.

```python

```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
