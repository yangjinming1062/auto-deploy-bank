# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Rsdoctor is a build analyzer for the Rspack ecosystem with full webpack compatibility. It visualizes compilation behavior, identifies build bottlenecks, and provides build-time analysis for loaders, plugins, and resolvers. Part of the [Rstack](https://rstack.rs/) toolchain.

## Commands

### Development Setup
```bash
# Install dependencies (uses pnpm workspaces)
pnpm install

# Build all packages
pnpm run build

# Build a specific package using nx
npx nx build @rsdoctor/core

# Start dev server for a package (watch mode)
npx nx start @rsdoctor/core

# Run unit tests
pnpm run test

# Run unit tests with watch mode
pnpm run ut:watch

# Run unit tests for a single package
npx nx test @rsdoctor/core

# Run E2E tests (playwright-based)
pnpm run e2e

# Run E2E tests with native Rspack
pnpm run e2e:native

# Run all tests
pnpm run test:all

# Lint with Biome
pnpm run lint

# Format code
pnpm run format
```

### Local Development
```bash
# Start the client UI dev server
cd packages/client && pnpm run dev

# Run build analysis on examples
cd examples/rspack-minimal && pnpm run build:analysis
```

## Architecture

### Monorepo Structure

```
packages/
├── ai/              @rsdoctor/mcp-server - MCP server for AI integration
├── cli/             @rsdoctor/cli - CLI tool
├── client/          @rsdoctor/client - React UI for analysis report (Rsbuild)
├── components/      @rsdoctor/components - Shared UI components
├── core/            @rsdoctor/core - Core analysis engine (Rslib)
├── graph/           @rsdoctor/graph - Module/package graph utilities
├── rspack-plugin/   @rsdoctor/rspack-plugin - Rspack plugin
├── sdk/             @rsdoctor/sdk - Server/client SDK with socket.io
├── types/           @rsdoctor/types - Shared TypeScript types
├── utils/           @rsdoctor/utils - Utility functions
└── webpack-plugin/  @rsdoctor/webpack-plugin - Webpack plugin

examples/            Demo projects (rspack-minimal, webpack-minimal, rsbuild-minimal, etc.)
e2e/                 End-to-end tests using Playwright
```

### Package Dependencies

```
client (React UI with Rsbuild)
    └── components, types

core (Analysis engine)
    ├── graph, sdk, types, utils
    └── inner-plugins/, rules/, build-utils/

rspack-plugin
    └── core, graph, sdk, types, utils

webpack-plugin
    └── core, graph, sdk, types, utils

sdk
    ├── client, graph, types, utils
    └── socket.io server for client communication

cli
    ├── core, sdk, types, utils, graph
    └── client (peerDependency)
```

### Build System

- **Rslib** is used for building TypeScript packages (core, graph, sdk, utils, plugins, cli, ai)
- **Rsbuild** is used for the client React UI package
- **Prebundle** is used to bundle external dependencies into compiled/ directories
- **nx** manages task scheduling and caching across the monorepo

### Core Concepts

- **Plugins**: The `inner-plugins/` directory in core contains Rsdoctor's internal loaders and plugins that intercept webpack/rspack compilation
- **Rules**: Built-in analysis rules for detecting issues like duplicate packages, ES version problems
- **Build Utils**: Utilities for parsing bundles, analyzing loaders, and processing sourcemaps
- **SDK Server**: Runs a socket.io server during builds to stream data to the client UI

### Test Framework

- **Unit tests**: Use `@rstest/core` (Rust-inspired testing framework) in each package's `tests/` directory
- **E2E tests**: Use Playwright in `e2e/cases/`, configured to run against both webpack and rspack