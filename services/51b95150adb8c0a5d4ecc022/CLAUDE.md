# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Reference

### Setup
```bash
# Install dependencies
pnpm install

# Build all packages
pnpm build

# Start production server
pnpm start

# Development mode (runs all packages in parallel with hot reload)
pnpm dev
# - Server runs on http://localhost:3000
# - UI runs on http://localhost:8080 (with VITE_PORT configured)
```

### Testing
```bash
# Run all tests
pnpm test

# Run server tests only
cd packages/server && pnpm test

# Run components tests only
cd packages/components && pnpm test

# Watch mode for components
cd packages/components && pnpm test:watch

# Generate coverage report
cd packages/components && pnpm test:coverage

# E2E tests (server must be running)
cd packages/server && pnpm e2e
```

### Code Quality
```bash
# Lint all packages
pnpm lint

# Fix linting issues
pnpm lint-fix

# Format code
pnpm format
```

### Package Management
```bash
# Clean build artifacts
pnpm clean

# Clean everything (node_modules, build, turbo cache)
pnpm nuke

# Force rebuild everything
pnpm build-force
```

### Database
```bash
# Generate migration
pnpm migration:create <migration-name>

# Run migrations (from packages/server)
cd packages/server && pnpm typeorm:migration-run

# Revert migrations
cd packages/server && pnpm typeorm:migration-revert
```

## Architecture

Flowise is a **visual AI agent builder** with a Node.js backend, React frontend, and a comprehensive component system for LangChain integrations. The application allows users to build, deploy, and manage AI workflows through a visual interface.

### System Components

**1. Server (`packages/server`)** - Express.js backend
- **Primary role**: REST API server, authentication, orchestration
- **Key features**:
  - TypeORM-based data layer (SQLite/MySQL/PostgreSQL)
  - JWT authentication with API key validation
  - Queue mode for background jobs (BullMQ + Redis)
  - Rate limiting per chatflow
  - Telemetry and metrics (Prometheus/OpenTelemetry)
  - Workspace and organization management
- **Database entities**: ChatFlow, ChatMessage, APIKey, Credential, Assistant, Dataset, Execution, Evaluation, etc.
- **API routes**: Chatflows, predictions, credentials, components, assistants, evaluations, documents, etc.

**2. UI (`packages/ui`)** - React frontend
- **Primary role**: Visual canvas for building AI workflows
- **Tech stack**: React 18, React Router, Redux Toolkit, Material-UI, ReactFlow
- **Key views**:
  - Canvas (drag-and-drop flow builder)
  - Chat interface (test flows)
  - Credentials management
  - Datasets and document stores
  - Evaluations and analytics
- **Build tool**: Vite for development, webpack for production

**3. Components (`packages/components`)** - LangChain integrations
- **Primary role**: Node definitions for the visual editor
- **Categories**:
  - `chains`: Sequential processing workflows
  - `agents`: AI agents with reasoning (ReAct, Plan-and-Execute, etc.)
  - `multiagents`: Multi-agent systems
  - `llms`: Large language models (OpenAI, Azure, Anthropic, local models)
  - `vectorstores`: Vector databases (Pinecone, Weaviate, Qdrant, Chroma, etc.)
  - `retrievers`: Document retrievers (Hybrid, Self-query, etc.)
  - `documentloaders`: File loaders (PDF, CSV, HTML, S3, Unstructured, etc.)
  - `memory`: Conversation memory (Buffer, Summary, etc.)
  - `textsplitters`: Text chunking strategies
  - `embeddings`: Embedding models
  - `prompts`: Prompt templates
  - `outputparsers`: Response parsing
  - `tools`: External tools (APIs, databases, etc.)
  - `moderation`: Content filtering
  - `speechtotext`: Speech-to-text services
- **Each node**: TypeScript class implementing `INode` with credentials, params, and execution logic

**4. API Documentation (`packages/api-documentation`)** - Swagger UI
- Auto-generates API documentation from Express routes
- Accessible at `/docs` when server is running

### Key Systems

**Authentication & Authorization**:
- API key-based authentication for external API calls
- JWT cookie middleware for web sessions
- Enterprise features: Organizations, workspaces, role-based permissions
- SSO support (Auth0, Google, GitHub, etc.)

**Queue System** (`MODE=QUEUE`):
- BullMQ for job queue management
- Redis for job storage and pub/sub
- Dashboard at `/admin/queues` (when enabled)
- Background processing for long-running operations

**Caching**:
- `CachePool`: In-memory cache for component instances
- Redis support for distributed caching
- Usage-based rate limiting

**Storage**:
- Local file storage (default)
- S3-compatible storage
- Google Cloud Storage
- Handles uploaded files, exports, and artifacts

**Telemetry**:
- Anonymous usage analytics
- Opt-in via environment variable
- Tracks feature usage and errors

### Data Flow

1. User creates flow in UI (visual canvas)
2. Flow saved as JSON in database (ChatFlow table)
3. On execution:
   - Server builds execution graph from node definitions
   - NodesPool loads component classes
   - Data flows through chain of nodes
   - Results streamed via Server-Sent Events (SSE)
4. Messages and metadata stored in database
5. Results returned to UI/consumer

## Development Workflow

### Typical Development Session

```bash
# 1. Start development environment
pnpm dev

# Changes to packages/ui or packages/server auto-reload
# For packages/components changes:
pnpm --filter flowise-components build

# 2. Run tests
pnpm test

# 3. Fix linting
pnpm lint-fix && pnpm format

# 4. Build before committing
pnpm build

# 5. Test production build
pnpm start
```

### Environment Configuration

Create `.env` files:

**`packages/server/.env`**:
```env
PORT=3000
DATABASE_TYPE=sqlite
DATABASE_PATH=~/.flowise
SECRETKEY_PATH=~/.flowise
FLOWISE_FILE_SIZE_LIMIT=50mb
```

**`packages/ui/.env`**:
```env
VITE_PORT=8080
VITE_API_URL=http://localhost:3000
```

See full environment variable list in [CONTRIBUTING.md](./CONTRIBUTING.md#-env-variables).

### Adding New Components

1. Create node in appropriate category folder: `packages/components/nodes/<category>/<NodeName>/`
2. Implement `INode` interface with:
   - `credentials`: API keys and auth
   - `inputParams`: User-configurable settings
   - `load()`: Initialize credentials
   - `run()`: Execute node logic
3. Register in `packages/components/src/index.ts`
4. Add to corresponding UI component in `packages/ui/src/ui-component/`
5. Test: `cd packages/components && pnpm test`
6. Build: `pnpm --filter flowise-components build`

### API Development

All routes defined in `packages/server/src/routes/<name>/index.ts`:
- Uses Express routers with JSDoc annotations
- Validation and sanitization via middleware
- Returns standardized response format
- API versioning: `/api/v1/*`

Key route handlers:
- Chatflows: Create, update, deploy, predict
- Predictions: Execute flows, stream responses
- Credentials: Manage API keys
- Components: List available nodes
- Assistants: Custom AI assistants

### Testing Strategy

**Unit Tests** (Jest):
- Components package: Comprehensive node testing
- Server package: Route handlers, utilities
- Watch mode: `pnpm test:watch`

**Integration Tests**:
- E2E tests via Cypress
- Test full flow: dev server → UI interactions → API calls
- Run: `pnpm e2e` (requires server running)

**Test Structure**:
```
packages/
├── server/
│   └── test/
│       ├── routes/        # API endpoint tests
│       └── utils/         # Utility tests
└── components/
    └── __tests__/         # Node-specific tests
```

## Important Notes

- **Node.js version**: >= 18.15.0 < 19.0.0 || ^20
- **PNPM version**: >= 9 (workspace monorepo)
- **Build memory**: Large projects may need `NODE_OPTIONS="--max-old-space-size=4096"`
- **Database migrations**: Auto-run on server startup
- **Hot reload**: Only for ui and server packages; components require rebuild
- **Production build**: Always test with `pnpm build && pnpm start` before PR
- **Credentials**: Never commit `.env` files or secrets
- **Rate limiting**: Per-chatflow configuration available

## Common Tasks

**Add a new API endpoint**:
1. Create route: `packages/server/src/routes/<name>/index.ts`
2. Add controller: `packages/server/src/controllers/<Name>Controller.ts`
3. Update route index: `packages/server/src/routes/index.ts`
4. Add Swagger JSDoc to route
5. Write tests in `packages/server/test/routes/`

**Modify database schema**:
1. Generate migration: `pnpm migration:create <name>`
2. Edit migration file in `packages/server/src/database/migrations/`
3. Run: `cd packages/server && pnpm typeorm:migration-run`
4. Test: `pnpm test`

**Update dependencies**:
1. Root `package.json` contains all workspace dependencies
2. Override versions using `pnpm.overrides` or `resolutions`
3. After updates: `pnpm nuke && pnpm install && pnpm build`

**Debug production issues**:
- Logs: `LOG_PATH` (default: `~/.flowise/logs`)
- Database: SQLite (default) at `~/.flowise/database/`
- API debug: Set `DEBUG=true` in environment
- Queue dashboard: `/admin/queues` (when enabled)

## Key Files

- `package.json` - Root workspace configuration
- `turbo.json` - Build pipeline configuration
- `pnpm-workspace.yaml` - Monorepo package declarations
- `.eslintrc.js` - Code linting rules
- `packages/server/src/index.ts` - Server bootstrap
- `packages/server/src/App.ts` - Application class
- `packages/server/src/Interface.ts` - TypeScript interfaces
- `packages/components/src/index.ts` - Component registry
- `CONTRIBUTING.md` - Detailed contribution guide