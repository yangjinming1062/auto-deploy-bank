# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run full test suite (includes linting and README validation)
npm test

# Run tests only, without linting
npm run tests-only

# Run a single test file
npx tape 'test/parse.js'

# Run linting
npm run lint

# Build browserify bundle for dist/
npm run dist

# Validate README.md (checks code examples)
npm run readme
```

## Architecture

**qs** is a querystring parsing and stringifying library with support for nested objects, arrays, and security-focused depth limits.

### Source Structure

- **lib/index.js** - Main entry point; exports `{ formats, parse, stringify }`
- **lib/parse.js** - Parses querystrings into nested objects. Handles bracket notation `foo[bar]=baz`, dot notation, array syntax, and charset detection. Uses `side-channel` pattern to track array overflow objects (when indices exceed `arrayLimit`).
- **lib/stringify.js** - Converts objects back to querystrings. Recursively traverses objects with cyclic reference detection via side-channel. Supports multiple array formats (`indices`, `brackets`, `repeat`, `comma`).
- **lib/utils.js** - Shared utilities: `encode`/`decode` for URI encoding, `merge` for deep object merging, `compact` for removing undefined values, `combine` for array concatenation with overflow handling.
- **lib/formats.js** - Defines RFC3986 (default, uses `%20` for space) and RFC1738 (uses `+` for space) format constants with formatters.

### Key Design Patterns

1. **Side-channel tracking**: Uses `side-channel` package to track objects that overflow array limits (indices >= `arrayLimit`) without modifying the objects themselves. Functions: `markOverflow`, `isOverflow`, `getMaxIndex`, `setMaxIndex`.

2. **Options normalization**: Both `parse` and `stringify` have `normalize*Options` functions that validate and merge user options with defaults, throwing `TypeError` for invalid inputs.

3. **Depth limiting**: Parse limits nesting depth (default 5) via `splitKeyIntoSegments` to mitigate DoS attacks.

4. **Plain objects**: When `plainObjects: true`, uses `{ __proto__: null }` to avoid prototype pollution.

### Test Organization

Tests use `tape` framework with nested `t.test()` calls. Key test files:
- **test/parse.js** - Extensive parsing tests with many option combinations
- **test/stringify.js** - Stringification tests
- **test/utils.js** - Utility function tests
- **test/empty-keys-cases.js** - Edge cases for empty/missing keys

### Important Options

**Parse options**: `depth`, `arrayLimit`, `parameterLimit`, `allowPrototypes`, `plainObjects`, `charset`, `charsetSentinel`, `strictDepth`, `throwOnLimitExceeded`

**Stringify options**: `arrayFormat`, `encode`, `encodeValuesOnly`, `skipNulls`, `strictNullHandling`, `allowDots`, `serializeDate`, `sort`, `filter`