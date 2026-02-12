# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**qs** is a querystring parsing and stringifying library with support for nesting, arrays, and security features like depth limits. It parses query strings into objects and stringifies objects into URL query strings.

## Build Commands

```bash
npm test              # Run full test suite with linting and coverage
npm run tests-only    # Run tests without linting
npm run lint          # Run ESLint on codebase
npm run dist          # Build browser bundle (outputs to dist/qs.js)
npm run readme        # Validate README.md with evalmd
```

To run a single test file or test case:
```bash
npx tape test/parse.js
npx tape test/parse.js -f "test name pattern"  # Run specific test
```

## Architecture

The library uses CommonJS (`'use strict'`) and has a simple modular structure:

- **lib/index.js** - Main entry point that exports `parse`, `stringify`, and `formats`
- **lib/parse.js** - Query string parsing with support for nested objects, arrays, and various options. Key functions:
  - `parseValues()` - Splits query string and handles delimiters
  - `splitKeyIntoSegments()` - Parses bracket notation into key segments
  - `parseObject()` - Recursively builds nested objects from parsed segments
  - `parseKeys()` - Main parsing orchestrator
- **lib/stringify.js** - Object to query string conversion with:
  - Cyclic reference detection using `side-channel` to prevent infinite loops
  - `arrayPrefixGenerators` for different array formats (`indices`, `brackets`, `repeat`, `comma`)
  - Recursive stringification with depth tracking
- **lib/utils.js** - Shared utilities:
  - `merge()` - Deep merging with overflow tracking for arrays exceeding `arrayLimit`
  - `encode()`/`decode()` - RFC 3986/RFC 1738 URL encoding
  - `compact()` - Removes `undefined` values from nested structures
  - `isOverflow()`/`markOverflow()` - Track arrays that exceeded `arrayLimit` (converted to objects)
- **lib/formats.js** - Encoding format constants (RFC3986, RFC1738) and formatters

## Key Security Features

- **Depth limiting** (default 5): Prevents deep object DoS attacks via `strictDepth` option
- **Array limiting** (default 20): High indices become object keys instead of array elements
- **Parameter limiting** (default 1000): Prevents large query string DoS attacks
- **Prototype pollution protection**: Ignores `__proto__` and prototype properties by default

## Code Style

- 4-space indentation
- ESLint config extends `@ljharb/eslint-config` with some overrides
- No `break` statements (use `return` or structured control flow instead)
- Custom `has` variable for `Object.prototype.hasOwnProperty` to avoid reassignment