# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mailchimp Open Commerce (formerly Reaction Commerce) is an API-first, headless ecommerce platform built on Node.js, MongoDB, and GraphQL. This is a monorepo containing:

- **apps/reaction**: GraphQL API server (main application)
- **apps/meteor-blaze-app**: Admin dashboard application
- **packages/**: 50+ plugin packages providing various ecommerce features

## Common Development Commands

### Running the API Server
```bash
# Start API in development mode (with auto-reload)
pnpm run start:dev

# Or from the apps/reaction directory
npm run start:dev

# Debug mode
npm run start:debug
```

### Testing
```bash
# Run all tests across packages
pnpm run test

# Run integration tests only (apps/reaction)
npm run test:integration

# Run specific integration test suites
npm run test:integration:query
npm run test:integration:mutation1
npm run test:integration:mutation2

# Watch mode for integration tests
npm run test:integration:watch
npm run test:integration:file:watch
```

### Linting & Code Quality
```bash
# Lint all JavaScript/TypeScript
pnpm run lint

# Lint GraphQL schemas
pnpm run lint:gql

# Lint Dockerfiles
npm run lint:docker
```

### Building
```bash
# Build all packages
pnpm run build:packages
```

## High-Level Architecture

### Plugin System
The platform uses a comprehensive plugin-based architecture. Each package in `packages/` is a plugin that can be loaded by the API server. Key plugin types:

**Core Plugins** (packages/api-*):
- `api-core`: Core framework (ReactionAPICore class in packages/api-core/src/ReactionAPICore.js:1)
- `api-plugin-accounts`: User accounts and authentication
- `api-plugin-products`: Product catalog management
- `api-plugin-orders`: Order processing
- `api-plugin-payments`: Payment processing (Stripe, example payments)
- `api-plugin-carts`: Shopping cart functionality
- `api-plugin-inventory`: Inventory tracking
- `api-plugin-catalogs`: Product catalogs
- `api-plugin-fulfillment`: Shipping and fulfillment
- `api-plugin-taxes`: Tax calculations
- And many more...

### Plugin Registration
Each plugin exports a `register` function that receives a ReactionAPI instance. Plugins can register:

- **Collections**: MongoDB collections with indexes
- **GraphQL**: Schemas and resolvers
- **Mutations**: GraphQL mutations
- **Queries**: GraphQL queries
- **Policies**: Authorization policies
- **SimpleSchemas**: Validation schemas
- **Functions**: Lifecycle hooks (preStartup, startup, etc.)

Example plugin structure (packages/api-plugin-accounts/src/index.js:19):

```javascript
export default async function register(app) {
  await app.registerPlugin({
    label: "Accounts",
    name: "accounts",
    version: pkg.version,
    i18n,
    functionsByType: {
      preStartup: [extendAccountSchema, checkDatabaseVersion],
      startup: [afterShopCreate]
    },
    collections: { ... },
    graphQL: { resolvers, schemas },
    mutations,
    queries,
    policies
  });
}
```

### API Server Bootstrap
The main API server (apps/reaction/src/index.js:14) bootstraps by:
1. Loading plugin configuration from `plugins.json`
2. Registering all plugins
3. Starting the server

### GraphQL Architecture
- Apollo Server is used as the GraphQL server
- Core schema defined in `packages/api-core/src/graphql/schema.graphql`
- Subscriptions supported via GraphQL
- Each plugin contributes GraphQL schemas and resolvers
- Custom GraphQL linter rules in `apps/reaction/.reaction/graphql-linter/`

### Database
- MongoDB is the primary database
- Each plugin defines its own collections with indexes
- Collections are registered through the plugin system
- Connection managed by ReactionAPICore

### Configuration
- Environment variables managed via `packages/api-core/src/config.js`
- Key config: MONGO_URL, PORT, REACTION_GRAPHQL_SUBSCRIPTIONS_ENABLED
- Local config in `apps/reaction/.env` (copy from `.env.example`)

## Development Workflow

### Prerequisites
- Node.js 18.10.0 or higher
- PNPM 7.11.0
- MongoDB (local or Docker)
- Docker & Docker Compose (for full stack)

### Initial Setup
```bash
git clone <repo>
cd reaction
pnpm install
cp apps/reaction/.env.example apps/reaction/.env
# Edit .env and set MONGO_URL
docker-compose up -d  # optional, for MongoDB
pnpm run start:dev
```

### Making Changes
1. Make changes to one or more packages
2. Add a changeset: `npx changeset` (follow conventional commits)
3. Ensure tests pass
4. Create PR

### Testing Strategy
- Unit tests: Within each package
- Integration tests: `apps/reaction/tests/integration/api/`
  - `queries/`: GraphQL query tests
  - `mutations1/` and `mutations2/`: Mutation tests (split for parallel runs)

### Release Process
This project uses Changesets for versioning:
1. Run `release` action → Creates Version PR (bumps versions, updates CHANGELOGs)
2. Merge Version PR → CircleCI publishes packages to npm

## Key Files & Directories

- **apps/reaction/src/index.js**: Main API entry point
- **apps/reaction/plugins.json**: Plugin registration configuration
- **packages/api-core/src/ReactionAPICore.js**: Core API framework class
- **packages/api-core/src/graphql/**: Core GraphQL schema
- **apps/reaction/tests/integration/api/**: Integration tests

## Environment Setup

### MongoDB Options
1. **Local MongoDB**: Set MONGO_URL in `.env` to `mongodb://localhost:27017/reaction`
2. **Docker**: Run `docker-compose up -d` then `pnpm run start:dev`

### Node Version Management
- Uses Node 18.10.0+
- `.nvmrc` file present for easy version switching
- Node version checked at startup (apps/reaction/src/checkNodeVersion.cjs)

## Testing Individual Components

### Test a Single Package
```bash
# Run tests for specific package
cd packages/<package-name>
npm test
```

### Run Specific Integration Test
```bash
# From apps/reaction directory
npm run test:integration:file -- --testPathPattern=name-of-test
```

### Debug Tests
```bash
# Run tests in debug mode
node --inspect-brk node_modules/jest/bin/jest.js --runInBand
```

## Working with Plugins

### Create New Plugin
Use the Reaction CLI:
```bash
reaction create-plugin api <your-plugin-name>
```

### Modify Existing Plugin
Each plugin has a consistent structure:
- `src/index.js`: Plugin registration
- `src/schemas/`: GraphQL schemas
- `src/resolvers/`: GraphQL resolvers
- `src/mutations/`: Mutation functions
- `src/queries/`: Query functions
- `src/simpleSchemas.js`: Validation schemas

### Plugin Dependencies
Plugins are registered via `plugins.json` in dependency order. The core framework loads them sequentially.

## GraphQL Development

### Schema Conventions
- All GraphQL files use `.graphql` extension
- Schemas must have descriptions
- Enums and inputs sorted alphabetically
- Relay connection specification compliance

### Adding New GraphQL Types
1. Define schema in plugin's `schemas/` directory
2. Implement resolvers in plugin's `resolvers/` directory
3. Register through plugin's `graphQL` property

### GraphQL Linting
Custom rules enforce consistency:
```bash
pnpm run lint:gql
```

Rules include: descriptions on all types/fields, alphabetical sorting, deprecation reasons, etc.

## Useful Utilities

Core utilities available in `@reactioncommerce/api-core`:
- `importAsString()`: Import GraphQL schemas as strings
- `getAbsoluteUrl()`: Generate absolute URLs
- `collectionIndex()`: Create MongoDB indexes
- And more...

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running: `docker-compose up -d` or local service
- Check MONGO_URL in `.env`
- For replica sets: set REACTION_SHOULD_INIT_REPLICA_SET=true

### Plugin Not Loading
- Verify plugin is in `plugins.json`
- Check for syntax errors in plugin's `index.js`
- Ensure all dependencies are installed: `pnpm install`

### Port Already in Use
- Change PORT in `.env`
- Or stop conflicting service

## Commit & PR Guidelines

- Use [conventional commits](https://conventionalcommits.org/) format
- Add changeset for every PR: `npx changeset`
- PR template requires: Resolves, Impact, Type, Solution, Breaking changes, Testing Instructions
- All PRs must pass linting and tests
- See CONTRIBUTING.md for full guidelines