# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Webpack is a module bundler for JavaScript applications. It processes applications and recursively builds a dependency graph that includes every module needed, then packages all those modules into one or more bundles.

## Common Commands

### Setup
```bash
yarn setup           # Install dependencies and set up the project
yarn link            # Link webpack globally
```

### Development
```bash
yarn fmt             # Format code with Prettier
yarn fix             # Run all fixers (eslint --fix, formatting, code generation)
```

### Linting
```bash
yarn lint            # Run all linters (eslint, types, schemas, spellcheck)
yarn lint:code       # Run ESLint on source code
yarn lint:types      # TypeScript type checking
yarn lint:spellcheck # Spell checking
```

### Testing
```bash
yarn test            # Run full test suite (requires passing lint first)
yarn test:unit       # Run unit tests only
yarn test:integration # Run integration tests only
yarn test:basic      # Run basic tests only
yarn test:base path/to/test.js --watch  # Run specific test in watch mode
yarn test:update-snapshots  # Update Jest snapshots
```

### Performance
```bash
yarn benchmark       # Run performance benchmarks
```

### Examples
```bash
yarn build:examples  # Build all example projects
```

## Architecture

### Core Entry Points
- `lib/index.js` - Main entry point exporting public API
- `lib/webpack.js` - Core webpack function and plugin interfaces
- `bin/webpack.js` - CLI entry point

### Key Compilation Flow

1. **Compiler** (`lib/Compiler.js`) - The main orchestration class that coordinates the build process
2. **Compilation** (`lib/Compilation.js`) - Manages the module/chunk graph and assets
3. **Module Factories** (`lib/NormalModuleFactory.js`, `lib/ContextModuleFactory.js`) - Create module instances from dependencies
4. **Resolvers** (`lib/ResolverFactory.js`, `lib/enhanced-resolve`) - Resolve module paths and requests
5. **Parsers** (`lib/javascript/Parser.js`) - Parse source code into AST and extract dependencies
6. **Generators** (`lib/javascript/JavascriptGenerator.js`, `lib/json/JsonGenerator.js`) - Generate code from modules
7. **Chunk Graph** (`lib/ChunkGraph.js`) - Organize modules into chunks for code splitting
8. **Templates** (`lib/ChunkTemplate.js`, `lib/MainTemplate.js`, `lib/ModuleTemplate.js`) - Generate bundle output

### Module System
- **Module types**: javascript, json, wasm, css, asset, etc.
- **Module subclasses**: `NormalModule`, `ContextModule`, `RawModule`, `ExternalModule`, `DllModule`, `CssModule`
- **Dependency types**: `SingleEntryDependency`, `HarmonyImportDependency`, `ContextDependency`, etc.

### Plugin System
- Uses Tapable hook system for plugin extension points
- Built-in plugins in `lib/` (e.g., `EntryPlugin`, `DllPlugin`, `HotModuleReplacementPlugin`)
- Plugin schemas in `schemas/plugins/`

### Configuration
- Options defined in `declarations/WebpackOptions.d.ts`
- JSON schemas in `schemas/WebpackOptions.json`
- Defaults in `lib/WebpackOptionsDefaulter.js`
- Applied via `lib/WebpackOptionsApply.js`

### Runtime
- Runtime modules in `lib/runtime/` (e.g., `CommonJsChunkLoadingRuntime`, `ESMChunkLoadingRuntime`)
- Hot update runtime in `hot/` and `lib/hmr/`
- Runtime globals defined in `lib/RuntimeGlobals.js`

### Utilities
- `lib/util/` - General utilities (memoize, identifiers, fs, etc.)
- `lib/util/semver.js` - Generated file for version matching

## Test Structure

| Directory | Purpose |
|-----------|---------|
| `test/cases/` | General integration test cases |
| `test/configCases/` | Configuration-specific test cases (require webpack.config.js) |
| `test/statsCases/` | Stats output test cases using snapshots |
| `test/hotCases/` | Hot Module Replacement test cases |
| `test/watchCases/` | Watch mode test cases |
| `test/benchmarkCases/` | Performance benchmark cases |
| `test/*.test.js` | Test suite runners (Jest) |
| `test/*.unittest.js` | Unit tests for specific modules |

## Code Style

- **Formatting**: Prettier (configured via `.prettierrc.js`)
- **Linting**: ESLint with custom webpack config (`eslint.config.mjs`)
- **Types**: JSDoc annotations with TypeScript definitions
- **Naming**: PascalCase for classes, camelCase for functions/variables
- **Exceptions**: Variables prefixed with `_` are intentionally unused

## Type Generation

Types are auto-generated from JSDoc comments. After adding new public types:
1. Run `yarn fix` to regenerate `types.d.ts`
2. Commit both the source change and the generated types

## Module Format

Webassembly modules in `assembly/` are compiled using AssemblyScript. Build with:
```bash
node tooling/generate-wasm-code.js
```