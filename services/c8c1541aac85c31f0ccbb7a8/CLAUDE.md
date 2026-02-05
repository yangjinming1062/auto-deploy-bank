# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

elecV2P is a Node.js-based network customization tool providing MITM proxy capabilities, scheduled task execution, and a Vue.js web UI for management. It allows users to modify network requests via JavaScript scripts and run scheduled shell commands.

## Common Commands

```sh
yarn                          # Install dependencies
yarn start                    # Start with PM2 (recommended for production)
yarn dev                      # Start with nodemon on port 12521 (dev mode)
yarn build                    # Build web UI frontend
yarn webdev                   # Build web UI in dev mode with HMR
```

**Alternative startup methods:**
```sh
node index.js                 # Direct Node.js start
PORT=8000 node index.js       # Custom port (default 80)
```

## Architecture

### Entry Points
- **index.js** - Initializes web server and AnyProxy; exports eproxy, wsSer, logger, message, checkupdate from utils
- **webmodule.js** - Express.js server setup with WebSocket support at `/elecV2P` path

### Core Modules
| Directory | Purpose |
|-----------|---------|
| `webser/` | Web API route handlers (wbconfig, wbjs, wbtask, wbhook, wbefss, etc.) |
| `func/` | Functional modules: task scheduling, script execution, certificate management |
| `utils/` | Utility exports: eproxy wrapper, websocket, axios, logging, file management |
| `script/` | User scripts and rule definitions (runJSFile.js, rule.js) |

### Configuration
- **config.js** - Runtime config and port initialization, loads from `script/Lists/config.json`
- **CONFIG_Port** - Runtime ports: webst (80), proxy (8001), webif (8002)
- **CONFIG** - User settings from JSON config file

### Key Data Flow
1. Web requests come through `webmodule.js` Express server
2. AnyProxy (eproxy) intercepts network traffic based on rules in `script/rule.js`
3. Rules execute JavaScript files via `runJSFile()` for request/response modification
4. Scheduled tasks run via `func/task.js` (cron/schedule/sub types)
5. Notifications sent through `utils/feed.js` (FEED/IFTTT/BARK/webhook)

### Script Execution Context
- Scripts run in sandboxed VM via `script/runJSFile.js`
- Available globals: `$axios`, `$store`, `$feed`, `$request`, `$response`, `$task`, `$env`
- @grant directives control capabilities (sudo, quiet, silent, calm)
- `$done` or `$fend` required for async scripts

## Rule System (script/rule.js)

Three rule types:
1. **Rewrite** - URL pattern matching, modifies request/response via JS
2. **Rules** - Request/response modification by matching type (js, block, 301, hold, ua)
3. **MITM hosts** - Domains to intercept for HTTPS decryption

## Web UI Ports
- 80 (configurable): Main web dashboard
- 8001: AnyProxy HTTP proxy port
- 8002: AnyProxy web interface for request viewing