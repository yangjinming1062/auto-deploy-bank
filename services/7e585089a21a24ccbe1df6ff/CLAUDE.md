# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Genkit is an open-source, multi-language AI framework for building full-stack AI-powered applications. The codebase is structured as a monorepo with:

- **JavaScript/TypeScript** (production-ready): Primary implementation in `/js`
- **Go** (production-ready): Implementation in `/go`
- **Python** (Alpha): Early implementation in `/py`
- **Developer Tools**: CLI and Developer UI in `/genkit-tools`

The JavaScript/TypeScript implementation is the most complete and includes `@genkit-ai/core` (core framework), `@genkit-ai/ai` (AI abstractions), and `genkit` (main package).

## Development Setup

### Prerequisites
- Node.js 20 or later
- pnpm (run `corepack enable pnpm` to install)
- Go 1.24+ (for Go development)
- Genkit CLI: `npm install -g genkit-cli`

### Initial Setup
```bash
pnpm i
pnpm run setup
```
This installs dependencies and builds all packages.

### Build Commands
```bash
pnpm build              # Build all packages
pnpm build:js           # Build JavaScript packages only
pnpm build:genkit-tools # Build CLI/UI tools only
pnpm build:watch        # Watch mode (run in specific package)
```

### Formatting & Linting
```bash
pnpm format             # Format with Prettier + add copyright headers
pnpm format:check       # Check formatting
pnpm format:biome       # Format with Biome
pnpm format:biome-check # Check Biome formatting
pnpm lint:biome         # Lint and fix with Biome
```

Biome configuration is in `biome.json` with 80-character line width, single quotes, and organized imports.

### Testing
```bash
pnpm test:all                    # Test all packages
pnpm test:js                     # Test JavaScript packages
pnpm test:genkit-tools-cli       # Test CLI tools
pnpm test:genkit-tools-common    # Test genkit-tools common
pnpm test:e2e                    # End-to-end tests
pnpm test:e2e-local              # Build, pack, then run e2e tests
```

Test files use Node's test runner with `tsx` for imports:
```bash
cd js/genkit && node --import tsx --test tests/flow_test.ts
```

### Packing for Distribution
```bash
pnpm pack:all      # Create tarballs in dist/
pnpm pack:js       # Pack JS packages
pnpm pack:tools    # Pack genkit-tools
```

## Code Architecture

### JavaScript/TypeScript Structure

**Core Framework** (`/js/core/`):
- `registry.ts` - Registration system for flows, actions, and model providers
- `flow.ts` - Flow abstraction for AI workflows
- `action.ts` - Action system for tool execution
- `reflection.ts` - Reflection API for Developer UI integration
- `tracing/` - Distributed tracing infrastructure
- `schema.ts` - Schema validation using Zod

**AI Layer** (`/js/ai/`):
- Abstract interfaces for AI operations (generate, embed, retrieve, etc.)
- Pluggable model provider architecture
- Format and extraction handlers

**Main Package** (`/js/genkit/`):
- `genkit.ts` - Main Genkit initialization and entry point
- `index.ts` - Exports all public APIs
- `model.ts` - Model abstraction layer
- `tool.ts` - Tool definition and execution
- `retriever.ts` - Retrieval systems (RAG)
- `embedder.ts` - Text/image embedding
- `evaluator.ts` - AI output evaluation
- `tracing.ts` - Tracing integration
- `context.ts` - Context management
- `testing.ts` - Testing utilities

**Plugins** (`/js/plugins/`):
- Provider plugins (Google, OpenAI, Anthropic, Ollama, etc.)
- Integration plugins (Vertex AI, Firebase, etc.)

### Development Workflow

1. **Make changes** to source files in `/js/genkit/src/`, `/js/core/src/`, or `/js/ai/src/`

2. **Build** the affected package:
   ```bash
   cd js/genkit && pnpm build
   # or watch mode
   pnpm build:watch
   ```

3. **Test changes** using a test app:
   ```bash
   cd js/testapps/flow-sample1
   genkit start -- tsx --watch src/index.ts
   # Open http://localhost:4000 for Developer UI
   ```

4. **Run tests** to verify changes:
   ```bash
   pnpm test:js
   # or specific test
   cd js/genkit && node --import tsx --test tests/flow_test.ts
   ```

5. **Format and lint** before committing:
   ```bash
   pnpm format:biome-check
   pnpm lint:biome
   ```

### Key Concepts

- **Flows**: The primary abstraction for AI workflows (similar to serverless functions)
- **Actions**: Executable units that can be called by flows (tools/functions)
- **Models**: Abstracted AI model providers with unified interface
- **Reflection API**: HTTP API that Developer UI uses to discover and execute flows
- **Tracing**: Distributed tracing for debugging complex AI flows
- **Middleware**: Request/response processing pipeline

### Go Development

Go code follows similar patterns:
```bash
cd go/samples/<sample-name>
go mod tidy
genkit start -- go run .
```

### Python Development

Python support is in Alpha:
```bash
cd py/samples/<sample-name>
pip install -e .
genkit start -- python main.py
```

## Developer UI

The Developer UI provides a local interface for testing and debugging:

- Access at http://localhost:4000 when running `genkit start -- <command>`
- **Run tab**: Execute flows with different inputs
- **Traces tab**: Inspect detailed execution traces
- **Evaluations tab**: View evaluation results
- Automatically discovers flows via the Reflection API

## Common Tasks

### Adding a New Flow
```typescript
import { genkit, z } from 'genkit';

export const myFlow = genkit.defineFlow({
  name: 'myFlow',
  inputSchema: z.string(),
  outputSchema: z.string(),
}, async (input) => {
  // Flow implementation
  return result;
});
```

### Creating a Tool
```typescript
import { tool } from 'genkit';

export const myTool = tool({
  name: 'myTool',
  description: 'What this tool does',
  inputSchema: z.object({...}),
  outputSchema: z.object({...}),
}, async (input) => {
  // Tool implementation
  return output;
});
```

### Registering a Model Provider
```typescript
import { ModelReference } from '@genkit-ai/core';

export const myModel: ModelReference<...> = {
  name: 'myModel',
  // Model configuration
};
```

## Package Structure

- `/js/genkit` - Main Genkit package, re-exports from core/ai
- `/js/core` - Core framework (registry, flows, actions, tracing)
- `/js/ai` - AI abstractions (generate, embed, retrieve, tools)
- `/js/plugins` - Provider integrations (Google, OpenAI, etc.)
- `/js/testapps` - Test applications demonstrating features
- `/genkit-tools/cli` - Genkit CLI commands
- `/genkit-tools/common` - Shared tooling for CLI/UI
- `/genkit-tools/telemetry-server` - Local telemetry collection
- `/tests` - End-to-end integration tests
- `/samples` - Multi-language sample applications

## Important Files

- `biome.json` - Biome configuration for JS/TS
- `.prettierrc.yaml` - Prettier configuration for non-TS files
- `js/tsconfig.json` - TypeScript configuration
- `js/tsup.common.ts` - Tsup bundler configuration
- `captainhook.json` - Pre-commit hook configuration
- `pnpm-workspace.yaml` - PNPM workspace configuration

## Build Outputs

Build output goes to `lib/` directory in each package:
- `lib/cjs/` - CommonJS modules
- `lib/esm/` - ES modules
- `lib/index.d.ts` - TypeScript definitions

The `genkit` package re-exports from `@genkit-ai/core` and `@genkit-ai/ai` packages.

## Tips

- Always build before testing to ensure TypeScript compilation passes
- Use `genkit start -- <command>` to wrap any command with the Developer UI
- Tests use Node's native test runner, not Jest
- Copyright headers are automatically added by `tsx scripts/copyright.ts`
- The Developer UI requires the Reflection API server running on port 4000
- When making breaking changes, update version in relevant `package.json` files