# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Syllepsis is a rich text editor built on ProseMirror, providing a simplified API layer and plugin system. It uses a three-layer architecture:
- **@syllepsis/adapter**: Core ProseMirror wrapper with controllers, schemas, formatters, and events
- **@syllepsis/editor**: Middle layer providing Editor service on top of adapter
- **@syllepsis/access-react**: React integration component (`<SylEditor />`)

## Common Commands

```bash
# Build all packages
yarn build

# Build specific packages
yarn build:adapter    # Core adapter only
yarn build:editor     # Editor layer only
yarn build:plugin     # All plugins
yarn build:react      # React access layer

# Development - watch mode (run in parallel)
yarn watch:adapter && yarn watch:editor && yarn watch:plugin && yarn watch:react
yarn watch:code       # Alias for watching all code packages

# Run tests (Jest with Puppeteer for E2E browser tests)
yarn test

# Lint with auto-fix
yarn lint

# Run documentation locally
yarn watch:doc        # docsify serve
```

## Architecture

**Plugin System** (`packages/plugin-basic/src/`):
- `inline/` - Inline formatting plugins (bold, italic, etc.)
- `block/` - Block-level plugins (paragraphs, headings, lists)
- `atom/` - Atom-level nodes (images, links)
- `extension/` - Extended functionality plugins

**Adapter Core** (`packages/adapter/src/`):
- `basic/` - Controllers for plugins (keymap, lifecycle, decorations, text-shortcut)
- `command/` - Node mapping and command definitions
- `schema/` - Prosemirror schema extensions
- `configurator.ts` - Editor configuration management

**Dependencies**:
- Core: ProseMirror (state, view, model, transform, keymap, commands, history)
- React: react, react-dom, react-modal, emoji-mart
- Utils: lodash (debounce, throttle, cloneDeep, isEqual, merge)

## Development Notes

- Tests run in a Puppeteer-controlled Chromium browser environment
- Editor is initialized via `SylEditorService.init(dom, config)` where config includes plugins, modules, event handlers, and transaction hooks
- Plugins extend functionality through controllers in the adapter layer
- Build outputs three formats: ES modules, CommonJS, and UMD (via Vite)