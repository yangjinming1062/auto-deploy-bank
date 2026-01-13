# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is the nteract monorepo - a literate coding environment that provides interactive computing experiences with Jupyter notebooks. The project consists of:
- **applications/**: Desktop (Electron), web, and Jupyter extension applications
- **packages/**: Core SDK packages (Redux actions, reducers, epics, types, selectors, React components)

## Common Development Commands

### Setup and Installation
```bash
yarn install
yarn build:all                    # Compile all TypeScript
yarn build:all:cleanly            # Clean install and rebuild everything
```

### Building Applications
```bash
yarn build:desktop:watch          # Progressive build of desktop app (recommended for dev)
yarn spawn                         # Launch Electron app after building
yarn build:desktop                 # One-time desktop build
yarn build:jext                    # Build Jupyter extension
yarn build:packages:watch          # Watch mode for package builds
```

### Running in Development
```bash
yarn start                         # Alias for app:desktop
yarn app:desktop                   # Run desktop app
yarn app:jupyter-extension         # Run Jupyter extension dev server
```

### Testing
```bash
yarn test                          # Run all tests (Jest)
yarn test:verbose                  # Run tests with verbose output
yarn test:coverage                 # Run tests with coverage report
yarn test:unit                     # Alias for yarn test
```

### Linting and Formatting
```bash
yarn lint                          # Run ESLint
yarn lint:fix                      # Run ESLint with auto-fix
yarn prettify                      # Format code with Prettier
yarn lint:jupyterExtension         # Lint Jupyter extension Python code (Black)
```

### Building Documentation
```bash
yarn docs                          # Start styleguidist server for component docs
yarn docs:build                    # Build styleguidist documentation
yarn package:docs                  # Build API docs for packages
```

## Code Architecture

### State Management Pattern

nteract follows the Redux pattern with three main layers:

1. **@nteract/actions** (`packages/actions`): Action creators for all application events
   - Actions are plain JavaScript objects with well-defined schemas
   - Every UI event maps to an action (e.g., adding a cell, setting Jupyter host)
   - Use action creators like `executeCell({ contentRef, cellId })`

2. **@nteract/reducers** (`packages/reducers`): Pure functions that update state based on actions
   - Reducers implement the functionality for actions
   - Example: `reducers.app(state, actions.saveFulfilled({}))`

3. **@nteract/epics** (`packages/epics`): Redux-Observable epics for async/side-effect operations
   - Handle kernel communication, network requests, and other async operations
   - Example: `watchExecutionStateEpic` monitors kernel state changes

4. **@nteract/selectors** (`packages/selectors`): Memoized selectors for reading state

5. **@nteract/types** (`packages/types`): TypeScript type definitions

6. **@nteract/core** (`packages/core`): Unified package that exports all of the above

### Application Structure

- **applications/desktop/**: Electron-based desktop application
  - Entry: `src/index.ts`
  - Main process: `src/main/`
  - Notebook UI: `src/notebook/`
  - Builds with webpack

- **applications/jupyter-extension/**: Browser extension for Jupyter
  - Runs in JupyterLab or classic Jupyter

- **applications/web/**: Web application

### Component Architecture

- **@nteract/presentational-components**: Dumb components for rendering
- **@nteract/stateful-components**: Connected components with state
- **@nteract/connected-components**: Higher-level connected components
- **@nteract/notebook-app-component**: Complete notebook application component

### Communication Layer

- **@nteract/messaging** (`packages/messaging`): Jupyter messaging protocol utilities
- **@nteract/rx-jupyter** (`packages/rx-jupyter`): RxJS wrappers for Jupyter REST API
- **@nteract/commutable** (`packages/commutable`): Immutable notebook data structures

## Development Workflow

### Making Changes

1. Create a branch: `git checkout -b feature-name`
2. Make changes in `packages/` or `applications/`
3. Build incrementally:
   ```bash
   # Terminal 1: Watch mode for packages
   yarn build:packages:watch

   # Terminal 2: Watch mode for desktop app
   yarn build:desktop:watch

   # Terminal 3: Spawn the app to test
   yarn spawn
   ```
4. Reload the app (`View > Reload` or restart `yarn spawn`)
5. Run tests: `yarn test`

### Testing Approach

- Uses **Jest** for unit tests
- Tests located in `__tests__/` directories alongside source files
- React component testing with **Enzyme**
- RxJS epic testing with ActionsObservable
- Coverage reports available with `yarn test:coverage`

### Key Libraries and Technologies

- **React 16** with TypeScript
- **Redux** for state management
- **Redux-Observable** (RxJS) for side effects
- **Electron** for desktop application
- **Immutable.js** for data structures
- **Enzyme** for component testing
- **Jest** for unit testing
- **TypeScript 3.7**
- **Lerna** for monorepo management

## Package Relationships

The `@nteract/core` package is the main entry point that aggregates:
- `@nteract/actions` - Action creators
- `@nteract/reducers` - State reducers
- `@nteract/epics` - Async operations
- `@nteract/selectors` - State selectors
- `@nteract/types` - TypeScript types

Applications depend on `@nteract/core` for a single dependency instead of individual packages.

## Useful Resources

- **General Documentation**: https://docs.nteract.io/
- **API Documentation**: https://packages.nteract.io/
- **Component Documentation**: https://components.nteract.io/
- **Jupyter Messaging Protocol**: http://jupyter-client.readthedocs.org/en/latest/messaging.html

## Monorepo Structure

```
applications/
├── desktop/          # Electron desktop app
├── jupyter-extension/ # Jupyter extension
└── web/              # Web app

packages/
├── actions/          # Redux action creators
├── commutable/       # Immutable notebook structures
├── core/             # Aggregated exports
├── epics/            # Redux-Observable epics
├── reducers/         # Redux reducers
├── selectors/        # Redux selectors
├── types/            # TypeScript types
├── messaging/        # Jupyter protocol utilities
├── rx-jupyter/       # Jupyter REST API clients
└── [components]/     # React components

changelogs/           # Release changelogs
docs/                 # User documentation
```

## Environment Requirements

- **Node.js**: >= 14.0.0 (use latest LTS)
- **Yarn**: >= 1.16.0 (use yarn, not npm)
- Python 3.x (for Jupyter extension development)

## Release Process

- Uses **Lerna** for versioning and publishing
- **Semantic-release** for automated releases
- **Conventional Commits** for release notes
- Run `yarn release` to release all packages

## Jupyter Kernels

To test locally, install kernels using `ipykernel`:
```bash
pip install ipykernel
python -m ipykernel install --user
```

## Troubleshooting

- **Hot reload issues**: If the app doesn't reload changes, restart `yarn spawn`
- **Type errors**: Run `yarn build:all` to ensure TypeScript compilation is up to date
- **Kernel connection issues**: Check that Jupyter kernels are properly installed
- **Electron debugging**: Add `debugger;` statements in source code to break in DevTools