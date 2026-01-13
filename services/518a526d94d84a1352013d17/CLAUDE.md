# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Jaaz.app is an open-source Canva AI alternative - a desktop application for multimodal canvas creative design. It's built as an Electron app that bundles a React frontend and Python FastAPI backend, with integrated ComfyUI support for local AI model execution.

**Technology Stack:**
- **Desktop Shell**: Electron (main process in `electron/`)
- **Frontend**: React + TypeScript + Vite (in `react/`)
- **Backend**: Python FastAPI + Socket.IO (in `server/`)
- **AI Integration**: ComfyUI, LangChain, OpenAI, Anthropic, Ollama
- **Testing**: Vitest for JavaScript tests

## Common Development Commands

### Full Development (Recommended)
```bash
npm run dev          # Runs React dev server and Electron app concurrently
```

### Individual Components
```bash
# Frontend only (React + Vite)
cd react
npm run dev          # Dev server at http://localhost:5173

# Electron app only
npm run dev:electron

# Python backend only
cd server
pip install -r requirements.txt
python main.py       # Starts on port 57988 (or --port flag)
```

### Building for Distribution
```bash
# Build everything and package Electron app
npm run build:electron

# Platform-specific builds
npm run build:win
npm run build:mac
npm run build:linux
```

### Testing
```bash
# Run all tests (Vitest)
npm test

# Run tests in watch mode
npm test:watch

# Run tests once
npm test:run
```

### TypeScript Compilation
```bash
# Compile Electron TypeScript
npm run build:ts

# Watch mode for Electron TS
npm run watch:ts
```

## Code Architecture

### Electron Main Process (`electron/`)

The Electron main process (`main.js`) initializes the application and manages:
- **ComfyUI integration**: `comfyUIManager.js` handles ComfyUI installation, startup, and workflow management
- **ComfyUI Installer**: `comfyUIInstaller.js` manages downloading and setting up ComfyUI
- **IPC Handlers**: `ipcHandlers.js` manages communication between Electron renderer and main process
- **Settings Service**: `settingsService.js` manages app configuration
- **Preload Script**: `preload.js` exposes safe APIs to renderer process

Key initialization flow in `main.js`:
1. Checks for existing ComfyUI installation
2. Launches ComfyUI if enabled
3. Starts Python backend server
4. Creates Electron window with React app

### React Frontend (`react/src/`)

Standard React + TypeScript + Vite structure:
- **Components**: UI components (buttons, modals, canvas elements)
- **API**: Backend communication layer
- **Contexts**: React context providers for state management
- **Hooks**: Custom React hooks
- **Stores**: State management (likely Zustand or similar)
- **Routes**: Application routing
- **Types**: TypeScript type definitions
- **i18n**: Internationalization (English/Chinese support)
- **i18n config**: `i18n-ally` for translation management (see `.vscode/settings.json`)

### Python Backend (`server/`)

FastAPI application (`main.py`) with modular router architecture:

**Routers** (`routers/`):
- `canvas.py` - Canvas operations and image handling
- `chat_router.py` - Chat functionality and AI interactions
- `config_router.py` - Configuration management
- `image_router.py` - Image processing and generation
- `root_router.py` - Root endpoint
- `settings.py` - Application settings
- `ssl_test.py` - SSL testing
- `tool_confirmation.py` - Tool confirmation workflows
- `websocket_router.py` - WebSocket communication
- `workspace.py` - Workspace management

**Services** (`services/`):
- `config_service.py` - Configuration loading and management
- `tool_service.py` - Tool initialization and management
- `websocket_service.py` - Socket.IO event handling
- `websocket_state.py` - WebSocket state management

**Other modules**:
- `common.py` - Shared utilities
- `asset/` - Asset management
- `models/` - AI model configurations
- `tools/` - Tool implementations
- `utils/` - Python utilities

The FastAPI server:
- Runs on port 57988 (configurable via `--port` flag)
- Uses Socket.IO for real-time communication
- Serves the built React app from `react/dist/`
- Handles file uploads, AI model interactions, and canvas operations

### Build System

**Development**: Vite dev server for React + Electron hot reload
**Production**:
- React build output: `react/dist/` (served by Python server)
- Python server bundled into Electron app
- Electron Builder creates platform-specific installers

**Build artifacts**:
- Windows: NSIS installer
- macOS: DMG + ZIP with hardened runtime
- Linux: AppImage + DEB package

## Configuration Files

- `pyproject.toml` - Python formatting (Black, isort, Ruff) and linting configuration
- `vitest.config.js` - Test configuration (Node environment, single fork mode)
- `.prettierrc.json` - JavaScript/TypeScript formatting
- `.vscode/settings.json` - VS Code configuration with Python/Pylance settings
- `react/vite.config.ts` - Vite configuration
- `react/eslint.config.js` - ESLint rules for React/TypeScript

## Development Notes

### Python Version
Requires Python >= 3.12

### Environment Setup
```bash
# Install React dependencies (may need --force due to peer dependencies)
cd react
npm install --force

# Install Python dependencies
cd server
pip install -r requirements.txt
```

### VS Code Configuration
Recommended extensions:
- Black Formatter (ms-python.black-formatter)
- Pylance (python.languageServer)
- i18n-ally (for translations)

### Code Style
- **Python**: Black formatter, isort, Ruff linter (line length: 88)
- **TypeScript/JavaScript**: Prettier formatting
- **Python type checking**: Strict mode enabled in Pylance

### Testing Structure
- Electron tests in `electron/test/**/*.test.js`
- Uses Vitest with Node environment
- Single fork mode to avoid concurrency issues

### Asset Management
- App icons in `assets/icons/` (jaaz.icns for macOS, jaaz.ico for Windows)
- Code signing handled by `scripts/notarize.js` for macOS
- Build output in `dist/` directory

### Important Environment Variables
- `UI_DIST_DIR` - Override React build directory path
- `no_proxy` / `NO_PROXY` - Proxy bypass settings for localhost (important for Ollama)

## Key Integration Points

1. **Electron ↔ Python**: IPC communication for server management
2. **React ↔ Python**: HTTP API + Socket.IO for real-time updates
3. **ComfyUI Integration**: Python service manages ComfyUI process for local AI models
4. **AI Providers**: Supports OpenAI, Anthropic, Ollama, and local ComfyUI models

## Common Development Tasks

### Adding a new API endpoint:
1. Create router in `server/routers/`
2. Import and include router in `server/main.py`
3. Update frontend API client in `react/src/api/`

### Adding a new Electron feature:
1. Implement in `electron/` using TypeScript
2. Add IPC handlers in `electron/ipcHandlers.js`
3. Expose API via `electron/preload.js`
4. Call from React frontend

### Running specific test:
```bash
npm test electron/test/comfyUIInstaller/core-functions.test.js
```

### Building and testing production build:
```bash
npm run start  # Builds React and starts Electron
```

### Port conflicts:
```bash
# Change Python server port
cd server
python main.py --port 57989
```