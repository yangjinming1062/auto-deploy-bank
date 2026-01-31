# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Rsbuild is a high-performance build tool powered by [Rspack](https://rspack.rs). It provides an out-of-the-box development experience with minimal configuration and supports multiple frontend frameworks (React, Vue, Svelte, Solid, Preact) through a modular plugin system.

- **Type**: TypeScript Monorepo (pnpm workspaces)
- **Tech Stack**: Node.js, TypeScript, Rspack, SWC, Lightning CSS
- **Package Manager**: pnpm >= 10.28.0
- **Node Version**: >= 22.18.0
- **Build System**: Nx >= 22.4.1

## Common Commands

```bash
# Build all packages
pnpm build

# Build a specific package
npx nx build @rsbuild/core

# Run all unit tests
pnpm test

# Run tests for a specific package
pnpm test core

# Run tests in watch mode
pnpm test:watch

# Run E2E tests (Playwright)
pnpm e2e
pnpm e2e css  # filter by keyword

# Lint code (Biome + Rslint)
pnpm lint

# Format code (Prettier)
pnpm format

# Check type consistency
pnpm lint:type

# Check dependency version consistency
pnpm check-dependency-version

# Run docs dev server
pnpm doc
```

## Monorepo Structure

- `/packages/core` - Core Rsbuild logic and orchestration
- `/packages/plugin-*` - Official framework plugins (react, vue, svelte, etc.)
- `/packages/create-rsbuild` - Scaffolding tool
- `/e2e` - End-to-end test suites
- `/website` - Documentation site
- `/scripts` - Internal build/maintenance scripts

## Architecture

### Plugin System

Rsbuild uses a hook-based plugin architecture. Plugins are objects with a `name` and `setup(api)` function:

```typescript
export const pluginExample = (): RsbuildPlugin => ({
  name: 'rsbuild:example',

  setup(api) {
    // Modify Rspack config at the bundler level
    api.modifyBundlerChain((chain, utils) => {
      // ...
    });

    // Modify fully resolved config
    api.modifyRspackConfig((config, utils) => {
      // ...
    });

    // Register lifecycle hooks
    api.onAfterBuild(({ isCompileComplete }) => {
      // ...
    });
  },
});
```

### Core Entry Points

- `packages/core/src/index.ts` - Public API exports (createRsbuild, defineConfig, loadConfig, etc.)
- `packages/core/src/createRsbuild.ts` - Main entry point for creating Rsbuild instances
- `packages/core/src/plugins/*.ts` - Core built-in plugins (entry, html, css, minify, etc.)

### Configuration Types

Types are defined in `packages/core/src/types/`:
- `config.ts` - RsbuildConfig and related types
- `plugin.ts` - RsbuildPlugin and RsbuildPluginAPI types
- `hooks.ts` - All lifecycle hook types

### Key Hooks

| Hook | Purpose |
|------|---------|
| `modifyRsbuildConfig` | Modify normalized Rsbuild config |
| `modifyBundlerChain` | Modify Rspack chain before config is finalized |
| `modifyRspackConfig` | Modify final Rspack config |
| `onBeforeBuild` | Before production build |
| `onAfterBuild` | After production build |
| `onBeforeStartDevServer` | Before dev server starts |
| `onAfterStartDevServer` | After dev server starts |
| `onDevCompileDone` | After each dev compile |

## Code Style

- **Linter**: Biome (`biome check`) for linting
- **Formatter**: Prettier for final formatting
- **Type Checker**: Rslint (`rslint`)
- **Testing**: Rstest for unit tests, Playwright for E2E

## Commit Conventions

PR titles follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>
feat(core): Add new option
fix(plugin-react): fix HMR issue
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

## Testing Guidelines

- Unit tests use Rstest and live in `<PACKAGE_DIR>/tests/`
- Add tests for every bug fix or feature
- E2E tests are in `/e2e` using Playwright