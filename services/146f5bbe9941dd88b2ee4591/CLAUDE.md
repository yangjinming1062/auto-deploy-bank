# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Spy Search is an agentic web search framework that generates comprehensive reports using multiple specialized agents. It supports various LLM providers (OpenAI, Claude, Ollama, DeepSeek, xAI/Grok, Gemini) and can run locally or in Docker.

## Commands

### Setup
```bash
# Install all dependencies (Python, npm, playwright)
python setup.py
# Or run installation script directly
sh installation.sh
```

### Development
```bash
# Run both backend and frontend
sh run.sh

# Run backend only (FastAPI on port 8000)
. .venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000

# Run frontend only (Vite on port 8080)
cd frontend && npm run dev
```

### Docker
```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### Frontend
```bash
cd frontend
npm run dev        # Development server
npm run build      # Production build
npm run lint       # Run ESLint
```

## Architecture

### Backend Structure (src/)

**Agent System (`src/agent/`)**
- `Agent`: Abstract base class defining the agent interface with `run()`, `get_recv_format()`, `get_send_format()`
- `Planner`: Orchestrates tasks - creates todo lists and routes to other agents
- `Search_agent`: Searches the web using DuckDuckGo and crawls pages with Crawl4ai
- `Reporter`: Generates comprehensive reports from gathered data
- `RAG_agent`: Handles local document retrieval using ChromaDB
- `Quick_searcher`: Lightweight search for simple queries

**Router/Server (`src/router/`)**
- `Server`: Workflow orchestrator that routes messages between agents
- `Router`: Communication bridge between an agent and the server
- Workflow: `Agent <--> Router <--> Server <--> Router <--> Agent`

**Model Layer (`src/model/`)**
- `Model`: Abstract base class for LLM providers
- Implementations: `OpenAI`, `Ollama`, `Deepseek`, `Gemini`, `Gork`
- Factory pattern in `src/factory/factory.py` to instantiate models by provider name

**API Layer (`src/api/`)**
- `app.py`: Main FastAPI app with route aggregation
- Routes: `streaming.py` (SSE responses), `messages.py`, `files.py`, `agents.py`, `misc.py`
- Services: `message_service.py`, `file_service.py`
- Core: `config.py` (reads/writes config.json), `model_cache.py` (caches model instances)

**Browser Tools (`src/browser/`)**
- `crawl_ai.py`: Crawl4ai integration for page content extraction
- `duckduckgo.py`: DuckDuckGo search functionality

**RAG System (`src/RAG/`)**
- ChromaDB-based document storage and retrieval

### Configuration

**config.json** controls runtime behavior:
```json
{
    "provider": "ollama",      // or openai, deepseek, gemini, gork
    "model": "qwen3:8b",       // model identifier
    "agents": ["reporter"],    // active agents
    "db": "./local_files/test",
    "base_url": "http://host.docker.internal:11434",
    "language": "en"
}
```

### Frontend (frontend/)

- Built with Vite + React + TypeScript
- UI components: shadcn/ui + Radix UI primitives
- Styling: Tailwind CSS
- State management: TanStack React Query
- Routing: React Router DOM
- Charts: Recharts

## Key Patterns

**Agent Communication**: All agents return dicts with keys `agent` (next agent name), `task` (task description), `data` (accumulated results). The Planner terminates when no tasks remain.

**Model Caching**: `model_cache.py` caches model instances to avoid 7+ second reload delays between requests.

**Streaming Responses**: The `/stream_completion/{query}` endpoint uses Server-Sent Events for real-time LLM output.

**Response Parsing**: `Agent._extract_response()` handles JSON/Python literals from markdown code blocks or raw strings.