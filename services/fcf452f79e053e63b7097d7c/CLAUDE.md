# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a monorepo showcasing **80+ examples** of Webpack 5's Module Federation feature, demonstrating various patterns across different frameworks including React, Vue, Angular, Next.js, Vite, and more. Each example is a standalone pnpm workspace demonstrating a specific Module Federation use case.

## Project Structure

```
/home/ubuntu/deploy-projects/fcf452f79e053e63b7097d7c
├── pnpm-workspace.yaml          # Defines all example workspaces
├── package.json                 # Root dependencies and scripts
├── basic-host-remote/           # Example: Host app loading remote component
│   ├── app1/                    # Host application
│   ├── app2/                    # Remote application
│   └── package.json
├── nextjs-ssr/                  # Example: Next.js with SSR
│   ├── home/
│   ├── shop/
│   └── checkout/
├── cypress-e2e/                 # E2E testing framework
└── [80+ other examples...]
```

**Key Pattern**: Most examples use a `host`/`remote` or `app1`/`app2` structure where:
- **Host**: The main application that consumes remote modules
- **Remote**: Application exposing modules for other apps to consume

## Package Manager

**pnpm is mandatory** - the repository has a `preinstall` hook that blocks other package managers:
```bash
pnpm i              # Install dependencies
pnpm install        # Same as above
```

## Common Development Commands

### Running Examples

```bash
# Navigate to any example directory
cd basic-host-remote

# Install dependencies for all workspaces in the example
pnpm i

# Run example in development mode (typically starts both host and remote)
pnpm start
# or
pnpm dev

# Build the example
pnpm build

# Serve built application
pnpm serve
```

### Testing

```bash
# Run Jest unit tests (from root)
pnpm test

# Run Cypress e2e tests in debug mode (interactive)
pnpm cypress:debug

# Run Cypress e2e tests in headless mode
pnpm cypress:run

# Build and run e2e tests in CI mode (for specific examples)
cd nextjs-ssr
pnpm e2e:ci

# Run Playwright tests (alternative to Cypress)
pnpm test:e2e
pnpm test:e2e:ui        # Interactive mode
pnpm test:e2e:debug     # Debug mode
```

### Code Quality

```bash
# Format code with Prettier (from root)
pnpm prettier

# Check formatting without changes
pnpm prettier:check
```

### Building All Examples

```bash
# Build all examples in parallel (from root)
pnpm build
```

## Example-Specific Commands

Different examples use different build tools and commands:

### Modern.js Examples
```bash
cd basic-host-remote
pnpm dev         # Start dev server
pnpm build       # Build for production
pnpm lint        # Run linting
pnpm serve       # Serve built files
```

### Vite Examples
```bash
cd module-federation-vite-react
pnpm dev         # Start dev server
pnpm build       # Build
pnpm preview     # Preview build
```

### Next.js Examples
```bash
cd nextjs-ssr
pnpm start       # Start dev server
pnpm build       # Build
pnpm serve       # Serve production build
```

## High-Level Architecture

### Module Federation Concepts

Each example demonstrates specific Module Federation patterns:

1. **Basic Host-Remote** (`basic-host-remote/`)
   - Simple one-way dependency (host consumes remote)
   - Host loads remote component at runtime

2. **Bi-Directional** (`bi-directional/`)
   - Two applications that both host and consume from each other
   - Circular dependency pattern

3. **Shared Context** (`shared-context/`)
   - Sharing React context across federated boundaries
   - State management between host and remote

4. **Dynamic Remotes** (`dynamic-system-host/`)
   - Remotes loaded dynamically at runtime
   - Runtime remote selection

5. **Server-Side Rendering** (`nextjs-ssr/`)
   - Module Federation with Next.js SSR
   - Hydration patterns across federated apps

6. **Cross-Framework** (`react-in-vue/`, `vue2-in-vue3/`)
   - React components in Vue apps
   - Vue components in React apps

### Build Tool Distribution

- **Webpack**: Traditional examples (webpack.config.js)
- **Rspack**: Rust-based fast bundler (rspack.config.js)
- **Vite**: Modern dev server (vite.config.js)
- **Modern.js**: Framework-agnostic build system (modern.config.js)
- **Next.js**: React framework (next.config.js)

## Testing Strategy

The repository uses multiple testing approaches:

1. **Jest**: Unit tests for core functionality (run from root)
2. **Cypress**: Full e2e testing (interactive and headless modes)
3. **Playwright**: Alternative e2e framework (used in many examples)

E2e tests typically:
- Build the example applications
- Start them on specific ports
- Test user interactions and Module Federation behavior
- Generate screenshots/videos on failure

## Documentation Generation

The `updateReadmeExampleList.js` script scans all examples and generates `output.md` with:
- List of all examples
- Their descriptions
- Build tool indicators (Webpack ✅/❌, Rspack ✅/❌)

Run it with:
```bash
node updateReadmeExampleList.js
```

## Important Notes

- Each example is independently runnable after `pnpm install`
- Examples use port patterns (typically 3001+, 3002+)
- Some examples have proprietary code (can be removed after checkout)
- The repository uses pnpm overrides to pin specific dependency versions
- Submodules may need to be pulled: `pnpm submodules`

## Finding Specific Examples

To locate examples:
1. Check `pnpm-workspace.yaml` for complete list
2. Look at individual `package.json` files for descriptions
3. Run `node updateReadmeExampleList.js` to generate `output.md` with all examples
4. Each example directory has its own README.md with specific instructions

## Dependencies

Root-level dependencies include:
- Build tools: TypeScript, pnpm
- Testing: Jest, Cypress, Playwright
- Utilities: Prettier, Husky, Lerna
- All examples use their own specific dependencies defined in their package.json

The repository enforces pnpm via the `preinstall` script and uses pnpm's `overrides` field to pin versions for critical dependencies.