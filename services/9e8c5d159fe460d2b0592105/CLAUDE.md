# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Locker is an open-source personal data locker platform that collects, aggregates, and manages personal data from various online services. It features a modular architecture with Connectors, Collections, and Apps.

## Build & Test Commands

```bash
# Initial setup (installs submodules, npm packages, builds Common)
make

# Install system dependencies into ./deps/
make deps

# Run all tests (both legacy Vows and modern Mocha tests)
make test

# Run only legacy tests (Vows framework in tests/)
make oldtest

# Run only modern tests (Mocha framework in test/)
make newtest

# Create distribution tarball
make bindist

# Start the locker daemon
./locker
```

## Code Architecture

Locker follows a service-oriented architecture with three main layers:

### 1. Core Platform (`lockerd.js`)
The main daemon that manages the platform lifecycle. It handles:
- MongoDB process management
- Service lifecycle (startup/shutdown)
- Event emission and scheduling
- Configuration loading from `Config/config.json`

### 2. Connectors (`Connectors/`)
Modular components that sync data from external services (Twitter, Facebook, Flickr, etc.).
- Each connector lives in its own directory (e.g., `Connectors/twitter/`)
- Data sync is handled by **synclets**, defined in `synclets.json`
- Synclet frequency is configured in seconds (e.g., `frequency: 120`)
- Data is published with service types like `contact/twitter` or `timeline/twitter`

### 3. Collections (`Collections/`)
Normalize and aggregate data by type across multiple connectors.
- 4 main collections: Contacts, Links, Photos, Places
- Provide deduplicated, merged views of data

### 4. Apps (`Apps/`)
User-facing applications that access locker data.
- Run as separate services with their own ports
- Access data via Collections or directly from Connectors
- Main dashboard: `Apps/dashboardv3/`

### 5. Common Libraries (`Common/node/`)
Shared modules used by all components:
- `locker.js`: Client library for apps/connectors
- `lmongoclient.js`: MongoDB connection management
- `lsyncmanager.js`: Synclet scheduling
- `lservicemanager.js`: Service discovery
- `lconfig.js`: Configuration loading
- `lutil.js`: Utility functions

## Key Patterns

### Service Types
The platform uses a type system like MIME types: `{collection}/{connector}`
- Examples: `contact/twitter`, `photo/flickr`, `place/foursquare`
- Defined in `Connectors/{name}/synclets.json` under `provides`

### Data Flow
1. Synclets fetch data from external services
2. Data stored in MongoDB collections named by service type
3. Collections aggregate and normalize data
4. Apps query Collections or MongoDB directly
5. Events notify services of data changes

### Configuration
- `Config/config.json`: Main platform configuration
- `Config/apikeys.json`: Required API keys (not checked in, use `Config/apikeys.json.example`)
- Uses `nconf` for hierarchical config (environment > file > defaults)

## Testing Notes

- **Modern tests**: Mocha with `--growl --timeout 500` in `test/`
- **Legacy tests**: Vows framework in `tests/` with custom runner
- Mock services for testing exist in `tests/Data.tests/node_modules/`
- Tests require `NODE_PATH` to include `Common/node`