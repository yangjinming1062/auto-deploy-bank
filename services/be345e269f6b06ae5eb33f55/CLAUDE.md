# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

LangChain.js is a TypeScript framework for building LLM-powered applications. The repository is a monorepo using pnpm workspaces and Turbo for builds, containing multiple packages:

- **`langchain-core`** (`libs/langchain-core/`): Core abstractions, schemas, and TypeScript interfaces. The foundational package that other libraries extend.
- **`langchain`** (`libs/langchain/`): High-level TypeScript bindings. Depends on `langchain-core`.
- **`langchain-community`** (`libs/langchain-community/`): Community-contributed integrations (vector stores, document loaders, tools, etc.).
- **`providers/*`** (`libs/providers/`): Individual provider packages (OpenAI, Anthropic, Google, etc.) as separate npm packages.

## Development Environment

**Prerequisites:**
- Node.js 20.x (check with `node -v`)
- pnpm v10.14.0
- Docker (for environment tests)

**Setup:**
```bash
# Install dependencies
pnpm install

# Build langchain-core first (required dependency)
cd libs/langchain-core
pnpm install
pnpm build
cd ../..
```

## Common Commands

### Building
```bash
# Build all packages
pnpm build

# Build specific package
pnpm --filter @langchain/core build

# Watch mode for development
turbo watch build:compile
# or for core specifically:
cd libs/langchain-core && pnpm dev
```

### Linting & Formatting
```bash
# Lint all packages
pnpm lint

# Lint specific package
pnpm --filter @langchain/core lint

# Format all packages
pnpm format

# Check formatting without fixing
pnpm format:check
```

**Linting includes:**
- ESLint for code quality
- dpdm for circular dependency detection

### Testing
```bash
# Run all unit tests
pnpm test:unit

# Run all tests including integration
pnpm test

# Run single test file
cd libs/langchain-core
pnpm test:single /path/to/test.test.ts

# Run in watch mode
pnpm test:watch

# Run integration tests only
pnpm test:integration

# Environment tests (requires Docker)
pnpm test:exports:docker

# Run standard tests
pnpm test:standard
```

**Test types:**
- Unit tests (`.test.ts`): Modular logic without external API calls
- Integration tests (`.int.test.ts`): Require external API credentials; create `.env` files
- Standard tests: Defined in `langchain-standard-tests`

### Additional Tasks
```bash
# Clean build artifacts
pnpm clean

# Pre-commit checks
pnpm precommit

# Release workflow (maintainers)
pnpm changeset          # Create changeset
pnpm changeset version  # Version packages
pnpm release            # Publish to npm

# Run dev release workflow (maintainers)
# Via GitHub Actions → Dev Release
```

## Architecture & Code Structure

### Monorepo Structure
```
libs/
├── langchain-core/        # Core abstractions and types
├── langchain/             # High-level API bindings
├── langchain-community/   # Community integrations
├── langchain-standard-tests/
├── providers/             # Individual provider packages
│   ├── langchain-openai/
│   ├── langchain-anthropic/
│   └── ...
└── create-langchain-integration/  # Scaffolding tool

examples/                  # Usage examples
environment_tests/         # Environment compatibility tests
dependency_range_tests/    # Dependency version tests
```

### Package Exports & Entrypoints

LangChain uses a granular entrypoint system defined in `package.json` `exports` field. For example, `langchain-core` exports:
- `"./agents"`: `src/agents.ts`
- `"./tools"`: `src/tools/index.ts`
- `"./language_models/chat_models"`: `src/language_models/chat_models.ts`

Users import specific functionality:
```typescript
import { ChatOpenAI } from "@langchain/openai";
import { BaseChatModel } from "@langchain/core/language_models/chat_models";
```

### Core Concepts (langchain-core)

**Base Classes & Abstractions:**
- **Language Models**: `BaseLanguageModel`, `BaseChatModel`, `BaseLLM` in `src/language_models/`
- **Tools**: `Tool` in `src/tools/index.ts`
- **Runnables**: `Runnable` in `src/runnables/index.ts` - core composition primitive
- **Vector Stores**: `VectorStore` in `src/vectorstores.ts`
- **Documents**: `Document`, `BaseDocumentTransformer` in `src/documents/`
- **Memory**: `BaseMemory` in `src/memory.ts`
- **Callbacks**: `BaseCallbackHandler` in `src/callbacks/`
- **Prompts**: Prompt templates in `src/prompts/`
- **Output Parsers**: `BaseOutputParser` in `src/output_parsers/`
- **Retrievers**: `BaseRetriever` in `src/retrievers/`

**Key Utilities:**
- **Messages**: `BaseMessage`, message handling in `src/messages/`
- **Callbacks & Tracers**: Observability in `src/callbacks/` and `src/tracers/`
- **Stores**: Key-value stores in `src/stores.ts`
- **Runnable composition**: Graph-based workflows in `src/runnables/graph.ts`

### Adding New Integrations

When contributing integrations to `langchain-community`:

1. **Create separate entrypoint** in `libs/langchain-community/package.json` `exports` field
2. **Add to `requiresOptionalDependency`** array to prevent build failures
3. **Use peer dependencies** for third-party libraries (not `dependencies`)
4. **Import third-party types** directly for client configuration when possible

Example from `.github/contributing/INTEGRATIONS.md`:
```typescript
// Create new entrypoint for hypothetical "langco" vector store
// Add to entrypoints: "vectorstores/langco": "vectorstores/langco"
// Add to requiresOptionalDependency: "vectorstores/langco"
```

For full packages, use the scaffolding tool:
```bash
npx create-langchain-integration
```

### Dependencies

**Peer Dependencies Strategy:**
- `langchain-community`: Third-party deps as `peerDependencies`
- Individual provider packages: Third-party deps as hard `dependencies`
- `langchain-core`: No peer deps (foundational)
- Use caret syntax (`^`) for version ranges

**Dependency Updates:**
- Check compatibility with `dependency_range_tests/`
- Use `dpdm` to detect circular dependencies

### Testing Strategy

**Test Location:**
- Tests in `tests/` folder alongside source files
- Unit tests: `*.test.ts`
- Integration tests: `*.int.test.ts`

**Integration Test Setup:**
- Create `.env` files in package directories
- Copy from `.env.example` if available
- Use `pnpm test:single` for selective testing

**Environment Tests:**
- Test compatibility across Node.js (ESM/CJS), Edge, and browser
- Run with Docker: `pnpm test:exports:docker`

## Build System

**Monorepo Management:**
- **pnpm workspaces**: Defined in `pnpm-workspace.yaml`
- **Turbo**: Build orchestration in `turbo.json`
- **tsdown**: TypeScript to JavaScript compilation

**Build Outputs:**
- ESM: `dist/index.js`
- CJS: `dist/index.cjs`
- Types: `dist/index.d.ts` and `dist/index.d.cts`

**Build Dependencies:**
- Turbo tasks depend on `^build:compile` (dependencies must build first)
- Clean with `pnpm clean` before rebuilding

## Release Process

**Version Management:**
- Uses Changesets (`@changesets/cli`)
- Create: `pnpm changeset`
- Version: `pnpm changeset version`
- Publish: `pnpm release`

**Dev Releases (Maintainers):**
- GitHub Actions workflow: "Dev Release"
- Format: `x.y.z-<tag>.<short-sha>` (e.g., `1.1.0-dev.abc1234`)
- Install: `npm install @langchain/core@dev`

## Important Files

- `package.json`: Root workspace configuration
- `pnpm-workspace.yaml`: Workspace structure
- `turbo.json`: Build pipeline configuration
- `CONTRIBUTING.md`: Detailed contribution guidelines
- `.github/contributing/INTEGRATIONS.md`: Integration-specific patterns
- `libs/langchain-core/package.json`: Core package with full export map
- `libs/langchain-community/langchain.config.js`: Community package configuration

## Key Practices

- **Node 20+** required for all packages
- **TypeScript strict mode** enabled
- **ESM-first** with CJS compatibility
- **Circular dependency detection** via dpdm
- **Format with Prettier**, lint with ESLint
- **Separate entrypoints** for each integration
- **Peer dependencies** for optional third-party libs
- **Integration tests** require credentials