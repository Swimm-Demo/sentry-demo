---
title: product-Job Data Update and Event Visualization
---
This document will cover the process of updating job data, storing it, and creating a visual representation of the event. The steps include:

1. Updating job data
2. Storing the updated data
3. Creating an event instance
4. Creating a visual representation of the event.

Technical document: <SwmLink doc-title="Understanding _pull_out_data Function">[Understanding \_pull_out_data Function](/.swm/understanding-_pull_out_data-function.6gtlwbx5.sw.md)</SwmLink>

# Updating Job Data

The process begins with updating every job in the list with required information. This involves iterating over the jobs, extracting the data, and updating the job with the extracted data. The data of interest is pulled from the top level. For instance, if a transaction name exists, it is forced into a string and added to the job. If a key_id exists, it is also added to the job.

# Storing Updated Data

The updated data is then stored in the nodestore. This is done by recursively traversing or creating the specified path and setting the given value if it does not exist. This function is equivalent to a recursive dict.setdefault, except for None values. If a value already exists and is not None, it is not overwritten.

# Creating an Event Instance

An event instance is created using the updated data and a project_id. The create_event method from the eventstore backend is called, passing in the project_id, event_id from the data, and the data itself wrapped in an EventDict.

# Creating a Visual Representation of the Event

Finally, a visual representation of the event is generated in the form of breadcrumbs. This involves using the useCrumbHandlers hook to handle mouse events and the getFrameDetails function to get details about each frame. The frames are mapped to buttons, and when a button is clicked, the frame's timestamp is clicked and the active tab is set to the frame's details.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
