---
title: Exploring Web Page Views
---
Views in the Sentry-Demo application are essentially React components that define what is rendered on a particular page. They are organized in a directory structure that mirrors the URL structure of the application. For example, the views for the 'insights' feature are located in the 'static/app/views/insights' directory, and each subdirectory corresponds to a different aspect of the insights feature, such as 'browser', 'http', 'database', etc.

Each view is typically defined in a '.tsx' file, and may have an associated '.spec.tsx' file for tests. For instance, the 'webVitalsLandingPage.tsx' file defines the view for the landing page of the 'webVitals' feature, and 'webVitalsLandingPage.spec.tsx' contains the tests for this view.

Views can also contain state and logic related to the data they display. For example, the 'SentryAppExternalInstallationContent' function in 'static/app/views/sentryAppExternalInstallation/index.tsx' is a view that uses the 'useApi' and 'useApiQuery' hooks to fetch data from the API, and maintains its own state with the 'useState' and 'useEffect' hooks.

# Directory Structure

The views for the 'insights' feature are located in the 'static/app/views/insights' directory, and each subdirectory corresponds to a different aspect of the insights feature, such as 'browser', 'http', 'database', etc.

<SwmSnippet path="/static/app/views/insights/http/views/httpDomainSummaryPage.tsx" line="1">

---

# View Definition

Each view is typically defined in a '.tsx' file. For instance, the 'httpDomainSummaryPage.tsx' file defines the view for the domain summary page of the 'http' feature.

```tsx
import React from 'react';
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/organizationDeveloperSettings/sentryApplicationDashboard/index.tsx" line="30">

---

# View State and Logic

Views can also contain state and logic related to the data they display. For example, the 'SentryApplicationDashboard' view uses the 'getEndpoints' method to fetch data from the API, and maintains its own state with the 'state' object.

```tsx
    componentInteractions: {
      [key: string]: [number, number][];
    };
    views: [number, number][];
  };
  stats: {
    installStats: [number, number][];
    totalInstalls: number;
    totalUninstalls: number;
    uninstallStats: [number, number][];
  };
};

class SentryApplicationDashboard extends DeprecatedAsyncView<Props, State> {
  getEndpoints(): ReturnType<DeprecatedAsyncView['getEndpoints']> {
    const {appSlug} = this.props.params;

    // Default time range for now: 90 days ago to now
    const now = Math.floor(new Date().getTime() / 1000);
    const ninety_days_ago = 3600 * 24 * 90;

```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
