# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Arco Design is a comprehensive React UI component library with 60+ crafted components. It follows semantic versioning and uses conventional commits.

**Technology Stack:**
- TypeScript for type safety
- LESS for styling with design tokens
- React 16+ support (includes React 19 adapter in `components/_util/`)
- Custom build tool: `arco-scripts`

## Development Commands

```bash
# Initial setup (run once after cloning)
yarn run init

# Start both component dev and site preview concurrently
yarn start

# Component development only (with hot reload)
yarn dev

# Site preview only (port 9000)
yarn dev:site

# Build all distributions (ES, CJS, CSS, UMD, hooks)
yarn build

# Build specific targets
yarn build:es       # ES modules
yarn build:cjs      # CommonJS
yarn build:dist     # UMD bundle
yarn build:css      # Styles only
yarn build:hooks    # Hooks package

# Testing
yarn test                    # Full test suite (client + node)
yarn test:client             # Client tests only (Jest + React Testing Library)
yarn test:node               # Node tests only
yarn test:watch              # Watch mode
yarn test:watch Alert        # Watch specific component tests

# Linting and formatting
yarn eslint                  # JavaScript/TypeScript linting
yarn stylelint               # CSS/LESS linting
yarn format                  # Prettier formatting

# Code generation
yarn docgen                  # Generate component READMEs from interface.ts
yarn docgen:hooks            # Generate hooks documentation
yarn icon                    # Generate icon components from icon source
yarn changelog               # Generate changelog

# Pre-commit checks
yarn pre-commit              # Runs prettier, eslint, and stylelint

# Other
yarn demo                    # Start Storybook
yarn test:screenshots        # Visual regression testing with Playwright
```

## Architecture

### Component Structure Pattern

Each component follows a consistent structure:

```
components/[ComponentName]/
├── index.tsx          # Main component (default export)
├── interface.ts       # TypeScript props interfaces with @zh/@en comments
├── group.tsx          # Sub-component (if applicable)
├── style/
│   ├── index.less     # Component styles
│   └── index.ts       # Style entry
├── __test__/
│   ├── index.test.tsx     # Unit tests
│   └── demo.test.ts       # Snapshot tests
├── __demo__/
│   ├── basic.md           # Demo examples
│   └── ...
├── __template__/
│   ├── index.en-US.md     # README template (EN)
│   └── index.zh-CN.md     # README template (CN)
└── __changelog__/
    ├── index.en-US.md     # Auto-generated (release)
    └── index.zh-CN.md     # Auto-generated (release)
```

### Component Implementation Pattern

Components use `forwardRef` and follow this pattern:

1. **Props handling**: Use `useMergeProps` hook to merge user props with default props and global config from `ConfigProvider`
2. **Prefix cls**: Use `getPrefixCls` from `ConfigContext` to generate BEM-compatible class names
3. **Context**: Access global config via `useContext(ConfigContext)`
4. **ClassNames**: Use `cs()` utility from `_util/classNames` for conditional classes
5. **Default props**: Define in `defaultProps` object, not as default parameters
6. **Export pattern**: Export component as `Component` and props type as `ComponentProps`

```typescript
import { forwardRef } from 'react';
import useMergeProps from '../_util/hooks/useMergeProps';

const defaultProps = { ... };
function Component(baseProps, ref) {
  const { getPrefixCls, ... } = useContext(ConfigContext);
  const props = useMergeProps(baseProps, defaultProps, componentConfig);
  // ...
}

const ForwardRefComponent = forwardRef(Component);
const Component = ForwardRefComponent as typeof ForwardRefComponent & { Group: typeof Group };
Component.displayName = 'Component';
export default Component;
```

### Global Configuration

`ConfigProvider` (components/ConfigProvider) provides global configuration:
- `componentConfig` - Default props for all components (keyed by component name)
- `prefixCls` - CSS prefix
- `rtl` - Right-to-left support
- `size` - Default component size
- `theme` - Theme configuration

Components access this via `useContext(ConfigContext)` and the `useMergeProps` hook automatically merges component-level defaults with global config.

**ComponentConfig pattern:**
```typescript
// Export componentConfig for ConfigProvider integration
export const componentConfig = {
  // Default props for this component when used in ConfigProvider
};

// Export componentProps for partial override
export const componentProps = {
  // Optional: additional props types for documentation
};
```

### Key Utilities

- `components/_util/hooks/useMergeProps.ts` - Merges user props, default props, and global config
- `components/_util/hooks/usePrefixCls.ts` - Generates BEM-style class names with prefix
- `components/_util/classNames.ts` - Conditional className builder (`cs()`)
- `components/_util/dom.ts` - DOM utilities
- `components/_util/dayjs.ts` - Day.js helpers
- `components/_util/warning.ts` - Warnings
- `components/_util/react-19-adapter.ts` - React 19 compatibility adapter

### Hooks Directory Structure

`hooks/` is a separate package with its own `package.json`:
```
hooks/
├── src/
│   ├── index.ts           # Main exports
│   └── useXxx/            # Individual hook implementations
├── lib/                   # Built CommonJS output
├── es/                    # Built ES modules output
└── package.json
```

### Testing Utilities

- `tests/util.ts` - Custom render function with Testing Library
- `tests/mountTest.tsx` - Basic mount/unmount test helper
- `tests/componentConfigTest.tsx` - Tests ConfigProvider integration
- `tests/demoTest.ts` - Demo snapshot tests

**Test files location:**
- Component tests: `components/[Name]/__test__/index.test.tsx`
- Snapshot tests: `components/[Name]/__test__/demo.test.ts`

**Run specific test:** `yarn test:watch ComponentName`

### Package Structure

- `@arco-design/web-react` - Main component library (`es/`, `lib/`, `dist/`)
- `@arco-design/web-react/hooks` - Reusable hooks in `hooks/` directory
- `@arco-design/web-react-icon` - Icon components in `icon/` directory

**Build Output:**
- `es/` - ES modules (browsers with bundlers)
- `lib/` - CommonJS (Node.js, older bundlers)
- `dist/` - UMD bundle (`arco.min.js` for direct browser include)
- `icon/` - Icon components (separate package)

## Contributing Guidelines

### TypeScript Configuration

Path aliases configured in `tsconfig.json`:
- `@arco-design/web-react` → `components/index.tsx`
- `@arco-design/web-react/_util/*` → `components/_util/*`

Use these imports for internal utilities when building components.

### Commit Messages

Follow conventional-changelog format:
```
<type>(<scope>): <description>

feat: New feature
fix: Bug fix
docs: Documentation only
style: Code formatting
refactor: Neither fix nor feature
perf: Performance improvement
test: Add tests
chore: Other changes
```

### Props Documentation

Use bilingual TSDoc comments in `interface.ts`:
```typescript
/**
 * @zh 按钮的标题
 * @en Title of the button
 */
title?: string;
```

**Do NOT edit README files manually** - they are auto-generated by `yarn docgen` from interface.ts. After changing props, run `yarn docgen` to update READMEs.

### New Components

1. Create component directory under `components/`
2. Follow the standard structure above
3. Add exports to `components/index.tsx`
4. Add tests to `__test__/`
5. Add demos to `__demo__/`
6. Run `yarn docgen` to generate READMEs
7. Update `tsdoc.json` if needed