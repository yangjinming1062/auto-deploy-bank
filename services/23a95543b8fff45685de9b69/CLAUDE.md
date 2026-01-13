# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start Commands

```bash
# Setup
make install              # Install all dependencies

# Development
make build                # Build all packages (TypeScript compilation)
make run-simple           # Run simple example with hot reload (port 8080)
make run-demo             # Run e-commerce demo
make run-crm              # Run CRM example
make run-tutorial         # Run tutorial example

# Testing
make test                 # Run all tests (unit + e2e)
make test-unit            # Run unit tests only
make test-unit-watch      # Run tests in watch mode
make test-e2e             # Run e2e tests
make test-e2e-local       # Run e2e tests with GUI (after make run-simple)

# Code Quality
make lint                 # ESLint checks
make prettier             # Format code
yarn test-unit [pattern]  # Run specific test file
```

## Repository Structure

This is a **Lerna monorepo** containing multiple packages:

```
react-admin/
├── packages/              # 19 packages managed by Lerna
│   ├── ra-core/           # Core logic, hooks, controllers (headless)
│   ├── ra-ui-materialui/  # Material UI components
│   ├── react-admin/       # Main distribution package
│   ├── ra-data-*/         # Data provider adapters (fakerest, graphql, simple-rest, etc.)
│   ├── ra-i18n-*/         # i18n providers
│   ├── ra-language-*/     # Translation packs
│   ├── ra-input-rich-text/# Rich text input
│   ├── ra-no-code/        # No-code admin builder
│   └── create-react-admin/# Project scaffolding CLI
├── examples/              # Example applications
│   ├── simple/            # E2E test app (use for dev)
│   ├── demo/              # Full e-commerce demo
│   ├── crm/               # CRM application
│   ├── tutorial/          # Tutorial app
│   └── no-code/           # No-code example
├── cypress/               # E2E tests (target: simple example)
├── docs/                  # Jekyll docs (UI components)
├── docs_headless/         # Astro docs (headless components)
└── scripts/               # Build scripts
```

## High-Level Architecture

### Provider Pattern
React-admin uses **adapters called "providers"** for external integrations:

- **Data Provider** - abstracts API calls (REST/GraphQL/custom)
- **Auth Provider** - handles authentication & authorization
- **i18n Provider** - manages translations

All providers are interfaces, allowing custom implementations.

### Headless Core Architecture
The framework is split into:
- **ra-core**: All business logic, hooks, controllers (no UI)
- **ra-ui-materialui**: Material UI rendering layer
- **react-admin**: Main package that re-exports everything

This allows creating custom UIs using core hooks or swapping UI libraries.

### Controller-View Separation
- Controllers (ra-core/src/controller/) handle business logic
- Views (ra-ui-materialui/src/) handle rendering
- Controllers expose data via hooks, enabling flexible composition

### Key ra-core Directories
- `src/auth/` - Authentication & authorization
- `src/controller/` - CRUD controllers & state management
- `src/dataProvider/` - Data fetching & caching (TanStack Query)
- `src/form/` - Form handling (React Hook Form)
- `src/routing/` - Navigation & routing (React Router)
- `src/i18n/` - Internationalization

## Development Patterns

### Hook-Based API
All functionality exposed through hooks following React patterns:
```typescript
// Data hooks
const { data, isLoading } = useGetList('posts', { pagination: { page: 1 } });

// State management
const [filters, setFilters] = useFilterState();

// Auth
const { permissions } = usePermissions();
```

### TypeScript Requirements
- **Strict mode enabled** - no implicit `any`
- **Complete type exports** - all public APIs must be typed
- **Generic types** for flexibility (e.g., `RecordType extends RaRecord`)
- **No commented code** or obvious documentation

### Component Patterns
1. **Composition over configuration** - Use React composition
2. **Smart defaults** - Components work out-of-box
3. **Props pass-through** - Spread additional props to root element
4. **No `React.cloneElement()`** - breaks composition
5. **No children inspection** - violates React patterns

```jsx
// Good pattern
export const MyField = ({ source, ...props }) => {
    const record = useRecordContext();
    return <TextField {...props} value={record?.[source]} />;
};
```

## Testing Requirements

### Unit & Integration Tests (Jest)
- Location: `*.spec.tsx` alongside source files
- Use testing-library for rendering and assertions
- **Don't test implementation details** - test user interactions and visible output
- Reuse stories as test cases

### Storybook
- Location: `*.stories.tsx` alongside components
- **All components must have stories** demonstrating all props
- Use mock data providers (FakeRest)
- Stories used for visual testing

### E2E Tests (Cypress)
- Location: `cypress/e2e/`
- Target: `examples/simple/` app
- Test critical user paths only
- Commands: `make run-simple` then `make test-e2e-local` for GUI

## Key Dependencies
- **React**: 18.3+ (also supports 19.0+)
- **TypeScript**: 5.8+
- **TanStack Query**: 5.90+ (React Query)
- **React Hook Form**: 7.65+
- **React Router**: 6.28+ or 7.1+
- **Material UI**: 5.16+ / 6.x / 7.x
- **Lodash**: 4.17+
- **Inflection**: 3.0+

## Build System

### Package Building
- Uses `zshy` bundler for package compilation
- Outputs: CJS (`dist/index.cjs`), ESM (`dist/index.js`), Types (`dist/index.d.ts`)
- Each package has own `build` script
- Run `make build` for all packages
- Individual packages: `make build-ra-core`, etc.

### Type Checking
- Root `tsconfig.json` for project-wide config
- Each package has own `tsconfig.json`
- Build validates types: `yarn build` runs typecheck

## Workflow & PR Process

### Branch Strategy
- **`master`** - bug fixes, documentation (non-breaking)
- **`next`** - features, breaking changes

### Pre-commit Hooks ( Husky)
Automatically run:
- Tests for modified files
- Prettier formatting
- ESLint validation
- TypeScript compilation

### Testing Changes in Examples
**Recommended**: Use simple example for visual testing
```bash
make run-simple  # Live reload on port 8080
```

**Complete**: Use demo example
```bash
make build  # Build all packages first
make run-demo
```

**External App**: Use yarn link
```bash
# Build local react-admin
make build
cd /path/to/myapp
yarn link /path/to/react-admin/packages/react-admin
yarn link /path/to/react-admin/packages/ra-core
```

### Commit Messages
Format: `<type>: <description>`

Types: `fix`, `feat`, `docs`, `perf`, `test`, `refactor`, `chore`

Examples:
```
fix: Prevent duplicate API calls in useGetList hook
feat: Add support for custom row actions in Datagrid
docs: Clarify dataProvider response format
```

## Important Notes

### What NOT to Do
- **Don't** add features achievable with pure React in a few lines
- **Don't** use `React.cloneElement()` or inspect children
- **Don't** skip tests - they run automatically on commit
- **Don't** force push to main branches

### Performance Considerations
- Use `React.memo()` for expensive components
- Leverage `useMemo()` and `useCallback()` appropriately
- Implement pagination for large datasets
- Use query caching via TanStack Query

### Browser Support
- Modern browsers only (Chrome, Firefox, Safari, Edge)
- No IE11 support
- ES5 compilation target

## Common Make Commands

```bash
make                      # Show all commands
make install              # Install dependencies
make build                # Build all packages
make run-simple           # Run simple example (dev)
make test                 # Run all tests
make lint                 # Check code quality
make prettier             # Format code
make storybook            # Launch Storybook
make doc                  # Build Jekyll docs
```

## Related Documentation
- Full dev guide: `Agents.md`
- Main docs: `README.md`
- Changelog: `CHANGELOG.md`
- Upgrade guide: `UPGRADE.md`