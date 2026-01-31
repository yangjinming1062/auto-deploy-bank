# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Multimodal AI Agent Monorepo** containing two main products:

1. **UI-TARS Desktop** - Native Electron desktop application for GUI automation
2. **Agent TARS** - General-purpose multimodal AI agent stack (CLI, web UI, MCP integration)

## Development Commands

### Common Commands

```bash
pnpm install              # Install dependencies
pnpm run format           # Format code with Prettier
pnpm run lint             # Run ESLint with auto-fix
pnpm run test             # Run all unit tests
pnpm run coverage         # Generate test coverage
pnpm run test:bench       # Run benchmarks
pnpm run typecheck        # Run TypeScript type checking
```

### UI-TARS Desktop Development

```bash
pnpm run dev:ui-tars      # Start UI-TARS Desktop with hot reload
pnpm run dev:w            # Include main process reload (HMR)
pnpm run build            # Build desktop app for current platform
pnpm run test:e2e         # Run E2E tests with Playwright
```

### Agent TARS / Multimodal Development

```bash
cd multimodal
pnpm run bootstrap        # Build all packages in multimodal/
pnpm run dev              # Start development with PDK (pdk.config.ts)
pnpm run build            # Build all packages
pnpm run test             # Run tests
```

### Package Publishing

```bash
pnpm changeset            # Create changeset for packages
pnpm run publish:packages # Publish latest packages to npm
pnpm run publish-beta:packages # Publish beta packages
```

## Monorepo Structure

```
/
├── apps/
│   └── ui-tars/           # UI-TARS Desktop Electron app
│       └── src/
│           ├── main/      # Electron main process
│           ├── preload/   # Preload scripts
│           └── renderer/  # React frontend (Vite)
├── packages/
│   ├── ui-tars/           # UI-TARS SDK and operators
│   │   ├── sdk/           # Main SDK for building GUI agents
│   │   ├── action-parser/ # Parses model outputs to actions
│   │   ├── electron-ipc/  # IPC communication layer
│   │   ├── operators/     # Platform-specific operators
│   │   │   ├── nut-js/    # Desktop automation (cross-platform)
│   │   │   ├── adb/       # Android device control
│   │   │   └── browser/   # Browser automation
│   │   ├── shared/        # Shared types and utilities
│   │   └── utio/          # Terminal I/O utilities
│   ├── agent-infra/       # Agent infrastructure (MCP servers, browsers)
│   │   ├── mcp-client/    # MCP protocol client
│   │   ├── mcp-servers/   # MCP server implementations
│   │   └── browser-use/   # Browser automation using MCP
│   └── common/            # Shared configs and build tools
└── multimodal/            # Agent TARS ecosystem
    ├── tarko/             # Tarko agent framework
    │   ├── agent/         # Core agent implementation
    │   ├── agent-cli/     # CLI for Tarko
    │   ├── model-provider/# LLM provider abstractions
    │   ├── context-engineer/ # Context compression/engineering
    │   └── shared-utils/  # Shared utilities
    ├── agent-tars/        # Agent TARS implementation
    │   ├── core/          # Agent TARS core logic
    │   ├── cli/           # Agent TARS CLI
    │   └── interface/     # Type interfaces
    ├── gui-agent/         # GUI agent operators
    │   ├── operator-aio/  # All-in-one operator
    │   ├── operator-nutjs/# NutJS-based operator
    │   └── operator-browser/ # Browser operator
    └── omni-tars/         # Omni-directional agent
```

## Architecture Notes

### UI-TARS Desktop Flow

```
User Input → React UI → IPC → Main Process → Model (Local/Remote)
                                        ↓
                                Action Parser → Operators (nut-js/adb/browser)
                                        ↓
                                Execute Actions → Return Results
```

### Agent TARS Event Stream Architecture

Agent TARS uses an **Event Stream** protocol where all interactions flow through a unified event stream, enabling:
- Context engineering and compression
- Agent UI real-time updates
- MCP tool integration
- Streaming tool execution

### Key Package Dependencies

- `@ui-tars/sdk` → Depends on `@ui-tars/action-parser`, `@ui-tars/shared`
- `@ui-tars/electron-ipc` → Bridge between renderer and main process
- `@agent-tars/core` → Uses `@tarko/*` packages and `@agent-tars/interface`
- `@tarko/context-engineer` → Depends on `@tarko/shared-media-utils`

## Build Tools & Configuration

- **Package Manager**: pnpm 9.10.0
- **Build Tool**: turbo for task orchestration, rslib for bundling
- **Bundler**: electron-vite (UI-TARS Desktop), rslib (packages in multimodal/)
- **Test Framework**: vitest (unit), playwright (E2E)
- **Node Version**: >=20 (UI-TARS Desktop), >=22 (Agent TARS)
- **State Management**: Zustand
- **Code Quality**: ESLint, Prettier, Husky (pre-commit hooks), commitlint

## Pre-commit Hooks

Husky and lint-staged are configured to run on commit:
- Prettier formatting
- TypeScript type checking

## Testing

```bash
# Run single test file
vitest run path/to/test.test.ts

# Run with coverage
vitest run --coverage

# Watch mode
vitest

# Run UI-TARS Desktop tests from root
pnpm --filter ui-tars-desktop test

# Run Agent TARS tests from multimodal/
cd multimodal && pnpm run test
```