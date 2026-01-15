# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Magick is a visual AI Development Environment (AIDE) for no-code data pipelines and multimodal agents. The system uses a node-based graph editor where data flows through "nodes" connected by "sockets" in "spells" (data pipelines).

## Build & Run Commands

```bash
# Development - runs server, cloud-agent-manager, cloud-agent-worker with client config generation
npm run dev

# Run specific apps
npm run dev:server          # Main server (port 7778)
npm run dev:agentManager    # Cloud Agent Manager
npm run dev:agentWorker     # Cloud Agent Worker
npm run dev:client          # Client UI (port 4200)
npm run dev:portal          # Portal (port 4000)
npm run dev:embedder        # Embedder service (port 4010)

# Build commands
npm run build               # Build server, cloud agents, and portal
npx nx build @magickml/client
npx nx build @magickml/server

# Database
npm run db:generate         # Generate Prisma client
npm run db:dev              # Run migrations in dev
npm run db:push             # Push schema to database
npm run db:seed             # Seed database

# Linting
npm run lint                # Lint all projects
npm run lint:engine         # Lint shared-core specifically
npm run lint:server-core    # Lint server/core specifically
npm run lint-fix            # Auto-fix lint issues

# Testing
npm run test                # Run all tests
npm run test:core           # Run shared-core tests
npx nx test <project>       # Run tests for specific project
```

## Architecture

### Monorepo Structure

```
apps/                          # Deployable applications
  client/                      # React/Vite client app (Magick IDE)
  server/                      # Main FeathersJS API server
  cloud-agent-manager/         # Manages agent instances
  cloud-agent-worker/          # Worker for running agents
  agent-connector/             # Agent communication connector
  embedder/                    # Vector embedding service
  seraph-express/              # Seraph AI service
  portal/                      # Git submodule (Next.js portal)

packages/                      # Shared libraries
  client/                      # Client packages (editor, core, chat, etc.)
  server/                      # Server packages (core, db, agent-service, etc.)
  embedder/                    # Embedder packages (worker, queue, config)
  plugins/                     # Connector plugins (discord, slack, knowledge)
  shared/                      # Shared utilities (services, nodeSpec, utils)
```

### Key Technologies

- **Backend Framework**: FeathersJS 5 with Koa
- **Frontend**: React 18 with Vite, Redux Toolkit, TanStack Query
- **Database**: PostgreSQL with pgvector extension, Prisma ORM, Knex
- **Caching/PubSub**: Redis with BullMQ queues
- **Graph Engine**: Grimoire (behave-graph) for node-based spell execution
- **API Layer**: tRPC for type-safe APIs, Zod for validation

### Core Concepts

**Spells**: JSON-defined data pipelines where nodes process data through sockets. A spell represents a complete workflow.

**Nodes**: Black-box transformations that take inputs, process them, and return outputs. Nodes are registered in the `agent-service` package and exposed to clients.

**Grimoire**: The node graph execution system that runs spells. Defined in `packages/server/agent-service/src/lib/grimoire.ts`.

### Key Server Modules

- `@magickml/server-core` - Main FeathersJS app with services (agents, spells, messages, users, etc.)
- `@magickml/agent-service` - Spell execution engine, node registry, and spell casting
- `@magickml/server-db` - Prisma schema and database operations

### Client Modules

- `client-editor` - Visual node graph editor (Composer), agent management, chat windows
- `client-core` - Shared UI components (Chip, Icon, Panel, Select, etc.)
- `client-chat` - Chat interface components
- `client-state` - Redux store configuration

## Database Schema

The Prisma schema is located at `packages/server/db/src/lib/prisma/schema.prisma`. Key tables:
- `Agent` - AI agent definitions
- `Spell` - Spell/pipeline definitions (JSON storage)
- `Project` - User projects
- `User` - User accounts
- `Event` - Events and message logs
- `Credential` - Encrypted API credentials

## Important Configuration

Environment variables are defined in `.env` with overrides in `.env.local`:
- `DATABASE_URL` - PostgreSQL connection
- `REDIS_URL` - Redis connection
- `JWT_SECRET` - Token signing secret
- `VITE_APP_TRUSTED_PARENT_URL` - Portal URL for iframe communication

## Linting Rules

The codebase uses relaxed ESLint rules:
- `@typescript-eslint/no-explicit-any`: off
- `@typescript-eslint/ban-types`: off
- `react-hooks/exhaustive-deps`: off

These rules are intentionally relaxed due to the legacy nature of parts of the codebase.

## Testing

Jest is configured for unit tests. Test files follow the `*.spec.ts` or `*.spec.tsx` naming convention.

## Git Workflow

 Husky is configured for pre-push hooks. Lint-staged runs on staged files.

## Common Patterns

### Adding New Nodes

1. Create node class in `packages/server/agent-service/src/lib/nodes/`
2. Register in `packages/server/agent-service/src/lib/coreRegistry.ts`
3. Export from `packages/server/agent-service/src/index.ts`

### Adding New Services

1. Create service class extending `Service<T>` in `packages/server/core/src/services/`
2. Register in `packages/server/core/src/services/index.ts`
3. Add hooks for authentication/authorization

### Database Changes

1. Modify schema in `packages/server/db/src/lib/prisma/schema.prisma`
2. Run `npm run db:dev` to create migration
3. Run `npm run db:generate` to regenerate client