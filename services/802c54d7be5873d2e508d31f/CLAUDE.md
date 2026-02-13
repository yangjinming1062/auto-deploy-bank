# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Setup dependencies (required first)
yarn setup

# Run full test suite (includes linting)
yarn test

# Run specific test types
yarn test:unit       # Unit tests (*.unittest.js)
yarn test:basic      # Basic tests (*.basictest.js)
yarn test:integration # Integration tests
yarn test:test262    # test262 spec tests

# Run tests with watch mode
yarn test:unit --watch
yarn test:integration --watch

# Update test snapshots
yarn test:update-snapshots

# Run benchmarks
yarn benchmark

# Build examples
yarn build:examples
```

## Linting & Formatting

```bash
# Run full linting suite
yarn lint

# Run specific linters
yarn lint:code       # ESLint
yarn lint:types      # TypeScript type checking
yarn lint:special    # Schemas, codegen, tooling
yarn fmt:check       # Prettier check
yarn fmt             # Auto-format with Prettier

# Auto-fix issues
yarn fix             # Fix lint + formatting
yarn fix:code        # Fix ESLint only
```

## High-Level Architecture

Webpack is a module bundler built around a plugin architecture using [tapable](https://github.com/webpack/tapable) hooks.

### Core Compilation Flow

1. **Options Normalization** (`lib/config/normalization.js`) - Raw options → normalized form
2. **Defaults Application** (`lib/config/defaults.js`) - Apply default values
3. **Plugin System** (`lib/webpack.js:createCompiler`) - Plugins registered and applied
4. **WebpackOptionsApply** (`lib/WebpackOptionsApply.js`) - Configure built-in plugins

### Key Classes

- **Compiler** (`lib/Compiler.js`) - Orchestrates the build, manages compilation lifecycle, handles watch mode
- **Compilation** (`lib/Compilation.js`) - Represents a single build, manages modules/chunks, handles code generation
- **NormalModule** (`lib/NormalModule.js`) - Regular JS/module file handling
- **Chunk** (`lib/Chunk.js`) - Output bundle segment
- **ModuleGraph** (`lib/ModuleGraph.js`) - Dependency relationships between modules
- **ChunkGraph** (`lib/ChunkGraph.js`) - Assignment of modules to chunks

### Module Types

Located in `lib/` subdirectories:
- `javascript/` - ESM, CommonJS, AMD parsing and generation
- `json/` - JSON handling
- `css/` - CSS modules
- `asset/` - Asset modules (images, fonts, etc.)
- `wasm-*/` - WebAssembly modules
- `container/` - Module Federation
- `sharing/` - Shared modules

### Plugin System

Webpack uses **tapable** hooks throughout. Key hooks on Compiler:
- `beforeRun`, `run` - Before compilation starts
- `beforeCompile`, `compile` - Before new compilation
- `thisCompilation`, `compilation` - During compilation setup
- `emit`, `afterEmit` - Before/after output files written
- `done` - Compilation complete

Plugins implement `apply(compiler)` method and tap into hooks using `compiler.hooks.<hookName>.tap(...)`.

### Dependency Graph Build

1. **Entry Points** → `NormalModuleFactory.create()` → Create dependency graph
2. **Resolve** → `enhanced-resolve` for file resolution
3. **Parse** → Parser extracts dependencies (`require()`, `import()`) using `javascript/javascript/Parser.js`
4. **Build** → `NormalModule.build()` → Process loaders, parse, extract dependencies
5. **Process Dependencies** → Recursively process all dependencies

### Code Generation

1. **Code Generation** (`Module.codeGeneration()`) - Generate module output
2. **Chunk Graph Building** (`buildChunkGraph.js`) - Assign modules to chunks
3. **Render** (`MainTemplate`, `ChunkTemplate`) - Generate bundle runtime
4. **Output** - Write assets to filesystem

### Configuration Schema

Options are defined in `schemas/WebpackOptions.json` with TypeScript declarations in `declarations/`. Run `yarn fix` to regenerate types from JSDoc annotations.

### Key Utilities

- `lib/util/` - Async queues, maps, helpers for concurrent operations
- `lib/dependencies/` - Dependency classes for different module formats
- `lib/runtime/` - Runtime modules injected into bundles

## Testing Patterns

Tests use **Jest** with snapshot testing for output validation.

- `test/cases/` - General test cases with `webpack.config.js` fixtures
- `test/configCases/` - Configuration option tests (auto-discovered)
- `test/hotCases/` - Hot Module Replacement tests
- `test/watchCases/` - Watch mode tests
- `test/statsCases/` - Stats output tests
- `test/__snapshots__/` - Jest snapshots

Integration tests compare output against snapshots. When adding features, update snapshots with `-u`.