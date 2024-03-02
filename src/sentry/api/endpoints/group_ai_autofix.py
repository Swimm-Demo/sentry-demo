from __future__ import annotations

import logging
from datetime import datetime

import requests
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from rest_framework.response import Response

from sentry import features
from sentry.api.api_owners import ApiOwner
from sentry.api.api_publish_status import ApiPublishStatus
from sentry.api.base import region_silo_endpoint
from sentry.api.bases.group import GroupEndpoint
from sentry.api.serializers import EventSerializer, serialize
from sentry.models.group import Group
from sentry.models.integrations.repository_project_path_config import RepositoryProjectPathConfig
from sentry.models.repository import Repository
from sentry.tasks.ai_autofix import ai_autofix_check_for_timeout
from sentry.types.ratelimit import RateLimit, RateLimitCategory
from sentry.utils import json

logger = logging.getLogger(__name__)

from rest_framework.request import Request

TIMEOUT_SECONDS = 60 * 30  # 30 minutes


@region_silo_endpoint
class GroupAiAutofixEndpoint(GroupEndpoint):
    publish_status = {
        "POST": ApiPublishStatus.EXPERIMENTAL,
        "GET": ApiPublishStatus.EXPERIMENTAL,
    }
    owner = ApiOwner.ML_AI
    # go away
    private = True
    enforce_rate_limit = True
    rate_limits = {
        "POST": {
            RateLimitCategory.IP: RateLimit(5, 1),
            RateLimitCategory.USER: RateLimit(5, 1),
            RateLimitCategory.ORGANIZATION: RateLimit(5, 1),
        }
    }

    @staticmethod
    def _get_repos_from_code_mapping(group: Group) -> list[dict]:
        repo_configs: list[
            RepositoryProjectPathConfig
        ] = RepositoryProjectPathConfig.objects.filter(project__in=[group.project])

        repos: dict[tuple, dict] = {}
        for repo_config in repo_configs:
            repo: Repository = repo_config.repository
            repo_name_sections = repo.name.split("/")

            # We expect a repository name to be in the format of "owner/name" for now.
            if len(repo_name_sections) > 1 and repo.provider:
                repo_dict = {
                    "provider": repo.provider,
                    "owner": repo_name_sections[0],
                    "name": "/".join(repo_name_sections[1:]),
                }
                repo_key = (repo_dict["provider"], repo_dict["owner"], repo_dict["name"])

                repos[repo_key] = repo_dict

        return list(repos.values())

    def _get_event_entries(
        self, group: Group, user: AbstractBaseUser | AnonymousUser
    ) -> list | None:
        latest_event = group.get_latest_event()

        if not latest_event:
            return None

        serialized_event = serialize(latest_event, user, EventSerializer())
        return serialized_event["entries"]

    def _make_error_metadata(self, autofix: dict, reason: str):
        return {
            **autofix,
            "completed_at": datetime.now().isoformat(),
            "status": "ERROR",
            "fix": None,
            "error_message": reason,
            "steps": [],
        }

    def _respond_with_error(self, group: Group, metadata: dict, reason: str, status: int):
        metadata["autofix"] = self._make_error_metadata(metadata["autofix"], reason)

        group.data["metadata"] = metadata
        group.save()

        return Response(
            {
                "detail": reason,
            },
            status=status,
        )

    def _call_autofix(
        self,
        group: Group,
        repos: list[dict],
        event_entries: list[dict],
        additional_context: str,
    ):
        response = requests.post(
            f"{settings.SEER_AUTOFIX_URL}/v0/automation/autofix",
            data=json.dumps(
                {
                    "organization_id": group.organization.id,
                    "project_id": group.project.id,
                    "repos": repos,
                    "issue": {
                        "id": group.id,
                        "title": group.title,
                        "events": [{"entries": event_entries}],
                    },
                    "additional_context": additional_context,
                }
            ),
            headers={"content-type": "application/json;charset=utf-8"},
        )

        response.raise_for_status()

    def post(self, request: Request, group: Group) -> Response:
        data = json.loads(request.body)

        created_at = datetime.now().isoformat()
        metadata = group.data.get("metadata", {})
        metadata["autofix"] = {
            "created_at": created_at,
            "status": "PROCESSING",
            "steps": [
                {
                    "id": "1",
                    "index": 1,
                    "title": "Waiting to be picked up...",
                    "status": "PROCESSING",
                }
            ],
        }

        if not features.has("projects:ai-autofix", group.project):
            return self._respond_with_error(
                group, metadata, "AI Autofix is not enabled for this project.", 403
            )

        event_entries = self._get_event_entries(group, request.user)

        if event_entries is None:
            return self._respond_with_error(
                group, metadata, "Cannot fix issues without an event.", 400
            )

        if not any([exception.get("type") == "exception" for exception in event_entries]):
            return self._respond_with_error(
                group, metadata, "Cannot fix issues without a stacktrace.", 400
            )

        repos = self._get_repos_from_code_mapping(group)

        if not repos:
            return self._respond_with_error(
                group, metadata, "Found no Github repositories linked to this project.", 400
            )

        try:
            self._call_autofix(group, repos, event_entries, data.get("additional_context", ""))

            # Mark the task as completed after TIMEOUT_SECONDS
            ai_autofix_check_for_timeout.apply_async(
                kwargs={
                    "group_id": group.id,
                    "created_at": created_at,
                },
                countdown=TIMEOUT_SECONDS,
            )
        except Exception as e:
            logger.exception(
                "Failed to send autofix to seer",
                extra={
                    "group_id": group.id,
                    "created_at": created_at,
                    "exception": e,
                },
            )

            return self._respond_with_error(
                group,
                metadata,
                "Failed to send autofix to seer.",
                500,
            )

        group.data["metadata"] = metadata
        group.save()

        return Response(
            status=202,
        )

    def get(self, request: Request, group: Group) -> Response:
        metadata = group.data.get("metadata", {})
        autofix_data = metadata.get("autofix", None)

        return Response({"autofix": autofix_data})
