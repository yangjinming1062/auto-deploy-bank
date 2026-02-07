# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Locker is a personal data platform that collects, unifies, and serves your personal data. It consists of three main component types:
- **Connectors**: Services that sync data from external sources (Twitter, Facebook, Flickr, etc.) into the locker
- **Collections**: Unified data schemas that normalize data from multiple connectors (Contacts, Links, Photos, Places, Search)
- **Apps**: User-facing applications that use the unified data

**Status**: This project is unmaintained. See README.md for details.

## Build Commands

```bash
make              # Full build: initializes submodules, installs npm deps, builds common
make test         # Run all tests (both vows and mocha)
make newtest      # Run only mocha tests
make oldtest      # Run only vows tests
make clean        # Clean build artifacts
./locker          # Start the locker server (requires API keys first)
./locker --production  # Start in production mode with auto-restart
```

The build process requires MongoDB to be running (lockerd.js starts it automatically).

**Note**: Before running `./locker`, you must copy `Config/apikeys.json.example` to `Config/apikeys.json` and add your API keys.

## Architecture

### Core Startup Sequence (lockerd.js)

The main daemon `lockerd.js` orchestrates startup in this order:
1. Load configuration from `Config/config.json` via `lconfig`
2. Spawn embedded MongoDB instance (data stored in `Me/mongodata`)
3. Verify cryptographic keys exist (`lcrypto`)
4. Run pre-service migrations
5. Initialize sync manager (`lsyncmanager`) and service manager (`lservicemanager`)
6. Initialize registry (`Ops/registry.js`) for service discovery
7. Start web service (`Ops/webservice.js`) - HTTP API on `lconfig.lockerPort`
8. Load scheduled tasks via `lscheduler`

### Key Core Modules (Common/node/)

- **lconfig.js**: Configuration loader, sets up `exports.*` for lockerDir, mongo settings, apps, collections
- **lservicemanager.js**: Manages installed services in `Me/` directory, tracks service map
- **lsyncmanager.js**: Manages connector synclet scheduling and execution
- **locker.js**: Client library for apps/connectors to communicate with locker core via HTTP
- **lmongo.js**: MongoDB connection and collection helpers
- **lcrypto.js**: Cryptographic key management (symmetric and asymmetric)
- **levents.js**: Event system for data change notifications
- **lpquery.js**: Query engine for searching unified data

### Connectors (Connectors/*/)

Connectors sync data from external services. Each connector has:
- `synclets.json`: Defines provided data types, sync frequencies, and mongo ID mappings
- `*.js` files: Each synclet exports a `sync(processInfo, cb)` function
- `package.json`: Dependencies and metadata

Synclets receive `processInfo` with:
- `auth`: OAuth credentials and profile
- `workingDirectory`: Service's Me/ subdirectory
- `absoluteSrcDir`: Connector source directory

Synclets return `{data: {...}, auth: {...}}` where data keys are the data types from synclets.json.

### Collections (Collections/*/)

Collections normalize data from multiple connectors into unified schemas:
- `index.js`: Main collection logic, implements `exports.sync(processInfo, cb)`
- Data stored in MongoDB with type classification for querying

### Apps (Apps/*/)

Apps run as separate Node processes, communicate via stdin/stdout JSON:
1. Receive JSON startup info on stdin with `workingDirectory`, `lockerUrl`, `mongo` info
2. Call `locker.initClient(instanceInfo)` to set up communication
3. Start HTTP server on ephemeral port
4. Write `{port: <port>}` to stdout to signal readiness
5. Use `locker.map()`, `locker.listen()`, `locker.ievent()` to interact with locker

Skeleton app template in `Apps/skeleton/`.

### Service Communication

Services communicate via:
- **HTTP API**: Core endpoints at `/core/<serviceId>/*` for event listening, scheduling, diary
- **Service Map**: `/map` returns all installed services and their capabilities
- **Events**: Services post events with IDR format (e.g., `contact://twitter/#123`) via `locker.ievent()`

## Testing

### Mocha Tests (test/*.test.js)
```bash
cd test
INTEGRAL_CONFIG=test/config.json ../node_modules/.bin/mocha --timeout 500
```

### Vows Tests (tests/*.js)
```bash
cd tests
env NODE_PATH="$(pwd)/../Common/node" node runTests.js
```

Tests use test fixtures in `tests/Me/` and `tests/Config/` as test data.

## Configuration

- `Config/config.json`: Main configuration (ports, paths, registered apps/collections)
- `Config/apikeys.json`: API credentials for connectors (not tracked in git)
- `Me/`: Runtime data directory (created on first run), contains installed service state

The locker runs by default on port 8042 with MongoDB on port 27018.