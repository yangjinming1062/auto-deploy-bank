# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Simulacrum is a React library that provides a code playground where users write TypeScript code and see it executed visually. Code is transformed into AsyncGenerator state machines that the runtime executes step-by-step on discrete "ticks", visualizing the heap and stack evolution as React Flow diagrams.

## Commands

```bash
# Development
yarn install              # Install dependencies
yarn dev                  # Start Vite dev server
yarn storybook            # Start Storybook on port 6006

# Build & Test
yarn build                # TypeScript check + Vite production build (outputs to dist/)
yarn test                 # Run Jest tests
yarn lint                 # ESLint on src (ts, tsx)

# Git hooks (automatic)
# .husky/pre-commit runs lint-staged → prettier on staged files
```

## Architecture

```
src/
├── compiler/      # Transforms TypeScript → AsyncGenerator state machines
│   ├── compiler.service.ts
│   └── command-handlers/  # Build command handlers
├── runtime/       # Executes state machines, manages ticks
│   ├── runtime.ts         # Core runtime with tick() function
│   ├── flow-manager.ts    # Orchestrates concurrent flows
│   ├── flow-executor.ts   # Executes individual AsyncGenerators
│   ├── heap.ts            # Object allocation tracking
│   └── execution-stack.ts # Call stack recording
├── ui/
│   ├── components/        # 30+ React components
│   │   ├── editor/        # Monaco editor wrapper
│   │   ├── playground/    # React Flow visualization canvas
│   │   ├── reactflow/     # Custom nodes/edges
│   │   └── ide/           # File/folder management
│   └── state-managers/    # Zustand stores
├── std/            # Standard library (flow, awaitAll, events)
└── index.tsx       # Exports: Editor, Playground
```

### Execution Model

Code transforms into AsyncGenerators yielding simple instructions: `LOAD`, `LOG`, `UNLOAD`, `HALT`, `NO_OP`, `AWAIT_FLOW`. The runtime maintains a `currentTick` counter and advances all state machines together on each tick. Multiple flows can execute concurrently per tick.

### Key Patterns

- **Dependency Injection**: `DIContainer` manages object instances with partitions for project isolation
- **State Management**: Zustand + Immer for immutable updates
- **Event System**: Pub/sub via event channels in `src/runtime/event-channels/`
- **Scheduling**: `ScheduledTaskManager` handles timers/intervals for scheduled flows

## Conventions

- **Formatting**: 4-space tabs, semicolons, single quotes, trailing commas (ES5)
- **Language**: All code and comments in English
- **Commits**: Imperative mood, present tense ("Add feature" not "Added feature")
- **PRs**: Single-feature atomic PRs with design explanation for complex features
- **Testing**: Jest with ts-jest, pattern: `**/?(*.)+(spec|test).[tj]s?(x)`

## External Resources

- Docs: https://docs.metz.sh
- Playground: https://try.metz.sh
- Templates: https://app.metz.sh