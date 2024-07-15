---
title: Basic Concepts of API Utility Modules
---
Helpers in the API of Sentry-Demo are utility modules that provide common functionalities used across the application. They encapsulate complex logic or repetitive tasks into reusable functions, improving code readability and maintainability.

For instance, the 'actionable_items_helper.py' file contains a class 'ActionPriority' that defines constants for different levels of action priority. It also includes lists of different types of errors and their corresponding action priorities.

Another example is the '[mobile.py](http://mobile.py)' file, which contains a function 'get_readable_device_name' that returns a readable name for a given device model. This function uses data from 'ANDROID_MODELS' and 'IOS_MODELS' to map device model identifiers to human-readable names.

The '[teams.py](http://teams.py)' file includes functions like 'is_team_admin' and 'get_teams' that are used to manage team-related data. These functions interact with the database to fetch and manipulate team data.

The 'source_map_helper.py' file contains functions that help in handling source maps in JavaScript projects. These functions include 'source_map_debug', '\_get_frame_filename_and_path', '\_find_matches', and others.

In summary, helpers in the API of Sentry-Demo are utility modules that provide common functionalities used across the application. They encapsulate complex logic or repetitive tasks into reusable functions, improving code readability and maintainability.

<SwmSnippet path="/src/sentry/api/helpers/actionable_items_helper.py" line="5">

---

# ActionPriority Class

The 'ActionPriority' class in 'actionable_items_helper.py' defines constants for different levels of action priority. These constants can be used to categorize errors based on their severity.

```python
class ActionPriority:
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    UNKNOWN = 4
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/helpers/actionable_items_helper.py" line="31">

---

# Error Priorities

This part of the code defines a dictionary that maps different types of errors to their corresponding action priorities. This allows the application to handle errors based on their severity.

```python
priority_ranking = {
    # Low Priority
    EventError.CLOCK_DRIFT: ActionPriority.LOW,
    EventError.FETCH_GENERIC_ERROR: ActionPriority.LOW,
    EventError.FUTURE_TIMESTAMP: ActionPriority.LOW,
    EventError.INVALID_ATTRIBUTE: ActionPriority.LOW,
    EventError.INVALID_DATA: ActionPriority.LOW,
    EventError.INVALID_ENVIRONMENT: ActionPriority.LOW,
    EventError.NATIVE_BAD_DSYM: ActionPriority.LOW,
    EventError.NATIVE_MISSING_DSYM: ActionPriority.LOW,
    EventError.NATIVE_MISSING_OPTIONALLY_BUNDLED_DSYM: ActionPriority.LOW,
    EventError.PAST_TIMESTAMP: ActionPriority.LOW,
    EventError.PROGUARD_MISSING_LINENO: ActionPriority.LOW,
    EventError.PROGUARD_MISSING_MAPPING: ActionPriority.LOW,
    EventError.RESTRICTED_IP: ActionPriority.LOW,
    EventError.SECURITY_VIOLATION: ActionPriority.LOW,
    # Medium Priority
    EventError.JS_MISSING_SOURCES_CONTENT: ActionPriority.MEDIUM,
    EventError.JS_SCRAPING_DISABLED: ActionPriority.MEDIUM,
    # High Priority
    SourceMapProcessingIssue.DEBUG_ID_NO_SOURCEMAPS: ActionPriority.HIGH,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/helpers/actionable_items_helper.py" line="92">

---

# Debug Frames

The 'find_debug_frames' function is used to find debug frames in an event. It iterates over the exceptions in the event and adds the indices of the frames that meet certain conditions to the 'debug_frames' list.

```python
def find_debug_frames(event):
    debug_frames = []
    exceptions = event.interfaces["exception"].values
    seen_filenames = []

    for exception_idx, exception in enumerate(exceptions):
        for frame_idx, frame in enumerate(exception.stacktrace.frames):
            if (
                frame.in_app
                and is_frame_filename_valid(frame)
                and frame.lineno
                and frame.filename not in seen_filenames
            ):
                debug_frames.append((frame_idx, exception_idx))
                seen_filenames.append(frame.filename)

    return debug_frames
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/helpers/actionable_items_helper.py" line="111">

---

# File Extension

The 'get_file_extension' function is used to get the file extension of a filename. It splits the filename by '.' and returns the last segment if there is more than one segment.

```python
def get_file_extension(filename):
    segments = filename.split(".")
    if len(segments) > 1:
        return segments[-1]
    return None
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/helpers/actionable_items_helper.py" line="118">

---

# Frame Filename Validation

The 'is_frame_filename_valid' function is used to check if a frame filename is valid. It checks various conditions and returns 'False' if any of the conditions is not met.

```python
def is_frame_filename_valid(frame):
    filename = frame.abs_path
    if not filename:
        return False
    try:
        filename = filename.split("/")[-1]
    except Exception:
        pass

    if frame.filename == "<anonymous>" and frame.in_app:
        return False
    elif frame.function in fileNameBlocklist:
        return False
    elif filename and not get_file_extension(filename):
        return False
    return True
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
