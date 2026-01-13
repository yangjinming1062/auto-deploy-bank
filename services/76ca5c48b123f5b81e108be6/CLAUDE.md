# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GPTs Works is a third-party GPTs store consisting of three main components:

1. **Website** (`web/` directory) - Next.js 14 frontend deployed on Vercel
2. **Index System** (`index/` directory) - FastAPI Python service for vector search using Azure OpenAI and Zilliz Cloud
3. **Browser Extension** (`extension/` directory) - Plasmo-based extension for showing GPTs in ChatGPT

Live demo: [https://gpts.works](https://gpts.works)

## Common Development Commands

### Website (web/)
```bash
cd web
pnpm install          # Install dependencies
make dev              # Start dev server (http://localhost:8067)
pnpm build            # Build for production
pnpm start            # Start production server
pnpm lint             # Run ESLint
```

### Index System (index/)
```bash
cd index
pip install -r requirements.txt  # Install Python dependencies
make dev                          # Start API server (http://127.0.0.1:8068)
make docker-build                 # Build Docker image
make tidy                         # Update requirements.txt
```

### Browser Extension (extension/)
```bash
cd extension
pnpm install          # Install dependencies
make dev              # Start dev server
pnpm build            # Build extension
pnpm package          # Package for distribution
```

## Architecture

### Web (Next.js)
- **Location**: `web/`
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS + DaisyUI
- **Database**: Vercel Postgres via `@vercel/postgres`
- **Key directories**:
  - `app/api/` - API routes (gpts endpoints)
  - `app/components/` - Reusable React components
  - `app/models/` - Data models
  - `app/services/` - API service functions
  - `app/utils/` - Utility functions

### Index System (FastAPI)
- **Location**: `index/`
- **Framework**: FastAPI (Python)
- **Vector Store**: Zilliz Cloud
- **LLM**: Azure OpenAI (GPT-3.5, text-embedding-ada-002)
- **Key directories**:
  - `apis/` - API endpoints (gpts, ping)
  - `components/` - Database, LLM, env, storage, logging
  - `services/` - Indexing and search logic
  - `models/` - Data models
  - `utils/` - Utility functions

### Browser Extension (Plasmo)
- **Location**: `extension/`
- **Framework**: Plasmo (Chrome Extension)
- **Frontend**: React 18 + TypeScript
- **Key directories**:
  - `src/background/` - Service worker and message handlers
  - `src/components/` - React UI components
  - `src/contents/` - Content scripts (ChatGPT sidebar)
  - `src/services/` - API service functions

## Database Schema

The project uses a single `gpts` table in Vercel Postgres:

```sql
CREATE TABLE gpts (
    id SERIAL PRIMARY KEY,
    uuid VARCHAR(255) UNIQUE NOT NULL,
    org_id VARCHAR(255),
    name VARCHAR(255),
    description TEXT,
    avatar_url TEXT,
    short_url VARCHAR(255),
    author_id VARCHAR(255),
    author_name VARCHAR(255),
    created_at timestamptz,
    updated_at timestamptz,
    detail JSON,
    index_updated_at INT NOT NULL DEFAULT 0
);
```

## Environment Setup

### Web (.env in web/)
```
POSTGRES_URL="postgres://default:xxx@xxx.postgres.vercel-storage.com/verceldb"
INDEX_API_BASE_URI="http://127.0.0.1:8068"
INDEX_API_KEY="gsk-xxx"
```

### Index System (.env in index/)
```
DATABASE_URL=postgres://default:xxx@xxx.postgres.vercel-storage.com:5432/verceldb
AZURE_API_KEY=xxx
AZURE_API_BASE=https://xxx.openai.azure.com/
AZURE_API_VERSION=2023-07-01-preview
AZURE_LLM_MODEL=gpt-35-turbo-16k
AZURE_EMBED_MODEL=text-embedding-ada-002
STORE_TYPE=zilliz
STORE_URI=https://xxx.zillizcloud.com
STORE_TOKEN=xxx
STORE_DIM=1536
STORE_COLLECTION=gpts
INDEX_API_KEY=gsk-xxx
```

## Key API Endpoints

### Website (web/app/api/gpts/)
- `GET /api/gpts/all` - Get all GPTs
- `GET /api/gpts/random` - Get random GPTs
- `POST /api/gpts/search` - Search GPTs
- `POST /api/process/update-gpts` - Update GPTs index

### Index System
- `POST /gpts/index` - Build vector index for GPTs data (requires INDEX_API_KEY)
- `POST /gpts/search` - Search GPTs using vector similarity (requires INDEX_API_KEY)

## Dependencies

- **Deployment**: Vercel (website), Docker (index system)
- **Database**: Vercel Storage Postgres
- **Vector Search**: Zilliz Cloud
- **LLM**: Azure OpenAI (GPT-3.5-turbo for processing, text-embedding-ada-002 for vectors)
- **Frontend**: Next.js, React, Tailwind CSS, DaisyUI
- **Backend**: FastAPI, Python
- **Extension**: Plasmo

## Development Workflow

1. Set up database table (see Database Schema section)
2. Insert GPTs data into the database
3. Start the index system (`make dev` in index/) to enable vector search
4. Start the web application (`make dev` in web/)
5. To develop the extension, load the unpacked extension from `extension/build/`

The web application serves as the main interface, while the index system provides search capabilities and the extension integrates with ChatGPT's UI.