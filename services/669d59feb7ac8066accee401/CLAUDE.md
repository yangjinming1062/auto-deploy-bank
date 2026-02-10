# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SiYuan is a privacy-first personal knowledge management system with fine-grained block-level reference and Markdown WYSIWYG editor. It's a cross-platform app available on Desktop (Windows/macOS/Linux), Android, iOS, and HarmonyOS.

## Architecture

The project is organized into two main components:

### Kernel (`/kernel`)
- **Language**: Go 1.25.4
- **Purpose**: Backend service handling data storage, business logic, and API serving
- **Key Dependencies**:
  - [Lute](https://github.com/88250/lute) - Markdown editor engine
  - Gin framework - HTTP server (port 6806)
  - SQLite with FTS5 - Full-text search
  - Gomobile - Mobile bindings
- **Entry Point**: `kernel/main.go`

### Desktop App (`/app`)
- **Language**: TypeScript/JavaScript, Electron 39.3.0
- **Purpose**: Frontend UI with Electron wrapper
- **Key Dependencies**:
  - Webpack - Build system
  - ESLint - Code linting
  - Sass - Styles
- **Entry Point**: `app/electron/main.js`

### Communication Pattern
The kernel runs as a separate HTTP server process. The Electron frontend communicates with it via REST API at `http://127.0.0.1:6806`. All data operations go through the kernel API (defined in `kernel/api/`).

## Build Commands

### Kernel (Go)
```bash
cd kernel
# Requires CGO_ENABLED=1 and fts5 build tag
# Windows:
go build --tags "fts5" -o "../app/kernel/SiYuan-Kernel.exe"
# Linux/macOS:
go build --tags "fts5" -o "../app/kernel/SiYuan-Kernel"
```

### Desktop App (Node.js/pnpm)
```bash
cd app
# Install dependencies (requires pnpm 10.28.1)
pnpm install

# Development
pnpm run dev          # Build with webpack dev mode
pnpm run start        # Run Electron app with NODE_ENV=development

# Production Build
pnpm run build        # Build for all platforms
pnpm run dist         # Create installers (uses electron-builder)
```

### Full Development Workflow
1. Build kernel to `app/kernel/SiYuan-Kernel` (or `.exe`)
2. Start kernel: `./app/kernel/SiYuan-Kernel --wd=app --mode=dev`
3. In another terminal, start frontend: `cd app && pnpm run start`

### Mobile Build
```bash
# iOS (requires macOS and Xcode)
cd kernel
gomobile bind --tags fts5 -ldflags '-s -w' -v -o ./ios/iosk.xcframework -target=ios ./mobile/

# Android
cd kernel
gomobile bind --tags fts5 -ldflags "-s -w" -v -o kernel.aar -target=android/arm64 -androidapi 26 ./mobile/
```

## Code Conventions

- **Go**: Follows standard Go formatting (gofmt). Uses `github.com/siyuan-note/siyuan` package path.
- **TypeScript**: Uses ESLint for linting. Run `pnpm lint` to fix issues.
- **Go API Handlers**: Located in `kernel/api/`. Each file handles a specific API domain (e.g., `block.go`, `filetree.go`, `notebook.go`).
- **Kernel API Middleware**: `model.CheckAuth` for authentication, `model.CheckAdminRole` for admin checks, `model.CheckReadonly` for read-only mode protection.

## Data Storage

- **Workspace Directory**: Contains all user data
  - `data/` - Document storage (`.sy` JSON files)
  - `assets/` - Images, files, etc.
  - `emojis/` - Emoji images
  - `snippets/` - Code snippets
  - `templates/` - Template snippets
  - `widgets/` - Widgets
  - `plugins/` - Plugins
  - `public/` - Public data

## Key File Locations

- Kernel API definitions: `kernel/api/router.go`
- Kernel server setup: `kernel/server/serve.go`
- Configuration models: `kernel/conf/`
- Data models: `kernel/model/`
- Electron main process: `app/electron/main.js`
- Frontend source: `app/src/`
- Appearance resources: `app/appearance/` (themes, icons, languages)
- Build configurations: `app/webpack*.js`, `app/electron-builder*.yml`