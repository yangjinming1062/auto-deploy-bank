# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Code Spell Checker** - a VS Code extension that provides spell checking for source code. It uses cspell internally for spell checking and implements a Language Server Protocol (LSP) architecture where the heavy lifting is done in a separate server process.

## Monorepo Structure

This is an npm workspaces monorepo with the following key packages:

- **`client`** - VS Code extension (activation, settings UI, server communication)
- **`_server`** - Language server that performs spell checking using cspell
- **`_settingsViewer`** - Webapp providing visual configuration interface
- **`_integrationTests`** - VS Code integration test suite using @vscode/test-electron
- **`webview-ui`** - Svelte-based webview for settings configuration UI
- **`__utils`** - Shared utilities used by both client and server
- **`utils-disposables`** - Disposable pattern utilities
- **`utils-logger`** - Logging utilities
- **`json-rpc-api`** - JSON-RPC API framework
- **`webview-api`** - Webview communication API
- **`webview-rpc`** - RPC for webview communication
- **`__locale-resolver`** - Locale resolution utilities
- **`_serverPatternMatcher`** - File pattern matching for the server

## Build Commands

```bash
# Install dependencies
npm install

# Build all workspaces
npm run build

# Watch and rebuild on changes (for development)
npm run watch  # Client: cd packages/client && npm run watch

# Clean build artifacts
npm run clean

# Build just the schema (configuration definitions)
npm run build-schema

# Build the VSIX extension package
npm run package-extension

# Build documentation
npm run build:docs

# Build everything including docs and extension
npm run build:all
```

## Test Commands

```bash
# Run all tests across all workspaces
npm run test

# Run a single test file
cd packages/client && npx vitest run src/commands.test.mts

# Run integration tests in VS Code
npm run test-client-integration

# Run client package tests
cd packages/client && npm run test

# Run server package tests
cd packages/_server && npm run test

# Run tests with file watcher (in package directory)
npm run test-watch
```

## Lint Commands

```bash
# Check linting and formatting
npm run prettier:check
npm run lint:eslint

# Fix linting and formatting issues
npm run lint
npm run prettier:fix

# Lint check only (CI)
npm run lint:eslint
```

## Debugging the Extension

Open the workspace `Spell Checker.code-workspace` in VS Code, then:

1. **Launch extension** - Press `F5` with `Client: Launch Extension (Spell Checker Root)` selected
2. **Attach to server** - After launching the client, use `Server: Attach Server (Server - Spell Checker)` to debug the server process
3. **Test current file** - Use the Vitest launch configurations to run tests on the current file

The server runs on port 60048. To check if it's locked: `lsof -i tcp:60048`

## Key Development Files

- **Workspace file**: `Spell Checker.code-workspace` - recommended for debugging
- **Extension activation**: `packages/client/src/extension.mts`
- **Server main**: `packages/_server/src/server.mts`
- **Settings configuration**: `packages/client/src/settings/`
- **Language server handlers**: `packages/_server/src/api/`
- **VS Code contribution**: root `package.json` `contributes` section
- **Test files**: `*.test.*` or `*.spec.*` (vitest)

## Architecture Notes

### Configuration Synchronization

Configuration fields are defined in two places and must be kept synchronized:
- Server config: `packages/_server/src/config/cspellConfig.ts` - defines `SpellCheckerSettings` interface
- Client config: `packages/client/src/settings/configFields.ts` - exports config field names

After modifying either file, run:
```bash
npm run build-package-schema
```

### Settings Flow

1. User changes setting in VS Code settings or `cspell.json`
2. Client receives notification and forwards to server via JSON-RPC
3. Server applies configuration and re-checks documents as needed

### Webview Communication

Settings UI uses Svelte webviews communicating via RPC:
- `webview-rpc` - handles the RPC layer
- `webview-api` - defines the API contract
- `webview-ui` - the Svelte-based UI implementation

## Node.js Version

Requires Node.js >= 22.20.0 as specified in all package.json `engines` fields.

## Package Management

The project uses npm workspaces (not yarn or pnpm). Common npm workspace commands:

```bash
# Run command in specific workspace
npm --workspace=code-spell-checker-server run build-schema

# Run command in all workspaces
npm --workspaces --if-present run build
```

## cspell Configuration

The project's own spelling is configured in `cspell.config.yaml`. Run spell check locally with: `npx cspell .`

To add words to the project dictionary, add them to the `words` section of `cspell.config.yaml`.

## ESLint Configuration

The project uses ESLint with custom rules defined in `eslint.config.js`. Key configurations:
- TypeScript support via @typescript-eslint
- Simple import sorting with simple-import-sort
- Node.js/EJS patterns for `eslint-plugin-n`
- Unicorn rules for best practices

## Adding New Configuration Options

When adding a new cSpell setting:

1. Define the setting in `packages/_server/src/config/cspellConfig.ts` (SpellCheckerSettings interface)
2. Add the field name to `packages/client/src/settings/configFields.ts`
3. Run `npm run build-package-schema` to sync the schema
4. Use the setting in code via `getSettingFromVSConfig(ConfigFields.settingName, document)`