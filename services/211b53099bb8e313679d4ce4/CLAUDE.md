# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Open-Agent is a monorepo containing a multi-agent AI system. It includes a backend server (NestJS), a frontend web app (React), shared packages, and native Rust bindings.

## Commands

### Installation & Setup
```bash
# Install dependencies
yarn

# Build Rust native bindings (required for @afk/server)
yarn oa @afk/server-native build

# Start backend services (Postgres, Redis, Mailhog) via Docker
docker compose -f ./.docker/dev/compose.yml up
```

### Development
```bash
# Run full dev environment (Web + Server)
yarn dev

# Run only the web frontend (Rspack dev server)
yarn dev:web

# Run only the backend server (NestJS)
yarn dev:server
```

### Building
```bash
# Build all packages
yarn build
# Or build a specific package
yarn oa build -p @afk/server
```

### Testing
```bash
# Run all tests (unit + integration)
yarn test

# Run specific test files (vitest)
yarn test src/utils/foo.test.ts

# Run backend API tests (ava)
cd packages/backend/server && yarn test
```

### Linting & Type Checking
```bash
# Lint all files
yarn lint

# Auto-fix linting issues
yarn lint:fix

# Type check all TypeScript projects
yarn typecheck
```

## Architecture

### Monorepo Structure
- `packages/backend/server/`: Main backend application (NestJS, GraphQL API). Uses Prisma for DB access.
- `packages/backend/native/`: Rust bindings for performance-critical operations.
- `packages/frontend/app/`: Web client application (React, Rspack).
- `packages/common/`: Shared types and utilities.
- `blocksuite/`: Block editor component (git submodule/integration).
- `tools/cli/`: Custom CLI built with `clipanion` (entry point `tools/cli/src/oa.ts`).

### Key Technologies
- **Runtime**: Node.js (< 23.0.0), Yarn 4 (Berry)
- **Backend**: NestJS, GraphQL, Prisma, PostgreSQL, Redis (BullMQ)
- **Frontend**: React, Rspack, Vanilla Extract
- **Testing**: Vitest (unit), Ava (backend API)
- **CLI**: Custom tool (`yarn oa <command>`) wrapping workspace operations

### Configuration
- **Backend Env**: Defaults are in `tools/public/dev.md`. Set `DATABASE_URL`, `NEXTAUTH_URL`, and API keys.
- **Ports**:
  - Web: 8080
  - Server: 3010 (GraphQL at /graphql)
  - Mailhog: 8025