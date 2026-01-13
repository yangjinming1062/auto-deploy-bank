# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Setup Development Environment
```bash
# Create a virtual environment with all dependencies
make virtualenv
source .venv/bin/activate

# Install git hooks for patch validation
make hooks
cp common/hooks/post-commit .git/hooks
```

### Code Quality & Validation
```bash
# Run comprehensive validation (checks style, tests, and documentation)
./common/validate.sh

# Run validation with quick mode (skip slow tests)
./common/validate.sh --quick

# Skip JavaScript tests
./common/validate.sh --no-js

# Run only Python tests
trial buildbot.test buildbot_worker.test

# Run a specific test
trial buildbot.test.unit.test_config

# Check formatting
pylint
flake8

# Sort imports and auto-format Python code
isort -rc worker master
```

### Frontend Development
```bash
# Install frontend dependencies
make frontend_deps

# Build frontend from source (requires Node.js and Yarn)
make frontend

# Build documentation only
make docs

# Check documentation for issues
make docschecks

# Upgrade frontend dependencies
make frontend_yarn_upgrade
```

### Testing
```bash
# Run all Python tests
trial buildbot.test buildbot_worker.test

# Set temp directory for faster integration tests (RAM-based)
export TRIALTMP=/dev/shm
trial buildbot.test buildbot_worker.test

# Run specific test suite
trial buildbot.test.unit.test_master
trial buildbot_worker.test.test_commands
```

## High-Level Architecture

Buildbot is a **distributed continuous integration framework** with a multi-component architecture:

### Core Components

1. **Master** (`master/`) - Central coordinator service
   - Orchestrates builds, manages workers, schedules tasks
   - Key modules:
     - `buildbot/master.py` - Main BuildMaster class
     - `buildbot/config.py` - Configuration loading and validation
     - `buildbot/data/` - REST API and data connector
     - `buildbot/db/` - Database layer (SQLAlchemy-based)
     - `buildbot/schedulers/` - Build scheduling logic
     - `buildbot/steps/` - Build step implementations
     - `buildbot/worker/` - Worker management
     - `buildbot/status/` - Status reporting
     - `buildbot/www/` - Web interface backend

2. **Worker** (`worker/`) - Build execution agent
   - Connects to master via Twisted PB protocol
   - Executes build commands in isolated environment
   - Reports build results back to master
   - Key files:
     - `buildbot_worker/base.py` - WorkerBase class
     - `buildbot_worker/commands/` - Build command implementations
     - `buildbot_worker/runprocess.py` - Process execution

3. **Web Interface** (`www/`) - Angular-based UI
   - Multiple Angular packages: `base`, `console_view`, `waterfall_view`, `grid_view`, etc.
   - Pre-built bundles distributed via Python wheel packages
   - Communicates with master via REST API and WebSocket (WAMP)

### Key Design Patterns

- **Plugin System**: Extensible via `buildbot/plugins/` and Zope interfaces
- **Service Architecture**: Built on Twisted services (`buildbot/util/service.py`)
- **Database Layer**: SQLAlchemy-based connector pattern in `buildbot/db/connector.py:63`
- **Message Queue**: MQ connector pattern in `buildbot/mq/connector.py:52`
- **Reactive Configuration**: Hot-reconfiguration without restart
- **Event-Driven**: Twisted deferreds throughout codebase

### Configuration

- Primary config: `master.cfg` (Python-based configuration)
- Configuration is loaded via `buildbot/config.py:63` FileLoader
- Supports dynamic reconfiguration

### Development Workflow

1. Run `./common/validate.sh` before submitting patches
2. All patches require release notes in `master/docs/relnotes/index.rst` (towncrier format)
3. Follow Python coding style enforced by flake8/pylint
4. Frontend changes require rebuilding bundles (or use prebuilt versions)

### Key Technologies

- **Backend**: Python (Twisted async framework)
- **Frontend**: AngularJS (CoffeeScript), bundled as wheels
- **Database**: SQLAlchemy (SQLite, MySQL, PostgreSQL)
- **Protocol**: Twisted PB ( Perspective Broker )
- **API**: REST API with WebSocket/WAMP for real-time updates
- **Build System**: Custom setup.py with Twisted plugins

### Testing Infrastructure

- Uses Twisted Trial test framework
- Integration tests need `TRIALTMP` set to RAM-based tmpfs
- Frontend tests require Node.js/NPM (can skip with `--no-js`)
- Documentation built with Sphinx

### Important Notes

- This is a **mature codebase** with extensive backward compatibility
- Uses both **legacy** (PB) and **modern** (REST API) communication patterns
- Worker compatibility is maintained across multiple master versions
- Release notes managed via towncrier (see `pyproject.toml` configuration)