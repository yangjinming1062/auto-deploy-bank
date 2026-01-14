# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Codemod is an AI-powered, community-led platform for automating code migrations, framework upgrades, and large-scale changes. This is a hybrid Rust/TypeScript monorepo containing the Codemod CLI, workflow engine, and supporting applications.

## Architecture

### Rust Core (`crates/`)

The performance-critical workflow engine and CLI are written in Rust:

- **cli** - Main Rust CLI binary (`cargo build --release` produces `codemod` binary)
- **core** - Workflow engine, registry, and execution logic
- **runners** - Executes codemods via direct, Docker, or Podman
- **models** - Shared data models
- **state** - State management for workflow execution
- **codemod-sandbox** - Sandboxed codemod execution environment
- **language-core/language-javascript/language-python** - Language-specific AST handling
- **mcp** - Model Context Protocol server implementation
- **scheduler** - Workflow node scheduler
- **telemetry** - Analytics and telemetry collection

### Node.js/TypeScript Applications (`apps/`)

Frontend, backend, and tooling are written in TypeScript:

- **cli** - Node.js wrapper that invokes the Rust CLI binary
- **backend** - API service (Next.js Pages Router + Fastify)
- **frontend** - Web application (Next.js App Router)
- **docs** - Documentation site (Mintlify)
- **auth-service** - Dedicated authentication service
- **modgpt** - AI-powered codemod generator

### Shared Packages (`packages/`)

Reusable TypeScript packages:

- **api-types** - Shared API type definitions
- **auth** - Authentication utilities
- **database** - Prisma database client and migrations
- **codemod-utils** - Shared codemod utilities
- **runner** - Codemod runner implementation
- **workflow** - Workflow utilities
- **printer** - Output formatting
- **telemetry** - Telemetry client

## Commands

### Rust Development

```bash
# Build all crates
cargo build --release

# Build specific crate
cargo build -p codemod

# Run tests
cargo test --release

# Run tests for specific crate
cargo test -p butterflow-core

# Run clippy linter
cargo clippy

# Format code
cargo fmt
```

### Node.js Development

```bash
# Install dependencies
pnpm install

# Build all apps/packages
pnpm build

# Build specific app
pnpm --filter @codemod-com/backend build

# Run development servers
pnpm dev

# Run unit tests (Vitest)
pnpm test:unit

# Run backend tests
pnpm test:backend

# Run all tests
pnpm test

# Run tests with coverage
pnpm coverage

# Lint with Biome
pnpm lint

# Auto-fix linting issues
pnpm lint:write

# Database operations
pnpm db:up           # Start Docker database
pnpm db:generate     # Generate Prisma client
pnpm db:migrate:deploy
pnpm db:seed         # Seed database
pnpm db:studio       # Open Prisma Studio
```

### Combined Operations

```bash
# Link local codemod CLI after building
pnpm link

# Create release and publish
pnpm release
```

## Important Conventions

### Git Workflow

- Uses **Changesets** for versioning and changelog management
- Commit messages should be conventional (enforced by husky)
- Contributors must sign the CLA before PRs are merged

### Linting and Formatting

- **Biome** is used for linting and formatting TypeScript/JavaScript code
- Configured in `biome.json`
- Lint-staged runs on commit to enforce standards

### Workflow Files

Workflows (codemod definitions) use YAML with JSON Schema validation:
- Schema: `schemas/workflow.json`
- Templates: `crates/cli/src/templates/`
- Workflow files use `$schema: https://raw.githubusercontent.com/codemod/codemod/refs/heads/main/schemas/workflow.json`

### Environment Variables

- Node.js apps use `.env` files
- Test environment configured in `vitest.config.ts` with in-memory SQLite database
- Rust CLI uses standard environment variables (no `.env` by default)

### Docker/Podman Support

Rust CLI supports Docker/Podman container runtimes via feature flags:
```bash
cargo build --features docker
cargo build --features podman
```

## Key File Locations

- **Database schema**: `packages/database/prisma/schema.prisma`
- **Workflow schema**: `schemas/workflow.json`
- **Turbo pipeline config**: `turbo.json`
- **Biome config**: `biome.json`
- **Workspace Cargo.toml**: `Cargo.toml`
- **Root package.json**: `package.json`
- **Cursor rules**: `.cursor/rules/mintlify-rules.mdc` (for docs only)

## Development Tips

- Node.js version: 22+ (specified in `.nvmrc`)
- Rust version: 1.76+ (specified in `rust-toolchain.toml`)
- Backend runs on port 3000 by default
- Auth service runs on port 8081
- Tests use in-memory SQLite database