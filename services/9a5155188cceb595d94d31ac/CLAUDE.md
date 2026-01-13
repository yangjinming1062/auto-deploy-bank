# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AnythingLLM is a full-stack AI application that enables you to turn documents into context for LLMs. It features multi-user support, workspace-based document organization, and supports 30+ LLM providers and 8+ vector databases.

## Development Commands

### Initial Setup
```bash
# Install dependencies and set up environment files
yarn setup

# Set up database (Prisma)
yarn prisma:generate
yarn prisma:migrate
yarn prisma:seed
```

### Running in Development
```bash
# Start all services concurrently
yarn dev:all

# Or start individual services in separate terminals
yarn dev:server  # Node.js Express API server
yarn dev:frontend  # React/Vite frontend
yarn dev:collector  # Document processing service
```

### Testing & Quality
```bash
# Run all tests
yarn test

# Run linter on all services
yarn lint
```

### Production
```bash
# Start server in production mode
yarn prod:server

# Build frontend for production
yarn prod:frontend
```

### Database Management
```bash
# Reset database
yarn prisma:reset

# Regenerate Prisma client
yarn prisma:generate

# Run migrations
yarn prisma:migrate
```

### Translation Management
```bash
# Verify translations are valid
yarn verify:translations

# Normalize and lint translations
yarn normalize:translations
```

## Code Architecture

### Server (`server/`)
Node.js Express API with modular endpoint structure:
- **`endpoints/`**: Route handlers for different features
  - `system.js`: System configuration & health checks
  - `workspaces.js`: Workspace CRUD operations (largest file)
  - `chat.js`: Chat interface with LLMs
  - `admin.js`: Admin panel functionality
  - `agentFlows.js`: No-code AI agent builder
  - `api.js`: Developer API endpoints
  - Other specialized endpoints for browser extension, mobile, etc.
- **`utils/`**: Shared utilities
  - `AiProviders/`: LLM provider integrations (OpenAI, Anthropic, Ollama, etc.)
  - `vectorDbProviders/`: Vector database connectors (LanceDB default)
  - `helpers/`: General utility functions
- **`storage/`**: Persistent data
  - `documents/`: Cached processed documents (JSON format with `pageContent` key)
  - `vector-cache/`: Vector embeddings cache
- **`prisma/`**: Database schema and migrations (SQLite by default)

### Frontend (`frontend/src/`)
React application with Vite build system:
- **`components/`**: Reusable UI components
- **`pages/`**: Route-based page components
- **`hooks/`**: Custom React hooks
- **`locales/`**: Internationalization files (multi-language support)
- **`utils/`**: Frontend utilities

### Collector (`collector/`)
Node.js service for document processing and parsing (runs separately from server).

## Configuration & Environment

### Required Environment Files
- `server/.env.development` - Server configuration (required for dev)
- `frontend/.env` - Frontend configuration
- `collector/.env` - Collector configuration
- `docker/.env` - Docker deployment configuration

### Database
- Uses Prisma ORM with SQLite by default
- Database file: `server/storage/anythingllm.db`
- Supports PostgreSQL (via PGVector), MySQL, and other databases
- See `server/utils/prisma/PRISMA.md` for details

### Supported Integrations
- **LLM Providers**: OpenAI, Anthropic, AWS Bedrock, Google Gemini, Ollama, LM Studio, 30+ providers
- **Vector Databases**: LanceDB (default), PGVector, Pinecone, Chroma, Weaviate, Qdrant, Milvus, Zilliz
- **Embedders**: AnythingLLM Native, OpenAI, Azure OpenAI, Cohere, Ollama

## Key Technical Details

### Document Storage
Documents are stored in `server/storage/documents/` as JSON files with:
- Required: `pageContent` field
- Optional: metadata fields
- Reserved: `published` field for timestamps

### API Design
The server uses a modular endpoint pattern. Each endpoint file exports functions that handle related routes. Main endpoint categories:
- System management (health, config)
- Workspace operations (CRUD, document management)
- Chat (LLM interactions, context retrieval)
- Agent flows (custom AI agents)
- Developer API (integrations)

### Testing
- Jest-based testing framework
- Test files in `__tests__` directories
- Tests cover utilities, providers, models, and core logic

### Code Style
- ESLint + Prettier configuration
- 2-space tabs, LF line endings
- Flow type annotations in server code
- React functional components with hooks in frontend

## Important Notes

- **Node.js >= 18** required
- The server uses a modular API design - when adding features, create new endpoint modules in `server/endpoints/`
- Workspace isolation: each workspace has its own document context and doesn't share with others
- Vector databases are swappable via the `getVectorDbClass()` utility
- LLM providers follow a standardized interface in `server/utils/AiProviders/`
- When modifying the database schema, update the Prisma schema and create migrations