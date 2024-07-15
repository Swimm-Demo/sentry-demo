---
title: Building Slack Messages
---
<SwmSnippet path="/src/sentry/integrations/slack/message_builder/issues.py" line="575">

---

# Build Function

The `build` function is a key part of the message construction process in the Slack integration. It is responsible for creating a Slack message block. The function begins by generating the text for the attachment, then retrieves the project and event details. It then constructs various blocks for the message, such as title, culprit, text, tags, context, actions, suggested assignees, suspect commit info, notes, and footer. These blocks are then combined and returned as a single `SlackBlock`.

```python
    def build(self, notification_uuid: str | None = None) -> SlackBlock:
        # XXX(dcramer): options are limited to 100 choices, even when nested
        text = build_attachment_text(self.group, self.event) or ""
        text = text.strip(" \n")

        text = escape_slack_markdown_text(text)

        project = Project.objects.get_from_cache(id=self.group.project_id)

        # If an event is unspecified, use the tags of the latest event (if one exists).
        event_for_tags = self.event or self.group.get_latest_event()

        obj = self.event if self.event is not None else self.group
        action_text = ""

        if not self.issue_details or (self.recipient and self.recipient.is_team):
            payload_actions, action_text, has_action = build_actions(
                self.group, project, text, self.actions, self.identity
            )
        else:
            payload_actions = []
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/integrations/slack/message_builder/issues.py" line="577">

---

## Building Attachment Text

The `build_attachment_text` function is used to create the text for the Slack message attachment. The text is then stripped of leading and trailing spaces and newlines.

```python
        text = build_attachment_text(self.group, self.event) or ""
        text = text.strip(" \n")

        text = escape_slack_markdown_text(text)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/integrations/slack/message_builder/issues.py" line="591">

---

## Building Actions

The `build_actions` function is used to create the actions for the Slack message. If the recipient is a team or if `issue_details` is not provided, the actions are built using the group, project, text, actions, and identity. Otherwise, no actions are created.

```python
            payload_actions, action_text, has_action = build_actions(
                self.group, project, text, self.actions, self.identity
            )
        else:
            payload_actions = []
            has_action = False

        rule_id = None
        if self.rules:
            rule_id = self.rules[0].id

        # build up actions text
        if self.actions and self.identity and not action_text:
            # this means somebody is interacting with the message
            action_text = get_action_text(self.actions, self.identity)
            has_action = True

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/integrations/slack/message_builder/issues.py" line="608">

---

## Building Blocks

Various blocks are built for the Slack message, such as title, culprit, text, tags, context, actions, suggested assignees, suspect commit info, notes, and footer. These blocks are then combined into a single list.

```python
        blocks = [self.get_title_block(rule_id, notification_uuid, obj, has_action)]

        if culprit_block := self.get_culprit_block(obj):
            blocks.append(culprit_block)

        # build up text block
        text = text.lstrip(" ")
        # XXX(CEO): sometimes text is " " and slack will error if we pass an empty string (now "")
        if text:
            blocks.append(self.get_text_block(text))

        if self.actions:
            blocks.append(self.get_markdown_block(action_text))

        # build tags block
        tags = get_tags(self.group, event_for_tags, self.tags)
        if tags:
            blocks.append(self.get_tags_block(tags))

        # add event count, user count, substate, first seen
        context = get_context(self.group)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/integrations/slack/message_builder/issues.py" line="688">

---

## Finalizing the Build

The `build` function finalizes the construction of the Slack message by calling the `_build_blocks` function with the combined list of blocks, fallback text, block id, and a flag indicating whether to skip the fallback. The result is a `SlackBlock` ready to be sent.

```python
        return self._build_blocks(
            *blocks,
            fallback_text=self.build_fallback_text(obj, project.slug),
            block_id=orjson.dumps(block_id).decode(),
            skip_fallback=self.skip_fallback,
        )
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

<SwmSnippet path="/src/sentry/integrations/slack/message_builder/issues.py" line="575">

---

# Build Function

The `build` function is responsible for constructing a Slack message block. It takes an optional `notification_uuid` as an argument and returns a `SlackBlock`. The function starts by creating the text for the attachment, then retrieves the project and event details. It then constructs various blocks for the message, such as title, culprit, text, tags, context, actions, suggested assignees, suspect commit info, notes, and footer. These blocks are then combined and returned as a single `SlackBlock`.

```python
    def build(self, notification_uuid: str | None = None) -> SlackBlock:
        # XXX(dcramer): options are limited to 100 choices, even when nested
        text = build_attachment_text(self.group, self.event) or ""
        text = text.strip(" \n")

        text = escape_slack_markdown_text(text)

        project = Project.objects.get_from_cache(id=self.group.project_id)

        # If an event is unspecified, use the tags of the latest event (if one exists).
        event_for_tags = self.event or self.group.get_latest_event()

        obj = self.event if self.event is not None else self.group
        action_text = ""

        if not self.issue_details or (self.recipient and self.recipient.is_team):
            payload_actions, action_text, has_action = build_actions(
                self.group, project, text, self.actions, self.identity
            )
        else:
            payload_actions = []
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/integrations/slack/message_builder/issues.py" line="577">

---

## Building Attachment Text

The `build_attachment_text` function is used to create the text for the Slack message attachment. The text is then stripped of leading and trailing spaces and newlines.

```python
        text = build_attachment_text(self.group, self.event) or ""
        text = text.strip(" \n")

        text = escape_slack_markdown_text(text)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/integrations/slack/message_builder/issues.py" line="591">

---

## Building Actions

The `build_actions` function is used to create the actions for the Slack message. If the recipient is a team or if `issue_details` is not provided, the actions are built using the group, project, text, actions, and identity. Otherwise, no actions are created.

```python
            payload_actions, action_text, has_action = build_actions(
                self.group, project, text, self.actions, self.identity
            )
        else:
            payload_actions = []
            has_action = False

        rule_id = None
        if self.rules:
            rule_id = self.rules[0].id

        # build up actions text
        if self.actions and self.identity and not action_text:
            # this means somebody is interacting with the message
            action_text = get_action_text(self.actions, self.identity)
            has_action = True

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/integrations/slack/message_builder/issues.py" line="608">

---

## Building Blocks

Various blocks are built for the Slack message, such as title, culprit, text, tags, context, actions, suggested assignees, suspect commit info, notes, and footer. These blocks are then combined into a single list.

```python
        blocks = [self.get_title_block(rule_id, notification_uuid, obj, has_action)]

        if culprit_block := self.get_culprit_block(obj):
            blocks.append(culprit_block)

        # build up text block
        text = text.lstrip(" ")
        # XXX(CEO): sometimes text is " " and slack will error if we pass an empty string (now "")
        if text:
            blocks.append(self.get_text_block(text))

        if self.actions:
            blocks.append(self.get_markdown_block(action_text))

        # build tags block
        tags = get_tags(self.group, event_for_tags, self.tags)
        if tags:
            blocks.append(self.get_tags_block(tags))

        # add event count, user count, substate, first seen
        context = get_context(self.group)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/integrations/slack/message_builder/issues.py" line="688">

---

## Finalizing the Build

The `build` function finalizes the construction of the Slack message by calling the `_build_blocks` function with the combined list of blocks, fallback text, block id, and a flag indicating whether to skip the fallback. The result is a `SlackBlock` ready to be sent.

```python
        return self._build_blocks(
            *blocks,
            fallback_text=self.build_fallback_text(obj, project.slug),
            block_id=orjson.dumps(block_id).decode(),
            skip_fallback=self.skip_fallback,
        )
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
