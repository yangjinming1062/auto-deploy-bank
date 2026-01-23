# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flowy Vue (`@hipsjs/flowy-vue`) is a Vue 2 library for creating draggable flowcharts and hierarchy systems. It uses Shopify Draggable for drag-and-drop functionality and renders connector lines between nodes.

## Common Commands

```bash
npm run serve          # Start dev server at http://localhost:8080/flowy-vue
npm run build:lib      # Build library to dist/lib (main package output)
npm run build:demo     # Build demo app to dist/demo
npm run build:gh-pages # Build docs to docs/ for GitHub Pages
npm run build:all      # Build lib + demo + docs
npm run lint           # Run ESLint on src and root JS files
npm run release        # Interactive release script (prompts for version)
```

## Architecture

### Library Structure

```
src/
├── index.js              # Entry point - exports Flowy, FlowyNode, FlowyBlock, FlowyNewBlock, FlowyDragHandle
├── components/
│   ├── Flowy.vue         # Root container, renders parent nodes (parentId: -1)
│   ├── FlowyNode.vue     # Recursive component rendering node trees with drag/drop
│   ├── FlowyBlock.vue    # Node content wrapper
│   ├── FlowyNewBlock.vue # New node creation block
│   ├── FlowyDragHandle.js# Drag handle registration
│   ├── ConnectorLine.vue # SVG connector lines between nodes
│   └── DropIndicator.vue # Visual feedback during drag
├── lib/
│   ├── moveNode.js       # Mutates node.parentId to new parent
│   ├── createNewNode.js  # Generates new node structure
│   └── generateId.js     # Generates unique node IDs
└── demo_*/               # Demo components and data for testing

quasar-app-extension/     # Optional Quasar Framework integration
```

### Node Data Structure

Nodes are objects with:
- `id`: Unique identifier
- `parentId`: Parent node ID (-1 for root nodes)
- `props`: User-defined content passed to the node component

The library maintains a flat array of nodes and computes the tree structure through parentId relationships.

### Key Component Flow

1. `Flowy` receives a `nodes` array prop and renders `FlowyNode` components for root nodes
2. `FlowyNode` recursively renders itself and its children
3. Drag events from Shopify Draggable emit events: `drag-start`, `drag-stop`, `add`, `move`, `remove`
4. Parent components must handle these events and update the `nodes` array

### Dependencies

- **Vue 2** - Peer dependency
- **@hipsjs/shopify-draggable-vue** - Wraps Shopify Draggable with Vue integration
- **lodash** - Utility functions for node filtering and manipulation

## Build Output

The main package exports `./dist/lib/flowy-vue.common.js`. JSON API files for components are also copied to `dist/lib/` during build.