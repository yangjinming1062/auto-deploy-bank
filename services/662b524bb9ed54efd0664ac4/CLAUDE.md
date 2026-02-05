# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Roxy-WI is a Flask web interface for managing HAProxy, Nginx, Apache, and Keepalived servers. It provides a GUI for configuration, monitoring, alerting, and remote server management via SSH.

## Tech Stack

- **Web Framework**: Flask 3.0.3 with Flask-APScheduler, Flask-JWT-Extended, Flask-Caching
- **ORM**: Peewee (SQLite by default, MySQL support via config)
- **SSH**: Paramiko for remote server management
- **Database**: SQLite (default) or MySQL
- **Authentication**: JWT with RS256 asymmetric keys
- **Background Jobs**: APScheduler (defined in `app/jobs.py`)

## Development Commands

This project is a deployed application with no test suite or build process. To run the application:

```bash
# Install dependencies
pip install -r requirements.txt

# Create database and initialize
cd /var/www/haproxy-wi/app
./create_db.py

# Run the Flask application
# Typically served via WSGI (app.app.wsgi) or gunicorn/uwsgi
```

## Architecture

### Entry Points

- `app/__init__.py` - Flask app initialization, extension setup (cache, JWT, scheduler), route registration
- `app/config.py` - Configuration class reading from `/etc/roxy-wi/roxy-wi.cfg`
- `app/create_db.py` - Database initialization and default values
- `app/jobs.py` - Scheduled background tasks (cleanup, version checks, status updates)
- `app/login.py` - Authentication handlers
- `app/migrate.py` - Database migration entry point

### Route Organization (Blueprints)

Routes are organized by feature in `app/routes/`:
- `main/` - Main pages and dashboard
- `overview/` - Server/service overview pages
- `add/` - Add servers, services, configurations
- `config/` - Configuration management
- `service/` - Service control (start/stop/restart)
- `logs/` - Log viewing and analysis
- `metrics/` - Metrics dashboards
- `waf/` - Web Application Firewall management
- `runtime/` - Runtime API for dynamic config changes
- `smon/` - Service monitoring (ping, TCP, HTTP, DNS checks)
- `checker/` - Service health checker
- `portscanner/` - Port scanning functionality
- `ha/` - High availability cluster management
- `udp/` - UDP load balancer management
- `admin/` - Admin functions
- `user/` - User management
- `server/` - Server management
- `channel/` - Notification channel setup (Telegram, Slack, etc.)
- `install/` - Service installation

### Module Organization (`app/modules/`)

- `db/` - Database models (`db_model.py`) and SQL operations (one file per feature)
- `roxywi/` - Core Roxy-WI functionality: auth, common utilities, error handling, logging, metrics, WAF
- `server/` - SSH connections (`ssh_connection.py`), server operations, SSH key management
- `service/` - Service management operations
- `config/` - HAProxy/Nginx/Apache/Keepalived config generation and parsing
- `common/` - Shared utilities including `common.py` with logging, auth helpers
- `tools/` - Utility functions

### Database Models

All models in `app/modules/db/db_model.py` using Peewee. Key models:
- `User`, `Role`, `Groups`, `UserGroups` - User and authorization
- `Server` - Managed servers with credentials
- `Cred` - SSH credentials (password or key-based)
- `SMON` - Service monitoring checks
- `Metrics`, `WafMetrics`, `NginxMetrics`, `ApacheMetrics` - Performance metrics
- `Alerts`, `ActionHistory` - Alerting and audit trail
- `HaproxySection`, `NginxSection` - Parsed config sections
- `HaCluster*` - HA cluster management tables
- `UDPBalancer` - UDP load balancer configurations

### Configuration

- Main config: `/etc/roxy-wi/roxy-wi.cfg` (parsed via `app/modules/roxy_wi_tools.py` `GetConfigVar`)
- JWT keys: `/var/lib/roxy-wi/keys/roxy-wi-key` and `.pub`
- Logs: `/var/log/roxy-wi/roxy-wi.log`

### Key Patterns

1. **SSH Connections**: Use `SshConnection` context manager from `app/modules/server/ssh_connection.py` with `with ssh_connection(...) as ssh:` pattern

2. **Database Access**: Import SQL modules from `app/modules/db/` (e.g., `import app.modules.db.server as server_sql`)

3. **Logging**: Use `from app.modules.roxywi import logger` and `logger.info/warning/error()`

4. **Error Handling**: Use `handle_exceptions()` from `app/modules/roxywi/common.py` with `keep_history=True` for auditable actions

5. **JWT Claims**: Get claims via `get_jwt_token_claims()` from `app/modules/roxywi/common.py`

6. **Group-based Access**: Users belong to groups; access controlled via `check_user_group_for_flask()` and `is_user_has_access_to_group()`