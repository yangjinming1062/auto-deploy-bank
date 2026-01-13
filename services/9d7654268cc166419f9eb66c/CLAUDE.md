# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OverVue is a Vue 3 prototyping development tool that allows developers to dynamically create and visualize Vue applications. It features a real-time component hierarchy tree display and live code preview. The app is distributed as an Electron desktop application built with Quasar Framework.

**Tech Stack:**
- Electron (desktop app wrapper)
- Quasar Framework (Vue 3 based UI framework)
- Vue 3 Composition API
- TypeScript
- Pinia (state management)
- Jest + Vue Test Utils (testing)

## Common Development Commands

### Development
```bash
npm run dev          # Run Electron app in development mode with hot reload
```

### Building & Distribution
```bash
npm run build        # Build production Electron app
npm run build:win    # Build for Windows (requires running `npm run build` first)
npm run build:mac    # Build for macOS (requires running `npm run build` first, builds universal binary)
npm run build:linux  # Build for Linux (requires running `npm run build` first)
npm run build:all    # Build for all platforms
```

### Testing
```bash
npm run test:unit              # Run Jest unit tests (updates snapshots)
npm run test:unit:ci           # Run tests in CI mode
npm run test:unit:coverage     # Run tests with coverage report
npm run test:unit:watch        # Watch mode for tests
npm run test:unit:watchAll     # Watch all tests
npm run serve:test:coverage    # Serve coverage report at http://localhost:8788
```

### Linting
```bash
npm run lint        # Run ESLint on all .js and .vue files
```

### Development with Tests
```bash
npm run concurrently:dev:jest   # Run dev server and Jest watch mode simultaneously
```

### Running Built App
```bash
npm start          # Run built Electron app (after running npm run build)
```

## High-Level Architecture

### Application Structure

**Electron Main Process** (`src-electron/electron-main.ts`):
- Creates and manages the main BrowserWindow
- Handles app lifecycle events
- Configures security context (contextIsolation: true)
- Loads the renderer process from APP_URL environment variable

**Renderer Process** (Quasar/Vue app):
- Vue 3 SPA running inside Electron's BrowserWindow
- Composition API throughout
- TypeScript support enabled

### State Management Pattern

OverVue uses a **reactive state + actions** pattern (not full Pinia pattern):

**State** (`src/stores/state/index.ts`):
- Reactive Vue 3 state using `reactive()` API
- Contains componentMap, routes, userActions, userProps, userState, etc.
- Single source of truth for the entire application

**Actions** (`src/stores/actions.ts`):
- All state mutations performed through actions
- Actions directly modify the reactive state
- Includes component management, HTML element handling, drag-and-drop, etc.

**Store Access** (`src/stores/main.js`):
- Pinia store wrapper (though actual state is reactive, not Pinia-based)
- Used to access actions throughout the app

**Type Definitions** (`types.ts`):
- Comprehensive TypeScript types for State, Actions, Component, HtmlElement, etc.
- Central location for all TypeScript interfaces

### Key Directories

```
src/
├── components/          # Vue components
│   ├── left-sidebar/    # Component creation/editing UI
│   ├── right-sidebar/   # Tree view, code preview, routes, tutorials
│   ├── Canvas.vue       # Visual component positioning canvas
│   ├── nav-buttons/     # Navigation/action buttons
│   └── ...
├── stores/              # State management
│   ├── state/           # Reactive state definitions
│   │   └── index.ts     # Main reactive state object
│   ├── actions.ts       # All state mutations
│   └── main.js          # Pinia store wrapper
├── router/              # Vue Router configuration
├── layouts/             # App layouts
├── pages/               # Route pages
├── assets/              # Static assets
├── utils/               # Utility functions (uploadImage, clearImage, search)
├── customTypings/       # Custom TypeScript type definitions for libraries
└── boot/                # Quasar boot files (pinia.js)
```

### Component Hierarchy Tree

The app manages a **component hierarchy tree** displayed in the right sidebar:
- Tree nodes represent Vue components
- Parent-child relationships define component hierarchy
- Drag-and-drop to reorganize components (OverVue 10.0+ feature)
- Real-time visual feedback of component structure

### Code Generation

The tool generates **Vue 3 boilerplate code**:
- Can toggle between Options API and Composition API
- Exports complete project structure with components, routes, store
- Includes HTML elements, CSS styling, state/actions/props
- Export options: TypeScript/JavaScript, with/without tests, OAuth integrations

### Environment Configuration

**Config Files:**
- `.env.development` - Development environment variables
- `quasar.conf.js` - Quasar framework configuration
- `electron-builder.yml` - Electron builder configuration
- `jest.config.js` - Jest testing configuration

## Important Notes

### State Pattern
- **Do not use Pinia's state directly** - the Pinia store in `main.js` is a thin wrapper
- Actual state is a reactive object in `stores/state/index.ts`
- Actions in `actions.ts` mutate this reactive state
- This pattern was chosen for the project - maintain consistency

### Code Generation Toggle
- State property `exportAsTypescript: "off" | "on"` controls code export format
- State property `composition: boolean` toggles between Composition API and Options API code generation

### Testing
- Jest configured with `@vue/vue3-jest` for Vue 3 support
- Snapshot testing for components
- Tests located in `test/jest/__tests__/`
- Coverage reports available at `test/jest/coverage/`

### Webpack Aliases
Configured in `quasar.conf.js`:
- `src/` mapped to `<rootDir>/src/`
- `~/` mapped to `<rootDir>/`
- Use these aliases in imports: `import from '@/components/...'`

### Known Issues (from README)
- Slack OAuth is currently disabled and not working
- Canvas tree movement limited to arrow keys
- Some peer dependencies not updated (testing libraries)

### Browser Compatibility
Configured in `package.json`:
- Targets last 10 versions of Chrome, Firefox, Edge
- Last 7 Safari versions, last 8 iOS/Android versions

## Development Tips

### Adding New Features
1. State changes → Add to `stores/state/index.ts`
2. Mutations → Add action to `stores/actions.ts`
3. UI → Create component in `src/components/`
4. Tests → Add to `test/jest/__tests__/`

### Working with Reactive State
- Import state from `stores/state/index.ts`
- Import actions from `stores/actions.ts`
- Actions are the only way to modify state
- State is reactive - changes trigger Vue reactivity

### Code Style
- ESLint configured with Vue and TypeScript plugins
- Follow Composition API patterns for new Vue components
- TypeScript strongly typed (definitions in `types.ts`)