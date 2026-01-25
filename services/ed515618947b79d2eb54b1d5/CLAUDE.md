# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Actionhero is a multi-transport API server with integrated cluster capabilities and delayed tasks. It's a reusable, scalable Node.js API framework supporting HTTP, WebSockets, and custom transports.

## Common Commands

```bash
# Development with hot-reload
npm run dev

# Debug mode with inspector
npm run debug

# Build TypeScript to JavaScript
npm run build

# Run tests (includes lint + build as pretest)
npm test

# Run specific test file
npm test -- --testPathPattern="actions/status"

# Lint check (prettier)
npm run lint

# Auto-format code (prettier)
npm run pretty

# Generate API documentation
npm run docs
```

**Note:** Redis must be running for tests and the server to function properly.

## Architecture

### Core Concepts

Actionhero uses an **initializer-based lifecycle system** where all components are loaded via prioritized initializers. The server boot sequence is: `load` → `initialize` → `start`.

**Key directories:**
- `src/actions/` - API endpoint definitions
- `src/tasks/` - Background job definitions
- `src/initializers/` - Core system bootstrapping
- `src/servers/` - Transport implementations (HTTP, WebSocket)
- `src/modules/` - Public API modules (cache, tasks, chatRoom, etc.)
- `src/config/` - Configuration files by topic

### Patterns

**Actions** (`src/classes/action.ts`):
- Extend the `Action` abstract class
- Define `name`, `description`, `inputs`, and `outputExample` statically
- Implement `async run({ response, params, connection })` to handle requests
- Inputs are validated automatically via the `inputs` definition

**Tasks** (`src/classes/task.ts`):
- Extend the `Task` abstract class
- Define `name`, `queue`, `frequency` (0 for non-recurring), and `description`
- Implement `async run(data, worker)` for background processing
- Uses node-resque for queue management (Redis-backed)

**Initializers** (`src/classes/initializer.ts`):
- Extend the `Initializer` abstract class
- Define priority-based lifecycle methods: `loadPriority`, `startPriority`, `stopPriority`
- Core initializers use priorities < 1000; project initializers use > 1000
- Methods: `initialize()` (setup), `start()` (connect), `stop()` (cleanup)

**Servers** (`src/classes/server.ts` + `src/servers/`):
- Extend the `Server` abstract class
- Handle connection lifecycle and protocol parsing
- Examples: `web.ts` (HTTP/HTTPS), `websocket.ts`

**Connections** (`src/classes/connection.ts`):
- Represent a client connection with `type` (http, websocket, etc.)
- Have `params` (action inputs), `response` (action outputs), `error`
- Connected via `api.connections`

### Global API Object

The `api` object (exported from `src/index.ts`) is globally available and contains:
- `api.actions` - Loaded action definitions
- `api.tasks` - Loaded task definitions
- `api.servers` - Active server instances
- `api.connections` - Active connections
- `api.config` - Runtime configuration
- `api.cache` - Key/value cache
- `api.chatRoom` - Chat/real-time messaging
- `api.redis` - Redis connection utilities
- `api.log` - Logging function
- `api.task` - Task enqueueing (`api.task.enqueue(taskName, params, queue)`)

### Configuration System

Config files in `src/config/` export a function receiving `api` and returning options. The config system uses dot-prop for nested property access. Core config sections: `api`, `redis`, `logger`, `tasks`, `web`, `websocket`, `routes`, `errors`, `plugins`.

### Middleware

Middleware runs before/after actions via `action.middleware` arrays. Each middleware implements `async run({ action, connection, response })`.

### Testing

Tests use Jest with `ts-jest`. The `specHelper` initializer enables direct action testing without network: `api.specHelper.runAction('actionName', params)`.