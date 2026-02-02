# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mixly is a visual block-based programming tool for hardware coding (similar to Scratch for Arduino, MicroPython, and Python). It supports multiple programming environments and hardware boards.

## Build Commands

```bash
# Install dependencies
npm install

# Lint board source code
npm run boards:lint

# Run tests (static server + deps generation)
npm test  # or npm start

# Start static file server
npm run static

# Build boards (outputs to boards/default/)
npm run build:boards:all        # Build all boards
npm run build:boards:arduino    # Build only Arduino boards
npm run build:boards:micropython # Build only MicroPython boards
npm run build:boards:python     # Build only Python boards

# Publish boards to npm registry
npm run publish:boards:all
```

Each board can also be built individually (navigate to board directory):
```bash
cd boards/default_src/<board-name>
npm run serve      # Dev server with hot reload
npm run build:dev  # Development build
npm run build:prod # Production build
```

## Architecture

### Core Structure
- **`main.js`** - Electron main process (handles app lifecycle, window management, USB detection, IPC)
- **`index.html`** - Web entry point, loads lazyload.js and main.js
- **`common/`** - Shared core modules (Blockly, UI components, CSS, messages, templates)
- **`boards/`** - Board definitions with source (`default_src/`) and built output (`default/`)
- **`boards.json`** - Registry of all available boards with metadata

### Board System
Each board (e.g., `arduino_avr`, `micropython_esp32`) follows this structure:
- **`index.js`** - Board entry point, imports blocks and generators
- **`config.json`** - Board configuration (processors, upload settings, serial config, libraries)
- **`blocks/`** - Block definitions for the visual programming blocks
- **`generators/`** - Code generators that translate blocks to target language
- **`template.xml`** - Blockly toolbox configuration
- **`origin/`** - Static assets to copy to output (images, examples)

Board packages are published to npm under the `@mixly/*` namespace (e.g., `@mixly/arduino-avr`).

### Module Loading
- **`common/deps.json`** - Declares module dependencies and load order
- **`common/modules/`** - Web modules (Ace editor, Monaco, esptool, etc.)
- **`common/blockly-core/`** - Blockly core and plugins

### Key Dependencies
- **Blockly** - Visual programming framework
- **Electron** - Desktop application framework
- **layui** - UI component library
- **Ace/Monaco** - Code editors

### Environment Modes
- **Electron** - Desktop app with full hardware access
- **Web** - Browser-based version with limited capabilities
- **WebSocket** - Remote compilation/flash via server

## Code Style

ESLint configuration in `.eslintrc.js`:
- 4-space indentation
- ES6+ syntax
- Extends `eslint:recommended`

## Language Conventions

- Code comments are primarily in Chinese
- Module naming: `Mixly.<ModuleName>` pattern
- Block definitions use `Blockly.Blocks.<name>` and `Blockly.<Language>.forBlock`