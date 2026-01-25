# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pm2-web is a web-based monitor for [PM2](https://github.com/Unitech/pm2), a process manager for Node.js. It provides a real-time web UI for monitoring and managing PM2 processes across one or more hosts.

## Development Commands

```bash
# Install dependencies
npm install

# Build UI assets (browserify + less)
npx grunt

# Watch for changes and rebuild automatically
npx grunt watch

# Run unit tests
npm test

# Run integration tests
npm run integration

# Run with coverage and submit to coveralls
npm run coveralls
```

## Architecture

### Server-Side (Express + WebSockets)

- **Entry point**: `pm2-web.js` → `server/app.js` (PM2Web class)
- **Dependency injection container**: Uses `wantsit` library to manage component lifecycle
- **Key components**:
  - `Configuration` - parses CLI args and config files (loads from `--config`, `~/.config/pm2-web/config.json`, `/etc/pm2-web/config.json`)
  - `PM2Listener` - connects to pm2 via `pm2-interface`, receives real-time events and system data
  - `WebSocketResponder` - broadcasts data to connected browsers
  - `ServerHostList` - manages HostData objects for each monitored host

- **Routes**: Express routes in `server/routes/` handle UI page serving (`/`, `/hosts/:host`)

### Client-Side (AngularJS)

- **Bundled via browserify**: `ui/index.js` → compiled to `server/public/js/monitor.js`
- **Modules**: AngularJS with `ngRoute`, `ngSanitize`, `ui.bootstrap`, `highcharts-ng`
- **Structure**: components, controllers, directives, filters in `ui/` subdirectories

### Data Flow

1. `PM2Listener` connects to pm2 via Unix sockets (RPC + event ports)
2. Polls for system data at configured `updateFrequency` interval
3. Emits `systemData` events with host/process information
4. `ServerHostList` updates `HostData` objects, emits to WebSocketResponder
5. WebSocket broadcasts to all connected browsers
6. Angular controllers receive data via WebSocket and update UI

### Common Data Models

- **HostData** (`common/HostData.js`) - wraps system info + array of ProcessData
- **ProcessData** (`common/ProcessData.js`) - individual process status, resource usage history

### Configuration

Default config in `config.json` with these key sections:
- `www` - web server host/port, SSL, authentication
- `ws` - WebSocket batch frequency
- `pm2` - array of hosts to monitor (host, rpc socket, event socket, optional inspector port)
- `updateFrequency` - how often to poll hosts (ms)
- `graph.datapoints` / `graph.distribution` - resource usage graph settings

## Testing

- Uses `nodeunit` for tests with `testsuite` helper
- Test aggregator at `test/unit/aggregator.js` discovers all tests
- Unit tests use `proxyquire` for mocking dependencies
- Integration tests in `test/integration/` (requires actual pm2)