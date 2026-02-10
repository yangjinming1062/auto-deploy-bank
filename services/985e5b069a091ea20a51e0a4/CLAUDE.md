# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Carbone is a fast, server-side report generator that injects JSON data into XML-based templates (DOCX, XLSX, ODT, ODS, PPTX, etc.) and can convert results to PDF or other formats using LibreOffice.

## Common Commands

```bash
# Run all tests (100s timeout, exits after completion)
npm test

# Watch mode for test-driven development
make test

# Lint all JavaScript files
npm run lint

# Auto-fix linting issues
npm run lint:fix
```

## Architecture

Carbone processes templates through a multi-stage pipeline:

### Entry Point: `lib/index.js`
- Main export with `render()`, `renderXML()`, `convert()`, and `set()` methods
- Manages template loading, translation loading, and document conversion
- Initializes dayjs locale/timezone and formatters

### Core Processing Pipeline

1. **`lib/file.js`** - Opens templates (unzips OOXML formats) and builds output files
2. **`lib/parser.js`** - Finds Carbone markers (`{d.}`, `{c.}`, `{#}`, `{bindColor}`) and variable declarations in XML
3. **`lib/extracter.js`** - Parses marker syntax to extract:
   - Data paths (`d.field`, `d.array[i]`)
   - Formatters (`{d.date:formatD(dddd)}`)
   - Loop/repetition markers
   - Conditional blocks
4. **`lib/builder.js`** - Generates JavaScript functions that inject data into XML, then assembles XML parts
5. **`lib/converter.js`** - Converts documents via LibreOffice in headless mode (PDF, etc.)

### Template Markers

- `{d.path}` - Data from JSON input
- `{c.path}` - Complement data (set via options)
- `{d.array[i]}` - Array iteration with implicit repetition
- `{#var}` - Pre-declared variables
- `{d.val:formatter(args)}` - Formatted values

### Formatters (`formatters/*.js`)

Built-in formatters include date, number, string, array, and condition formatters. Custom formatters can be added via `carbone.addFormatters()`.

### Translation System (`lib/translator.js`)

Templates can include translation files in `templatePath/lang/` directory. Use `carbone.set({ lang: 'fr' })` or options `{lang: 'fr'}` to activate.

## Code Style

The project uses ESLint with specific rules:
- Single quotes for strings (with `avoidEscape`)
- Semicolons required
- Space before blocks and function parentheses
- 2-space indentation
- No console methods except `warn`, `error`, `log`

## Key Files

- `lib/params.js` - Global configuration state
- `lib/input.js` - Options parsing and formatter registry
- `lib/preprocessor.js` - XML preprocessing before rendering
- `bin/carbone` - CLI tool (`carbone translate`, `carbone find`)