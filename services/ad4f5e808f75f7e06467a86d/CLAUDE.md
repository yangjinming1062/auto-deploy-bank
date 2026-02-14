# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Playwright MCP is a Model Context Protocol server that provides browser automation capabilities using Playwright. It enables LLMs to interact with web pages through structured accessibility snapshots.

**Architecture Note**: The core MCP implementation is located in the [Playwright monorepo](https://github.com/microsoft/playwright) at `packages/playwright/src/mcp`. This repository serves as the npm distribution package, test suite, and browser extension.

## Commands

### Installation
```bash
npm install
npx playwright install  # Install browsers (required before running tests)
```

### Build
```bash
npm run build           # Build all workspaces
```

### Testing
```bash
npm run test            # Run all tests

# MCP server tests (from package directory)
cd packages/playwright-mcp
npm run test            # All browsers (defaults to Chrome)
npm run ctest           # Chrome only (fastest)
npm run ftest           # Firefox only
npm run wtest           # Webkit only
npm run dtest           # Docker-based Chromium tests

# Extension tests
cd packages/extension && npm run test
```

### Linting
```bash
npm run lint            # Lint all workspaces
```

### Publishing
```bash
cd packages/playwright-mcp && npm run lint && npm run test && npm publish
```

### Docker
```bash
npm run docker-build   # Build the MCP server Docker image
```

### Version Updates (Maintainers)
```bash
npm run roll            # Roll to next Playwright version (auto-detects)
npm run roll <version>  # Roll to specific version
```

## Package Structure

- **packages/playwright-mcp** - Main npm package (@playwright/mcp), entry point for MCP server
- **packages/extension** - Chrome/Edge browser extension for connecting to existing browser instances
- **packages/playwright-cli-stub** - CLI stub package for the separate Playwright CLI repository

## Key Entry Points

- `packages/playwright-mcp/cli.js` - CLI entry point that delegates to `playwright/lib/mcp/program`
- `packages/playwright-mcp/index.js` - Exports `createConnection` for programmatic usage
- `packages/extension/src/background.ts` - Extension service worker and WebSocket message relay

## Extension Architecture

The browser extension bridges MCP to existing Chrome/Edge tabs using:
1. **WebSocket relay** (`RelayConnection`): Forwards CDP commands/events between MCP server and `chrome.debugger` API
2. **Service worker** (`background.ts`): Handles extension-runtime communication and WebSocket connections
3. **React UI**: Connection management and status display in the extension popup

**Required permissions** (in `packages/extension/manifest.json`):
- `debugger`: Core CDP instrumentation
- `tabs`, `activeTab`, `storage`: Supporting functionality

To develop the extension:
```bash
cd packages/extension && npm run watch  # Watches TypeScript and Vite builds
```

## Test Fixtures

The MCP tests use custom fixtures (`packages/playwright-mcp/tests/fixtures.ts`):
- `client` - Connected MCP client
- `startClient(options)` - Factory for creating clients with custom args/config/roots
- `server` - HTTP test server on port 8907+
- `httpsServer` - HTTPS test server
- `mcpBrowser` - Browser variant (chrome/firefox/webkit)
- `mcpHeadless` - Run browser headless
- `cdpServer` - CDP endpoint for browser connection tests

### MCP Response Format

Tools return structured responses with `###`-prefixed sections:
- `### Error` - Error messages
- `### Result` - Return values
- `### Snapshot` - Accessibility tree
- `### Ran Playwright code` - Generated code output

Use `formatOutput()` helper from fixtures to clean debug output.

## Configuration

- MCP config types defined in `packages/playwright-mcp/config.d.ts`
- Server accepts CLI args, env vars (`PLAYWRIGHT_MCP_*`), or JSON config file (`--config`)
- `update-readme.js` generates tool documentation from source
- `roll.js` synchronizes Playwright version across packages and copies type definitions

## Technology Stack

- **Node.js**: >=18
- **TypeScript**: Core language
- **Playwright**: Browser automation (`playwright` peer dependency)
- **MCP SDK**: `@modelcontextprotocol/sdk`
- **Vite**: Extension UI build tool
- **React**: Extension UI components