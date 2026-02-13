# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Playwright is a TypeScript/JavaScript framework for Web Testing and Automation that tests Chromium, Firefox, and WebKit with a single API. This is a multi-package npm workspace (monorepo) requiring Node.js 18+.

## Common Commands

### Setup and Development
```bash
npm ci                    # Install dependencies
npm run watch             # Build in watch mode (recompiles + regenerates types/docs)
npx playwright install    # Install browser binaries
npm run build             # Full production build
npm run clean             # Remove lib/, node_modules/, and generated files
```

### Running Tests
```bash
npm run test              # All library tests (3 browsers)
npm run ctest             # Library tests - Chromium only (fast path)
npm run ftest             # Library tests - Firefox only
npm run wtest             # Library tests - WebKit only
npm run ttest             # Test runner tests
npm run biditest          # BiDi protocol tests
npm run test-mcp          # MCP tests
npm run ct                # Component tests
npm run atest             # Android tests
npm run etest             # Electron tests

# Single test file
npx playwright test tests/library/specific-file.spec.ts

# Custom browser path
CRPATH=/path/to/executable npm run ctest
DEBUG=pw:browser npm run ctest
```

### Linting and Type Checking
```bash
npm run lint              # Full lint (eslint + tsc + doc + deps + types + tests)
npm run eslint            # ESLint only
npm run tsc               # TypeScript compilation
npm run flint             # Fast parallel lint (same as lint, runs concurrently)
```

## Architecture

### Package Structure

- **`packages/playwright`** - Test runner and main API (`@playwright/test`)
- **`packages/playwright-core`** - Low-level browser automation library
- **`packages/playwright-test`** - Test runner core (re-exported by `playwright`)
- **`packages/playwright-browser-*`** - Browser-specific bundles (Chromium, Firefox, WebKit)
- **`packages/trace-viewer`** - Web-based trace viewer (React, Vite)
- **`packages/html-reporter`** - HTML test report UI (React, Vite)
- **`packages/recorder`** - Code generator and recorder
- **`packages/protocol`** - Generated Protocol types
- **`packages/web`** - Shared web UI components
- **`packages/injected`** - Injected scripts for browser automation

### Source Organization (playwright-core)

```
packages/playwright-core/src/
├── client/           # Client-side API (Browser, Page, Context, etc.)
├── server/           # Server-side implementation
│   ├── chromium/     # Chromium-specific implementation
│   ├── firefox/      # Firefox-specific implementation
│   ├── webkit/       # WebKit-specific implementation
│   ├── dispatchers/  # IPC dispatchers for cross-process communication
│   └── ...
├── common/           # Shared types and utilities
├── protocol/         # JSON-RPC protocol definitions
└── utils/            # Utility functions
```

**Client-Server Model**: The `client/` directory implements the public API (Browser, Page, Context, etc.). API calls are translated to protocol commands handled by `server/` dispatchers, which communicate with browsers via CDP (Chromium) or custom protocols (Firefox, WebKit).

### Source Organization (playwright test runner)

```
packages/playwright/src/
├── runner/           # Test runner execution engine
├── loader/           # Test file loading and configuration
├── matchers/         # Assertion matchers (expect)
├── reporters/        # Test result reporters
├── worker/           # Worker process implementation
└── transform/        # TypeScript transformation and bundling
```

### Tests Structure

```
tests/
├── library/          # Core library API tests
├── page/             # Page-level API tests
├── components/       # Component tests (React/Vue/Svelte)
├── playwright-test/  # Test runner tests
├── bidi/             # BiDi protocol tests
├── mcp/              # MCP protocol tests
├── installation/     # Installation tests
├── electron/         # Electron tests
├── android/          # Android tests
└── stress/           # Stress tests
```

## Key Conventions

- **TypeScript**: All source is TypeScript with `strict: true`
- **Copyright**: All files must include the Apache 2.0 Microsoft license header
- **Commits**: Use [Semantic Commit Messages](https://www.conventionalcommits.org/en/v1.0.0/) (`fix/feat/docs/test: description`)
- **Documentation**: Public API docs are in `docs/src/` as markdown files with custom structure. API types are generated from these markdown files - do not edit `packages/playwright-core/types/` directly.
- **Generated Files**: Many files are generated during build - don't edit them directly:
  - `packages/*/lib/` - Compiled JavaScript output
  - `packages/*/src/generated/` - Generated protocol types
  - `packages/playwright-core/types/` - API type definitions

## Development Guidelines

- **Dependencies**: Very high bar for adding new dependencies. Discuss with maintainers before adding any.
- **Tests**: Required for new features, bug fixes, and most changes. Tests should be hermetic (no external service dependencies) and work on macOS, Linux, and Windows.
- **Documentation**: Update `docs/src/` markdown files alongside any API changes. Documentation is generated from these files.

## Editor Configuration

The project uses path aliases configured in `tsconfig.json`:
- `playwright-core/lib/*` → `packages/playwright-core/src/*`
- `playwright/lib/*` → `packages/playwright/src/*`
- `@isomorphic/*` → `packages/playwright-core/src/utils/isomorphic/*`
- `@trace/*` → `packages/trace/src/*`
- `@web/*` → `packages/web/src/*`