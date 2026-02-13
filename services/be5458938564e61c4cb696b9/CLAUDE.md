# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Monaco Editor is the browser-based code editor that powers VS Code. It is built from VS Code's source code with language enhancements bundled on top. The editor uses `monaco-editor-core` (a stripped-down VS Code) as a peer dependency and adds language features like CSS, HTML, JSON, and TypeScript/JavaScript support.

## Build Commands

```bash
# Install dependencies
npm install

# Watch mode for development (compiles TypeScript in src/)
npm run watch

# Build everything (LSP client + Monaco editor)
npm run build

# Build everything including smoke test packages
npm run build-all

# Build just the Monaco editor
npm run build-monaco-editor

# Run tests for language definitions (requires build first)
npm run test

# Run grammar tests only
npm run test:grammars

# Format code with Prettier
npm run prettier

# Check code formatting
npm run prettier-check

# Run playground locally (needs watch mode running)
npm run simpleserver
```

### Smoke Tests

```bash
# Package for smoketesting with all bundlers
npm run package-for-smoketest

# Package for individual bundlers
npm run package-for-smoketest-webpack
npm run package-for-smoketest-esbuild
npm run package-for-smoketest-vite

# Run smoke tests
npm run smoketest
npm run smoketest-debug    # Debug mode
npm run smoketest-headed   # Headed mode
npm run smoketest-ui       # UI mode
```

### LSP Client

```bash
# Build the LSP client (standalone)
cd monaco-lsp-client && npm install && npm run build
```

### Website

```bash
cd website
npm install
npm run dev
```

## Architecture

### Source Structure

- **`src/`** - Language features and editor API extensions built on top of `monaco-editor-core`
  - **`languages/definitions/`** - Individual language implementations (60+ languages)
    - Each language has `*.contribution.ts`, `*.ts`, and `*.test.ts` files
    - Register languages in `src/languages/register.all.ts`
  - **`languages/register.all.ts`** - Central registration point for all bundled languages
  - **`features/`** - Editor features that enhance the core editor
  - **`deprecated/`** - Deprecated language definitions and features
  - **`internal/`** - Internal utilities and helpers

- **`monaco-lsp-client/`** - Language Server Protocol client adapter for Monaco Editor (alpha)
  - Uses `@hediet/json-rpc` for WebSocket-based LSP communication
  - Provides adapters for connecting Monaco to external language servers
  - Built with Rolldown, outputs to `out/`

- **`build/`** - Build system scripts
  - **`build-monaco-editor.ts`** - Main build orchestrator (ESM + AMD builds)
  - **`esm/`** - ESM bundle configuration
  - **`amd/`** - Legacy AMD bundle configuration
  - **`releaseMetadata.ts`** - Generates package metadata

- **`test/`** - Test infrastructure
  - **`smoke/`** - Playwright-based smoke tests for webpack/vite/esbuild bundling
  - **`manual/`** - Manual test pages
  - **`test-setup.js`** - Test configuration (uses Mocha TDD UI)

- **`samples/`** - Integration examples for various bundlers
  - `browser-esm-webpack/`, `browser-esm-vite/`, `browser-esm-esbuild/`, etc.

### Key Concepts

1. **Models** - Represent file content, track edits, identified by URIs
2. **Editors** - Visual views attached to models
3. **Providers** - Implement smart features (completions, hover, etc.) mapped to LSP concepts
4. **Disposables** - Resources that implement `.dispose()` for cleanup

### Build Output

The build process produces:
- **`out/monaco-editor/`** - Published package with:
  - `esm/` - ESM bundle (modern, tree-shakeable)
  - `min/` - Minified AMD bundle (legacy, deprecated)
  - `monaco.d.ts` - TypeScript definitions

## Important Notes

- Core editor changes must be made in VS Code repository, not here
- The `monaco-editor-core` version in `package.json` tracks VS Code commits via `vscodeRef`
- Web workers are used for language services; they require HTTP/HTTPS (not `file://`)
- AMD build support is deprecated and will be removed in future versions