# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AriaNg Native** is an Electron desktop application (version 1.3.11) that provides a native desktop frontend for the aria2 download manager. It includes all features of AriaNg web version plus additional desktop-specific features like file drag-and-drop, taskbar tray, command-line arguments, and file associations.

**Tech Stack:**
- Electron 22.3.7 (main process)
- Angular 1.6.10 (renderer process)
- Node.js (>=14)

## Architecture

The application follows a standard Electron architecture with separate main and renderer processes:

### Main Process (`/main/`)
Contains the Electron main process code that manages application lifecycle, windows, and native OS integration.

**Key Files:**
- `main.js:1` - Main entry point that initializes the Electron app, creates BrowserWindow, handles window events, and manages IPC
- `core.js:1` - Shared state including app ID, version, build commit, and window reference
- `config/config.js:1` - Persistent user settings using electron-store (window size/position, tray settings, startup commands)
- `cmd.js:1` - Command-line argument parsing (supports --development, --classic, --minimal flags)
- `components/menu.js` - Application menu bar
- `components/tray.js` - System tray integration
- `lib/` - Utility modules for file operations, page routing, websocket, and process management
- `ipc/` - Inter-process communication handlers

### Renderer Process (`/app/`)
Angular 1.6.10 single-page application providing the UI.

**Structure:**
- `index.html:1` - Main HTML entry point
- `scripts/` - Angular application code
  - `config/` - Language and routing configuration
  - `controllers/` - Angular controllers
  - `core/` - Core Angular services and utilities
  - `directives/` - Custom Angular directives
  - `filters/` - Angular filters
  - `services/` - Angular services (aria2 RPC, storage, settings, localization, etc.)
- `views/` - HTML templates for different views (new task, settings, status, etc.)
- `langs/` - Translation files (.txt format) for multiple languages
- `styles/` - CSS stylesheets
- `assets/` - Static assets

### Build System
Uses electron-builder for packaging:
- `electron-builder-mac.json:1` - macOS build configuration (supports x64 and arm64)
- `electron-builder-windows-x64.json` - Windows x64 build configuration
- `electron-builder-windows-x86.json` - Windows x86 build configuration
- `generate-build-json.js` - Generates build.json with git commit hash
- `copy-main-modules.js` - Copies main process dependencies to dist
- `copy-app-modules.js` - Copies app dependencies to dist

## Development Commands

**Install dependencies:**
```bash
npm install
```

**Run in development mode:**
```bash
npm start
```

**Clean build directory:**
```bash
npm run clean
```

**Build for Windows (creates both x86 and x64 installers):**
```bash
npm run publish:win
```

**Build for macOS (creates universal binary for x64 and arm64):**
```bash
npm run publish:osx
```

Built applications will be placed in the `dist/` directory.

## Command-Line Options

When running the application:

- `--development, -d` - Enable debug mode (enables DevTools and DevTools shortcuts)
- `--classic, -c` - Use classic window title bar (Windows only)
- `--minimal, -m` - Hide main window at startup

Usage:
```bash
AriaNg Native.exe [file] [options]
```

The application also accepts `.torrent` and `.metalink` files as arguments to create new download tasks directly.

## Key Features

**Desktop-Specific Enhancements:**
- Drag-and-drop file support for creating download tasks
- System tray with minimize-to-tray option
- File associations for .torrent and .metalink files
- Command execution on startup
- Custom window positioning and state persistence
- Native OS integration (macOS file open events, Windows app user model ID)

**IPC Communication:**
The main and renderer processes communicate via IPC for:
- File drop operations (new-drop-file, new-drop-text)
- Dev mode changes
- Electron service initialization
- WebSocket initialization

## Internationalization

Translation files are in `/app/langs/` directory:
- cz_CZ.txt - Czech
- de_DE.txt - German
- es.txt - Spanish
- fr_FR.txt - French
- it_IT.txt - Italian
- pl_PL.txt - Polish
- ru_RU.txt - Russian
- zh_Hans.txt - Simplified Chinese
- zh_Hant.txt - Traditional Chinese

To add a new language:
1. Copy `/i18n/en.sample.txt` to `/app/langs/`
2. Rename to target language code
3. Translate all strings
4. Add language configuration in `/app/scripts/config/languages.js`

## Build Configuration

The build process:
1. Cleans the `dist/` directory
2. Generates build.json with git commit hash
3. Copies main process dependencies
4. Copies app process dependencies
5. Packages using electron-builder

Build artifacts exclude:
- build.json from root
- node_modules from root
- Includes only specific file types from dependencies (JS, CSS, fonts, etc.)

## No Tests

This repository does not include automated tests. Testing would require setting up Electron testing infrastructure separately.

## Dependencies

**Main Process Dependencies** (defined in `mainDependencies` array):
- axios - HTTP client
- bencode - Bencode encoding/decoding
- electron-localshortcut - Keyboard shortcuts
- electron-store - Persistent storage
- simple-sha1 - SHA1 hashing
- ws - WebSocket library
- yargs - Command-line argument parsing

**App Dependencies** (loaded in renderer):
- Angular 1.6.x ecosystem
- Bootstrap 3.4.1
- AdminLTE 2.4.18
- Font Awesome 4.7.0
- jQuery 3.4.1
- ECharts 3.8.5
- Moment.js 2.29.4
- SweetAlert 1.1.3