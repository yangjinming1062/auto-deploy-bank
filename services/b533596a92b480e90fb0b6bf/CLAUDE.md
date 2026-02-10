# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Homarr is a lightweight, open-source dashboard software that integrates with self-hosted services. It's a monorepo using pnpm workspaces, Turbo, and Next.js.

## Tech Stack

- **Framework**: Next.js 16 (App Router) with React 19
- **API Layer**: tRPC v11 with OpenAPI support (trpc-to-openapi)
- **Database**: Drizzle ORM with SQLite (better-sqlite3), MySQL (mysql2), and PostgreSQL (pg) support
- **Authentication**: Auth.js (NextAuth v5) with LDAP and OIDC providers
- **UI**: Mantine v8 + Tailwind CSS via PostCSS preset
- **State Management**: Jotai for local state, TanStack Query (React Query) for server state
- **Testing**: Vitest with React Testing Library
- **Package Manager**: pnpm 10.x
- **Build System**: Turbo for task orchestration

## Common Commands

```bash
# Install dependencies
pnpm install

# Start development (runs all apps in parallel)
pnpm dev

# Start production servers (nextjs + tasks + websocket)
pnpm start

# Build all packages and apps
pnpm build

# Run type checking across workspace
pnpm typecheck

# Run linter
pnpm lint
pnpm lint:fix  # Auto-fix linting issues

# Format code
pnpm format
pnpm format:fix  # Auto-format code

# Run tests (unit tests)
pnpm test
pnpm test:ui  # UI mode for debugging tests

# Run e2e tests
pnpm test:e2e

# Database migrations
pnpm db:migration:sqlite:generate  # Generate migration
pnpm db:migration:sqlite:run       # Run migration
pnpm db:push                        # Push schema changes (dev only)
pnpm db:studio                      # Open Drizzle Studio

# Database seeding
pnpm db:seed  # Located in packages/db/migrations/run-seed.ts

# Create a new workspace package
pnpm package:new

# Docker development environment
pnpm docker:dev
```

## Architecture

### Monorepo Structure

```
apps/
  nextjs/          # Main Next.js web application (dashboard UI)
  tasks/           # Background tasks daemon (cron jobs, integrations)
  websocket/       # WebSocket server for real-time updates

packages/
  api/             # tRPC API with ~30 routers for all backend operations
  auth/            # Auth.js configuration with OIDC/LDAP providers
  db/              # Drizzle ORM schema, migrations, and queries
  core/            # Infrastructure (Redis, database connections, logs)
  widgets/         # Dashboard widget components and types
  integrations/    # Third-party service integrations (Jellyfin, qBittorrent, etc.)
  ui/              # Shared Mantine UI components
  translation/     # i18n translations (i18n-ally configured)
  boards/          # Board/grid management
  settings/        # Settings forms and management
  forms-collection # Form component collections
  common/          # Shared utilities and types
  validation/      # Zod validation schemas
  ...              # Other supporting packages
tooling/
  eslint/          # ESLint configurations (base, nextjs, react)
  prettier/        # Prettier configuration
  typescript/      # TypeScript configurations
```

### API Layer (tRPC)

The API is defined in `packages/api/src/router/` with the main router in `root.ts`. All routers use lazy loading:

- **User/Group Management**: `user`, `group`, `invite`
- **Dashboard Content**: `board`, `section`, `widget`, `app`
- **Integrations**: `integration`, `media`, `docker`, `kubernetes`
- **System**: `serverSettings`, `log`, `info`, `certificates`, `cronJobs`
- **Utilities**: `searchEngine`, `location`, `icon`, `import`, `onboard`, `home`

Context and router creation is in `packages/api/src/trpc/trpc.ts`. The API is also exposed as OpenAPI via `trpc-to-openapi`.

### Database Schema

Database schema is in `packages/db/`. The project supports multiple database drivers:

- SQLite (default for development)
- MySQL
- PostgreSQL

Configure via `DB_DRIVER`, `DB_URL` env vars. Schema definitions use Drizzle ORM with Zod validation schemas for type safety.

### Widget System

Widgets are defined in `packages/widgets/` with:
- Widget types in `src/` subdirectories
- Modals for widget configuration
- Error boundaries for fault tolerance
- Integration with `@dnd-kit` for drag-and-drop

### Authentication Flow

`packages/auth/` handles Auth.js with:
- Session management
- OIDC/LDAP provider integration
- API key authentication
- Security middleware

### Real-time Updates

WebSocket server in `apps/websocket/` handles real-time updates for:
- Widget data refresh
- Integration status changes
- Collaborative dashboard updates

## Environment Variables

Key variables in `.env`:
- `DB_DRIVER`: Database driver (better-sqlite3, mysql2, node-postgres)
- `DB_URL`: Database connection string
- `SECRET_ENCRYPTION_KEY`: 32-byte key for encrypting integration secrets
- `AUTH_SECRET`: Auth.js JWT encryption key
- `LOG_LEVEL`: Winston log level
- `UNSAFE_ENABLE_MOCK_INTEGRATION`: Set to `true` for development to enable mock integrations

## Node.js Version

Requires Node.js >= 24.13.0 (specified in package.json engines field)

## Code Conventions

- **TypeScript**: Strict mode enabled, use workspace protocols for internal packages
- **Imports**: Use path aliases (defined in tsconfig.json)
- **Formatting**: Prettier with custom config in `tooling/prettier/`
- **Linting**: ESLint flat config with TypeScript support
- **Tests**: Place `.spec.ts` files alongside implementation, exclude from `apps/nextjs/.next/`

## Database Development

When modifying the schema:
1. Update `packages/db/schema/` files
2. Generate migration: `pnpm db:migration:sqlite:generate`
3. Review migration in `packages/db/migrations/sqlite/`
4. Run migration: `pnpm db:migration:sqlite:run`

## VS Code Configuration

Extensions recommended:
- ESLint (`eslint.experimental.useFlatConfig: true`)
- i18n-ally for translations (configured to look in `packages/translation/src/lang`)
- TypeScript SDK configured to workspace node_modules

## Running Specific Tests

```bash
# Run single test file
vitest run packages/widgets/src/my-widget.spec.ts

# Run with coverage
vitest run --coverage.enabled

# Run specific e2e test
vitest e2e home.spec.ts
```

## E2E Testing

E2E tests use Playwright with test containers. Tests are in `e2e/` directory with helpers in `e2e/shared/`:
- `create-homarr-container.ts` - Docker container for test isolation
- `e2e-db.ts` - Database helper for tests
- `redis-container.ts` - Redis container for real-time tests

## Cron Jobs System

Background tasks run via `apps/tasks/` and are scheduled using cron expressions:
- Widget data refresh jobs
- Integration sync jobs
- Health monitoring checks

Cron job definitions are in `packages/cron-jobs/` with API endpoints in `packages/cron-job-api/`.

## Real-time Updates Architecture

WebSocket connections in `apps/websocket/` work with Redis pub/sub:
1. Widgets subscribe to Redis channels via tRPC subscriptions
2. `apps/websocket` server publishes updates when data changes
3. Clients receive real-time updates without polling

Set `DISABLE_REDIS_LOGS=1` to reduce Redis logging noise.