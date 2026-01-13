# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

ArcherySec is a Django-based open-source vulnerability assessment and management tool. It integrates with popular security scanning tools (OWASP ZAP, OpenVAS, Arachni, etc.) to perform web application and network vulnerability scans, correlate results, and manage vulnerabilities through a centralized platform.

## Architecture

This is a Django application (`manage.py` in root) with the following major modules:

- **webscanners/**: Web application vulnerability scanning (ZAP, Arachni, Burp, Acunetix, Netsparker, WebInspect)
- **networkscanners/**: Network vulnerability scanning (OpenVAS, Nmap)
- **staticscanners/**: Static code analysis (Bandit, RetireJS, Dependency Check)
- **APIScan/**: API vulnerability scanning and REST API endpoints
- **projects/**: Project and scan management
- **osintscan/**: Open Source Intelligence (OSINT) scanning
- **jiraticketing/**: JIRA integration for vulnerability tracking
- **archerysettings/**: Application settings and configuration
- **tools/**: Utility tools
- **manual_scan/**: Manual scan management
- **Dashboard/**: Main dashboard and reporting

## Common Commands

### Initial Setup

```bash
# Clone and setup
git clone https://github.com/archerysec/archerysec.git
cd archerysec
cp archerysecurity/local_settings.sample.py archerysecurity/local_settings.py

# Automated installation
./install.sh

# Manual installation
pip install -r requirements.txt
python manage.py collectstatic
python manage.py migrate
python manage.py initadmin
```

### Running the Application

```bash
# Start background task processor (required)
python manage.py process_tasks &

# Run development server
python manage.py runserver 0.0.0.0:8000
```

### Docker Development

```bash
# Start all services with PostgreSQL
docker-compose up -d

# This starts:
# - archerysec web application
# - archerysec-worker (background tasks)
# - PostgreSQL database
# - ZAP scanner
# - Arachni scanner
# - OpenVAS scanner
# - Mailhog (for email testing)
```

### Testing

```bash
# Run integration tests
./integration-test.sh

# Run security linting with Bandit
pip install bandit
bandit -r . -x venv

# Run code quality checks with flake8
flake8
```

### Code Quality Tools

```bash
# Install pre-commit hooks (required for contributors)
pre-commit install

# Run pre-commit checks on all files
pre-commit run --all-files
```

## Configuration

### Settings Files

- `archerysecurity/settings/base.py`: Base Django settings
- `archerysecurity/settings/development.py`: Development-specific settings
- `archerysecurity/settings/production.py`: Production-specific settings
- `archerysecurity/local_settings.sample.py`: Template for local configuration

### Environment Variables (Docker)

- `DB_PASSWORD`, `DB_USER`, `DB_NAME`, `DB_HOST`: Database configuration
- `DJANGO_SETTINGS_MODULE`: Settings module to use (default: `archerysecurity.settings.base`)
- `DJANGO_SECRET_KEY`: Django secret key (always set in production)
- `DJANGO_DEBUG`: Set to `1` for debug mode
- `ARCHERY_WORKER`: Set to `True` to run as background worker instead of web server

### Database

- Default: SQLite (`db.sqlite3` in project root)
- Docker Compose: PostgreSQL 10.1

### Background Tasks

The application uses `django-background-tasks` for async processing:
- Run background worker: `python manage.py process_tasks`
- REFRESH_TIMER setting controls task polling interval

## Key Dependencies

- Django (web framework)
- django-rest-framework (REST API)
- django-background-tasks (async tasks)
- django-stronghold (authentication middleware)
- openvas_lib (OpenVAS integration)
- python-owasp-zap-v2.4 (ZAP integration)
- selenium (web application scanning)
- psycopg2-binary (PostgreSQL adapter)
- reportlab, WeasyPrint (PDF generation)

## Testing & CI/CD

CI is configured via Travis CI (`.travis.yml`) with tests:
- Integration tests using Docker
- Docker Bench Security
- Bandit static security analysis

## External Tool Integration

### ZAP (OWASP ZAP)

```bash
# Start ZAP in daemon mode
zap.sh -daemon -host 0.0.0.0 -port 8080 -config api.disablekey=true -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true

# Configure in ArcherySec: Settings → ZAP Setting
# - ZAP API Key: Leave blank if using daemon mode
# - ZAP API Host: e.g., 127.0.0.1
# - ZAP API Port: 8080
```

### OpenVAS

```bash
# OpenVAS runs on port 9390 by default
# Configure in ArcherySec: Settings → OpenVAS Setting
```

### Arachni

```bash
# Docker-based Arachni REST server
# Runs on port 9292
```

## API Documentation

- Official API docs: https://archerysec.github.io/archerysecapi/
- Demo application: https://archerysec-test.herokuapp.com/
  - Username: archerysec
  - Password: archerysec@archerysec

## Development Notes

- Python 2.7 (legacy project - planned migration to Python 3)
- Uses django-stronghold for authentication (all routes require login except `/api/*` and `/admin/*`)
- Pre-commit hooks enforce code quality via flake8
- Docker setup uses Ubuntu 18.04 base image
- Static files collected via `collectstatic`
- Migrations are in each app's `migrations/` directory

## Directory Structure

```
├── archerysecurity/          # Django project settings
├── webscanners/              # Web app vulnerability scanners
├── networkscanners/          # Network scanners (OpenVAS, Nmap)
├── staticscanners/           # Static code analysis tools
├── APIScan/                  # API scanning and REST endpoints
├── projects/                 # Project and scan management
├── osintscan/                # OSINT tooling
├── jiraticketing/            # JIRA integration
├── docs/                     # Documentation
├── docker-files/             # Docker initialization scripts
├── tools/                    # Utility tools
└── requirements.txt          # Python dependencies
```