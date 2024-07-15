---
title: Introduction to Api in Main Application
---
The 'Api' in the Main Application of sentry-demo refers to the set of endpoints that allow interaction with the application's data and functionalities. It is implemented through various classes and functions, such as 'ApiApplicationsEndpoint' and 'ApiApplicationDetailsEndpoint', which define the behavior of specific endpoints. These classes include methods like 'get' and 'post' that correspond to HTTP methods and define how the application should respond to different types of requests. The 'Api' also involves various models like 'ApiApplication' and 'ApiToken' that represent the data structures used in the application.

<SwmSnippet path="/src/sentry/api/endpoints/group_notes_details.py" line="20">

---

# GroupNotesDetailsEndpoint Class

The 'GroupNotesDetailsEndpoint' class is an example of an API endpoint in the application. It defines methods like 'delete' and 'put' that correspond to HTTP methods. These methods define how the application should handle DELETE and PUT requests to this endpoint.

```python
class GroupNotesDetailsEndpoint(GroupEndpoint):
    publish_status = {
        "DELETE": ApiPublishStatus.PRIVATE,
        "PUT": ApiPublishStatus.PRIVATE,
    }

    # We explicitly don't allow a request with an ApiKey
    # since an ApiKey is bound to the Organization, not
    # an individual. Not sure if we'd want to allow an ApiKey
    # to delete/update other users' comments
    def delete(self, request: Request, group, note_id) -> Response:
        if not request.user.is_authenticated:
            raise PermissionDenied(detail="Key doesn't have permission to delete Note")

        notes_by_user = Activity.objects.filter(
            group=group, type=ActivityType.NOTE.value, user_id=request.user.id
        )
        if not len(notes_by_user):
            raise ResourceDoesNotExist

        user_note = [n for n in notes_by_user if n.id == int(note_id)]
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/group_notes_details.py" line="30">

---

# delete Method

The 'delete' method in the 'GroupNotesDetailsEndpoint' class handles DELETE requests to the endpoint. It performs various operations like checking the user's authentication, filtering notes by the user, and deleting a note.

```python
    def delete(self, request: Request, group, note_id) -> Response:
        if not request.user.is_authenticated:
            raise PermissionDenied(detail="Key doesn't have permission to delete Note")

        notes_by_user = Activity.objects.filter(
            group=group, type=ActivityType.NOTE.value, user_id=request.user.id
        )
        if not len(notes_by_user):
            raise ResourceDoesNotExist

        user_note = [n for n in notes_by_user if n.id == int(note_id)]
        if not user_note or len(user_note) > 1:
            raise ResourceDoesNotExist
        note = user_note[0]

        webhook_data = {
            "comment_id": note.id,
            "timestamp": note.datetime,
            "comment": note.data.get("text"),
            "project_slug": note.project.slug,
        }
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/api_publish_status.py" line="4">

---

# ApiPublishStatus Class

The 'ApiPublishStatus' class is an enumeration used to track if an API is publicly documented. It can have values like 'UNKNOWN', 'PUBLIC', 'PRIVATE', and 'EXPERIMENTAL'.

```python
class ApiPublishStatus(Enum):
    """
    Used to track if an API is publicly documented
    """

    UNKNOWN = "unknown"

    PUBLIC = "public"  # stable API that is visible in public documentation
    PRIVATE = "private"  # any API that will not be published at any point
    EXPERIMENTAL = "experimental"  # API in development and will be published at some point
```

---

</SwmSnippet>

# Endpoint Explanations

Project Reprocessing and Release Files Endpoints

<SwmSnippet path="/src/sentry/api/endpoints/project_reprocessing.py" line="22">

---

## Project Reprocessing Endpoint

The ProjectReprocessingEndpoint class defines a POST endpoint that triggers the reprocessing process as a task. The endpoint requires the user to be authenticated and have the necessary permissions to initiate reprocessing.

```python
        return Response(status=200)

```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/api/endpoints/project_release_files.py" line="32">

---

## Project Release Files Endpoint

The ProjectReleaseFilesEndpoint class defines GET and POST endpoints for handling release files associated with a project. The GET endpoint retrieves a list of files for a given release, while the POST endpoint allows for the upload of a new file for the given release.

```python
def load_dist(results):
    # Dists are pretty uncommon.  In case they do appear load them now
    # as trying to join this on the DB does terrible things with large
    # offsets (it would otherwise generate a left outer join).
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
