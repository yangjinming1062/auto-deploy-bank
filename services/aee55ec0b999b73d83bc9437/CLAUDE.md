# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ListSync automatically synchronizes watchlists from multiple providers (IMDb, Trakt, Letterboxd, MDBList, AniList, TMDB, TVDB, StevenLu) to Overseerr/Jellyseerr media servers. It consists of three components running in a single Docker container:

- **Core Sync Engine** (`list_sync/`): Python service that scrapes lists and creates requests
- **FastAPI Backend** (`api_server.py`): REST API on port 4222
- **Nuxt 3 Frontend** (`listsync-nuxt/`): Vue 3 web dashboard on port 3222

## Development Commands

### Python Backend
```bash
# Install dependencies
pip install -r requirements.txt -r api_requirements.txt

# Run core sync service
python -m list_sync

# Run FastAPI server (development)
python start_api.py

# Linting (ruff)
ruff check .
ruff format .
```

### Nuxt Frontend
```bash
cd listsync-nuxt

# Install dependencies
npm install

# Development server (port 3222 for proxy, Nuxt runs on 3000)
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

### Docker
```bash
# Run pre-built image
docker-compose up -d

# Build and run from source
docker-compose -f docker-compose.local.yml up -d --build
```

### Pre-commit Hooks
```bash
pip install pre-commit
pre-commit install
```

## Architecture

### Core Components

**list_sync/**
- `main.py`: Entry point and orchestration
- `config.py`: Environment-based configuration (`RUNNING_IN_DOCKER` flag)
- `database.py`: SQLite persistence with schema migrations
- `providers/`: Modular provider system using decorator pattern (`@register_provider`)
  - Each provider implements `fetch_<provider>_list()` returning `List[Dict[str, Any]]`
  - Keys required: `title`, `year`, `media_type` ("movie"/"tv"), `imdb_id` (optional)
- `api/overseerr.py`: Overseerr/Jellyseerr API client with fuzzy matching
- `notifications/discord.py`: Discord webhook integration
- `utils/`: Helpers including logger, timezone utilities, sync status

**api_server.py**: FastAPI REST API with 40+ endpoints
- Categories: system health, list management, sync operations, analytics, logging
- Request validation with Pydantic models
- CORS enabled for frontend

**listsync-nuxt/**
- `stores/`: Pinia stores (collections, lists, stats, sync, system, ui, users)
- `composables/`: Vue 3 composables (useApi, useSyncMonitor, useRealtime, useTheme, etc.)
- `pages/`: Route components
- `components/`: Reusable UI components (Shadcn Vue / Radix Vue)
- `types/`: TypeScript type definitions
- `services/`: API client (`api.ts`)

### Data Flow

```
Scheduler → Load Config → Initialize Providers → Fetch Lists
  → Deduplicate (IMDb ID) → Search Overseerr (fuzzy match)
  → Check Status → Create Request → Save to DB → Notify
```

### Database Schema

```sql
lists (list_type, list_id, list_url, item_count, last_synced)
synced_items (title, media_type, year, imdb_id, overseerr_id, status)
sync_interval (interval_hours)
```

### Environment Configuration

Configuration hierarchy (highest to lowest priority):
1. Environment variables (Docker deployments)
2. Encrypted config file (Fernet encryption)
3. Interactive user prompts

Key variables:
- `OVERSEERR_URL`, `OVERSEERR_API_KEY`: Target media server
- `TRAKT_CLIENT_ID`: Required for TMDB/IMDb ID resolution
- `AUTOMATED_MODE`, `SYNC_INTERVAL`: Automation settings
- `RUNNING_IN_DOCKER`: Enables headless Chrome/Xvfb

## Port Reference

| Service | Port | Path |
|---------|------|------|
| Nuxt Frontend | 3222 | `/` |
| FastAPI Backend | 4222 | `/api/*`, `/docs` |

## Provider System

Add a new provider by implementing a function with `@register_provider("name")` decorator:

```python
from . import register_provider

@register_provider("newprovider")
def fetch_newprovider_list(list_id: str) -> List[Dict[str, Any]]:
    return [{title, year, media_type, imdb_id}]
```

## Key Integration Points

- **SeleniumBase** with undetected Chrome for web scraping (IMDb, Letterboxd, MDBList)
- **Trakt API v2** for ID resolution (IMDB → TMDB)
- **FastAPI** with Uvicorn for the REST API
- **Supervisor** manages processes in Docker (xvfb, api, frontend, core)