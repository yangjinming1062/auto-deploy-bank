# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MineContext is an open-source, proactive context-aware AI partner - a cross-platform desktop application that captures user context (screenshots, documents), processes it with LLMs, and provides intelligent retrieval and generation. Built with Electron + React (frontend) and Python FastAPI (backend).

## Development Commands

### Frontend (React + Electron + TypeScript)

```bash
cd frontend

# Install dependencies (requires original PyPI source, not mirrors)
pnpm install

# Development with hot reload (dev server at localhost:5173)
pnpm dev

# Build for production (outputs to frontend/dist)
pnpm build:mac   # macOS
pnpm build:win   # Windows
pnpm build:linux # Linux

# Type checking
pnpm typecheck           # Both node and web
pnpm typecheck:node      # Main process only
pnpm typecheck:web       # Renderer process only

# Code quality
pnpm format              # Prettier formatting
pnpm lint                # ESLint
```

### Backend (Python FastAPI)

```bash
# Install uv (Rust-based Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies and create virtual environment
uv sync

# Start backend server (default port: 1733)
uv run opencontext start
uv run opencontext start --port 1733        # Custom port
uv run opencontext start --config config.yaml  # Custom config

# Development mode with rebuild
./build.sh  # Rebuild Python extensions after code changes
```

### Full Stack Development

```bash
# Terminal 1: Start backend
uv run opencontext start --port 1733

# Terminal 2: Start frontend
cd frontend && pnpm dev
```

Access backend debug UI at `http://localhost:1733` for task configuration and monitoring.

## Architecture

### Frontend (`frontend/`)

**Electron Process Model:**
- `src/main/` - Electron main process (window management, app lifecycle, IPC orchestration, backend integration)
- `src/preload/` - Secure bridge exposing Node APIs to renderer via context isolation
- `src/renderer/` - React application (UI, state management, API communication)

**Key Patterns:**
- State: Jotai for atomic state, Redux for complex state (user settings, cached data)
- Routing: React Router v6 with HashRouter
- Styling: Tailwind CSS v4 + class-variance-authority
- IPC: Custom channel-based communication via preload scripts (`@shared/ipc-server-push-channel`)
- Data: Dexie.js (IndexedDB wrapper) for local persistence

**Renderer Structure:**
```
src/renderer/src/
├── components/   # Shared UI components
├── pages/        # Route pages (home, vault, screen-monitor, settings, files)
├── hooks/        # Custom hooks (use-events for IPC polling)
├── store/        # Redux store and slices
├── atom/         # Jotai atoms (event-loop.atom for task scheduling)
├── services/     # API service layer
├── utils/        # Helper functions
└── databases/    # Dexie database definitions
```

### Backend (`opencontext/`)

**Modular Layered Architecture:**

```
opencontext/
├── server/           # FastAPI REST API + WebSocket
├── managers/         # Business orchestration (CaptureManager, ProcessorManager, ConsumptionManager)
├── context_capture/  # Data sources (screenshot, document monitors)
├── context_processing/# Processing pipeline (chunking, entity extraction, merging)
├── context_consumption/# AI generation and retrieval
├── storage/          # Multi-backend storage (SQLite, ChromaDB, Qdrant)
├── llm/              # LLM integration (OpenAI-compatible, Doubao)
├── tools/            # Tool system for AI agents
├── monitoring/       # System health monitoring
└── interfaces/       # Abstract base classes for extensions
```

**Data Flow:** Capture → Process → Store → Consume (via LLM)

**Key Classes:**
- `OpenContext` - Main application orchestrator
- Manager classes coordinate all operations
- `ICaptureComponent` / `BaseContextProcessor` interfaces for extensions

**Extension Points:**
- Custom capture modules: Implement `ICaptureComponent` interface
- Custom processors: Extend `BaseContextProcessor`
- Register via factory patterns or configuration

### Build System

- **Frontend bundler**: electron-vite (separate configs for main/renderer)
- **Packaging**: electron-builder (platform-specific builds)
- **Python packaging**: hatchling (wheel distribution)

## Code Style

### Python (Backend)
- Format with Black (line-length: 100)
- Sort imports with isort
- Pre-commit hooks enforce formatting on commit
- Use type hints (PEP 484)
- Follow Pydantic for configuration models

### TypeScript (Frontend)
- Prettier for formatting
- ESLint for linting
- Strict TypeScript mode

### Git Branch Convention
- `feature/` or `feat/` - New features
- `fix/` - Bug fixes
- `hotfix/` - Critical production fixes
- `refactor/` - Code refactoring
- `test/` - Test updates

## Configuration

- Backend config: `config/config.yaml`
- Prompt templates: `config/prompts_en.yaml`, `config/prompts_zh.yaml`
- Frontend env: `frontend/.env.example`

## Key Files

- `frontend/electron.vite.config.ts` - Vite build configuration
- `frontend/electron-builder.yml` - App packaging settings
- `opencontext/cli.py` - Backend CLI entry point
- `opencontext/server/opencontext.py` - Main backend orchestrator