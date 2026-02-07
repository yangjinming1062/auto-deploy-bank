# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Rsdoctor is a build analyzer for the Rspack and Webpack ecosystems. It's a TypeScript monorepo using pnpm workspaces and nx for task management. The project visualizes build processes to help identify bottlenecks and optimization opportunities.

## Development Commands

```bash
# Install dependencies (requires pnpm 10.17.1+)
pnpm install

# Build all packages
pnpm build

# Build a single package
npx nx build @rsdoctor/core

# Run unit tests
pnpm test        # or pnpm ut
pnpm ut:watch    # watch mode

# Run tests for a single package
pnpm run --filter @rsdoctor/core test

# Lint code
pnpm lint        # uses Biome
pnpm format      # uses Prettier

# Run E2E tests
pnpm e2e

# Check spelling
pnpm check-spell
```

## Architecture

### Package Structure

- **@rsdoctor/core** - Core analysis engine with inner plugins that hook into bundlers (Webpack/Rspack)
- **@rsdoctor/sdk** - SDK for data collection and report generation
- **@rsdoctor/client** - React-based visualization dashboard for reports
- **@rsdoctor/components** - Shared React UI components
- **@rsdoctor/webpack-plugin** - Webpack integration plugin
- **@rsdoctor/rspack-plugin** - Rspack integration plugin
- **@rsdoctor/cli** - Command-line interface
- **@rsdoctor/types** - Shared TypeScript type definitions
- **@rsdoctor/utils** - Common utility functions
- **@rsdoctor/ai** - MCP server and AI-related features
- **@rsdoctor/graph** - Graph utilities for module/package graphs

### Build System

- **rslib** - Builds library packages with dual ESM/CJS output
- **rsbuild** - Builds the client React application
- **prebundle** - Pre-bundles certain dependencies (configured in `prebundle.config.mjs`)

### Data Flow

1. Plugins (webpack/rspack) hook into bundlers to collect build data
2. SDK collects data into a standard manifest format
3. React client consumes the manifest for visualization

## Testing

Tests use **rstest** framework (similar to Rust's rstest). Unit tests live in `packages/*/tests/` directories. E2E tests are in the `e2e/` directory using Playwright.

Tests use snapshot serialization configured in `scripts/rstest.setup.ts` for consistent path handling.

## Code Style

- **Biome** for linting (configured in `biome.json`)
- **Prettier** for formatting
- Strict rules enabled: `useExportType: error`, `noNonNullAssertion: off`
- Non-null assertions (`!`) are allowed ( Biome's `noNonNullAssertion` is off)

## Key Configuration Files

- `package.json` - Scripts and pnpm workspace configuration
- `nx.json` - Nx task distribution and caching
- `biome.json` - Linting rules
- `rstest.config.ts` - Test configuration
- `packages/*/rslib.config.ts` - Per-package build configuration

## Viewing Changes

To view analysis reports after making changes, run in example projects:

```bash
pnpm run build:analysis
# Available in: modern-minimal, webpack-minimal, rspack-minimal, rsbuild-minimal
```