# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

知乎助手 (ZhihuHelper) - An Electron desktop application for scraping Zhihu content (answers, articles, columns, topics, collections, pins, etc.) and generating EPUB e-books for personal reading.

## Build Commands

```bash
# Development
npm run watch              # Compile TypeScript to dist/ with watch mode and source maps
npm run start              # Start Electron app (uses prebuilt dist/)
npm run startgui           # Start Vite dev server for GUI (localhost:8080)

# Production build
npm run build              # Compile with source maps
npm run build-without-sourcemap  # Production build (smaller size)

# Linting & formatting
npm run lint               # Run TypeScript compiler + ESLint
npm run eslint             # Run ESLint only
npm run prettier-with-fix  # Format all source files

# CLI commands (no Electron dependencies)
npm run ace                # Run ACE CLI commands
npm run ace <command>      # Run specific command, e.g., npm run ace Init:Env

# Distribution
npm run pack               # Build GUI + compile, output to release/ (no compression)
npm run dist               # Build full Electron distributable installer

# Database & debugging
npm run server             # Start dev server with nodemon (port 9229 for debugging)
```

## Architecture

### Three-Step E-book Generation Pipeline

1. **Init:Env** - Initialize environment (database, config files)
2. **Fetch:XXX** - Fetch data from Zhihu API, store in SQLite
3. **Generate:XXX** - Read from SQLite, generate EPUB/HTML output

Custom tasks use `Fetch:Customer` and `Generate:Customer` which read config from `config.json`.

### Directory Structure

```
src/
├── ace.ts              # CLI entry point (ACE command runner)
├── index.ts            # Electron main process (GUI entry)
├── command/            # ACE command implementations
│   ├── base.ts         # Command base class
│   └── fetch/          # Data fetching commands (Fetch:Customer, etc.)
│   └── generate/       # E-book generation commands
├── api/                # Zhihu API layer
│   ├── batch/          # Batch fetching (multiple items)
│   └── single/         # Single item fetching
├── model/              # Database models (answer, article, author, etc.)
├── library/
│   ├── epub/           # EPUB generation (opf, toc, content)
│   ├── http/           # Axios wrapper with Zhihu signature encryption
│   ├── zhihu_encrypt/  # Client-side signature generation (js-rpc)
│   └── knex.ts         # SQLite connection configuration
├── config/             # Request, path, and app configuration
├── constant/           # Task types, configuration constants
├── type/               # TypeScript type definitions
└── public/             # Static assets (icons, js-rpc frontend)
```

### Key Patterns

**API Requests**: All Zhihu API calls go through `src/library/http/index.ts`. It handles:
- Signature generation via `x-zse-96` header (requires js-rpc bridge)
- LRU caching of responses (1 hour TTL)
- Request retry on failure

**Database**: SQLite with Knex ORM. Each model (answer.ts, article.ts, etc.) extends `Base` from `model/base.ts` and defines `TABLE_NAME`, `TABLE_COLUMN`, and `PRIMARY_KEY`.

**Task Execution**: Batch fetching uses async pooling via `CommonUtil.addAsyncTaskFunc()` to limit concurrent requests.

## Code Conventions

### Naming Patterns

| Pattern | Example | Description |
|---------|---------|-------------|
| Type | `Type_Task_Config` | TypeScript interfaces |
| Model | `MAnswer`, `MArticle` | Database models (M prefix) |
| Async function | `asyncGetList`, `asyncFetchData` | Async functions prefixed with `async` |
| File names | `base.ts`, `task_config.d.ts` | Underscore/snake_case |

### Import Conventions

```typescript
import TypeXxx from '~/src/type/xxx'
import MXxx from '~/src/model/xxx'
import xxx from '~/src/library/util/xxx'
```

## Frontend (GUI)

Located in `/client` - a separate Vite + React + Ant Design project.

```bash
cd client
npm run dev    # Start Vite dev server
npm run build  # Build for production
```

## Common Development Workflow

1. Make TypeScript changes in `src/`
2. Run `npm run watch` to auto-compile to `dist/`
3. Test with `npm run ace <command>` for CLI features
4. For GUI: modify `src/index.ts` to use `loadURL('http://localhost:8080')`, run `npm run startgui`, then `npm run start`