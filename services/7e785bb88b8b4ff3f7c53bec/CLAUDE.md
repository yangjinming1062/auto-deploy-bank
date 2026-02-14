# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the Microsoft Fluent UI monorepo - a comprehensive design system and UI component library. It contains three major projects:

1. **Fluent UI v9** (`@fluentui/react-components`) - Current stable, actively developed, located in `packages/react-components/`
2. **Fluent UI v8** (`@fluentui/react`) - Maintenance mode, located in `packages/react/`
3. **Fluent UI Web Components** (`@fluentui/web-components`) - Framework-agnostic, located in `packages/web-components/`

For new work, prioritize v9 components in `packages/react-components/`.

## Common Commands

### Installation & Setup
```bash
yarn                              # Install dependencies and link packages
yarn clean                        # Clean all build artifacts
```

### Development
```bash
yarn start                        # Interactive prompt to choose project to run
yarn nx run <project>:build       # Build specific project with dependencies
yarn nx run-many -t build         # Build multiple projects
yarn nx run <project>:test        # Run tests for specific project
yarn nx run <project>:test -u     # Update Jest snapshots
yarn nx run <project>:start       # Start Storybook for component
```

### Component Generation (v9)
```bash
yarn create-component             # Interactive component generator
```

### Release Management
```bash
yarn change                       # Create beachball change file (REQUIRED for PRs)
yarn check:change                 # Verify change files are correct
```

### Project Discovery
```bash
yarn nx show projects             # List all projects
```

## v9 Component Architecture

All v9 components follow this exact structure:

```
packages/react-components/react-component-name/
├── library/src/
│   ├── index.ts                  # Main package exports
│   ├── ComponentName.tsx         # ForwardRefComponent export
│   ├── components/ComponentName/
│   │   ├── ComponentName.test.tsx
│   │   ├── ComponentName.tsx
│   │   ├── ComponentName.types.ts
│   │   ├── useComponentName.ts
│   │   ├── useComponentNameStyles.styles.ts
│   │   └── renderComponentName.tsx
│   └── testing/
└── stories/
    ├── ComponentName.stories.tsx
    └── ComponentNameDefault.stories.tsx
```

### Core Hook Pattern

v9 components use three mandatory hooks:
1. `useComponentName_unstable()` - State management
2. `useComponentNameStyles_unstable()` - Griffel styling
3. `renderComponentName_unstable()` - JSX rendering

### Slots System

All v9 components use slots for extensibility:

```tsx
type ButtonSlots = {
  root: Slot<'button'>;
  icon?: Slot<'span'>;
};

// Use slot.always() for required slots, slot.optional() for optional
state.root = slot.always(props.root, { elementType: 'button' });
state.icon = slot.optional(props.icon, { elementType: 'span' });
```

### Styling with Griffel

v9 uses Griffel for compile-time CSS-in-JS with atomic classes:

```tsx
import { makeStyles } from '@griffel/react';
import { tokens } from '@fluentui/react-theme';

export const useButtonStyles = makeStyles({
  root: {
    color: tokens.colorNeutralForeground1,
    ':hover': { backgroundColor: tokens.colorNeutralBackground1Hover },
  },
});
```

**Critical**: Always use design tokens from `@fluentui/react-theme`, never hardcoded values.

## Testing Architecture

```bash
# Unit tests (Jest)
yarn nx run react-button:test
yarn nx run react-button:test -u              # Update snapshots

# Visual regression (Storybook + StoryWright)
yarn nx run vr-tests-react-components:test-vr # Creates diff images only

# E2E integration (Cypress)
yarn nx run react-components:e2e

# SSR compatibility
yarn nx run ssr-tests-v9:test-ssr

# Cross-version React testing
yarn nx run rit-tests-v9:test-rit
```

## Build System

- **Package Manager**: Yarn v1 with workspace support
- **Build System**: Nx with custom workspace plugin (`tools/workspace-plugin/`)
- **Compiler**: SWC for Jest, esbuild for bundles
- **API Documentation**: API Extractor generates api.md files
- **Lint**: ESLint with `@fluentui/eslint-plugin`
- **Format**: Prettier (automatic via lint-staged)

## Key Conventions

### Change Files (Beachball)
All changes require a beachball change file created via `yarn change`. This tracks version bumps and changelog entries automatically.

### TypeScript
- Strict mode enabled
- Components use `ForwardRefComponent<ComponentProps>`
- Props extend `ComponentPropsWithRef<'elementType'>`

### Package Versioning
- Beachball manages versioning
- Each package has `beachball` config in package.json
- `disallowedChangeTypes` defines allowed change types (typically ["major", "prerelease"] excluded)

### API Generation
After changing component APIs, run:
```bash
yarn nx run <project>:generate-api
```