# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Semi-UI is a modern, comprehensive React component library with 80+ components. It's a monorepo using Lerna + Yarn workspaces containing multiple packages for UI components, design tokens, animations, icons, build tools, and more.

## Commands

```bash
# Install dependencies (after cloning)
npm run bootstrap

# Start development
npm start                    # Run Storybook (JS config, port 6006)
npm run story:ts             # Run Storybook with TypeScript config (port 6007)
npm run docsite              # Run documentation site (Gatsby, port 3666)

# Testing
npm run test                 # Run all tests (unit + story)
npm run test:unit            # Run unit tests only
npm run test:story           # Run Storybook integration tests
npm run test:coverage        # Run tests with coverage
npm run test:cy              # Run Cypress E2E tests (requires Storybook running)

# Building
npm run build:lib            # Build all packages
npm run build:icon           # Build icon packages
npm run build:storybook      # Build static Storybook

# Linting
npm run lint                 # Run all linting
npm run lint:script          # Run ESLint
npm run lint:style           # Run Stylelint
npm run lint:script-fix      # Run ESLint with auto-fix
```

## Architecture

### Foundation/Adapter Pattern

Semi-UI uses an architecture inspired by Material Components Web, splitting components into:

**semi-foundation package**: Contains business logic, state management, and event handling
- `foundation.ts`: Base Foundation class with state management
- `<Component>/foundation.ts`: Component-specific Foundation class
- `<Component>/constants.ts`: CSS classes, string constants, numeric values
- `<Component>/*.scss`: Component styles (mixins, variables, rtl)

**semi-ui package**: Contains React components that use Foundation classes via Adapter pattern
- Components extend `BaseComponent` which provides default adapter methods
- `get adapter()`: Returns adapter object merging base adapter with component-specific adapters
- Adapter methods bridge Foundation logic to React component rendering

Example pattern (Select):
```tsx
// UI Component creates foundation with adapter
foundation = new SelectFoundation(this.adapter);

// Adapter provides methods like:
- getOptionsFromChildren()  // Parse children into options
- updateOptions()           // Update options state
- openMenu()/closeMenu()    // Control dropdown
- notifyChange()            // Emit change events
```

### Package Structure

```
packages/
├── semi-animation/         # Core animation utilities
├── semi-animation-react/   # React animation components
├── semi-animation-styled/  # Styled animation components
├── semi-eslint-plugin/     # Custom ESLint rules
├── semi-foundation/        # Business logic layer (Foundation/Adapter)
├── semi-icons/             # Icon components
├── semi-icons-lab/         # Lab/experimental icons
├── semi-illustrations/     # Illustration components
├── semi-json-viewer-core/  # JSON viewer core logic
├── semi-next/              # Next.js integration
├── semi-rspack/            # Rspack configuration
├── semi-scss-compile/      # SCSS compilation utilities
├── semi-theme-default/     # Default theme (3000+ design tokens)
├── semi-ui/                # Main UI component library
└── semi-webpack/           # Webpack configuration
```

### Component Structure (in semi-ui)

Each component typically has:
- `index.tsx` - Main export file
- `ComponentName.tsx` - Main component class
- `ComponentNameGroup.tsx` - Related group component
- `__test__/` - Unit tests (`.test.{tsx,ts}`)
- `_story/` - Storybook stories (`.stories.{tsx,js,jsx}`)
- `*.scss` - Style files (variables, animation, rtl, main)
- `index.md` / `index-en-US.md` - Documentation

### Base Component

`packages/semi-ui/_base/baseComponent.tsx` provides:
- Default adapter with state/prop/cache management
- `componentDidMount()` - Calls `foundation.init()`
- `componentWillUnmount()` - Calls `foundation.destroy()`
- `isControlled()` - Check if prop is controlled
- `getDataAttr()` - Extract data attributes from props

### SCSS Architecture

Components use SCSS with:
- Design tokens from `semi-theme-default`
- RTL support via `rtl.scss`
- CSS variables in `variables.scss`
- Mixins in `mixin.scss`
- Animation styles in `animation.scss`

## Key Conventions

- Class components with TypeScript (not hooks-based)
- Static `propTypes` for runtime validation
- Static `defaultProps` with `getDefaultPropsFromGlobalConfig()` support
- Static `__SemiComponentName__` for component identification
- Prop forwarding to underlying elements
- `x-semi-prop` attribute for analytics/tracking
- Event handlers call foundation methods, never directly modify state
- Use `@douyinfe/semi-foundation/utils/*` for utilities

## Configuration Files

- `jest.config.js`: Jest with enzyme, handles `type=unit` vs `type=story` env
- `.eslintrc.js`: ESLint with semi-design plugin
- `.stylelintrc.js`: Stylelint for SCSS
- `babel.config.js`: Babel configuration
- `tsconfig.json`: TypeScript with path aliases for `@douyinfe/semi-*`