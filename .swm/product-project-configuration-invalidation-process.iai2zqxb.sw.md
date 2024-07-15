---
title: product-Project Configuration Invalidation Process
---
This document will cover the 'Project Configuration Invalidation' process in the Sentry application. We'll cover:

1. Scheduling the invalidation of a project's configuration
2. Incrementing the metrics for scheduled tasks
3. Applying tasks asynchronously
4. Checking for bad uses of pickle

Technical document: <SwmLink doc-title="_schedule_invalidate_project_config">[\_schedule_invalidate_project_config](/.swm/understanding-the-_schedule_invalidate_project_config-function.kza5zhl5.sw.md)</SwmLink>

# Scheduling the Invalidation of a Project's Configuration

The first step in the 'Project Configuration Invalidation' process is to schedule the invalidation of a project's configuration. This is done to ensure that the project's configuration is always up-to-date. The system first validates the arguments and checks if the task is already in the queue. If not, it proceeds to the next step.

# Incrementing the Metrics for Scheduled Tasks

Once the invalidation of a project's configuration is scheduled, the system increments the metrics for scheduled tasks. This is done to keep track of the number of tasks that have been scheduled. This information can be useful for monitoring and debugging purposes.

# Applying Tasks Asynchronously

The next step in the process is to apply the tasks asynchronously. This means that the tasks are executed in the background, allowing the system to continue with other tasks without waiting for the current task to complete. This is particularly useful for tasks that may take a long time to complete.

# Checking for Bad Uses of Pickle

Finally, the system checks for bad uses of pickle. Pickle is a method used to serialize and deserialize objects in Python. However, it can be unsafe if used incorrectly, as it can execute arbitrary code during deserialization. Therefore, the system checks if the task arguments contain objects that should not be passed via pickle. If a bad object is found, it raises a TypeError.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
