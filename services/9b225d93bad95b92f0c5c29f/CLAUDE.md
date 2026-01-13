# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VectorAdmin is a universal GUI and tool suite for managing vector databases at scale. It supports multiple vector databases including Pinecone, ChromaDB, QDrant, and Weaviate. The project is a monorepo with a full-stack architecture.

**Status**: This repository is no longer actively maintained by Mintplex Labs, though it remains functional.

## Architecture

VectorAdmin follows a microservices-style architecture with four main components:

### 1. **backend** (Node.js + Express + Prisma)
- API server handling all vector database interactions
- Express server on port 3001 (configurable via `SERVER_PORT`)
- PostgreSQL database with Prisma ORM
- JWT-based authentication
- Key directories:
  - `endpoints/` - API route handlers organized by version/functionality
    - `v1/` - v1 API endpoints (vector DB operations, workspaces, documents)
    - `auth.js` - Authentication endpoints
    - `system.js` - System/installation endpoints
  - `models/` - Prisma data models
  - `utils/` - Helper utilities
    - `vectordatabases/` - Database-specific implementations (Pinecone, Chroma, QDrant, Weaviate)
    - `jobs/` - Background job utilities
    - `openAi/` - OpenAI integration utilities
  - `storage/` - Local file storage for vector cache
- **Database Schema**: PostgreSQL with entities for users, organizations, workspaces, documents, document_vectors, jobs, and RAG tests (see `backend/prisma/schema.prisma:1-180`)

### 2. **frontend** (React + Vite + TypeScript)
- Single-page application for the management UI
- Vite dev server on port 5173 (default)
- React 18 with React Router for navigation
- Tailwind CSS for styling
- Key directories:
  - `src/pages/` - Route components
  - `src/components/` - Reusable UI components
  - `src/utils/` - Frontend utilities
  - `src/models/` - Type definitions and data models
  - `src/hooks/` - Custom React hooks

### 3. **workers** (Node.js + Inngest)
- Background job processor using Inngest for async task execution
- Handles long-running operations:
  - Vector database sync operations (Pinecone, Chroma, QDrant, Weaviate)
  - Document cloning and migration
  - Embedding updates and deletions
  - RAG test automation (hourly, daily, weekly, monthly)
  - Workspace management tasks
- Functions are organized in `workers/functions/` by operation type
- Express server that also serves Inngest endpoints

### 4. **document-processor** (Python + Flask)
- Flask API on port 8888 for document processing
- Parses and extracts text from uploaded documents
- Supports multiple file formats (PDF, DOCX, MD, TXT, MBOX, etc.)
- File parsers in `document-processor/scripts/parsers/`
- Stores processed files in `hotdir/` temporary directory

## Development Commands

### Initial Setup
```bash
# Install all dependencies for all services
yarn dev:setup

# Setup database (generates Prisma client and runs initial migration)
yarn prisma:setup
```

### Running Development Servers
Start each service in separate terminal windows:

```bash
# Backend API server (port 3001)
yarn dev:server

# Frontend React app (port 5173)
yarn dev:frontend

# Background workers
yarn dev:workers

# Document processor (from document-processor directory)
cd document-processor
python3.9 -m venv v-env
source v-env/bin/activate
pip install -r requirements.txt
flask run --host '0.0.0.0' --port 8888
```

### Database Commands
```bash
# Generate Prisma client after schema changes
yarn prisma:generate

# Create new migration
yarn prisma:migrate

# Reset database (destructive)
yarn prisma:reset
```

### Other Commands
```bash
# Lint all packages
yarn lint

# Build frontend for production (from frontend directory)
yarn build
```

## Environment Configuration

Each service requires its own `.env` file. The `devSetup.js` script copies templates to create these files.

### Backend (.env)
- `SERVER_PORT` - API server port (default: 3001)
- `JWT_SECRET` - Secret for JWT signing
- `DATABASE_CONNECTION_STRING` - PostgreSQL connection string
- `DISABLE_TELEMETRY` - Set to "true" to disable analytics

### Frontend (.env)
- `VITE_APP_NAME` - Application name (default: VectorAdmin)
- `VITE_API_BASE` - API base URL (default: /api)

### Workers (.env)
- `INNGEST_EVENT_KEY` - Event key for Inngest
- `INNGEST_SIGNING_KEY` - Signing key for Inngest
- `DISABLE_TELEMETRY` - Set to "true" to disable analytics

See `.env.example` files in each service directory for all options.

## Key Technologies

- **Backend**: Node.js 18+, Express, Prisma ORM, PostgreSQL
- **Frontend**: React 18, Vite, TypeScript, Tailwind CSS, React Router
- **Workers**: Node.js, Inngest (background jobs), Express
- **Document Processing**: Python 3.9+, Flask, various parsers (pdfplumber, python-docx, etc.)
- **Vector Databases**: Pinecone, ChromaDB, QDrant, Weaviate
- **AI/ML**: OpenAI API, LangChain, TikToken for tokenization

## Database Model Summary

The PostgreSQL schema uses these main entities:

- **users** - System users with email/password authentication
- **organizations** - Multi-tenant organizations with multiple workspaces
- **organization_users** - User-organization membership
- **organization_connections** - Vector DB connection configurations per org
- **organization_workspaces** - Namespaces/collections in vector DBs
- **workspace_documents** - Uploaded documents associated with workspaces
- **document_vectors** - Individual vector embeddings linked to documents
- **jobs** - Background job queue with status tracking
- **organization_rag_tests & organization_rag_test_runs** - Automated testing framework

See `backend/prisma/schema.prisma:12-179` for complete schema definitions.

## Vector Database Operations

Vector database interactions are abstracted through utility modules in `backend/utils/vectordatabases/`. Each supported database (Pinecone, Chroma, QDrant, Weaviate) has implementation modules.

Background operations are handled by workers and triggered via Inngest events. Common operations include:
- Syncing existing data from vector DB
- Adding/updating/deleting documents and embeddings
- Cloning workspaces or documents
- Running automated RAG tests

## Document Processing Flow

1. User uploads document via frontend
2. Document sent to backend, stored temporarily
3. Backend triggers background job via Inngest
4. Document processor (Python/Flask) extracts text based on file type
5. Text is chunked and embedded using OpenAI
6. Embeddings stored in configured vector database
7. Document metadata stored in PostgreSQL

See `document-processor/scripts/extract_text.py:1-35` for the extraction logic.

## Development Notes

- The system creates a root user on first boot (email: `root@vectoradmin.com`, password: `password`) - change this immediately after setup
- Telemetry is enabled by default using PostHog for anonymous usage analytics - can be disabled via `DISABLE_TELEMETRY="true"`
- The backend serves the built frontend in production mode (`NODE_ENV=production`)
- Large file uploads are supported (10GB limit configured in body parser)
- Vector cache storage is auto-created at `backend/storage/vector-cache`
- Inngest landing page can be enabled for debugging workers via `INNGEST_LANDING_PAGE="true"`

## API Structure

API routes are prefixed with `/api` and organized as:
- `/api/auth/*` - Authentication endpoints (login, register)
- `/api/system/*` - System initialization and settings
- `/api/v1/*` - Main application API including:
  - Workspaces management
  - Documents upload/management
  - Vector database operations
  - Organizations settings
  - RAG testing

See `backend/index.js:9-13` for endpoint registration and `backend/endpoints/v1/` for implementation.

## Common Development Tasks

### Adding a New Vector Database
1. Create implementation in `backend/utils/vectordatabases/[db-name]/`
2. Add database type to Prisma schema if needed
3. Add worker functions in `workers/functions/` for background operations
4. Update frontend to support the new database type

### Adding New Document Type Support
1. Add parser to `document-processor/scripts/parsers/as_[ext].py`
2. Register in `document-processor/scripts/filetypes.py`
3. Add to requirements.txt if new Python dependencies needed

### Database Schema Changes
1. Modify `backend/prisma/schema.prisma`
2. Run `yarn prisma:migrate` to create migration
3. Update TypeScript types if needed

## Docker Deployment

For production, use Docker Compose. See `docker/DOCKER.md:1-75` for complete instructions. Key points:
- Requires external PostgreSQL database
- Frontend needs `VITE_API_BASE` configured for non-localhost deployments
- Pull pre-built image: `mintplexlabs/vectoradmin` or build from source

## Important Files

- `backend/index.js:1-78` - Main Express server entry point
- `backend/utils/boot/index.js:44-79` - System initialization logic
- `backend/prisma/schema.prisma:1-180` - Complete database schema
- `package.json:1-22` - Root package scripts
- `README.md:1-122` - Project documentation and overview
- `devSetup.js:1-35` - Development environment setup script