---
title: Handling Username Collisions
---
# Preprocessing Colliding Users

The `preprocessing_colliding_users` function is designed to handle potential username collisions during the import process. It fetches existing users whose usernames match those found in the import data. The function is designed to be idempotent, meaning it can be run multiple times without changing the result beyond the initial application.

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="522">

---

# Preprocessing Colliding Users

The function starts a relocation task with the `start_relocation_task` function. This task is assigned a unique identifier (`uuid`), a task type (`OrderedTask.PREPROCESSING_COLLIDING_USERS`), and a maximum number of attempts (`MAX_FAST_TASK_ATTEMPTS`).

```python
    relocation: Relocation | None
    attempts_left: int
    (relocation, attempts_left) = start_relocation_task(
        uuid=uuid,
        task=OrderedTask.PREPROCESSING_COLLIDING_USERS,
        allowed_task_attempts=MAX_FAST_TASK_ATTEMPTS,
    )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="532">

---

The `retry_task_or_fail_relocation` function is used to handle task retries. If the task fails, it will be retried until the maximum number of attempts is reached. If the task still fails after the maximum number of attempts, the relocation process will be marked as failed.

```python
    with retry_task_or_fail_relocation(
        relocation,
        OrderedTask.PREPROCESSING_COLLIDING_USERS,
        attempts_left,
        ERR_PREPROCESSING_INTERNAL,
    ):
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="538">

---

The function then exports the user data within the scope of the relocation task. This data is encrypted and saved to a specific path in the relocation storage.

```python
        kind = RelocationFile.Kind.COLLIDING_USERS_VALIDATION_DATA
        path = f'runs/{uuid}/in/{kind.to_filename("tar")}'
        relocation_storage = get_relocation_storage()
        fp = BytesIO()
        log_gcp_credentials_details(logger)
        export_in_user_scope(
            fp,
            encryptor=GCPKMSEncryptor.from_crypto_key_version(get_default_crypto_key_version()),
            user_filter=set(relocation.want_usernames),
            printer=LoggingPrinter(uuid),
        )
        fp.seek(0)
        relocation_storage.save(path, fp)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="552">

---

Finally, the `preprocessing_complete` function is called asynchronously, signaling the completion of the preprocessing step.

```python
    preprocessing_complete.apply_async(args=[uuid])
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

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="514">

---

# Preprocessing Colliding Users

The function `preprocessing_colliding_users` is designed to handle potential username collisions during the import process. It fetches existing users whose usernames match those found in the import data. The function is designed to be idempotent, meaning it can be run multiple times without changing the result beyond the initial application.

```python
def preprocessing_colliding_users(uuid: str) -> None:
    """
    Pulls down any already existing users whose usernames match those found in the import - we'll
    need to validate that none of these are mutated during import.

    This function is meant to be idempotent, and should be retried with an exponential backoff.
    """
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="522">

---

The function starts a relocation task with the `start_relocation_task` function. This task is assigned a unique identifier (`uuid`), a task type (`OrderedTask.PREPROCESSING_COLLIDING_USERS`), and a maximum number of attempts (`MAX_FAST_TASK_ATTEMPTS`).

```python
    relocation: Relocation | None
    attempts_left: int
    (relocation, attempts_left) = start_relocation_task(
        uuid=uuid,
        task=OrderedTask.PREPROCESSING_COLLIDING_USERS,
        allowed_task_attempts=MAX_FAST_TASK_ATTEMPTS,
    )
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="532">

---

The `retry_task_or_fail_relocation` function is used to handle task retries. If the task fails, it will be retried until the maximum number of attempts is reached. If the task still fails after the maximum number of attempts, the relocation process will be marked as failed.

```python
    with retry_task_or_fail_relocation(
        relocation,
        OrderedTask.PREPROCESSING_COLLIDING_USERS,
        attempts_left,
        ERR_PREPROCESSING_INTERNAL,
    ):
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="538">

---

The function then exports the user data within the scope of the relocation task. This data is encrypted and saved to a specific path in the relocation storage.

```python
        kind = RelocationFile.Kind.COLLIDING_USERS_VALIDATION_DATA
        path = f'runs/{uuid}/in/{kind.to_filename("tar")}'
        relocation_storage = get_relocation_storage()
        fp = BytesIO()
        log_gcp_credentials_details(logger)
        export_in_user_scope(
            fp,
            encryptor=GCPKMSEncryptor.from_crypto_key_version(get_default_crypto_key_version()),
            user_filter=set(relocation.want_usernames),
            printer=LoggingPrinter(uuid),
        )
        fp.seek(0)
        relocation_storage.save(path, fp)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/tasks/relocation.py" line="552">

---

Finally, the `preprocessing_complete` function is called asynchronously, signaling the completion of the preprocessing step.

```python
    preprocessing_complete.apply_async(args=[uuid])
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
