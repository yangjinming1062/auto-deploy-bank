# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`cornerstone-tools` is a medical imaging toolkit that provides a framework for creating interactive tools on top of Cornerstone.js. It includes annotation tools (length, angle, ROI measurements), segmentation tools (brushes, scissors), and navigation tools (pan, zoom, scroll). Tools leverage DICOM metadata for advanced functionality.

## Commands

```bash
# Install dependencies
npm install

# Build (runs tests, clean, version, prod build, dev build)
npm run build

# Development build with watch mode
npm run dev

# Production build only
npm run build:prod

# Run tests
npm run test

# Run single test file
npm run test:unit -- path/to/file.test.js

# Tests with coverage and codecov upload
npm run test:ci

# Lint and format code
npm run lint

# Generate API documentation
npm run docs:api

# Interactive commit (uses commitizen)
npm run commit

# Add contributor to README
npm run contributors:add
```

## Architecture

### Tool System (src/tools/)

All tools inherit from base classes in `src/tools/base/`:
- **BaseTool**: Abstract parent for all tools; defines tool lifecycle, modes, and strategy pattern
- **BaseAnnotationTool**: Extends BaseTool for annotation tools with handles and data storage
- **BaseBrushTool**: Extends BaseTool for segmentation brush tools

**Tool lifecycle callbacks**:
- `preMouseDownCallback` / `postMouseDownCallback`: Handle mouse button presses
- `mouseDragCallback`: Handle drag operations
- `mouseMoveCallback`: Handle cursor movement
- `touchDragCallback` / `touchStartCallback` / `touchEndCallback`: Touch interactions
- `keyboardCallback`: Keyboard shortcuts

**Strategy pattern**: Tools can switch behaviors at runtime via `setActiveStrategy()`. Strategies are named functions stored in `this.strategies`.

**Tool modes**:
- `disabled`: Tool is registered but inactive
- `passive`: Tool is active but doesn't consume events
- `enabled`: Tool is active and consumes relevant events
- `active`: Tool exclusively handles all events on the element

**Tool types**:
- `src/tools/annotation/`: AngleTool, ArrowAnnotateTool, BidirectionalTool, CircleRoiTool, EllipticalRoiTool, FreehandRoiTool, LengthTool, ProbeTool, RectangleRoiTool, TextMarkerTool
- `src/tools/segmentation/`: BrushTool, SphericalBrushTool, CircleScissorsTool, RectangleScissorsTool, FreehandScissorsTool, CorrectionScissorsTool
- `src/tools/`: Navigation and utility tools (PanTool, ZoomTool, RotateTool, WwwcTool, StackScrollTool, etc.)

### State Management

**Tool state managers** (src/stateManagement/):
- `imageIdSpecificStateManager`: Stores state per image ID
- `stackSpecificStateManager`: Stores state per stack of images
- `frameOfReferenceStateManager`: Stores state per frame of reference (volumetric data)

**Store modules** (src/store/):
- `globalConfiguration`: Global settings via `getModule('globalConfiguration')`
- `textStyle`, `toolStyle`, `toolColors`: Styling configuration
- `toolCoordinates`: Current mouse/touch position on canvas

### Initialization (src/init.js, src/index.js)

Call `cornerstoneTools.init()` to initialize the library. This sets up event listeners and the global store. The main entry point exports all tools and utilities as both default and named exports.

### Event Handling (src/eventDispatchers/, src/eventListeners/)

Events flow:
1. Raw DOM events → cornerstone-core normalizes them
2. Event listeners in `src/eventListeners/` re-emit as `cornerstonetools*` prefixed events
3. Event dispatchers route events to appropriate tool callbacks based on tool mode and priority

### External Modules (src/externalModules.js)

The library uses `external.cornerstone` to access the peer dependency `cornerstone-core`. This pattern allows the consuming application to inject its configured cornerstone instance via `cornerstoneTools.external.cornerstone = cornerstone`.

### Utilities (src/util/)

Specialized modules for:
- `src/util/ellipse/`: Ellipse calculations and point-in-ellipse tests
- `src/util/freehand/`: Freehand line rendering and hit testing
- `src/util/segmentation/`: Brush stroke handling, flood fill, shape operations
- `src/util/zoom/`: Viewport scale management

### Mixins (src/mixins/)

Reusable tool behaviors applied via the `mixins` configuration property:
- `activeRenderMixin`: Renders tool data when active
- `segmentationMixin`: Common segmentation brush behaviors
- `boundaryMixin`, `paginationMixin`: Handle manipulation

### Synchronization (src/synchronization/)

Synchronizers link state across multiple viewports:
- `wwwcSynchronizer`: Window/level presets
- `stackScrollSynchronizer`: Stack navigation
- `panZoomSynchronizer`: Pan/zoom state
- `Synchronizer`: Base class for custom synchronizers

## Code Style

- Uses ES6 modules with both named and default exports
- JSDoc documentation required for public APIs (processed by docma)
- Prettier formatting enforced via husky pre-commit hooks
- ESLint configuration in `.eslintrc.js`
- Tests use Jest with `jsdom` environment, co-located as `[FileName].test.js`

## Peer Dependencies

- `cornerstone-core`: ^2.6.0 (core rendering library)
- `cornerstone-math`: 0.1.10 (math utilities)
- `hammerjs`: Touch event support