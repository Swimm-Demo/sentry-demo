---
title: product-Differential Flamegraph View
---
This document will cover the Differential Flamegraph View feature, which includes:

1. Fetching the current project
2. Fetching the data for the differential flamegraph
3. Handling resizing of the flamegraph canvas
4. Creating the model for the differential flamegraph.

Technical document: <SwmLink doc-title="Understanding DifferentialFlamegraphView">[Understanding DifferentialFlamegraphView](/.swm/understanding-differentialflamegraphview.s6k3g8cy.sw.md)</SwmLink>

# Fetching the current project

The current project is fetched from the route parameters. This is necessary to ensure that the flamegraph data is relevant to the project that the user is currently viewing.

# Fetching the data for the differential flamegraph

The data for the differential flamegraph is fetched based on a set of parameters. This data includes the before and after states of the flamegraph, which are used to show how the execution of the program changed over time.

# Handling resizing of the flamegraph canvas

The flamegraph canvas is resized to fit the available space. This ensures that the flamegraph is always displayed in an optimal size for the user's screen.

# Creating the model for the differential flamegraph

A model for the differential flamegraph is created using the fetched data. This model is used to render the flamegraph in the user interface. The model includes the before and after flamegraphs, as well as information about any changes in the execution of the program.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
