---
title: Basic Concepts of Settings Components
---
Components in the Settings section of the sentry-demo repository are primarily used to build the user interface for the settings page. They are modular pieces of code that are responsible for rendering part of the user interface and handling any user interactions. They are written in TypeScript and use the React library for building the user interface.

The components are styled using the styled-components library, which allows the use of CSS in JavaScript. This approach enables the components to have their own encapsulated styles that don't affect other parts of the application.

The components in the Settings section are organized in a hierarchical manner. At the top level, there is a SettingsLayout component that serves as a container for other components. It uses various styled components to define its layout and appearance.

The SettingsLayout component uses a number of child components to render different parts of the settings page. For example, it uses the SettingsNavigation component to render the navigation menu, and the SettingsHeader component to render the header of the settings page.

Each component has a specific role in the overall layout of the settings page. For example, the SettingsNavigation component is responsible for rendering the navigation menu, while the SettingsHeader component is responsible for rendering the header of the settings page.

The components also use various hooks and functions to handle user interactions and state changes. For example, the SettingsLayout component uses the useState and useEffect hooks from React to manage the visibility of the mobile navigation menu.

In addition to the main layout components, there are also many smaller components that are used to render specific parts of the settings page. These include components for rendering individual settings items, navigation items, and text blocks.

<SwmSnippet path="/static/app/views/settings/components/teamSelect/teamSelectForMember.tsx" line="194">

---

# TeamPanelItem Component

The `TeamPanelItem` is a styled component that is used to render each team item in the team selection panel. It uses the `PanelItem` component and adds additional styles to it.

```tsx
const TeamPanelItem = styled(PanelItem)`
  ${GRID_TEMPLATE}
  padding: ${space(2)};
`;
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/components/teamSelect/teamSelectForMember.tsx" line="146">

---

Here, the `TeamPanelItem` component is used in the render method of the parent component. It is used as a JSX tag and wraps other components and HTML elements that make up each team item.

```tsx
  return (
    <TeamPanelItem data-test-id="team-row-for-member">
      <div>
        <Link to={`/settings/${organization.slug}/teams/${team.slug}/`}>
          <TeamBadge team={team} />
        </Link>
      </div>

      <div>
        <TeamRoleSelect
          disabled={disabled}
          size="xs"
          organization={organization}
          team={team}
          member={member}
          onChangeTeamRole={newRole => onChangeTeamRole(team.slug, newRole)}
        />
      </div>

      <div>
        <Button
```

---

</SwmSnippet>

<SwmSnippet path="/static/app/views/settings/components/teamSelect/teamSelectForProject.tsx" line="149">

---

# TeamPanelItem Component in teamSelectForProject

In a different file, `TeamPanelItem` is defined again with slightly different styles. This shows how components can be customized to fit the needs of different parts of the application.

```tsx
const TeamPanelItem = styled(PanelItem)`
  padding: ${space(2)};
  align-items: center;
  justify-content: space-between;
`;
```

---

</SwmSnippet>

&nbsp;

*This is an auto-generated document by Swimm AI 🌊 and has not yet been verified by a human*

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBc2VudHJ5LWRlbW8lM0ElM0FTd2ltbS1EZW1v" repo-name="sentry-demo" doc-type="overview"><sup>Powered by [Swimm](/)</sup></SwmMeta>
