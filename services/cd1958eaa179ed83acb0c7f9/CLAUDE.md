# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Rspress is a fast Rsbuild-based static site generator with MDX support, full-text search, plugin system, and component documentation features. It's part of the Rstack ecosystem (centered on Rspack).

## Commands

```bash
# Install dependencies (requires Node.js 20+ and pnpm 10.28+)
pnpm install

# Build all packages
pnpm build

# Watch mode for development (all packages)
pnpm dev

# Build only the documentation website
pnpm build:website

# Run website in dev mode
pnpm dev:website

# Preview production website
pnpm preview:website

# Run all tests
pnpm test

# Run only unit tests (rstest)
pnpm test:unit

# Run only e2e tests (playwright)
pnpm test:e2e

# Lint and format
pnpm lint          # Check for issues
pnpm format        # Auto-fix lint issues

# Create a changeset for user-facing changes
pnpm changeset
```

**Running single tests:**
- Unit: `pnpm test:unit -- <test-name>` (uses pattern matching)
- E2E: `pnpm exec playwright test e2e/<test-file>.spec.ts`

## Architecture

### Monorepo Structure

- `packages/core` - Main package (`@rspress/core`): CLI, config, MDX processing, route service, SSG, Rsbuild integration
- `packages/shared` - Shared utilities: constants, node utils, logger, markdown parsing
- `packages/theme-default` - Default theme components and layouts
- `packages/plugin-*` - Official plugins (algolia, api-docgen, client-redirects, llms, playground, preview, rss, sitemap, twoslash, typedoc)
- `packages/create-rspress` - Project scaffolding tool
- `e2e/` - End-to-end test fixtures
- `website/` - Rspress documentation site

### Core Package (`packages/core`)

Key modules under `src/`:
- `cli/` - CLI entry points (`rspress build/dev`)
- `config/` - Configuration (`defineConfig`, `loadConfigFile`)
- `node/` - Build/runtime logic:
  - `PluginDriver.ts` - Plugin system orchestrating hook lifecycle
  - `route/` - Route generation and page data extraction
  - `mdx/` - MDX compilation with remark/rehype plugins
  - `ssg/` - Static site generation
  - `build.ts`, `dev.ts` - Build/dev entry points
- `theme/` - Default theme components (`components/`, `layout/`, `hooks/`)

### Plugin System

Plugins implement `RspressPlugin` interface with hooks:
- `config` - Modify user config
- `beforeBuild` / `afterBuild` - Build lifecycle
- `extendPageData` - Extend page metadata
- `modifySearchIndexData` - Search index customization
- `addRuntimeModules` - Add client-side runtime modules
- `globalUIComponents` / `globalStyles` - Inject global UI

The `PluginDriver` class manages plugin lifecycle and hooks execution.

### Build Flow

1. `rspress dev` or `rspress build` loads config via `defineConfig`
2. `PluginDriver` initializes plugins and normalizes config
3. `initRsbuild.ts` creates Rsbuild config with MDX support
4. `RouteService` generates routes from docs directory
5. MDX files compiled via `@mdx-js/mdx` with custom remark/rehype plugins
6. Production: SSG renders pages to static HTML

## Coding Conventions

- **Language**: TypeScript + ESM
- **Styling**: Biome for JS/TS (single quotes, spaces), Prettier for MD/CSS/JSON
- **Naming**: `camelCase` for files, `PascalCase` for components
- **Commits**: Conventional Commits with scope (e.g., `feat(core): description`, `fix(theme/Nav): description`)

## Testing

- Unit tests: `rstest` framework, located in `packages/*/tests/*.test.ts`
- E2E tests: Playwright, located in `e2e/*.spec.ts`
- Snapshots: `__snapshots__/` directories

## Key Dependencies

- **@rsbuild/core** - Build tool (wrapper around Rspack)
- **@mdx-js/mdx** - MDX compiler
- **React 19** - UI framework
- **Shiki** - Syntax highlighting
- **@unhead/react** - Head management
