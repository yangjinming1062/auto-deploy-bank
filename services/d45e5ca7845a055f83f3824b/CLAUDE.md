# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

jsPDF is a JavaScript library for generating PDF documents in the browser and Node.js. It supports multiple module formats (ESM, UMD, CommonJS), various image formats, custom fonts, encryption, and advanced PDF features.

## Common Commands

```bash
# Build the library (required before running tests)
npm run build

# Run all tests
npm run test

# Run unit tests only (fastest)
npm run test-unit

# Run full local test suite (includes deployment tests for different module formats)
npm run test-local

# Run Node.js tests only
npm run test-node

# Run linting (Prettier check)
npm run lint

# Format code with Prettier
npm run prettier

# Generate API documentation
npm run generate-docs

# Start local development server
npm start
```

## Architecture

### Source Structure

- **`src/index.js`** - Entry point that imports the core `jsPDF` class and all feature modules
- **`src/jspdf.js`** - Core jsPDF class containing the main document API, PDF generation logic, and internal utilities (PubSub, GState, Pattern classes)
- **`src/modules/`** - Feature modules that extend the jsPDF prototype (imported via `index.js`):
  - `addimage.js` - Image loading and embedding
  - `context2d.js` - Canvas-like 2D drawing API
  - `acroform.js` - PDF form support
  - `ttfsupport.js` - Custom font support
  - `html.js` - HTML-to-PDF conversion (requires html2canvas, dompurify)
  - Plus: svg, canvas, cell, annotations, outline, and more
- **`src/libs/`** - Internal utility libraries:
  - `pdfsecurity.js` - PDF encryption and permissions
  - `bidiEngine.js` - Bidirectional text support
  - `ttffont.js` - TTF font parsing
  - Image decoders (BMP, GIF, JPEG, PNG, WebP)
- **`src/polyfills.js`** - Core-js polyfills for older browsers
- **`types/index.d.ts`** - TypeScript definitions

### Build System

Uses **Rollup** with Babel transpilation. Three output formats are built:
- **ES module** (`dist/jspdf.es*.js`) - Modern browsers and bundlers
- **UMD** (`dist/jspdf.umd*.js`) - Script tags and AMD loaders
- **CommonJS** (`dist/jspdf.node*.js`) - Node.js environments

The `MODULE_FORMAT` preprocessor variable is available in source files for conditional imports.

### API Modes

jsPDF has two API modes that affect method signatures and behavior:
- **"compat"** (default) - Original MrRio API, full plugin compatibility
- **"advanced"** - yWorks fork API with patterns, FormObjects, transformation matrices

Switch modes using `doc.advancedAPI(doc => {...})` or `doc.compatAPI(doc => {...})`.

## Development Notes

- Write new code in ES6+; the build step transpiles to ES5
- When using new EcmaScript/Browser APIs, add polyfills to `src/polyfills.js`
- Update TypeScript definitions in `types/index.d.ts` when adding/modifying public APIs
- New tests go in `test/specs/` (unit tests) or `test/deployment/` (format-specific tests)
- Reference PDFs for testing are stored in the repository; new references can be generated with `npm run test-training`
- Don't commit changes to `dist/` - these are only updated during releases

## Dependencies

- **Core dependencies**: `fflate` (compression), `fast-png` (image decoding)
- **Optional dependencies** (dynamically loaded): `canvg`, `dompurify`, `html2canvas`
- These are excluded from builds via Rollup externals for the UMD format