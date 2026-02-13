# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Build the compiler into built/local
npx hereby local

# Clean build outputs
npx hereby clean

# Build test infrastructure
npx hereby tests

# Run all tests (MANDATORY before finishing any changes)
npx hereby runtests-parallel

# Run only fourslash tests
npx hereby runtests --runner=fourslash

# Run only compiler tests
npx hereby runtests --runner=compiler

# Run a specific test
npx hereby runtests --tests=<testPath>

# Accept new test baselines
npx hereby baseline-accept

# Run lint (MANDATORY before finishing any changes)
npx hereby lint

# Run code formatting (MANDATORY before finishing any changes)
npx hereby format
```

## Project Overview

This is the **TypeScript compiler** repository (v6.0.0). TypeScript adds optional types to JavaScript that support tools for large-scale JavaScript applications.

### Key Directories

- **`src/compiler/`** - Core compiler components:
  - `parser.ts` - Parsing TypeScript source into AST
  - `binder.ts` - Symbol resolution and binding
  - `checker.ts` - Type checking and semantic analysis
  - `emitter.ts` - JavaScript code generation
  - `program.ts` - Entry point for compilation
  - `types.ts` - AST node type definitions

- **`src/services/`** - Language services for IDE integration:
  - `completions.ts` - IntelliSense completions
  - `goToDefinition.ts` - Definition lookup
  - `findAllReferences.ts` - Find references
  - `refactorProvider.ts` - Code refactoring support
  - `services.ts` - Core language service interface

- **`src/server/`** - tsserver implementation (language server protocol)

- **`src/tsc/`** - tsc CLI entry point

- **`src/harness/`** - Test harness and FourSlash test framework

- **`src/lib/`** - Standard library type definitions (lib.d.ts, etc.)

- **`tests/cases/`** - Test cases:
  - `compiler/` - Compiler behavior tests
  - `fourslash/` - IDE/language service tests
  - `conformance/` - ECMAScript spec compliance tests

### Build Outputs (in `built/local/`)

- `tsc.js` - Command-line compiler
- `typescript.js` - Library for external consumption
- `tsserver.js` - Language server
- `tsserverlibrary.js` - tsserver as a library
- `typingsInstaller.js` - npm typings installer

## Code Conventions

- **Line endings**: CRLF (Windows-style) - do not change
- **Indentation**: 4 spaces, no tabs
- **Quotes**: Prefer double quotes
- **Semicolons**: Always required

Run `npx hereby format` before committing to enforce formatting.

## Test System

Tests use **baseline comparison** - expected outputs are stored in `tests/baselines/reference/`. When tests run, outputs go to `tests/baselines/local/`. Compare differences with:

```bash
git diff --diff-filter=AM --no-index ./tests/baselines/reference ./tests/baselines/local
```

After verifying baselines are correct, run `npx hereby baseline-accept` to update reference baselines.

### FourSlash Test Syntax

```typescript
/// <reference path='fourslash.ts'/>

////code goes here with /*markers*/

// Navigate to markers
goTo.marker("markerName");
goTo.marker(); // anonymous marker

// Multi-file tests
// @Filename: /a.ts
////export const value = 42;

// @Filename: /b.ts
////import { value } from './a';

// Verification (prefer over baselines)
verify.completions({ includes: "itemName" });
verify.quickInfoIs("expected info");
```

## Debugging Tips

```typescript
// Print node kind as symbolic name
console.log(`Got node with kind = ${SyntaxKind[n.kind]}`);
```

## Important Notes

- All code changes should go to https://github.com/microsoft/typescript-go - this codebase is in maintenance mode
- Development in this repo is only for critical 6.0 bug fixes
- Tests in `tests/cases/compiler/` must have `.ts` extension, not `.d.ts`
- Do not write direct unit tests - use compiler or FourSlash tests instead
- Development is winding down - PRs will only be merged for critical issues