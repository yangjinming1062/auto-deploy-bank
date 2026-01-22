# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Monorepo** managed by [Lerna](https://github.com/lerna/lerna) containing the **We-Vue** project. We-Vue is a mobile UI component library for Vue.js, styled with WeUI, suitable for WeChat Official Accounts development.

### Key Packages

- `packages/we-vue`: The core component library (Vue 2.x + TypeScript).
- `packages/demo`: A Vue CLI based demo application showing component usage.
- `packages/docs`: Documentation site built with [Nuxt.js](https://nuxtjs.org).

## Commands

### Development

```bash
# Start development servers for components and demo (in parallel)
yarn dev

# Start only the documentation site
yarn dev:docs
```

### Building

```bash
# Build the we-vue library (dist and lib)
cd packages/we-vue && yarn build
```

### Testing

```bash
# Run all unit tests for the library
yarn test

# Run unit tests with coverage
yarn test:coverage

# Run e2e tests for the demo app
yarn test:demo
```

### Linting

```bash
# Run linting for all packages
yarn lint

# Run linting with auto-fix
yarn lint:fix
```

## Code Architecture

### Components (`packages/we-vue/src/components`)

Components are located in subdirectories matching their names (e.g., `WButton`). Each component typically consists of:

- `index.ts`: Exports the component and its types.
- `ComponentName.tsx`: The main Vue component file (using JSX/TSX).
- `__test__/ComponentName.spec.ts`: Unit tests.

Components are written in **TypeScript** using **Vue Class Components** or functional JSX components.

### Styles (`packages/we-vue/src/scss`)

Global and component-specific styles are written in **SCSS**.

### Routing & Navigation (`packages/demo`)

The demo app uses `vue-router`. Route definitions are in `packages/demo/src/router/index.js`. Navigation config is in `nav.json`.

## Coding Standards

- **Linting**: Enforced via ESLint and Prettier. Configuration is handled by `lint-staged` on commit.
- **Testing**: Jest is used for unit tests in `we-vue`. Cypress is used for E2E tests in `demo`.
- **TypeScript**: Strict mode is generally enabled.

## Dependency Management

Dependencies for all workspaces are installed together:
```bash
yarn install
lerna bootstrap
```