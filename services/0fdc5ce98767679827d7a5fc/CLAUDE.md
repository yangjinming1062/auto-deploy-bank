# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Garfish is a micro-frontend framework by ByteDance for composing multiple independently delivered frontend applications into a cohesive product. It addresses challenges in cross-team collaboration, diverse technology stacks, and application complexity in large-scale web applications.

## Commands

```bash
# Install dependencies
pnpm install

# Build all packages (outputs to dist/)
pnpm build

# Build with watch mode (useful during development)
pnpm build:watch

# Run all dev apps in parallel (main app on 8090, sub-apps on 8091-8099)
pnpm dev

# Run unit tests
pnpm test

# Run tests in watch mode
pnpm test:watch

# Run tests with coverage
pnpm test:coverage

# Lint code
pnpm lint

# Format code (TypeScript)
pnpm format

# Format JavaScript and config files
pnpm format:js

# Format markdown files
pnpm format:md

# TypeScript type checking
pnpm type:check

# Run E2E tests
pnpm test:e2e

# Open Cypress UI
pnpm cy:open

# Run Cypress tests headless
pnpm cy:run

# Release a new version (prompts for version bump)
pnpm release
```

## Architecture

### Monorepo Structure

```
packages/          # Core framework packages
  core/            # Main Garfish class, plugins, app management
  loader/          # Loads and parses sub-app entry resources (HTML/JS)
  sandbox/         # Runtime isolation (browser-snapshot, browser-vm)
  router/          # Route-driven sub-app activation and isolation
  hooks/           # Plugin hook system (SyncHook, AsyncHook, etc.)
  utils/           # Common utilities
  css-scope/       # CSS scope compiler
  es-module/       # ESM loader and compiler
  remote-module/   # CJS loader
  bridge-*/        # Framework-specific bridges (React 16/17/18, Vue 2/3, Angular)
dev/               # Development demo apps for testing different frameworks
website-new/       # Documentation site
```

### Core Concepts

**Sub-app Lifecycle**: Load → Bootstrap → Mount → Unmount → Destroy

**Sandbox Modes**:
- **Snapshot Sandbox**: Captures/restores global state via `save()`/`load()`. Suitable for linear execution.
- **VM Sandbox**: Uses `iframe` or context isolation for non-linear multi-instance scenarios.

**Router Design**: Uses scope-based namespace isolation to prevent route conflicts between sub-apps. Sub-apps should use history mode with proper `basename` configuration.

**Plugin System**: Hook-based architecture using `SyncHook`, `AsyncHook`, `SyncWaterfallHook`, and `AsyncWaterfallHook`. Plugins extend `this.hooks.lifecycle` with events like `beforeLoad`, `afterLoad`, `beforeMount`, etc.

### Code Patterns

- **No default exports** (enforced by ESLint)
- **Semicolons required**, single quotes, camelCase
- **Unused args** must be prefixed with `_` or listed in `argsIgnorePattern`
- Path aliases: `@garfish/*` maps to `packages/*/src`

## Development Workflow

1. Make code changes in `packages/*/src`
2. Run `pnpm build:watch` to rebuild on changes
3. Run `pnpm dev` to start all demo apps
4. Navigate to `http://localhost:8090` for the main demo
5. Tests located in `packages/*/__tests__/**/*spec.[jt]s?(x)`