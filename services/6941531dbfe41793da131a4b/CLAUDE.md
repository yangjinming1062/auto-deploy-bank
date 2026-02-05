# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

changedetection.io is a web-based change detection monitoring tool. It watches URLs for content changes and sends notifications via Discord, Email, Slack, Telegram, Webhook, and 50+ other services using the apprise library.

## Development Commands

### Install and Run
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application (entry point: changedetectionio/__init__.py)
python changedetectionio -d /path/to/data -p 5000

# Run in batch mode (process queue then exit, useful for CI/CD)
python changedetectionio -d /path/to/data -b -r all

# Docker development
docker compose up -d
```

### Testing
```bash
# Run all tests in parallel (18 workers, use -n auto for auto-detection)
pytest tests/ -n 18 --dist=loadfile -vv

# Run a single test file
pytest tests/test_notification.py -vv

# Run a single test
pytest tests/test_notification.py::test_send_notification -vv

# Run unit tests only
pytest tests/unit/ -vv

# Run with custom datastore path
pytest --datastore-path=/tmp/test-datastore tests/test_api.py

# Run with TRACE logging visible
pytest tests/test_api.py -vv --log-cli-level=TRACE
```

### Linting and Formatting
```bash
# Lint with ruff (configured in .ruff.toml)
ruff check .              # Full check
ruff check . --select B,E,F,I,N,UP,C  # All enabled rules

# Fix auto-fixable issues
ruff check . --fix

# Format code
ruff-format .

# Run pre-commit hooks
pre-commit run --all-files
```

### Building
```bash
# Build the Docker container
docker build -t changedetection.io .

# Build Python package
python setup.py build_py
```

## Architecture

### Core Application Flow

1. **Startup** (`changedetectionio/__init__.py`): Entry point that initializes Flask app, datastore, workers
2. **Flask App** (`flask_app.py`): Handles HTTP requests, Socket.IO, UI routes, API endpoints
3. **Store** (`store/`): Manages JSON-based persistence for watches, tags, settings
4. **Workers** (`worker_pool.py`): Background processes that fetch and check URLs
5. **Scheduler** (`ticker_thread_check_time_launch_checks`): Determines when watches should be rechecked

### Key Directories

| Directory | Purpose |
|-----------|---------|
| `blueprint/` | Flask blueprints for modular feature organization |
| `api/` | REST API endpoints (Flask-RESTful) |
| `model/` | Data models (Watch, Tag, App) |
| `store/` | Data persistence layer |
| `content_fetchers/` | URL fetching implementations |
| `processors/` | Content processing before diff (text, JSON, image) |
| `conditions/` | Conditional triggering system |
| `notification/` | Notification handling via apprise |
| `realtime/` | Socket.IO server for real-time updates |

### Data Model

**Watch** (`model/Watch.py`):
- UUID-identified watched URLs with configuration
- Contains: url, fetch_backend, filters, triggers, scheduler, notifications, browser_steps
- Processors: `text_diff`, `text_json_diff`, `restock_diff`, `screenshot_diff`
- Per-watch directory in datastore: `{datastore}/{uuid}/`

**DataStore** (`store/__init__.py`):
- Main `ChangeDetectionStore` class manages all data
- Settings in `changedetection.json`
- Watches stored as individual `{uuid}/watch.json` files
- Snapshots stored in watch directories

### Content Fetchers

| Fetcher | File | Use Case |
|---------|------|----------|
| requests | `content_fetchers/requests.py` | Fast, no-JS pages |
| playwright | `content_fetchers/playwright.py` | JS-enabled, visual selector |
| puppeteer | `content_fetchers/puppeteer.py` | Alternative JS fetcher |
| selenium | `content_fetchers/webdriver_selenium.py` | WebDriver support |

### Processors

Processors extract/filter content before diff:
- `text_diff`: Standard text comparison
- `text_json_diff`: JSON-aware comparison with JSONPath/jq
- `restock_diff`: Product price/stock detection from metadata
- `screenshot_diff`: Visual comparison (requires OpenCV)

### Queue System

Two priority queues via `queue_handlers.py`:
- `update_q`: Watch recheck queue (prioritized by time)
- `notification_q`: Notification delivery queue
- Workers process from queues using `worker_pool.py`

### Plugin System

Uses `pluggy` for plugins (`pluggy_interface.py`):
- Content fetchers, processors, notification handlers extend via hook specs
- Hooks: `fetcher`, `processor`, `notification_handler`
- Templates searched in plugin directories

### Scheduler

Time-based scheduling in `time_handler.py`:
- Supports day-of-week and time-of-day constraints
- Per-watch or system-wide settings
- Timezone-aware (configurable via `scheduler_timezone_default`)

### i18n/Internationalization

- Flask-Babel for translations
- Translation files in `translations/`
- Template helpers: `gettext`, `get_flag_for_locale`, `available_languages`

## Important Patterns

### Multiprocessing (Python 3.12+)
All `Process()` calls use explicit context:
```python
import multiprocessing
ctx = multiprocessing.get_context('spawn')
p = ctx.Process(target=...)
```
This prevents deadlocks from forked locks.

### DataStore Access
- Access via `flask_app.app.config['DATASTORE']` or global `datastore` variable
- Thread-safe with `lock` attribute
- Changes mark watch/settings as `dirty` for async save

### Signals
Uses `blinker` for event publication:
- `watch_check_update`: Sent when watch check completes
- Defined in `flask_app.py` as module-level singleton

### API Authentication
- API access token in `settings/application/api_access_token`
- Header: `x-api-key: {token}`
- Token generated on first run

### CSS Dark Mode
Cookie-based via `css_dark_mode` cookie, filter: `get_darkmode_state()`

## Configuration

### Environment Variables
| Variable | Purpose |
|----------|---------|
| `FETCH_WORKERS` | Number of concurrent fetch workers (default: from settings) |
| `NOTIFICATION_WORKERS` | Number of notification delivery workers |
| `LISTEN_HOST` | Bind address (default: 0.0.0.0) |
| `PORT` | HTTP port (default: 5000) |
| `BASE_URL` | Public URL for notification links |
| `MINIMUM_SECONDS_RECHECK_TIME` | Min seconds between checks |
| `LOGGER_LEVEL` | Log level (DEBUG, INFO, TRACE, etc.) |
| `PLAYWRIGHT_DRIVER_URL` | Remote Playwright WebSocket URL |
| `WEBDRIVER_URL` | Selenium WebDriver URL |
| `SOCKETIO_MODE` | `threading` (default) or `gevent` |

### Settings File
`changedetection.json` contains:
- `settings/requests/`: Workers, time between checks, proxies
- `settings/application/`: Password, base URL, UI settings, tags
- `settings/headers/`: Global request headers

## Testing Notes

- Tests use `pytest-flask` with `LiveServer` fixture
- Xdist for parallel execution (tests in same file run on same worker)
- Each test gets isolated datastore via `prepare_test_function` fixture
- Log files per test in `changedetectionio/tests/logs/`
- Browser tests require `sockpuppetbrowser` or selenium container
- Short timeout (5s) for fetch in tests via `DEFAULT_SETTINGS_REQUESTS_TIMEOUT`

## Code Conventions

- Line length: 100 characters (ruff)
- Indent: 4 spaces
- Python 3.10+ required
- All `Process()` must use spawn context
- New features as Flask blueprints in `blueprint/`
- Tests required for new functionality