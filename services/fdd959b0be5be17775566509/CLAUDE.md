# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Install dependencies
npm install

# Setup database and seed data (requires running PostgreSQL)
npm run setup

# Start development server (runs from compiled dist)
npm run dev

# Build for production (compiles TypeScript with SWC, runs webpack)
npm run build

# Build without minification (faster)
npm run build-fast

# Start production server
npm run start

# Run unit tests (Jest)
npm run test

# Run linter with auto-fix
npm run lint

# Compile all packages with SWC
npm run compile

# Compile only postgres-query-builder
npm run compile:db

# Compile with TypeScript compiler (slower, generates declaration files)
npm run compile:tsc
```

## Architecture

EverShop is a TypeScript-first eCommerce platform built with Express, React, GraphQL, and PostgreSQL. It uses a monorepo structure with modules and extensions.

### Package Structure
- **packages/evershop** - Core platform (Express server, React admin/frontend, GraphQL API)
- **packages/postgres-query-builder** - SQL query builder library
- **packages/create-evershop-app** - CLI scaffolding tool
- **extensions/** - Optional extensions (Stripe, PayPal, product review, etc.)

### Core Modules
Located in `packages/evershop/src/modules/`:
- **auth** - Authentication, sessions, login/logout
- **catalog** - Products, categories, attributes, collections
- **checkout** - Cart, payment methods, shipping
- **customer** - Customer accounts, addresses
- **cms** - Pages, widgets, media management
- **oms** - Order management
- **graphql** - GraphQL schema and resolvers
- **promotion** - Discounts, coupons
- **setting** - System configuration
- **tax** - Tax calculation

### Module Structure

```
modules/{name}/
├── api/          # REST API endpoints
│   └── {action}/
│       ├── route.json           # { "methods": ["POST"], "path": "/products", "access": "private" }
│       └── [context]handler[finish].ts  # Middleware chain files
├── graphql/      # GraphQL types and resolvers
├── pages/        # React pages (admin/ and frontStore/)
├── services/     # Business logic functions
├── subscribers/  # Event subscribers
├── components/   # React components
├── migration/    # Database migrations
├── bootstrap.js  # Module initialization
└── events.d.ts   # Event type definitions
```

### Routing & Middleware

**File-based routing**: Routes are auto-discovered from `api/` and `pages/` directories.

**Middleware chain**: Handler files use bracket notation for execution order:
- `[context]bodyParser[auth].ts` - Context prefix, then bodyParser, then auth
- Files execute alphabetically by bracket content

### Extension System

Extensions (`extensions/`) follow the same structure as modules and extend core through:

1. **Registry Pattern**: `addProcessor(name, callback, priority)` - processors sorted by priority
   - Common registries: `productCollectionFilters`, `cartItemFields`, `configurationSchema`

2. **Event System**: `eventSubscriber` with `subscribe(eventName, callback)`

3. **Hookable Pattern**: `hookable.ts` provides WordPress-like hooks (`addAction`, `addFilter`)

### Key Libraries

- **@evershop/postgres-query-builder** - SQL query builder (`insert`, `select`, `update`, `delete`)
- **Registry** (`lib/util/registry.ts`) - Central extension system
- **Router** (`lib/router/`) - URL building with `buildUrl()`, `buildAbsoluteUrl()`
- **Event Emitter** (`lib/event/`) - Async event system
- **Componee** (`lib/componee/`) - Component rendering system for widgets

### Component Organization

- `@components/common` - Shared UI components
- `@components/admin` - Admin dashboard components
- `@components/frontStore` - Storefront components

### Theme System

Themes are separate projects. Use CLI:
```bash
npm run theme:create       # Create new theme
npm run theme:active       # Activate a theme
npm run theme:twizz        # Convert theme to extension
```

## Development Patterns

### Adding a New API Endpoint
1. Create `modules/{module}/api/{action}/` directory
2. Add `route.json`: `{ "methods": ["POST"], "path": "/products", "access": "private" }`
3. Create handler files with bracket notation for middleware chain

### Adding a GraphQL Type
1. Create `modules/{module}/graphql/types/{TypeName}/`
2. Add `{TypeName}.graphql` schema and `{TypeName}.resolvers.ts`
3. Export from `modules/{module}/graphql/types/index.ts`

### Database Migrations
Create `migration/Version-{Version}.ts` exporting a function that runs SQL or uses query builder.

### Configuration
Use `config.get('module.setting')` and register defaults in `bootstrap.ts` with `config.util.setModuleDefaults()`.

### Creating an Extension
Use `npm run theme:create` or create a new extension in `extensions/` following the module structure.

### Testing
Tests are in `dist/**/tests/**` directories. Always run `npm run compile` before testing.
Run a single test file: `npm run test -- --testPathPattern="middleware/buildMiddlewareFunction"`