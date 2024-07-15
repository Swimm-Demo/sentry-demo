---
title: Basic Concepts of Event Receivers in Main Application
---
Receivers in the Main Application of sentry-demo are functions that respond to signals sent by Django or Sentry. Signals are a type of messaging system that allows certain senders to notify a set of receivers when certain actions have taken place. They're used for decoupling applications and are an implementation of the Observer design pattern.

In the context of sentry-demo, receivers are used to handle various events such as user login, project creation, event processing, and more. They are defined across multiple files in the 'receivers' directory, each file typically handling a specific type of event or functionality.

For example, in '[features.py](http://features.py)', receivers are defined to record various events like the first event received, user feedback received, project creation, and more. These receivers are connected to the corresponding signals, and when those signals are sent, the connected receiver functions are invoked.

In '[core.py](http://core.py)', receivers are used to create default projects and keys for projects. In '[useremail.py](http://useremail.py)', a receiver is defined to create a UserEmail instance whenever a new User instance is created. Similarly, other files in the 'receivers' directory define receivers for handling different types of events.

<SwmSnippet path="/src/sentry/receivers/useremail.py" line="8">

---

# User Email Receiver

In '[useremail.py](http://useremail.py)', a receiver is defined to create a UserEmail instance whenever a new User instance is created. The `post_save` signal is connected to the `create_user_email` receiver, which is invoked whenever a new User instance is saved.

```python
def create_user_email(instance, created, **kwargs):
    if created:
        try:
            UserEmail.objects.create(email=instance.email, user=instance)
        except IntegrityError:
            pass


post_save.connect(create_user_email, sender=User, dispatch_uid="create_user_email", weak=False)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/receivers/users.py" line="9">

---

# First User Receiver

In '[users.py](http://users.py)', a receiver is defined to create the first user after an upgrade. The `post_upgrade` signal is connected to the `create_first_user` receiver, which is invoked after an upgrade.

```python
def create_first_user(**kwargs):
    if User.objects.filter(is_superuser=True).exists():
        return

    if not sys.stdin.isatty() and not is_self_hosted():
        return

    if not kwargs["interactive"]:
        return

    import click

    if not click.confirm("\nWould you like to create a user account now?", default=True):
        # Not using `abort=1` because we don't want to exit out from further execution
        click.echo("\nRun `sentry createuser` to do this later.\n")
        return

    from sentry.runner import call_command

    call_command("sentry.runner.commands.createuser.createuser", superuser=True)

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/receivers/outbox/control.py" line="26">

---

# Outbox Receiver

In '[control.py](http://control.py)', the `maybe_process_tombstone` receiver is imported from the 'outbox' module. This receiver is likely used to process tombstone messages in the outbox.

```python
from sentry.receivers.outbox import maybe_process_tombstone
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
