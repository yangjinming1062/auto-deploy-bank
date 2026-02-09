# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

jsPDF is a JavaScript library for generating PDF documents in the browser and Node.js. It implements parts of the PDF 1.3 specification and supports multiple output formats (UMD, ES modules, CommonJS).

## Build Commands

```bash
# Install dependencies
npm install

# Build the library (produces dist/ with UMD, ES, and Node bundles)
npm run build

# Run local development server for examples
npm start

# Format code with Prettier
npm run prettier

# Check code formatting (lint)
npm run lint

# Generate JSDoc documentation
npm run generate-docs
```

## Testing

```bash
# Run only unit tests (browser-based via Karma)
npm run test-unit

# Run only Node.js tests (Jasmine)
npm run test-node

# Run all tests (unit, node, amd, esm, globals, typescript, webworker)
npm run test-local

# Full CI test (builds first, then runs all tests)
npm run test

# Check TypeScript typings
npm run test-typings

# Generate new reference PDFs for tests (run in background)
npm run test-training
```

**Note:** Uses `yarpm` internally to support both yarn and npm.

## Architecture

**Entry point:** `src/index.js` - exports the jsPDF class and imports all feature modules.

**Core:**
- `src/jspdf.js` - Main jsPDF class (~180KB)
- `src/modules/` - Feature modules (imported side-effects in index.js):
  - `addimage.js` - Image support (PNG, JPEG, GIF, BMP, WebP)
  - `acroform.js` - PDF form support
  - `html.js` - HTML to PDF via html2canvas
  - `ttfsupport.js` / `utf8.js` - Unicode/font support
  - `context2d.js` - Canvas 2D API implementation
  - Plus: annotations, arabic, canvas, cell, filters, split_text_to_size, etc.

**Libraries:** `src/libs/` - External-like dependencies (bidiEngine, ttffont)

**Types:** `types/index.d.ts` - TypeScript definitions

**Tests:**
- `test/specs/` - Unit test specs matching module names
- `test/deployment/` - Module format tests (AMD, ESM, globals, TypeScript, webworker)
- `test/reference/` - Reference PDF files for comparison

## Key Concepts

- **API modes:** Use `doc.advancedAPI()` and `doc.compatAPI()` to switch between advanced features (patterns, FormObjects) and legacy compat mode.
- **Polyfills:** `src/polyfills.js` - required polyfills for older browsers; `dist/polyfills.es.js` and `dist/polyfills.umd.js` are built separately.
- **Optional dependencies:** canvg, dompurify, html2canvas are loaded dynamically when features are used.
- **Build output:** Three formats are built to `dist/`: ES modules (modern browsers), UMD (script tag/AMD), CommonJS (Node.js).