# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Modern.js is a progressive React framework for modern web development. It's a monorepo containing:
- `@modern-js/app-tools` - Main application solution
- `@modern-js/builder` - Build system wrapping Rsbuild/Rspack
- Runtime plugins for React (state, routing, SSR, etc.)
- Server-side rendering and BFF (backend-for-frontend) packages
- CLI plugins for build optimizations and features

## Common Commands

```bash
# Install dependencies
pnpm install

# Build all packages (runs via prepare script automatically after install)
pnpm run prepare

# Build a specific package
cd packages/some-path && pnpm run build
pnpm run --filter @modern-js/some-package build

# Run unit tests (using rstest)
pnpm run test:ut
pnpm run test:ut:update  # Update snapshots
pnpm run --filter @modern-js/some-package test

# Run framework integration tests (using Jest + Puppeteer)
pnpm run test:framework

# Run E2E tests
pnpm run test:e2e

# Run all tests
pnpm run test

# Lint and format (Biome)
pnpm run lint

# Add a changeset
pnpm run change

# Bump versions
pnpm run bump
```

## Architecture

### Plugin System

Modern.js uses a unified plugin system with three types:

1. **CLI Plugins** (`@modern-js/plugin`): Configure build, dev, and deployment
   - Location: `packages/toolkit/plugin/src/cli/`
   - Define using `createCliPlugin()`

2. **Runtime Plugins** (`@modern-js/plugin`): Extend React component behavior
   - Location: `packages/runtime/plugin-runtime/src/`
   - Define using `createRuntimePlugin()`

3. **Server Plugins** (`@modern-js/plugin`): Handle server-side requests
   - Location: `packages/toolkit/plugin/src/server/`
   - Define using `createServerPlugin()`

### Key Packages

- `@modern-js/builder` - Wraps Rsbuild/Rspack with Modern.js presets
- `@modern-js/server-core` - Server runtime with Hono adapter
- `@modern-js/utils` - Shared utilities (lodash wrappers, fs helpers, etc.)
- `@modern-js/runtime-utils` - Runtime utilities for plugin hooks

### Build System

- Uses **Rslib** (Rspack-based library tool) for building packages
- Output formats: ESM, CJS, and type definitions
- Configuration: `rslib.config.mts` in each package

### Directory Structure

```
packages/
├── cli/          # CLI plugins and builder
├── runtime/      # React runtime plugins (state, router, etc.)
├── server/       # SSR, BFF, and server utilities
├── toolkit/      # Core plugin system and utilities
├── solutions/    # High-level solutions (app-tools)
└── document/     # Documentation (Rspress)
tests/
├── e2e/          # E2E tests (Jest + Puppeteer)
└── integration/  # Integration tests
```

## Code Style

- **Linting/Formatting**: Biome (configured in `biome.json`)
  - Single quotes for JS/TS
  - Double quotes for JSX
  - Line width: 80 characters

- **Testing**: rstest for unit tests, Jest for integration/E2E

## Dependencies

- Node.js >= 20
- pnpm >= 10.0.0

## Related Documentation

- [Contributing Guide](packages/document/docs/en/community/contributing-guide.mdx)
- [API Reference](packages/document/docs/en/apis/)