# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Cognita is an open-source RAG (Retrieval-Augmented Generation) framework with a frontend UI for managing document collections and querying them. It provides modular, API-driven components for data loading, parsing, embedding, and retrieval.

## Development Commands

### Frontend (React/TypeScript/Vite)

```bash
cd frontend

# Start development server on port 5001
npm run dev

# Build for production
npm run build

# Preview production build on port 5000
npm run preview

# Format code with Prettier
npm run format

# Run TypeScript check and ESLint
npm run lint
```

### Full System (Docker Compose)

```bash
# Start all services (Postgres, Qdrant, Backend, Frontend)
docker-compose --env-file compose.env up

# Start with Ollama and Infinity services for local LLM/embeddings
docker-compose --env-file compose.env --profile ollama --profile infinity up

# Rebuild and start (for code changes)
docker-compose --env-file compose.env up --build
```

### Backend Development

Changes to files in `backend/` are automatically reflected in the running backend server when using Docker Compose.

## Architecture

### Backend Structure (`backend/`)

- **`modules/`** - Pluggable RAG components
  - **`dataloaders/`** - Load data from sources (local dir, S3, GitHub, web URLs, TrueFoundry artifacts)
  - **`parsers/`** - Parse files into chunks (PDF, Markdown, HTML, etc.)
  - **`vector_db/`** - Vector database integrations (Qdrant, SingleStore)
  - **`query_controllers/`** - QnA logic and retrieval strategies
  - **`model_gateway/`** - Unified API for LLM and embedding providers
  - **`metadata_store/`** - Prisma ORM for storing collection/data source metadata
- **`indexer/`** - Async job for ingesting and indexing documents
- **`server/`** - FastAPI server with route decorators (`@post`, `@get`, `@query_controller`)

### Frontend Structure (`frontend/src/`)

- **`screens/`** - Page components (DataSources, Collections, QnA)
- **`components/`** - Reusable UI components
- **`api/`** - Backend API client
- **`stores/`** - Redux state management
- **`router/`** - React Router configuration
- **`utils/`** - Helper utilities

### Data Flow

1. **Indexing**: Data Source → Dataloader → Parser → Embedder → Vector DB
2. **Querying**: User Query → Query Controller → Retriever → LLM → Response

### Key Configuration Files

- `models_config.yaml` - Model provider configurations (LLM, embeddings, rerankers)
- `compose.env` - Environment variables for Docker services
- `truefoundry.yaml` - TrueFoundry deployment configuration

## Adding New Components

### Custom Dataloader
1. Inherit from `BaseDataLoader` in `backend/modules/dataloaders/loader.py`
2. Register in `backend/modules/dataloaders/__init__.py`

### Custom Parser
1. Inherit from `BaseParser` in `backend/modules/parsers/parser.py`
2. Register in `backend/modules/parsers/__init__.py`

### Custom Query Controller
1. Create class in `backend/modules/query_controllers/`
2. Use `@query_controller("/path")` decorator
3. Add methods with `@post("/method")` or `@get("/method")` decorators
4. Import in `backend/modules/query_controllers/__init__.py`

### Custom VectorDB
1. Inherit from `BaseVectorDB` in `backend/modules/vector_db/base.py`
2. Register in `backend/modules/vector_db/__init__.py`

## API Endpoints

The backend exposes routes via FastAPI. Query controllers are auto-registered and accessible at `/<controller-name>/<method>`. Key routes include collection management, data source management, and QnA operations.

## Environment Variables

Frontend environment variables use `VITE_` prefix (e.g., `VITE_DOCS_QA_ENABLE_REDIRECT`, `VITE_USE_LOCAL`). See `frontend/vite.config.ts` and `compose.env` for configuration details.