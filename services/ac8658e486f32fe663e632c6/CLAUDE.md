# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NLUX is a JavaScript and React library for building conversational AI interfaces. It supports multiple LLM backends (OpenAI, LangChain, HuggingFace, etc.) through a flexible adapter system.

## Development Commands

```bash
# First-time setup (required before other commands)
yarn set        # Generates package.json files from templates, installs deps, builds
yarn reset      # Cleanup + set (use when resetting environment)

# Development
yarn build      # Build all packages (production mode)
yarn watch      # Watch mode for all packages (rollup --watch)
yarn test       # Run all tests (vitest run)
yarn lint       # Run ESLint on packages
```

**Testing individual packages:** Tests run via `cd specs && yarn test`. Individual test patterns: `cd specs && npx vitest run -t "pattern"`

## Monorepo Structure

```
packages/
├── js/           # Vanilla JS packages (core + adapters)
│   └── core/     # @nlux/core - Main chat interface
│   ├── openai/   # @nlux/openai - OpenAI adapter
│   ├── langchain/ # @nlux/langchain - LangChain adapter
│   ├── hf/       # @nlux/hf - HuggingFace adapter
│   ├── nlbridge/ # @nlux/nlbridge - Express middleware adapter
│   └── bedrock/  # @nlux/bedrock - AWS Bedrock adapter
├── react/        # React packages (mirror JS structure with React hooks)
│   └── core/     # @nlux/react - React components and hooks
├── css/
│   └── themes/   # @nlux/themes - CSS themes (Luna theme)
├── extra/
│   ├── markdown/ # @nlux/markdown - Markdown stream parser
│   └── highlighter/ # @nlux/highlighter - Syntax highlighter
└── shared/       # Shared types and utilities
```

**Package naming:** Dev packages use `@nlux-dev/` prefix (e.g., `@nlux-dev/core`), published to npm as `@nlux/core`.

## Architecture Patterns

### Chat Adapters (`@shared/types/adapters/chat/chatAdapter.ts`)

All LLM integrations implement the `ChatAdapter` interface with two modes:
- `streamText(message, observer, extras)` - Streaming responses
- `batchText(message, extras)` - Non-streaming responses

The adapter calls `observer.next(chunk)`, `observer.complete()`, or `observer.error(error)` to communicate with the UI.

### Core Components

- **AiChat** - Main chat interface component (Vanilla JS class + React component)
- **AiContext** - Context/items management for RAG-like features
- **Observable pattern** - Event bus in `packages/js/core/src/bus/`

### Shared Types

`packages/shared/src/types/` contains type definitions used across packages:
- `adapters/chat/` - ChatAdapter, StreamingAdapterObserver, etc.
- `adapters/context/` - ContextAdapter types
- `conversation/` - ChatItem, ParticipantRole
- `aiContext/` - AiContext types

## Key Files

- `pipeline/scripts/` - Build pipeline scripts (build.mjs, watch.mjs, set.mjs, test.mjs)
- `pipeline/scripts/packages.mjs` - Package configuration and metadata
- `packages/*/core/src/` - Main source code for each package
- `specs/specs/` - Test specifications organized by feature
- `specs/vite.config.mts` - Vitest configuration

## Build System

- **Rollup** for bundling with ESBuild
- **TypeScript** throughout
- **Package templates** - Individual packages use `package.tpl.json` which is processed by `yarn set` to generate `package.json` with proper versions
- **Yarn workspaces** - Dependencies managed via root package.json

## TypeScript Configuration

- ESLint: `eslint.config.mjs` (typescript-eslint)
- Package-level tsconfig: `pipeline/config/packageLevelTsConfig.json`
- Ignore patterns: `dist/**`, `specs/**`, `packages/shared/src/markdown/snapshot/marked/*`