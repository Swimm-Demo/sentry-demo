---
title: Introduction to Onboarding Components
---
Components in the Onboarding directory are a set of reusable React components that are used to build the onboarding user interface. These components are designed to guide the user through the initial setup process after they have created an account.

The components include setup instructions, post-install code snippets, and visual elements like the welcome background. Each component is encapsulated and manages its own state, making it easy to test and reuse across the onboarding flow.

For example, the `SetupIntroduction` component displays the step header and platform icon for the current step in the onboarding process. The `WelcomeBackground` component, on the other hand, is responsible for rendering the animated background on the welcome page.

<SwmSnippet path="/static/app/views/onboarding/components/integrations/addInstallationInstructions.tsx" line="12">

---

# Usage of Components

This is an example of a component that provides installation instructions. It is used to guide the user in setting up AWS Lambda with Sentry.

```tsx
          'The automated AWS Lambda setup will instrument your Lambda functions with Sentry error and performance monitoring without any code changes. We use CloudFormation Stack ([learnMore]) to create the Sentry role which gives us access to your AWS account.',
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/onboarding/components/integrations/postInstallCodeSnippet.tsx" line="46">

---

# Post Install Code Snippet Component

This component is used after the installation process. It provides the user with a code snippet and guides them on the next steps after installation.

```tsx
              "If you're new to Sentry, use the email alert to access your account and complete a product tour."
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
