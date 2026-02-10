# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Code Spell Checker is a VS Code extension that provides spell checking for source code. It uses a Language Server Protocol (LSP) architecture where the heavy spell-checking logic runs in a separate server process, while the client handles VS Code integration, diagnostics display, and user interactions.

## Commands

```bash
# Install dependencies
npm install

# Build all packages and generate schema
npm run build

# Build only (without schema generation)
npm run build:workspaces

# Run tests in all packages
npm test

# Run tests in a specific package
npm workspace code-spell-checker-server test
npm workspace client test

# Watch mode for development
npm run watch  # In client package

# Lint and format code
npm run lint
npm run lint:eslint  # ESLint only
npm run prettier:fix # Prettier only

# Package the extension for release
npm run build-release

# Run integration tests
npm run test-client-integration
```

**Note:** Requires Node >= 22.20.0

## Architecture

### Package Structure

- **client** - VS Code extension client that handles UI, commands, and LSP client lifecycle. Entry: `packages/client/src/extension.mts`
- **_server** - Language server that performs spell checking using cspell-lib. Entry: `packages/_server/src/main.mts`
- **webview-ui** - Svelte-based webviews for configuration UI and info views
- **webview-api / webview-rpc** - Communication layer between VS Code and webviews
- **json-rpc-api** - Shared RPC definitions
- **__utils** - Shared utilities across all packages

### Communication Layers

1. **Standard LSP** - Document synchronization, diagnostics, and code actions
2. **Custom JSON-RPC** - Extended operations like "Trace Word", configuration sync
3. **Webview RPC** - Communication between VS Code and Svelte webviews

### Spell Check Flow

1. Client opens document → sends to server via LSP
2. Server validates using RxJS streams (debounced)
3. Server invokes cspell-lib to check spelling
4. Diagnostics sent back to client → displayed as underlines
5. Quick Fix requests send to server → suggestions returned

### Adding New Configuration

When adding a new configuration option:

1. Define in `packages/_server/src/config/cspellConfig.ts` using JSDoc annotations
2. Add to `packages/client/src/settings/configFields.ts`
3. Run `npm run build-package-schema` to update package.json schemas

## Key Technologies

- **Language**: TypeScript
- **Build**: tsdown (bundling), tsc (type checking)
- **Testing**: Vitest
- **Linting**: ESLint + Prettier
- **Webviews**: Svelte + custom RPC
- **Reactive**: RxJS (server-side validation streams)
- **Spell Engine**: cspell-lib

## VS Code Debugging

Open `Spell Checker.code-workspace` and press F5 to launch the extension in a new VS Code window. Attach to port 60048 to debug the server process.

## Related Repositories

- Dictionaries have been migrated to [cspell-dicts](https://github.com/streetsidesoftware/cspell-dicts)