---
title: Introduction to Debug Tools
---
Debug in the Sentry-Demo repository refers to a set of tools and functionalities that help in identifying, understanding, and resolving issues that might occur in the application. It includes various scripts and views that generate mock data and simulate different scenarios for testing purposes. This helps in ensuring the robustness of the application by allowing developers to anticipate and handle potential errors.

For instance, the 'debug_chart_renderer.py' file contains various constants and data structures that simulate different types of data for testing the chart rendering functionality. It includes mock data for different types of charts such as 'discover_total_period', 'discover_geo', 'discover_total_daily', etc. These constants are used to generate different types of charts for debugging and testing purposes.

Another example is the 'debug_weekly_report.py' file, which contains a class 'DebugWeeklyReportView' that generates a context for a weekly report. This is used for testing the weekly report generation functionality of the application.

The 'debug_auth_views.py' file contains classes like 'DebugAuthConfirmIdentity' and 'DebugAuthConfirmLink' which are used to simulate the authentication process. These classes are used to test the authentication views of the application.

In summary, the debug functionality in the Sentry-Demo repository is a crucial part of the development process, helping to ensure the reliability and robustness of the application by allowing developers to test different functionalities and handle potential errors.

<SwmSnippet path="/src/sentry/web/frontend/debug/debug_chart_renderer.py" line="8">

---

# Debug Chart Renderer

This file contains various constants and data structures that simulate different types of data for testing the chart rendering functionality. It includes mock data for different types of charts such as 'discover_total_period', 'discover_geo', 'discover_total_daily', etc. These constants are used to generate different types of charts for debugging and testing purposes.

```python
discover_total_period = {
    "seriesName": "Discover total period",
    "stats": {
        "data": [
            [1616168400, [{"count": 0}]],
            [1616168700, [{"count": 12}]],
            [1616169000, [{"count": 13}]],
            [1616169300, [{"count": 9}]],
            [1616169600, [{"count": 12}]],
            [1616169900, [{"count": 21}]],
            [1616170200, [{"count": 11}]],
            [1616170500, [{"count": 22}]],
            [1616170800, [{"count": 18}]],
            [1616171100, [{"count": 15}]],
            [1616171400, [{"count": 14}]],
            [1616171700, [{"count": 31}]],
            [1616172000, [{"count": 18}]],
            [1616172300, [{"count": 13}]],
            [1616172600, [{"count": 17}]],
            [1616172900, [{"count": 9}]],
            [1616173200, [{"count": 9}]],
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/web/frontend/debug/debug_weekly_report.py" line="23">

---

# Debug Weekly Report View

This file contains a class 'DebugWeeklyReportView' that generates a context for a weekly report. This is used for testing the weekly report generation functionality of the application.

```python
class DebugWeeklyReportView(MailPreviewView):
    def get_context(self, request):
        organization = Organization(id=1, slug="myorg", name="MyOrg")

        random = get_random(request)

        duration = 60 * 60 * 24 * 7
        timestamp = floor_to_utc_day(
            to_datetime(
                random.randint(
                    datetime(2015, 6, 1, 0, 0, 0, tzinfo=timezone.utc).timestamp(),
                    datetime(2016, 7, 1, 0, 0, 0, tzinfo=timezone.utc).timestamp(),
                )
            )
        ).timestamp()
        ctx = OrganizationReportContext(timestamp, duration, organization)
        ctx.projects_context_map.clear()

        start_timestamp = ctx.start.timestamp()

        daily_maximum = random.randint(1000, 10000)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/web/frontend/debug/debug_auth_views.py" line="1">

---

# Debug Authentication Views

This file contains classes like 'DebugAuthConfirmIdentity' and 'DebugAuthConfirmLink' which are used to simulate the authentication process. These classes are used to test the authentication views of the application.

```python
from django.http import HttpRequest, HttpResponse
from django.views.generic import View

from sentry.models.user import User
from sentry.web.helpers import render_to_response


class DebugAuthConfirmIdentity(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        auth_identity = {"id": "bar@example.com", "email": "bar@example.com"}
        return render_to_response(
            "sentry/auth-confirm-identity.html",
            context={
                "existing_user": User(email="foo@example.com"),
                "identity": auth_identity,
                "login_form": None,
                "identity_display_name": auth_identity["email"],
                "identity_identifier": auth_identity["id"],
            },
            request=request,
        )
```

---

</SwmSnippet>

# Debug Functionality

This section provides an overview of the main functions in the Debug functionality of the Sentry-Demo repository.

<SwmSnippet path="/src/sentry/web/frontend/debug/debug_chart_renderer.py" line="522">

---

## DebugChartRendererView

The `DebugChartRendererView` class is used to generate different types of charts for debugging and testing purposes. It uses various constants and data structures that simulate different types of data.

```python
class DebugChartRendererView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        ret = []

        ret.append(
            charts.generate_chart(ChartType.SLACK_DISCOVER_TOTAL_PERIOD, discover_total_period)
        )
        ret.append(
            charts.generate_chart(ChartType.SLACK_DISCOVER_TOTAL_PERIOD, discover_multi_y_axis)
        )
        ret.append(charts.generate_chart(ChartType.SLACK_DISCOVER_TOTAL_PERIOD, discover_empty))
        ret.append(
            charts.generate_chart(ChartType.SLACK_DISCOVER_TOTAL_DAILY, discover_total_daily)
        )
        ret.append(
            charts.generate_chart(ChartType.SLACK_DISCOVER_TOTAL_DAILY, discover_total_daily_multi)
        )
        ret.append(charts.generate_chart(ChartType.SLACK_DISCOVER_TOTAL_DAILY, discover_empty))
        ret.append(charts.generate_chart(ChartType.SLACK_DISCOVER_TOP5_PERIOD, discover_top5))
        ret.append(charts.generate_chart(ChartType.SLACK_DISCOVER_TOP5_PERIOD, discover_empty))
        ret.append(charts.generate_chart(ChartType.SLACK_DISCOVER_TOP5_PERIOD_LINE, discover_top5))
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/web/frontend/debug/debug_organization_integration_request.py" line="14">

---

## DebugOrganizationJoinRequestEmailView

The `DebugOrganizationJoinRequestEmailView` class is used to simulate the process of a user requesting to join an organization. It generates a mock email notification for this scenario.

```python
class DebugOrganizationIntegrationRequestEmailView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        org = Organization(id=1, slug="default", name="Default")
        requester = User(name="Rick Swan")
        recipient = User(name="James Bond")
        recipient_member = OrganizationMember(user_id=recipient.id, organization=org)

        notification = IntegrationRequestNotification(
            org,
            requester,
            provider_type="first_party",
            provider_slug="slack",
            provider_name="Slack",
        )

        # hack to avoid a query
        notification.role_based_recipient_strategy.set_member_in_cache(recipient_member)
        return render_preview_email_for_notification(notification, recipient)
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/web/frontend/debug/debug_generic_issue.py" line="15">

---

## DebugGenericIssueEmailView

The `DebugGenericIssueEmailView` class is used to generate a mock issue for testing purposes. It uses the `make_generic_event` function to create a generic event and then generates an email preview for this event.

```python
class DebugGenericIssueEmailView(View):
    def get(self, request):
        org = Organization(id=1, slug="example", name="Example")
        project = Project(id=1, slug="example", name="Example", organization=org)

        event = make_generic_event(project)
        group = event.group

        rule = Rule(id=1, label="An example rule")

        generic_issue_data_html = get_generic_data(event)
        section_header = "Issue Data" if generic_issue_data_html else ""

        return MailPreview(
            html_template="sentry/emails/generic.html",
            text_template="sentry/emails/generic.txt",
            context={
                "rule": rule,
                "rules": get_rules([rule], org, project),
                "group": group,
                "event": event,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/web/frontend/debug/debug_performance_issue.py" line="16">

---

## DebugPerformanceIssueEmailView

The `DebugPerformanceIssueEmailView` class is used to simulate a performance issue. It uses the `make_performance_event` function to create a performance event and then generates an email preview for this event.

```python
class DebugPerformanceIssueEmailView(View):
    def get(self, request, sample_name="transaction-n-plus-one"):
        project = Project.objects.get(id=1)
        org = project.organization
        perf_event = make_performance_event(project, sample_name)
        if request.GET.get("is_test", False):
            perf_event.group.id = 1
        perf_group = perf_event.group

        rule = Rule(id=1, label="Example performance rule")

        transaction_data = get_transaction_data(perf_event)
        interface_list = get_interface_list(perf_event)

        context = {
            **get_shared_context(rule, org, project, perf_group, perf_event),
            "interfaces": interface_list,
            "project_label": project.slug,
            "commits": json.loads(COMMIT_EXAMPLE),
            "transaction_data": [("Span Evidence", mark_safe(transaction_data), None)],
            "issue_type": perf_group.issue_type.description,
```

---

</SwmSnippet>

<SwmSnippet path="/src/sentry/web/frontend/debug/debug_new_release_email.py" line="21">

---

## DebugNewReleaseEmailView

The `DebugNewReleaseEmailView` class is used to simulate the release of a new version. It generates mock data for a new release and then generates an email preview for this release.

```python
class DebugNewReleaseEmailView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        org = Organization(id=1, slug="organization", name="My Company")
        projects = [
            Project(id=1, organization=org, slug="project", name="My Project"),
            Project(id=2, organization=org, slug="another-project", name="Another Project"),
            Project(id=3, organization=org, slug="yet-another-project", name="Yet Another Project"),
        ]
        version = "6c998f755f304593a4713abd123eaf8833a2de5e"
        version_parsed = parse_release(version)["description"]
        release = Release(
            organization_id=org.id,
            version=version,
            date_added=datetime.datetime(2016, 10, 12, 15, 39, tzinfo=timezone.utc),
        )

        deploy = Deploy(
            release=release,
            organization_id=org.id,
            environment_id=1,
            date_finished=datetime.datetime(2016, 10, 12, 15, 39, tzinfo=timezone.utc),
```

---

</SwmSnippet>

# Debug Endpoints

Debug Endpoints

<SwmSnippet path="/src/sentry/web/frontend/debug/debug_onboarding_continuation_email.py" line="11">

---

## DebugOrganizationOnboardingContinuationEmail

The `DebugOrganizationOnboardingContinuationEmail` class is a part of the debug functionality. It simulates the process of sending an onboarding continuation email to a user. The `get` method in this class generates a mock organization and user, and then uses these to create a mail preview. This preview is then rendered to a response, simulating the process of sending an email.

```python
class DebugOrganizationOnboardingContinuationEmail(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        platforms = request.GET.getlist("platforms", ["javascript", "python", "flutter"])
        org = Organization(id=1, name="My Company")
        user = User(name="Ben")
        preview = MailPreviewAdapter(**get_request_builder_args(user, org, platforms))

        return render_to_response("sentry/debug/mail/preview.html", {"preview": preview})
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
