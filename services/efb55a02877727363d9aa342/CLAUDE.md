# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Caption is an Electron-based desktop application for finding and downloading subtitles. It's a two-process architecture:
- **Main process** (`main/`): Electron backend that handles IPC, file operations, downloads, and native window management
- **Renderer process** (`renderer/`): React/Next.js frontend with Redux state management

## Build Commands

```bash
# Install dependencies
npm install

# Run development server (with Electron debugging on port 5858)
npm start

# Run tests
npm test
npm run test:watch

# Build for production
npm run build

# Build distributables for all platforms
npm run dist

# Platform-specific builds
npm run dist:mac
npm run dist:windows
npm run dist:linux
```

## Architecture

### Main Process (`main/`)
- `index.js`: App entry point, handles app lifecycle events (ready, activate, window-all-closed), sets up IPC listeners
- `windows/`: Window factory functions (main, about, check, progress) using electron-window-state for persistence
- `sources.js`: Integrates with caption-core for searching subtitles via IPC events
- `download.js`: Handles subtitle file downloads using caption-core
- IPC communication pattern: Renderer sends commands via `ipcRenderer.send()`, Main responds via `webContents.send()`

### Renderer Process (`renderer/`)
- **Pages** (`pages/`): Next.js pages with static export paths configured in `next.config.js`
  - `/start`: Main search page
  - `/about`: About window
  - `/check`: Update check window
  - `/progress`: Download progress window

- **Redux** (`store/`, `reducers/`, `actions/`, `types/`):
  - Two root reducers: `ui` (language, notifications) and `search` (query, results, file state)
  - Actions use thunk middleware and communicate with main process via `ipcRenderer`
  - State flows: UI action → IPC to main → caption-core → IPC response → Redux update

- **Containers** (`containers/`): Smart components connected to Redux (App, Search, Content, Footer)
- **Components** (`components/`): Dumb/presentational React components
- **Utils** (`utils/`): Analytics (react-ga), helper functions

### IPC Communication Pattern
Main process listens for events (`ipcMain.on`) and sends results back:
- `textSearch`: Search by query string
- `fileSearch`: Search by dropped file paths
- `downloadSubtitle`: Download a single subtitle
- `processFiles`: Handle dropped files

Renderer listens for responses (`ipcRenderer.on`):
- `results`: Search results from caption-core
- `allFilesDownloaded`: Download complete notification
- `updateFileSearchStatus`: Per-file download status

### Key Dependencies
- `caption-core`: Subtitle search and download logic (external library)
- `electron-next`: Bridges Next.js with Electron
- `electron-store`: Persistent settings storage
- `redux` + `redux-thunk`: State management

## Code Style

ESLint configuration extends Airbnb base with custom rules:
- 2-space indentation
- PropTypes required for component props
- Filename extensions: `.jsx` for React components, `.js` for other files
- Global `__CLIENT__`, `__DEVELOPMENT__`, `__PRODUCTION__` globals available

## Testing

Jest is configured for testing. Component tests use `react-test-renderer` for snapshot testing. Tests are located in `renderer/components/__tests__/`.