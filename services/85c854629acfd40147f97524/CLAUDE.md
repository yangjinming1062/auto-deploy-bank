# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Unigraph is a local-first, universal knowledge graph and personal search engine/workspace. A monorepo with TypeScript backend (Node.js + Express + Dgraph), React frontend, and Electron desktop app.

**Tech Stack:**
- TypeScript 4.2+, Node.js 16.13.1, React 17, Dgraph (graph database), Electron 17.1
- Lerna 4 + Yarn workspaces for monorepo management
- Zustand (state), Material-UI, Monaco Editor, FlexLayout

## Build/Test/Lint Commands

```bash
# Installation
yarn                              # Install dependencies
yarn build-deps                   # Build all dependencies and packages
yarn prepare                      # Setup husky hooks

# Development
./scripts/start_server.sh         # Start backend with Dgraph (requires Dgraph binary)
yarn explorer-start               # Run frontend in browser (port 3000)
yarn electron-start               # Run as Electron desktop app

# Building
yarn backend-build                # Build backend
yarn build-common                 # Build common libraries
yarn link-common                  # Link common package locally
yarn build-packages:linux:darwin  # Build all default packages

# Testing & Linting
yarn test                         # Run all tests (via Lerna)
yarn lint                         # Run linter
yarn lint --fix                   # Auto-fix linter issues

# Distribution
yarn prepare-electron && yarn electron-dist  # Build Electron distribution
```

## Architecture

```
packages/
├── unigraph-dev-backend/       # Express server + Dgraph client + API
├── unigraph-dev-common/        # Shared types, utilities, API definitions
├── unigraph-dev-explorer/      # React frontend (Vite)
├── unigraph-dev-electron/      # Electron wrapper (main.js, preload.js)
├── unigraph-packager/          # Package builder tool
└── default-packages/           # 20+ default Unigraph packages (core, email, calendar, notes, todo, etc.)
```

**Key Patterns:**
- Each default package contains: `package.json`, `schemas/`, `executables/`
- Dynamic package loading/unloading at runtime
- Graph entities use `unigraph.id` for canonical identification
- Real-time subscriptions via WebSocket

## Configuration

**ESLint:** Extends Airbnb + TypeScript + Prettier, 120 char line limit, 4 space indent
**Prettier:** Single quote, trailing comma all, 4 space width, 120 print width
**TypeScript:** Strict mode, path aliases (@/*) in backend

## Ports

- 3000: Frontend web app
- 4001: Backend WebSocket API
- 4002: Backend HTTP API
- 8080: Dgraph (must be free for server startup)

## API Keys

Third-party integrations require `secrets.env.json` at repo root:
```json
{
  "twitter": { "api_key": "...", "api_secret_key": "...", "bearer_token": "..." },
  "reddit": { "client_id": "..." },
  "openai": { "api_key": "..." },
  "google": { "client_id": "...", "client_secret": "..." }
}
```