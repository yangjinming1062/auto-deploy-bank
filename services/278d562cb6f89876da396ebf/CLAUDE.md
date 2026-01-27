# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LiveScript is a functional programming language that compiles to JavaScript. This is the self-hosted compiler written in LiveScript itself. The project uses a Make-based build system and Jison for parsing.

## Build Commands

- **Build**: `make build` - Compiles all `.ls` files in `src/` to `.js` in `lib/`, generates parser
- **Build browser version**: `make build-browser` - Creates `browser/livescript.js` and minified version
- **Force rebuild**: `make force` - Full rebuild with `-B` flag
- **Run tests**: `make test` or `npm test`
- **Test coverage**: `make coverage` - Generates coverage reports with Istanbul
- **Full development cycle**: `make full` - Forces build twice, runs tests, and generates coverage
- **Install globally**: `make install` - Builds and installs via `npm install -g .`
- **Dev install**: `make dev-install` - Installs dependencies after building `package.json`
- **Clean**: `make clean` - Removes all generated files and build artifacts
- **Count source lines**: `make loc` - Shows line count for source files

**Note**: `package.json` is generated from `package.json.ls` - edit the `.ls` file and run `make package.json`.

## Architecture

The compiler follows a classic pipeline architecture:

```
Source Code → Lexer (src/lexer.ls) → Token Stream
                ↓
            Parser (Jison) → AST (src/ast.ls)
                ↓
         Code Generator → JavaScript Output
```

### Key Components

- **Lexer** (`src/lexer.ls`): Tokenizes input code into a stream of tagged tokens. Includes a `rewrite` method that performs multiple transformation passes to handle implicit syntax (indentation, parentheses, braces).

- **Grammar** (`src/grammar.ls`): Jison grammar definitions. Used by `scripts/build-parser` to generate `lib/parser.js`. Defines how tokens are combined into AST nodes.

- **AST** (`src/ast.ls`): Contains all node classes for the abstract syntax tree. Each node has `compile` methods that generate JavaScript code using `SourceNode` for source map support.

- **Main Entry** (`src/index.ls`): Exposes the public API (`compile`, `run`, `tokens`, `ast` functions).

- **CLI** (`src/command.ls`): Command-line interface for the `lsc` executable.

- **Node Integration** (`src/node.ls`): Node.js module loading support (enables `require` for `.ls` files).

### Source vs Generated Files

- **Source**: All `.ls` files in `src/` and `package.json.ls`
- **Generated**: All `.js` files in `lib/`, `lib/parser.js`, `package.json`

Never edit generated files directly - they are overwritten on build.

## Testing

Tests are written in LiveScript in `test/` directory. The custom test runner (`scripts/test`):

1. Compiles and runs each `test/*.ls` file using `LiveScript.run()`
2. Tests use global assertion functions (`ok`, `eq`, `throws`) and helpers (`compileThrows`, `commandEq`)
3. Async tests are conditionally skipped based on Node.js version features

## Important Notes

- The `pretest` script runs `make force` twice to ensure a clean build state
- The `posttest` script restores `lib/` to git state after tests (prevents dirty working directory)
- Source maps are supported with options: `'none'`, `'embedded'`, `'linked'`, `'debug'`
- The language uses `prelude-ls` for functional programming utilities