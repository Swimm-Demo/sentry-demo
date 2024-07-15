---
title: product-Organization Report Preparation and Delivery in Sentry
---
This document will cover the process of preparing and delivering organization reports in Sentry. The steps include:

1. Gathering data for the report
2. Delivering the report

Technical document: <SwmLink doc-title="Understanding prepare_organization_report Function">[Understanding prepare_organization_report Function](/.swm/understanding-prepare_organization_report-function.2phmpdm1.sw.md)</SwmLink>

# Gathering Data for the Report

The process of preparing an organization report in Sentry involves gathering data related to the organization's events, errors, transactions, and performance issues. This data is collected from different entities within the organization. The data includes event counts, key errors, key transactions, and key performance issues for the organization. This data is crucial for understanding the organization's performance and identifying areas for improvement.

# Delivering the Report

Once all the necessary data has been gathered, the report is prepared and delivered. The delivery process checks if the report is available. If it is, it proceeds to deliver the reports. The delivery can be specific to a user if there's an email override, or it can be for all active users in the organization who are not restricted. The report is prepared with a specific context for each user, and then sent to the user.

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="product-flows"><sup>Powered by [Swimm](/)</sup></SwmMeta>
