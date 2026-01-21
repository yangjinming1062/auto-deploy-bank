# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is the **Ledger Live** monorepo - a comprehensive ecosystem for Ledger's cryptocurrency wallet applications. It contains:

- **Applications**: Ledger Live Desktop (Electron) and Ledger Live Mobile (React Native)
- **Libraries**: Core business logic (`ledger-live-common`), hardware wallet communication (`ledgerjs`), UI components, and blockchain integrations
- **Tools**: CLI, testing utilities, and development tools

The project uses **pnpm workspaces** with **turborepo** for monorepo management and **changesets** for versioning.

## Key Commands

All commands run from the repository root.

### Development Workflow

```bash
# Install dependencies (required first time)
pnpm i

# Build all library dependencies
pnpm build:libs

# Run linter and fix issues
pnpm lint:fix

# Run type checking
pnpm typecheck

# Run all tests
pnpm test

# Watch mode for specific areas
pnpm watch:coin           # Watch coin modules
pnpm watch:ljs            # Watch ledgerjs packages
pnpm watch:common         # Watch live-common
```

### Working with Applications

```bash
# Ledger Live Desktop
pnpm dev:lld              # Start desktop app in development
pnpm build:lld            # Build desktop app
pnpm desktop test         # Run desktop tests

# Ledger Live Mobile
pnpm dev:llm              # Start mobile app in development
pnpm build:llm:ios        # Build iOS
pnpm build:llm:android    # Build Android
pnpm mobile test          # Run mobile tests
```

### Working with Specific Libraries

Use the library aliases defined in package.json:

```bash
# Core library
pnpm common              # ledger-live-common

# Coin-related work
pnpm coin:bitcoin        # coin-bitcoin
pnpm coin:evm            # coin-evm
pnpm coin:polkadot       # coin-polkadot
# ... (see package.json for all coin aliases)

# LedgerJS packages
pnpm ljs:hw-app-eth      # @ledgerhq/hw-app-eth
pnpm ljs:hw-transport    # @ledgerhq/hw-transport
# ... (see package.json for all ledgerjs aliases)

# UI components
pnpm ui:react            # @ledgerhq/react-ui
pnpm ui:native           # @ledgerhq/native-ui
pnpm ui:icons            # @ledgerhq/icons-ui
```

### Scoping Commands

Use `--filter` to target specific packages:

```bash
# Run lint on changed packages only
pnpm lint --filter=[origin/develop]

# Test specific package
pnpm test --filter="live-mobile"

# Build specific library and its deps
pnpm build --filter="@ledgerhq/coin-bitcoin"
```

### Testing

```bash
# All tests
pnpm test

# Coin module tests
pnpm coin:coverage

# Single test file (example for ledger-live-common)
pnpm --filter @ledgerhq/live-common test src/__tests__/account.ts
```

### Release Process

```bash
# Add changeset for changelog
pnpm changeset

# Version bump
pnpm bump

# Publish (for maintainers)
pnpm release
```

## Architecture

### High-Level Structure

```
apps/                    # End-user applications
├── ledger-live-desktop  # Electron desktop app
├── ledger-live-mobile   # React Native mobile app
└── web-tools           # Developer tools

libs/                    # Shared libraries and packages
├── ledger-live-common   # Core business logic (currency, accounts, transactions)
├── ledgerjs/           # Hardware wallet communication libraries
│   ├── hw-transport-*  # Transport layers (USB, BLE, WebUSB, etc.)
│   ├── hw-app-*        # Device app interfaces (BTC, ETH, etc.)
│   └── types-*         # TypeScript type definitions
├── coin-modules/       # Blockchain integration modules
├── ui/                 # UI component libraries
└── [other libs]        # Feature-specific libraries
```

### Key Architecture Components

**ledger-live-common** (`libs/ledger-live-common/`)
- Central business logic library
- Defines Currency and Account models
- Implements CurrencyBridge (device scanning) and AccountBridge (sync/transactions)
- Uses RxJS for reactive programming
- Platform-agnostic core used by both Desktop and Mobile apps

**ledgerjs** (`libs/ledgerjs/`)
- Hardware wallet communication layer
- `@ledgerhq/hw-transport-*`: Platform-specific transport implementations
- `@ledgerhq/hw-app-*`: Blockchain-specific device app protocols
- Provides unified Transport interface across platforms

**coin-modules** (`libs/coin-modules/`)
- Individual blockchain integrations
- Each coin implements bridge logic for synchronization and transactions
- Follows standardized pattern defined in ledger-live-common

**UI Libraries** (`libs/ui/`)
- `@ledgerhq/react-ui`: React components
- `@ledgerhq/native-ui`: React Native components
- `@ledgerhq/icons-ui`: Icon library
- Shared design system across platforms

### Data Flow

```
Device (USB/BLE) → Transport (ledgerjs) → App Protocol (ledgerjs)
    ↓
Business Logic (ledger-live-common) → Platform App (Desktop/Mobile)
    ↓
UI Layer (react-ui/native-ui)
```

## Important Notes

- **Applications are in maintenance mode**: Only bugfixes are accepted for Desktop and Mobile apps
- **Library contributions welcome**: New blockchain integrations and library improvements are accepted
- **Monorepo workflow**: Always run commands from root, use `pnpm --filter` or aliases for specific packages
- **Build dependencies**: Libraries must be built before apps. Use `pnpm build:libs` first
- **Type safety**: Ensure typecheck passes before committing
- **Testing**: Coin modules require coverage reports

## Development Guidelines

- Follow Conventional Commits (`feat/`, `bugfix/`, `support/`)
- Branch from `develop`
- Add tests for new functionality
- Use `pnpm changeset` to document changes
- Ensure `pnpm lint:fix`, `pnpm typecheck`, and `pnpm test` pass
- Translations managed externally via Smartling (only edit English files)

## Environment Setup

**Required**: Install [proto](https://moonrepo.dev/proto) toolchain manager and run `proto use` in the repository root.

**For Mobile development**:
- Ruby 3.3.x required
- Install bundler and cocoapods
- See README.md for detailed setup instructions