---
title: API
---
This document will cover the following topics:

1. Overview of the API and its offerings
2. Details on where to find the list of endpoints
3. Explanation of API documentation tools available in the repo

<SwmSnippet path="/api-docs/openapi.json" line="1">

---

# Overview of the API

The API is defined in the `openapi.json` file. It provides a variety of endpoints for different resources such as Teams, Organizations, Projects, Events, Releases, Integration, and SCIM. Each resource has its own set of endpoints.

```json
{
  "openapi": "3.0.1",
  "info": {
    "title": "API Reference",
    "description": "Sentry Public API",
    "termsOfService": "http://sentry.io/terms/",
    "contact": {
      "email": "partners@sentry.io"
    },
    "license": {
      "name": "Apache 2.0",
      "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
    },
    "version": "v0"
  },
  "servers": [
    {
      "url": "https://sentry.io/"
    }
  ],
  "tags": [
```

---

</SwmSnippet>

<SwmSnippet path="/api-docs/openapi.json" line="89">

---

# List of Endpoints

The list of endpoints for each resource is defined under the `paths` section in the `openapi.json` file. Each endpoint is associated with a specific resource and has a reference to its detailed definition.

```json
  "paths": {
    "/api/0/teams/{organization_id_or_slug}/{team_id_or_slug}/stats/": {
      "$ref": "paths/teams/stats.json"
    },
    "/api/0/organizations/{organization_id_or_slug}/eventids/{event_id}/": {
      "$ref": "paths/organizations/event-id-lookup.json"
    },
    "/api/0/organizations/{organization_id_or_slug}/": {
      "$ref": "paths/organizations/details.json"
    },
    "/api/0/organizations/{organization_id_or_slug}/repos/": {
      "$ref": "paths/organizations/repos.json"
    },
    "/api/0/organizations/{organization_id_or_slug}/repos/{repo_id}/commits/": {
      "$ref": "paths/organizations/repo-commits.json"
    },
    "/api/0/organizations/{organization_id_or_slug}/shortids/{short_id}/": {
      "$ref": "paths/organizations/shortid.json"
    },
    "/api/0/projects/": {
      "$ref": "paths/projects/index.json"
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/snuba/query_sources.py" line="6">

---

# API Documentation Tools

The API is available via Swagger. The specification path is defined in the `query_sources.py` file.

```python
    API = "api"
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="api"><sup>Powered by [Swimm](/)</sup></SwmMeta>
