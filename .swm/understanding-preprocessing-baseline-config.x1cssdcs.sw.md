---
title: Understanding Preprocessing Baseline Config
---
<SwmSnippet path="/src/sentry/tasks/relocation.py" line="461">

---

# Preprocessing Baseline Config

The `preprocessing_baseline_config` function is responsible for pulling down the global config data needed to check for collisions and global data integrity. It is designed to be idempotent and should be retried with an exponential backoff in case of failure.

```python
def preprocessing_baseline_config(uuid: str) -> None:
    """
    Pulls down the global config data we'll need to check for collisions and global data integrity.

    This function is meant to be idempotent, and should be retried with an exponential backoff.
    """

    relocation: Relocation | None
    attempts_left: int
    (relocation, attempts_left) = start_relocation_task(
        uuid=uuid,
        task=OrderedTask.PREPROCESSING_BASELINE_CONFIG,
        allowed_task_attempts=MAX_FAST_TASK_ATTEMPTS,
    )
    if relocation is None:
        return

    with retry_task_or_fail_relocation(
        relocation,
        OrderedTask.PREPROCESSING_BASELINE_CONFIG,
        attempts_left,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="470">

---

## Starting the Relocation Task

The function starts a relocation task by calling `start_relocation_task`. It passes the `uuid`, the task type as `OrderedTask.PREPROCESSING_BASELINE_CONFIG`, and the maximum number of fast task attempts.

```python
    (relocation, attempts_left) = start_relocation_task(
        uuid=uuid,
        task=OrderedTask.PREPROCESSING_BASELINE_CONFIG,
        allowed_task_attempts=MAX_FAST_TASK_ATTEMPTS,
    )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="478">

---

## Retry Task or Fail Relocation

The function then enters a context managed by `retry_task_or_fail_relocation`. If the task fails, it will be retried until the number of attempts left reaches zero, at which point the relocation will be marked as failed.

```python
    with retry_task_or_fail_relocation(
        relocation,
        OrderedTask.PREPROCESSING_BASELINE_CONFIG,
        attempts_left,
        ERR_PREPROCESSING_INTERNAL,
    ):
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="493">

---

## Exporting Config Scope

The function then exports the in-config scope into a `BytesIO` object. This is done using the `export_in_config_scope` function, which takes the `BytesIO` object, an encryptor, and a printer as arguments.

```python
        export_in_config_scope(
            fp,
            encryptor=GCPKMSEncryptor.from_crypto_key_version(get_default_crypto_key_version()),
            printer=LoggingPrinter(uuid),
        )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="499">

---

## Saving the Config Data

The function then saves the exported config data to the relocation storage. The path for the storage is constructed using the `uuid` and the kind of the file.

```python
        relocation_storage.save(path, fp)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="501">

---

## Applying Preprocessing Colliding Users

Finally, the function applies the `preprocessing_colliding_users` task asynchronously. This task is responsible for handling any user collisions that might occur during the relocation process.

```python
    preprocessing_colliding_users.apply_async(args=[uuid])
```

---

</SwmSnippet>

# Flow drill down

```mermaid
graph TD;

classDef mainFlowStyle color:#000000,fill:#7CB9F4
classDef rootsStyle color:#000000,fill:#00FFF4
classDef Style1 color:#000000,fill:#00FFAA
classDef Style2 color:#000000,fill:#FFFF00
classDef Style3 color:#000000,fill:#AA7CB9
```

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="461">

---

# Preprocessing Baseline Config

The `preprocessing_baseline_config` function is responsible for pulling down the global config data needed to check for collisions and global data integrity. It is designed to be idempotent and should be retried with an exponential backoff in case of failure.

```python
def preprocessing_baseline_config(uuid: str) -> None:
    """
    Pulls down the global config data we'll need to check for collisions and global data integrity.

    This function is meant to be idempotent, and should be retried with an exponential backoff.
    """

    relocation: Relocation | None
    attempts_left: int
    (relocation, attempts_left) = start_relocation_task(
        uuid=uuid,
        task=OrderedTask.PREPROCESSING_BASELINE_CONFIG,
        allowed_task_attempts=MAX_FAST_TASK_ATTEMPTS,
    )
    if relocation is None:
        return

    with retry_task_or_fail_relocation(
        relocation,
        OrderedTask.PREPROCESSING_BASELINE_CONFIG,
        attempts_left,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="470">

---

## Starting the Relocation Task

The function starts a relocation task by calling `start_relocation_task`. It passes the `uuid`, the task type as `OrderedTask.PREPROCESSING_BASELINE_CONFIG`, and the maximum number of fast task attempts.

```python
    (relocation, attempts_left) = start_relocation_task(
        uuid=uuid,
        task=OrderedTask.PREPROCESSING_BASELINE_CONFIG,
        allowed_task_attempts=MAX_FAST_TASK_ATTEMPTS,
    )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="478">

---

## Retry Task or Fail Relocation

The function then enters a context managed by `retry_task_or_fail_relocation`. If the task fails, it will be retried until the number of attempts left reaches zero, at which point the relocation will be marked as failed.

```python
    with retry_task_or_fail_relocation(
        relocation,
        OrderedTask.PREPROCESSING_BASELINE_CONFIG,
        attempts_left,
        ERR_PREPROCESSING_INTERNAL,
    ):
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="493">

---

## Exporting Config Scope

The function then exports the in-config scope into a `BytesIO` object. This is done using the `export_in_config_scope` function, which takes the `BytesIO` object, an encryptor, and a printer as arguments.

```python
        export_in_config_scope(
            fp,
            encryptor=GCPKMSEncryptor.from_crypto_key_version(get_default_crypto_key_version()),
            printer=LoggingPrinter(uuid),
        )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="499">

---

## Saving the Config Data

The function then saves the exported config data to the relocation storage. The path for the storage is constructed using the `uuid` and the kind of the file.

```python
        relocation_storage.save(path, fp)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="501">

---

## Applying Preprocessing Colliding Users

Finally, the function applies the `preprocessing_colliding_users` task asynchronously. This task is responsible for handling any user collisions that might occur during the relocation process.

```python
    preprocessing_colliding_users.apply_async(args=[uuid])
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
