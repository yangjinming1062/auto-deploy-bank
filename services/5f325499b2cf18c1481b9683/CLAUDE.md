# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Lospec Pixel Editor is a **deprecated** browser-based pixel art creation tool. It is no longer in active development. The codebase is a vanilla JavaScript application with a custom Gulp-based build system.

**Note**: Before contributing, open an issue for discussion. Use the `bug-fixes` branch for bug fixes and `new-feature` branch for new features.

## Development Commands

```bash
# Install dependencies (requires npm 7+, use nvm if needed)
npm install

# Build the application (outputs to ./build/)
npm run build

# Serve the built app on port 3000
npm run serve

# Build and serve (full test cycle)
npm test

# Hot reload development - rebuilds on file changes and opens browser
npm run hot

# Hot reload with automatic browser refresh (may steal focus)
npm run hot:reload
```

## Architecture

### Build System
- **build.js**: Custom Gulp build pipeline that compiles:
  - `js/pixel-editor.js` + gulp-include modules → `build/pixel-editor.js`
  - Handlebars templates (`views/`) → `build/index.htm`
  - SCSS files (`css/`) → `build/pixel-editor.css`
  - Copies images and assets to `build/`

- **server.js**: Express server serving the built application with optional hot reload via the `reload` module.

### Frontend Structure
- **js/**: Core editor logic, organized by functionality:
  - **tools/**: Tool implementations (Brush, Eraser, Line, Rectangle, Ellipse, Fill, EyeDropper, Pan, Zoom, Selection tools)
  - **layers/**: Layer classes (Layer, Checkerboard, PixelGrid)
  - **EditorState.js**: Centralized state management for the document
  - **ToolManager.js**: Global tool management (attached to `window`)
  - **FeatureToggles.js**: Feature flag system using localStorage

- **views/**: Handlebars templates:
  - `index.hbs`: Main template
  - **components/**: Reusable UI components
  - **popups/**: Modal dialog templates

- **css/**: SCSS partials (prefixed with `_`) compiled to CSS

- **helpers/**: Handlebars helpers for templates (e.g., `svg.js`)

### Key Patterns

**JavaScript Module Inclusion**: Uses `gulp-include` with comment syntax:
```javascript
//=include ToolManager.js
//=include tools/BrushTool.js
```

**Tool System**: Tools inherit from base classes:
- `Tool` → `DrawingTool` → specific tools (Brush, Eraser, etc.)
- `Tool` → `SelectionTool` → selection tools (Rectangular, Lasso, etc.)

**Global Objects**: Core modules are designed for global access:
- `EditorState`: Current document state
- `ToolManager`: Active tool management
- `FileManager`: File I/O operations
- `PaletteManager`: Color palette handling

### URL Routing
The editor supports deep linking for pre-loading palettes:
```
/pixel-editor/{palette-slug}/{width}x{height}
```
Fetches palette from Lospec's API and creates a new document with those dimensions.

## Linting

ESLint configuration enforces:
- 4-space indentation
- Single quotes
- Mandatory semicolons
- ES2018 syntax

Run with: `npx eslint .`