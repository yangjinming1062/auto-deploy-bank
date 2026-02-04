# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Midscene.js is an AI-powered UI automation framework that drives web, Android, iOS, and desktop applications using vision-language models. It provides a JavaScript SDK, YAML scripting, Chrome extension, and MCP server for controlling UIs with natural language.

## Monorepo Structure

This is a pnpm workspace with two main directories:
- `packages/` - Core libraries and platform integrations
- `apps/` - End-user applications (Chrome extension, playground, documentation site)

### Key Packages

| Package | Published As | Description |
|---------|--------------|-------------|
| `packages/core` | `@midscene/core` | Core AI automation logic, agent, YAML parser |
| `packages/shared` | `@midscene/shared` | Shared utilities, image processing, constants |
| `packages/web-integration` | `@midscene/web` | Web automation (Puppeteer/Playwright integration) |
| `packages/android` | `@midscene/android` | Android automation via ADB |
| `packages/ios` | `@midscene/ios` | iOS automation via WebDriverAgent |
| `packages/computer` | `@midscene/computer` | Desktop automation (cross-platform native input) |
| `packages/mcp` | `@midscene/mcp` | MCP server exposing Midscene tools |
| `packages/visualizer` | `@midscene/visualizer` | Visualization and debugging tools |

## Common Commands

```bash
# Install dependencies (runs prepare script to build all packages)
pnpm install

# Build all packages
pnpm run build

# Build with fresh cache (fixes circular dependency issues)
pnpm run build:skip-cache

# Watch mode for development
pnpm run dev

# Run unit tests
pnpm run test

# Run AI-related tests (requires .env with API keys)
pnpm run test:ai

# Run a single test file
npx vitest run packages/core/tests/ai/evaluate/some.test.ts
npx nx test @midscene/core -- tests/ai/evaluate/some.test.ts

# Run E2E tests (Playwright)
pnpm run e2e
npx nx e2e @midscene/web

# Run E2E with caching enabled
pnpm run e2e:cache

# Run E2E with report generation
pnpm run e2e:report

# Run linting
pnpm run lint

# Format staged files
pnpm run format

# Check spelling
pnpm run check-spell

# Run a specific package's dev server
cd packages/android-playground && pnpm run dev
```

## Build System

- **Bundler**: [Rslib](https://rsbuild.dev/rslib/) (Rust-based, built on Rsbuild)
- **Monorepo Tool**: [Nx](https://nx.dev/)
- **Test Runners**: Vitest (unit tests), Playwright (E2E tests)
- **Linting**: Biome with single quotes and relaxed TypeScript rules

All packages use `rslib.config.ts` for configuration. Output goes to `dist/` with CJS (`lib/`) and ESM (`es/`) formats plus TypeScript definitions.

## Architecture

### Core Flow

1. **Agent** (`packages/core/src/agent/`) - Main orchestrator that plans and executes UI tasks using AI
2. **AI Model** (`packages/core/src/ai-model/`) - Interface to VLMs (Qwen3-VL, UI-TARS, Gemini, etc.)
3. **Task Runner** (`packages/core/src/task-runner.ts`) - Executes planned actions and handles screenshots
4. **Dump/Screenshot** (`packages/core/src/dump/`, `packages/core/src/screenshot-item.ts`) - Manages screenshot capture and serialization

### Platform Integration

Each platform implements a common interface defined in `@midscene/core`:
- **Web**: Puppeteer/Playwright hooks, Chrome extension
- **Android**: ADB-based device control via `appium-adb`
- **iOS**: WebDriverAgent/XCTest integration
- **Computer**: Native keyboard/mouse via `libnut-core`

### Shared Layer

`@midscene/shared` provides:
- Image processing with Sharp/Jimp and photon (Rust bindings)
- MCP protocol implementation
- Environment/logger utilities
- Polyfills for cross-platform compatibility

## AI Testing Setup

To run tests with AI features, create a `.env` file in the root:

```env
OPENAI_API_KEY="your_api_key"
MIDSCENE_MODEL_NAME="qwen3-vl-plus"
```

Test variants:
- `AI_TEST_TYPE=web` - Web-specific AI tests
- `AITEST=true` - Enable AI evaluation mode
- `MIDSCENE_CACHE=true` - Enable caching for faster replay
- `MIDSCENE_REPORT=true` - Generate HTML reports

## Commit Convention

Use Conventional Commits with mandatory scope:

```
<type>(<scope>): <subject>
```

**Types**: `feat`, `fix`, `refactor`, `chore`, `docs`, `perf`, `style`, `test`, `ci`, `build`

**Scopes** (required): Top-level directories in `packages/` or `apps/`, or: `workflow`, `llm`, `playwright`, `puppeteer`, `mcp`, `bridge`

**Example**: `feat(mcp): add screenshot tool with element selection`

## Common Issues

### "REPLACE_ME_WITH_REPORT_HTML" in reports
Run `pnpm run build:skip-cache` to rebuild everything without cache.

### Circular dependency issues
The full monorepo build must be run, not individual packages.

## Dependencies

- Node.js >= 18.19.0 (Node 20.9.0 recommended)
- pnpm >= 9.3.0