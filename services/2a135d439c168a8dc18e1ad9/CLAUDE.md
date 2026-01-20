# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Development with watch mode (runs both extension and client compilation in parallel)
npm run dev

# Production build (webpack)
npm run build

# Lint source code
npm run lint

# Check prettier formatting
npm run lint-format

# Fix prettier formatting
npm run prettier-fix

# Run integration tests
npm test

# Create VSIX package for distribution
npm run package
```

## Architecture Overview

This is a VS Code extension that provides Node.js notebook support (`.nnb` files). The architecture consists of two main components communicating via WebSocket:

### VS Code Extension (`src/extension/`)

The extension handles notebook lifecycle, cell execution orchestration, and output rendering:

- **Kernel Management** (`kernel/`): `JavaScriptKernel` spawns a node-kernel subprocess and communicates via WebSocket. `Controller` registers notebook controllers for node-notebook and interactive window types. `CellExecutionQueue` manages sequential cell execution.

- **TypeScript Compilation** (`kernel/compiler.ts`): Transpiles cell code using TypeScript API, generates source maps, and wraps code for top-level await support. Handles variable hoisting issues and source map translation for debugging.

- **Debugging** (`kernel/debugger/`): Integrates with VS Code debugger protocol. `DebuggerFactory` manages debug sessions attached to the kernel's debug port.

- **Server Components** (`server/`): Runs in the kernel subprocess. `codeExecution.ts` is the core executor using Node's `vm.runInNewContext` and REPL. Formatters for rich output (`danfoFormatter.ts`, `arqueroFormatter.ts`, `tfjsVisProxy.ts`, `plotly.ts`) transform data structures into displayable output.

- **Content Provider** (`content/`): Registers the notebook serializer and content provider for `.nnb` files.

### Node Kernel (`src/node-kernel/`)

A separate Node.js process that executes code:

- Entry point: `src/extension/server/index.ts` → compiled to `out/extension/server/index.js`
- Uses Node's `vm` module for sandboxed code execution
- Intercepts module loads to inject formatters and utilities
- Handles `node-kernel` pseudo-module that exposes `display` API to user code

### Client Renderers (`src/client/`)

Webview-based output renderers for notebook cells:

- `plotGenerator.ts`: Renders Plotly charts (`application/vnd.ts.notebook.plotly+json`)
- `tfvis.ts`: Renders TensorFlow.js visualizations (`application/vnd.tfjsvis` MIME types)

## Notebook Cell Execution Flow

1. User runs a cell in VS Code
2. `Controller.executeHandler` queues cell in `CellExecutionQueue`
3. `JavaScriptKernel.runCell` compiles cell code (TypeScript → JavaScript with source maps)
4. Compiled code sent via WebSocket to node-kernel subprocess
5. Kernel's `codeExecution.ts` executes via `vm.runInNewContext` with REPL
6. Output streams back through stdout/stderr → WebSocket → `CellOutput`
7. Results formatted via extension formatters (danfo, plotly, etc.)
8. Renderers display rich output in notebook cells

## Key Patterns

- **WebSocket Communication**: `RequestType`/`ResponseType` messages with `requestId` correlation
- **Output Ordering**: Console output marker pattern ensures stdout appears before cell results
- **Source Maps**: Generated for TypeScript cells to enable debugging with line/column translation
- **Module Interception**: `Module._load` override injects custom formatters for danfojs, arquero, tfjs-vis
- **Disposable Registry**: Centralized tracking of VS Code disposables for cleanup

## Testing

Integration tests use `vscode-test` framework. Tests run in a headless VS Code instance. Test files are in `src/test/suite/`.