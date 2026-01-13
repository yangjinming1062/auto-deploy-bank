# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Gatsby** monorepo - a React-based static site generator. It's organized as a Lerna monorepo with 100+ packages in the `packages/` directory. The main `gatsby` package is in `packages/gatsby/` and contains the core framework logic.

## Common Development Commands

### Setup & Installation
```bash
# Install all dependencies
yarn

# Bootstrap the monorepo (runs prepare scripts for all packages)
npm run bootstrap

# Install git hooks
npm run hooks:install
```

### Building
```bash
# Build all packages
npm run build

# Watch mode for development (builds as you edit)
npm run watch

# Build specific package
cd packages/gatsby && npm run build

# Typecheck all packages
npm run typecheck
```

### Testing
```bash
# Run all tests (lint + jest + integration tests)
npm test

# Run unit tests only
npm run jest

# Run integration tests
npm run test:integration

# Run E2E tests (requires setup - see e2e-tests/README.md)
cd e2e-tests/<test-name> && yarn test

# Run specific test file
npx jest packages/gatsby/src/utils/__tests__/my-test-file.test.ts

# Update snapshots
npm run test:update

# Run tests in watch mode
npm run test:watch

# Debug tests
npm run jest:inspect
```

### Linting & Formatting
```bash
# Lint all code
npm run lint

# Fix linting issues
npm run format

# Format code only (Prettier)
npm run format:other
```

### Publishing
```bash
# Publish canary version
npm run publish-canary

# Publish next version
npm run publish-next

# Publish release version
npm run publish-release
```

## Code Architecture

### High-Level Structure

**packages/gatsby/src/** contains the core framework:

- **commands/** - CLI command implementations (develop, build, serve, etc.)
  - `develop.ts` - Development server
  - `build.ts` - Production build
  - `serve.ts` - Serve production build
  - `build-html.ts` - HTML generation

- **bootstrap/** - Application initialization and plugin loading
  - `load-plugins/` - Discovers and loads Gatsby plugins
  - `load-themes/` - Handles theme composition
  - Creates the initial Redux store and initializes the GraphQL schema

- **redux/** - Centralized state management using Redux
  - `actions/` - Redux action definitions
  - `reducers/` - State reducers for different parts of the app (pages, schema, plugins, etc.)
  - `index.ts` - Store configuration
  - `persist.ts` - State persistence logic

- **schema/** - GraphQL schema generation and management
  - `schema.js` - Main schema generation orchestrator
  - `node-model.js` - Node model for GraphQL resolvers
  - `resolvers.ts` - Custom GraphQL resolver implementations
  - `infer/` - Automatic type inference from data
  - `print.ts` - Schema printing and introspection

- **utils/** - Utility modules and helpers
  - `api-runner-node.js` - Plugin API execution
  - `webpack/` - Webpack configuration and utilities
  - `source-nodes.ts` - Data sourcing orchestration
  - `webpack.config.js` - Main webpack configuration

- **state-machines/** - State machine implementations using XState for complex workflows

- **datastore/** - Low-level data storage (LMDB-based)

### Key Entry Points

- **packages/gatsby/index.js** - Main entry point after build
- **packages/gatsby/src/cli.js** - CLI entry point
- **packages/gatsby/package.json#bin** - `gatsby` CLI binary

### GraphQL Data Layer

Gatsby builds a centralized GraphQL data layer from all data sources:
1. Source plugins pull data (from CMS, filesystem, APIs, etc.)
2. Data is normalized into nodes in Redux store
3. Schema is inferred from node types
4. Pages can query the schema using GraphQL

## Testing Strategy

### Three Levels of Testing

1. **Unit Tests** (Jest) - packages/gatsby/src/**/__tests__/
   - Fast, isolated tests
   - Run with `npm run jest`
   - Mock dependencies heavily

2. **Integration Tests** - integration-tests/
   - Test full workflows in JSDOM environment
   - Create test fixture Gatsby sites
   - Run with `npm run test:integration`

3. **End-to-End Tests** - e2e-tests/
   - Run in real browser with Cypress
   - Test complete user workflows
   - Each test is its own Gatsby site
   - Run individually per test directory

### Test Patterns

- Unit tests use `jest.mock()` and manual module mocking
- Integration tests use fixture sites in `__tests__/fixtures/`
- E2E tests use `gatsby-dev-cli` to test local changes

## Monorepo Structure

### Package Organization

- **packages/gatsby** - Core framework
- **packages/gatsby-cli** - CLI commands
- **packages/create-gatsby** - Project initialization
- **packages/gatsby-plugin-*** - Official Gatsby plugins
- **packages/gatsby-*** - Supporting packages and utilities

### Cross-Package Dependencies

- Dependencies between packages are managed by Lerna
- Use `npm run watch` during development to rebuild packages as you edit
- Use `gatsby-dev-cli` to link local packages to test sites

## Development Workflow

### Typical Development Cycle

1. Make changes to code
2. Run `npm run watch` to build affected packages
3. Run `npm test` to verify changes
4. Create test cases for new functionality
5. Submit PR for review

### Plugin API

Gatsby's API is extensible through plugins and themes:
- **Plugins** - Extend Gatsby's functionality
- **Themes** - Shareable Gatsby configurations
- **Source plugins** - Pull data from external sources (WordPress, Contentful, etc.)
- **Transform plugins** - Transform data (Markdown to HTML, etc.)

API hooks are defined in `packages/gatsby/src/utils/api-*.ts` and executed via `api-runner-node.js`.

## Important Notes

- **Node Version**: Requires Node 18.0.0 or higher
- **Package Manager**: Uses Yarn (v1.22.19) not npm
- **TypeScript**: Mixed JS/TS codebase, TypeScript used in newer code
- **State Machines**: Complex workflows use XState (see `state-machines/`)
- **Webpack**: Custom webpack configuration for development and production
- **Bundle Size**: Uses code splitting and performance optimizations by default

## Common Issues

- Tests may need updating when changing APIs (`npm run test:update`)
- Webpack changes require rebuild of the gatsby package
- Schema changes affect GraphQL queries in user sites
- Plugin API changes require major version bump (follow semver)