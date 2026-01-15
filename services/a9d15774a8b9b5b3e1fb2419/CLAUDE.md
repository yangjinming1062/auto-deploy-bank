# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Kinopio is a spatial thinking canvas built as a Vue 3 web application. The client stores data locally in indexedDB and syncs with the `kinopio-server` via API requests (queued for offline support) and websocket broadcasts for real-time collaboration.

## Common Commands

```bash
# Development
npm run dev --host              # Start dev server on https://kinopio.local:8080
npm run build                   # Build for production with SSG
npm run build-dev               # Build with dev API and auto-rebuild
npm run preview                 # Preview production build locally

# Testing
npm run test                    # Run all tests with Vitest
npm run test -- src/utils.test.js    # Run specific test file

# Linting
npm run lint                    # Lint with ESLint
```

## Architecture

### Tech Stack
- **Vue 3** with Composition API
- **Vite** for bundling
- **Pinia** for state management
- **Vite SSG** for static site generation (pre-renders `/` and `/about`)
- **Stylus** for CSS preprocessing
- **IndexedDB** (via `idb-keyval`) for offline-first data persistence

### Entry Points
- `src/main.js` - App initialization, sets up Pinia with websocket plugin and ViteSSG
- `src/router.js` - Vue Router config with route-specific logic (invites, embeds, etc.)

### Store Architecture

**Global State (`useGlobalStore.js`)**: Central UI/interaction state including:
- Viewport, zoom, scroll state
- Toolbar mode, selection state
- User interaction tracking (dragging, painting, connecting)
- Notifications and dialog visibility
- Remote user presence (selections, cursors, dragging items)

**Space State (`useSpaceStore.js`)**: Current space data and operations:
- Space metadata, settings, tags
- Space loading/restoring from cache or API
- Space membership and permissions
- Coordinates space item actions (create, duplicate, etc.)

**Item Stores** - Each handles CRUD and specific item behavior:
- `useCardStore.js` - Card operations, dimensions, positioning
- `useBoxStore.js` - Box/group containers
- `useConnectionStore.js` - Connections and connection types
- `useLineStore.js` - Line drawing

**Supporting Stores**:
- `useUserStore.js` - User auth, preferences, favorites
- `useApiStore.js` - API queue for offline-first operations
- `useBroadcastStore.js` - WebSocket communication
- `useHistoryStore.js` - Undo/redo for local changes
- `useGroupStore.js` - Group/collaborator management

### Data Persistence Flow

1. User action → Store action → Optimistic UI update
2. `cache.js` saves to IndexedDB immediately
3. `useApiStore` queues request for server sync
4. `useBroadcastStore` broadcasts to other connected users
5. On reconnect, queued API requests are replayed

### Key Files
- `src/utils.js` - Utility functions (90KB+), handles DOM, positioning, data transforms
- `src/cache.js` - IndexedDB persistence layer
- `src/consts.js` - Configuration and environment constants
- `src/collisionDetection.js` - Spatial collision detection

### Views
- `views/Space.vue` - Main canvas, handles all space interactions
- `views/Add.vue` - `/add` page for browser extensions/iOS share sheet
- `views/About.vue` - Marketing page (static)

### Components Pattern

Components use a naming convention for common patterns:
- `ItemDetails*` - Detail panels for cards, boxes, connections
- `Remote*` - Display remote user cursors, selections, dragging
- `*Toolbar` - Drawing, card, box toolbars
- `*Handler` - Global event handlers (keyboard, scroll, touch)
- `dialogs/` - Modal dialogs
- `layers/` - Canvas overlays (PaintSelectCanvas, MinimapCanvas)
- `sidebar/` - Sidebar panels
- `page/` - Page-level overlays
- `subsections/` - Reusable UI sections

### Communication

**WebSocket (`useBroadcastStore`)**: Real-time updates for:
- Remote cursor positions (sonar ping)
- Remote selections (cards, boxes, connections)
- Remote dragging positions
- Item updates and deletions

**PostMessage**: Communicates with parent `secureAppContext` (iOS webview wrapper).

## User States to Design For

| State | Description |
|-------|-------------|
| `offline` | IndexedDB and API queue operations only |
| `not signed in` | IndexedDB only |
| `space is read only` | Cannot add/edit cards |
| `space is open` | Can add cards, edit own cards only |
| `mobile` | Touch handlers, no hover, small screen |
| `desktop zoom out` | Using zoom bar or cmd+/- |
| `pinch zoom out/in` | Native touch gesture on mobile |
| `group member/admin` | Can see/edit all group spaces |

## Conventions

- **Component naming**: Single word allowed (disabled rule in ESLint)
- **CSS**: Stylus with `-` naming (e.g., `border-radius`)
- **Icons**: SVG inline, typically 24x24
- **API responses**: Normalized via `utils.normalize*` functions
- **Event handlers**: Use `trigger*` pattern in global store for cross-component communication
- **Type checking**: `utils.typeCheck({ value, type })` validates inputs
- **lodash-es**: Preferred over lodash for tree-shaking

## API Server Connection

To use production API server, create `.env.local` from `.env.local.sample`:
```
VITE_PROD_SERVER=true
```

The server URL is logged in browser console on startup.