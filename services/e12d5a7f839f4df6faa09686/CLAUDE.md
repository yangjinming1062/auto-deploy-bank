# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Rslib is a library development tool built on top of Rsbuild (which uses Rspack/webpack). It provides a high-level abstraction for building JavaScript/TypeScript libraries with features like multiple output formats (ESM, CJS, UMD), declaration file generation, and CSS handling.

## Common Commands

```bash
# Install dependencies (builds all packages via prepare script)
pnpm install

# Build all packages
pnpm build

# Watch mode for a specific package
pnpm -C packages/core dev

# Run all tests
pnpm test

# Run specific test suites
pnpm test:unit           # Unit tests in packages/*/tests
pnpm test:integration    # Integration tests in tests/integration
pnpm test:e2e            # End-to-end tests in tests/e2e
pnpm test:benchmark      # Benchmark tests

# Filter integration tests
pnpm test:integration <pattern>    # Filter by file path
pnpm test:integration -t <pattern> # Filter by test name
pnpm test:unit -u           # Update snapshots

# Lint and format
pnpm lint               # Run all linters (Biome, Prettier, cspell, type-check)
pnpm format             # Auto-fix format issues (Biome + Prettier)

# Type checking
pnpm type-check         # Type-check all packages

# Version management
pnpm changeset          # Create a changeset for user-facing changes
```

**Node.js**: v24.5.0 (use `fnm use` or `nvm use` to match `.nvmrc`)

## Monorepo Structure

```
packages/
  core/          (@rslib/core) - Main CLI and configuration
  plugin-dts/    (rsbuild-plugin-dts) - Declaration file generation
  create-rslib/  (create-rslib) - Project scaffolding
tests/
  integration/   - Build artifact verification tests
  e2e/           - Playwright end-to-end tests
  benchmark/     - Performance benchmarks
examples/        - Example projects (React, Vue, etc.)
website/         - Documentation site
```

## Architecture

### Core Package (`packages/core`)

The main package containing:
- **CLI** (`cli/`): Entry point using `cac` for argument parsing, defines `build` and `inspect` commands
- **Config** (`config.ts`): `defineConfig` and configuration composition - RslibConfig → RsbuildConfig transformation
- **CreateRslib** (`createRslib.ts`): Programmatic API for building libraries
- **Plugins** (`plugins/`): Custom Rsbuild plugins (EntryChunkPlugin, shims for CJS/ESM compatibility)
- **CSS** (`css/`): CSS modules, Sass/Less support, PostCSS configuration
- **Asset** (`asset/`): Asset handling configuration

Key files:
- `packages/core/src/config.ts` - Main configuration logic (1300+ lines)
- `packages/core/src/createRslib.ts` - Build execution logic
- `packages/core/src/loadConfig.ts` - Config file loading (rslib.config.ts)

### Plugin DTS (`packages/plugin-dts`)

Handles TypeScript declaration file generation:
- `dts.ts` - Main plugin logic
- `tsc.ts` - TSC-based declaration bundling
- `tsgo.ts` - TypeScript compiler API based bundling
- `apiExtractor.ts` - API extraction using @microsoft/api-extractor

### Configuration Flow

1. User defines `rslib.config.ts` with `defineConfig({...})`
2. `config.ts` transforms `RslibConfig` → `RsbuildConfig`:
   - Applies `output` settings (formats, bundleless vs bundle)
   - Composes CSS/asset/entry configurations
   - Applies shim plugins for CJS/ESM compatibility
3. Rsbuild executes with the composed config
4. For dts: `plugin-dts` runs declaration generation as a separate step

## Coding Conventions

- **Language**: TypeScript + ESM
- **Quotes**: Single quotes
- **Formatting**: Biome for JS/TS; Prettier for MD/CSS/JSON/package.json
- **Filenames**: camelCase or PascalCase (enforced by Biome)
- **Pre-commit hooks**: nano-staged runs Biome/Prettier on staged files
- Run `pnpm biome check --write` on modified source files before committing

## Key Dependencies

- `@rsbuild/core` - Build tool abstraction layer
- `@rspack/core` - Underlying bundler
- `rsbuild-plugin-dts` - Declaration generation
- `tinyglobby` - File globbing
- `tsconfck` - TypeScript config resolution
- `nx` - Build orchestration and caching
- `@rstest/core` - Unit/integration test framework
- `@changesets/cli` - Version and changelog management

## Build Pipeline

1. **prebundle**: Bundles external dependencies into `packages/*/compiled/`
2. **build**: Compiles TypeScript to `dist/` and generates `dist-types/` declarations
3. Nx caching enabled via `nx.json` for faster rebuilds

## Test Framework

- **Unit/Integration**: `@rstest/core` - Rust-inspired testing framework
- **E2E**: `@playwright/test`
- Test patterns are in `packages/*/tests` (unit) and `tests/` (integration/e2e)

## Important Configuration Files

- `nx.json` - Nx build system configuration
- `biome.json` - Linter/formatter rules
- `rslint.jsonc` - TypeScript ESLint rules
- `pnpm-workspace.yaml` - Monorepo workspace structure