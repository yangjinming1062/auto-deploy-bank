# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Lowcoder is an open-source low-code platform for building internal and customer-facing applications. It evolved from the abandoned Openblocks project. The platform features a visual UI builder, 120+ components, custom components, native data connections, and a plugin architecture.

## Common Commands

### Frontend (client)

```bash
# Start development server (requires API service running on port 3000)
yarn start

# Start with custom API URL
LOWCODER_API_SERVICE_URL=http://localhost:3000 yarn start

# Start enterprise edition
yarn start:ee

# Build for production
yarn build
yarn build:ee

# Run frontend tests
yarn test

# Run linting with auto-fix
yarn lint
```

### Backend (server)

```bash
# Node.js service (runs on port 6060 by default)
cd server/node-service
yarn dev        # Development with nodemon
yarn debug      # With debugging enabled
yarn start      # Production build
yarn test       # Run tests
yarn build      # Compile TypeScript

# Java API service (Spring Boot)
cd server/api-service
# Build and run with Maven (pom.xml present)
```

### Both Sides

```bash
# Generate translations
yarn translate
```

## Architecture

### Frontend Monorepo (`client/`)

The frontend uses Yarn workspaces with a monorepo structure under `client/packages/`:

- **lowcoder** - Main React application using Vite, React 18, Redux-Saga, and styled-components. Contains the editor, components, and pages.
- **lowcoder-core** - Core library for building components. Exposes evaluation logic, actions, base components, and i18n utilities. Built with Rollup.
- **lowcoder-comps** - Additional 30+ chart components (ECharts-based) and meeting components. Charts include bar, line, pie, scatter, funnel, gauge, sankey, radar, heatmap, tree, treemap, and more.
- **lowcoder-design** - Design system components and icons. Built with Rollup.
- **lowcoder-sdk** - SDK package for plugin and custom component development.
- **lowcoder-cli** - CLI tool for creating custom components.
- **lowcoder-cli-template-typescript** - TypeScript template for custom components.

### Backend Services (`server/`)

- **node-service** - Node.js/TypeScript service using Express. Handles query execution, JavaScript evaluation, and plugin system for data sources. Runs on port 6060.
- **api-service** - Java/Spring Boot service (Maven project). Handles authentication, org management, application persistence, and plugin endpoints.

### Key Frontend Patterns

**UI Component Registration** (`client/packages/lowcoder/src/comps/uiCompRegistry.ts`):
- Components are registered using `registerComp()` function
- Each component has a manifest with name, categories, keywords, icon, layout info
- Categories: dashboards, layout, forms, collaboration, projectmanagement, scheduling, documents, itemHandling, multimedia, integration, legacy

**Component Structure** (in `lowcoder/src/comps/`):
- `comps/` - Built-in component implementations
- `controls/` - Reusable form controls
- `generators/` - HOCs for component features (withExposing, withMobile, etc.)
- `hooks/` - Custom React hooks
- `queries/` - Query types and handlers
- `utils/` - Component utilities

**State Management**:
- Redux with Redux-Saga for async operations
- Sagas in `redux/sagas/`, actions in `redux/reduxActions/`, reducers in `redux/reducers/`
- Selectors in `redux/selectors/`

**Evaluation System** (`lowcoder-core/src/eval/`):
- `execute/` - JavaScript expression evaluation
- `actions/` - Built-in actions (setValue, setDisabled, etc.)

### Plugin System

**Backend Plugins** (`server/node-service/src/plugins/`):
- 50+ datasource plugins (PostgreSQL, MongoDB, MySQL, Redis, Elasticsearch, REST, GraphQL, etc.)
- Plugin structure: `index.ts` exports connection/query methods
- Each plugin has server-side (Node.js) and optionally frontend components

**Frontend Component Plugins**:
- Can be loaded from npm packages via `npmPlugin` component type
- Custom components can be created using `lowcoder-cli`

## Important Paths

```
client/packages/lowcoder/src/
├── comps/          # Component implementations
├── pages/          # Route pages (editor, applications, settings, etc.)
├── redux/          # Redux store, sagas, actions, reducers
├── api/            # API client layer
├── constants/      # Constants including routes
├── util/           # Utility functions
└── layout/         # Layout components

server/node-service/src/
├── plugins/        # Datasource plugins
├── controllers/    # API controllers
├── services/       # Business logic
├── eval/           # Query evaluation
├── common/         # Shared utilities
└── routes/         # Express routers
```

## Technologies

- **Frontend**: React 18, TypeScript, Vite, Redux-Saga, styled-components, Ant Design 5, ECharts
- **Backend Node**: Express, TypeScript, Jest, Axios
- **Backend Java**: Spring Boot (api-service)
- **Package Manager**: Yarn 3.x with workspaces
- **Build Tools**: Vite (frontend), Rollup (libraries), Maven (Java)

## Environment Variables

Frontend uses these at build time:
- `REACT_APP_API_SERVICE_URL` - API service URL
- `REACT_APP_NODE_SERVICE_URL` - Node service URL
- `REACT_APP_EDITION` - "enterprise" for EE edition
- `REACT_APP_ENV` - "local" for development
- `REACT_APP_LOG_LEVEL` - Debug logging level

Node service:
- `NODE_SERVICE_PORT` - Port (default 6060)
- `LOWCODER_MAX_REQUEST_SIZE` - Max request size (e.g., "50mb")

## Contributing Notes

- Follow existing code patterns and conventions
- Use TypeScript for all new code
- Components should be registered in `uiCompRegistry.ts`
- Backend plugins are in `server/node-service/src/plugins/`
- New components should follow the `withExposingConfigs` pattern for exposing properties
- Run `yarn lint` before committing; prettier runs automatically on staged files via husky