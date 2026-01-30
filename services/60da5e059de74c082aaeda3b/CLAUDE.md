# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

xgplayer is a web video player library from ByteDance with a plugin-based architecture. Everything is componentized - both the UI layer and video format support are implemented as plugins. The core player extends MediaProxy (HTML5 video element wrapper) and provides a plugin system for extensibility.

## Commands

### Development
```bash
yarn                   # Install dependencies
yarn dev:xgplayer      # Start dev server for main player
yarn dev:hls           # Dev server for HLS plugin
yarn dev:flv           # Dev server for FLV plugin
yarn dev:mp4           # Dev server for MP4 plugin
yarn dev:dash          # Dev server for DASH plugin
yarn dev:subtitle      # Dev server for subtitle plugin
yarn dev:ads           # Dev server for ads plugin
```

### Building
```bash
yarn build             # Build selected package (prompts in monorepo)
yarn build:all         # Build all packages in parallel
```

### Linting & Formatting
```bash
yarn lint              # Check linting with Biome
yarn format            # Format code with Biome
```

### Testing
```bash
yarn test              # Run Jest tests (flv, hls, transmuxer packages)
yarn test:watch        # Watch mode
yarn test:coverage     # Coverage report
yarn test:ci           # CI mode with coverage
```

### Releasing
```bash
yarn release           # Run lint, test, build, then publish (interactive)
yarn release -l -t -b  # Skip individual steps (lint, test, build)
```

## Architecture

### Core Player (`packages/xgplayer/src/player.js`)
- Extends `MediaProxy` which wraps HTML5 video element
- ~70KB single file, manages plugin lifecycle, playback control, and events
- Static getters/setters: `Player.debugger`, `Player.instManager`

### Plugin System

**BasePlugin** (`src/plugin/basePlugin.js`): Base class for all plugins
- Lifecycle hooks: `beforeCreate`, `afterCreate`, `beforeDestroy`, `afterDestroy`
- Event handling: `on`, `once`, `off` methods for player events
- Hooks system: `useHooks`, `hook`, `removeHooks` for lifecycle hooks

**Plugin** (`src/plugin/plugin.js`): UI component class extending BasePlugin
- Defines DOM structure and positioning (`POSITIONS` enum)
- Positions: `ROOT`, `ROOT_LEFT`, `ROOT_RIGHT`, `CONTROLS_LEFT`, `CONTROLS_RIGHT`, `CONTROLS_CENTER`, `CONTROLS`
- Handles icon creation and template rendering
- Built-in plugins in `src/plugins/`: controls, progress, volume, fullscreen, playbackRate, etc.

### Package Structure (Monorepo)

| Package | Purpose |
|---------|---------|
| `xgplayer` | Core player (~70KB) |
| `xgplayer-hls` | HLS streaming support |
| `xgplayer-flv` | FLV streaming support |
| `xgplayer-dash` | DASH streaming support |
| `xgplayer-mp4` | MP4 progressive loading |
| `xgplayer-transmuxer` | Audio/video transmuxing |
| `xgplayer-subtitles` | Subtitle/caption support |
| `xgplayer-ads` | Advertising integration |
| `xgplayer-music` | Audio-only player |
| `xgplayer-streaming-shared` | Shared streaming utilities |

### Events System
Uses `eventemitter3` for event bus:
- Player emits events like `play`, `pause`, `timeupdate`, `error`, `destroy`
- Plugins subscribe via `player.on(event, callback)` and `player.once(event, callback)`

### Global Replacements (at build time)
- `__VERSION__`: Package version string
- `__DEV__`: Boolean for development mode
- `__GIT_HASH__`: Current git commit hash
- `__BUILD_TIME__`: Build timestamp
- `process.env.NODE_ENV`: Set to 'development' or 'production'

### Fixtures (Development Demos)
Located in `fixtures/` directory with demo HTML files for each plugin. Run `yarn dev:xyz` to start a dev server with that fixture.

## Build System

Uses custom `libd` CLI built on Vite + Rollup:
- **Dev mode**: Vite dev server with hot module replacement
- **Production**: Rollup with babel for transpilation, terser for minification
- **Outputs**: ES modules (`es/`), UMD bundles (`dist/`), TypeScript definitions (`es/*.d.ts`)
- **Legacy builds**: Optional IE11 support with core-js polyfills

Build configuration in each package's `package.json` under `libd` key.