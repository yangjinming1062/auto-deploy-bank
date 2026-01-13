# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Stoplight Elements is an API documentation toolkit that generates beautiful, interactive API documentation from OpenAPI specifications. It provides React Components and Web Components for building API reference documentation with a three-column "Stripe-esque" layout or stacked layouts for CMS integration.

## Quick Start

```bash
# Install dependencies
yarn

# Start demo (http://localhost:4025)
cd demo && yarn start

# Develop using storybooks
yarn elements-core storybook
yarn elements storybook
yarn elements-dev-portal storybook
```

## Common Commands

### Building
```bash
yarn build                    # Build all packages
yarn build.docs              # Build documentation
yarn type-check              # Type check all packages
yarn lint                    # Lint all code
```

### Testing

#### Unit Tests
```bash
yarn test                     # Run all unit tests
yarn test.prod               # Run tests with coverage

# Run tests for specific package
yarn elements test           # Run tests for elements package
yarn elements-core test      # Run tests for elements-core package
yarn elements-dev-portal test # Run tests for elements-dev-portal package

# Jest flags (append to any test command)
yarn elements test --verbose           # Show individual test results
yarn elements test -o                  # Only run tests for changed files
yarn elements test --watch             # Watch mode (implies -o)
yarn elements test -t Test\ Name       # Run tests matching pattern
```

#### End-to-End Tests (Framework Integration)
```bash
# Run as CI would (headless)
yarn build                    # Build Elements first (required)
yarn copy:react-cra          # Set up integration test env (once)
yarn build:react-cra
yarn e2e:run:react-cra

# Manual testing with Cypress console
yarn e2e:open                # Opens Cypress test runner

# Available integrations: react-cra, angular, static-html
yarn e2e:run:angular
yarn e2e:run:static-html
```

Note: E2E tests require Elements to be built first. The `copy:$INTEGRATION-NAME` command only needs to run once after cloning.

### Development
```bash
# Start storybooks for component development
yarn elements-core storybook
yarn elements storybook
yarn elements-dev-portal storybook

# Note: Package changes are automatically reflected when linked
```

### Release Process
```bash
yarn version                 # Interactive version bumping (main branch only)
yarn release                 # Publish to npm
yarn release.docs            # Release documentation
```

## Code Architecture

### Monorepo Structure

This is a **Yarn monorepo** with three main packages:

1. **`@stoplight/elements-core`** (packages/elements-core/)
   - Shared React components, utilities, and business logic
   - Contains 11 component subdirectories
   - Used by both elements and elements-dev-portal
   - **Most code lives here**

2. **`@stoplight/elements`** (packages/elements/)
   - User-facing package for API documentation UI
   - Wraps elements-core components
   - Provides React and Web Component interfaces
   - Focuses on single API

3. **`@stoplight/elements-dev-portal`** (packages/elements-dev-portal/)
   - Full documentation portal with multiple APIs
   - Search functionality
   - Markdown article support
   - Version selection

### Development Patterns

- **Component-Based**: React 16.14.0 with functional components and hooks
- **Higher-Order Components (HOC)**: Used for code reuse
- **Container/Presenter**: Separation of concerns pattern
- **Context API**: State management
- **Web Components**: Shadow DOM encapsulation for framework-agnostic usage
- **Storybook-Driven Development**: Component development and testing

### Key Technologies

- React 16.14.0 with hooks
- React Router for navigation
- React Query for data fetching
- Jotai for state management
- Mosaic UI component library (custom)
- styled-components for styling
- OpenAPI parsing and sampling

## Testing Philosophy

**Test behavior, not implementation.** The project emphasizes:

- Use React Testing Library with `findByRole` queries and jest-dom assertions
- Avoid Jest snapshots (except for AST parsers/linters)
- Avoid DOM hierarchy queries (tag name, CSS class, parentElement)
- Focus on business requirements coverage
- Jest/JSDOM for unit tests; Cypress for high-level integration only

Legacy Enzyme tests exist but should be migrated when modified.

## Package Dependencies

**Critical**: `elements` and `elements-dev-portal` use `~` (tilde) instead of `^` (caret) for `elements-core` dependency. This ensures patch-only updates to `elements-core` until explicitly bumped, preventing breaking changes.

## Versioning Guidelines

- **elements-core**: Can include breaking changes in minor versions (internal package)
- **elements** & **elements-dev-portal**: Only feature additions in minor versions, bug fixes in patches
- **Changes to elements-core**: Require releasing all three packages
- **Changes only to elements**: Can release just elements package
- **Changes only to elements-dev-portal**: Can release just elements-dev-portal package
- **Major versions**: Require consultation with Stoplight team

## CI/CD

**CircleCI Pipeline** (`.circleci/config.yml`):
- `lint-and-check`: Type check, lint, unit tests
- `build`: Multi-package build with caching
- `build-docs`: Documentation generation
- `run-e2e-tests`: Integration tests (react-cra, angular, static-html)
- `release`: Automated npm publishing (main branch only)
- `lockfile-maintenance`: Weekly automated dependency updates

**GitHub**:
- Dependabot for daily npm dependency updates
- PR template required
- CODEOWNERS for reviewer assignments

## Integration Examples

Example projects demonstrating framework integration:
- **`examples/react-cra/`** - Create React App integration
- **`examples/angular/`** - Angular app using Web Components
- **`examples/bootstrap/`** - Single HTML page with global script tag
- **`examples/static-html/`** - Static HTML example

## File Organization

```
packages/
├── elements-core/
│   ├── src/components/     # 11 component subdirectories
│   ├── src/hooks/         # Custom React hooks
│   ├── src/containers/    # Container components
│   ├── src/utils/         # Utility functions
│   ├── src/constants/     # Constants
│   ├── src/context/       # React contexts
│   ├── src/__fixtures__/  # Test fixtures
│   └── web-components/    # Web component generation
├── elements/
│   └── src/               # React + Web Component wrappers
└── elements-dev-portal/
    └── src/               # Multi-API portal components

cypress/                    # E2E tests and integration tests
docs/                      # Documentation guides
demo/                      # Demo application (localhost:4025)
.storybook/               # Storybook configuration
```

## Important Notes

1. **No pre-commit hooks** configured (can add `yarn lint --fix && yarn type-check` if needed)
2. Node.js 16+ required
3. Use Yarn (not npm) for package management
4. Demo runs on port 4025, not typical ports
5. **Never release `elements-demo`** package
6. Storybooks support hot-reload during development
7. E2E tests require build step before running
8. When releasing, manually revert `^` to `~` for `elements-core` in `elements` and `elements-dev-portal` package.json files

## Documentation

- **README.md** - Project overview and basic usage
- **CONTRIBUTING.md** - Development, testing, and release guide
- **docs/** - Comprehensive guides:
  - Introduction and getting started
  - Elements vs Dev Portal comparison
  - Framework-specific integration guides
  - Additional development guides