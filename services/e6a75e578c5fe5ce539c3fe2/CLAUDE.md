# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NVM-Desktop is an Electron-based desktop application for managing multiple Node.js versions. It provides a GUI for downloading, installing, and switching between Node.js versions, with support for project-level version management.

**Architecture**: Electron app with main process (Node.js) and renderer process (React 18). The renderer communicates with main process via IPC through a preload bridge.

## Development Commands

```bash
# Install dependencies (uses pnpm)
pnpm install

# Start development server with hot reload
pnpm dev

# Type checking
pnpm typecheck          # Both node and web
pnpm typecheck:node     # Main process only
pnpm typecheck:web      # Renderer only

# Linting and formatting
pnpm lint
pnpm format

# Build for release
pnpm build

# Package as distributable (output: release/build)
pnpm package            # Current platform
pnpm package:mac        # macOS
pnpm package:linux      # Linux
pnpm package:win        # Windows

# Run E2E tests (requires building first)
pnpm package:test       # Build test version
pnpm test               # Run WebdriverIO tests

# Rebuild native modules (after Electron updates)
pnpm rebuild
```

## Architecture

### Process Structure

- **`src/main/`** - Electron main process (Node.js)
  - `main.ts` - App lifecycle, window creation, IPC handlers, tray menu
  - `deps/` - Node.js download/installation logic (fetch, archive extraction)
  - `utils/` - Settings, projects, versions, groups management, data migration
  - `menu.ts` - Application menu builder
  - `updater.ts` - Auto-update handler (Windows only)

- **`src/preload/`** - IPC bridge (CommonJS, loaded before renderer)
  - `index.ts` - Exposes `window.Context` API to renderer via contextBridge

- **`src/renderer/`** - React 18 frontend
  - `src/index.tsx` - React entry point
  - `routes.tsx` - React Router v6 configuration
  - `pages/` - Route components (Home, Versions, Installed, Projects, Groups)
  - `components/ui/` - Shadcn UI components (Radix primitives + Tailwind)
  - `components/` - Shared components (VersionCard, Loading, etc.)

### IPC Communication Pattern

Main process exposes handlers via `ipcMain.handle()` (async, returns value) and listeners via `ipcMain.on()` (sync/fire-and-forget). The preload bridge exposes these to the renderer as `window.Context.*`:

```typescript
// Main process (src/main/main.ts)
// Handler - async, use for operations that return values
ipcMain.handle("get-projects", async (_event, load: boolean = false) => {
  return getProjects(load);
});

// Listener - sync, use for fire-and-forget messages
ipcMain.on("current-version-update", (_event, version: string) => {
  // Handle the event
});

// Preload (src/preload/index.ts)
// Expose handler to renderer
getProjects: (load: boolean = false) =>
  ipcRenderer.invoke("get-projects", load) as Promise<Nvmd.Project[]>,

// Expose listener callback registration
onRegistCurVersionChange: (callback: OnCurVersionChange) => {
  onCurVersionChange = callback;
},

// Renderer (any React component)
const projects = await window.Context.getProjects(true);
```

The preload script maintains callback state for one-time events and listeners.

### Data Storage

All data stored in `~/.nvmd/`:
- `setting.json` - App settings (theme, locale, mirror, proxy)
- `projects.json` - Project configurations with assigned Node versions
- `groups.json` - Node version groups
- `versions.json` - Cached Node.js version list
- `versions/` - Downloaded Node.js installations
- `bin/` - Shim executables (node, npm, npx, nvmd)

### Key Types

Types are defined in `src/types.ts` and `src/renderer/src/env.d.ts`. Global `Nvmd` namespace is used:
- `Nvmd.Setting` - App configuration (theme, locale, mirror, proxy, directory)
- `Nvmd.Project` - Project with Node version assignment
- `Nvmd.Group` - Node version group (multiple projects share same version)
- `Nvmd.Version` - Node.js version info from nodejs.org
- `Nvmd.ProgressData` - Download progress (percent, transferred, total)
- `Nvmd.Arch` - Architecture type (x64, arm64, etc.)

### Build System

Uses `electron-vite-tsup` with Vite and tsup for building:
- **Main**: Compiled from `src/main/main.ts` to ESM (`release/app/dist/main/`)
- **Preload**: Compiled from `src/preload/index.ts` to CJS (`release/app/dist/preload/`)
- **Renderer**: Built via Vite+esbuild with Tailwind CSS processing (`release/app/dist/renderer/`)

Build configuration in `electron.vite.config.ts` with path aliases:
- `@src/*` -> `./src/*`
- `@renderer/*` -> `./src/renderer/src/*`

## Testing

Tests use WebdriverIO v8 with Mocha framework. Test specs located in `src/__tests__/specs/`. Tests run against the packaged Electron app, not the dev server.

**Setup:**
1. Build test version: `pnpm package:test`
2. Run tests: `pnpm test`

**Test configuration**: `wdio.conf.ts` with WebdriverIO Electron service.

```bash
# Single test file
pnpm test -- --spec ./src/__tests__/specs/setting.spec.ts

# Run with specific mocha grep
pnpm test -- --grep "setting"
```

## Important Notes

1. **nvmd-command binary (REQUIRED for development)**: Project-level Node version switching requires a Rust binary (`nvmd-command`). Before running `pnpm dev`, you must:
   - Build `nvmd-command` from [1111mp/nvmd-command](https://github.com/1111mp/nvmd-command)
   - Copy the binary to:
     - macOS: `assets/sources/nvmd`
     - Windows: `assets/sources/x64.exe` and `assets/sources/arm64.exe`
     - Windows also needs `temp.cmd` wrapper script in the same directory

2. **Platform differences**:
   - Auto-updates only on Windows
   - Custom window controls on macOS (frameless window)
   - System tray behavior differs on Windows

3. **Mirror support**: Custom download mirrors configurable via settings (default: `https://nodejs.org/dist`)

4. **Locale**: Auto-detects system locale (en/zh-CN), translations in `_locales/`

5. **System tray menu**: Built dynamically in `buildTray()` from current state (installed versions, projects, groups). Updates via `buildTray()` after changes.

6. **Version comparison**: Uses `semver` (gt function) for sorting Node versions; versions should follow semver format.

7. **Custom window controls**: Frameless window on macOS uses custom traffic lights; window controls handled via IPC (`window:close`, `window:minimize`).