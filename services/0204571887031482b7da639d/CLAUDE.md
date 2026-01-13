# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**flaskSaas** - A Flask-based SaaS boilerplate starter project, forked from Max Halford's flask-boilerplate. Provides user authentication, form handling, email confirmation, admin panel, and logging. Intended as a starting point for SaaS applications.

## Technology Stack

- **Backend**: Flask 0.10.1 with SQLAlchemy, Flask-Login, Flask-WTF, Flask-Mail, Flask-Admin, Flask-Script
- **Database**: SQLite (default) via SQLAlchemy
- **Frontend**: Semantic UI, Leaflet JS (for maps)
- **Server**: Gunicorn with Nginx reverse proxy
- **Deployment**: Docker and docker-compose

## Common Development Commands

### Setup and Installation
```bash
make install && make dev  # Install dependencies and setup dev environment
python manage.py initdb   # Create the SQLite database
python manage.py runserver # Start development server (default: localhost:5000)
```

### Configuration Management
```bash
make dev   # Symlink app/config_dev.py to app/config.py
make prod  # Symlink app/config_prod.py to app/config.py
```

### Database Operations
```bash
python manage.py initdb  # Create all database tables
python manage.py dropdb  # Delete database (with confirmation prompt)
python manage.py shell   # Open Python shell with app context
```

### Docker Operations
```bash
docker-compose up        # Start containers
docker-compose up -d     # Start containers in detached mode
docker-compose down      # Stop containers
```

## Application Architecture

### Directory Structure
```
app/
├── __init__.py           # Application factory and extension setup
├── models.py             # SQLAlchemy models (User model)
├── admin.py              # Flask-Admin configuration
├── logger_setup.py       # Logging configuration (structlog)
├── config.py             # Active config (symlink to *_dev.py or *_prod.py)
├── config_common.py      # Shared configuration settings
├── config_dev.py         # Development configuration
├── config_prod.py        # Production configuration
├── views/                # Route handlers
│   ├── main.py          # Index, map, contact routes
│   ├── user.py          # Authentication routes (signup, signin, password reset)
│   ├── error.py         # Error handlers
│   └── __init__.py
├── forms/               # WTForms form definitions
│   ├── user.py          # User-related forms
│   └── __init__.py
├── toolbox/             # Utility functions and helpers
│   ├── email.py         # Email utilities
│   └── __init__.py
├── static/              # Static assets (CSS, JS, images)
└── templates/           # Jinja2 templates
    ├── layout.html      # Base layout
    ├── macros/          # Reusable template macros
    └── [various pages]
```

### Core Components

**app/__init__.py:1-46** - Application factory that initializes:
- Flask app with config
- SQLAlchemy database
- Mail server (Gmail SMTP by default)
- Debug Toolbar
- Bcrypt password hashing
- Login manager with user loader
- Flask-Admin integration

**app/models.py:7-41** - User model with:
- Email as primary key
- Password hashing with bcrypt
- Full name property
- Login integration (UserMixin)
- Paid/subscription tracking fields

**manage.py:15-26** - Management commands:
- `initdb` - Create database tables
- `dropdb` - Drop database tables (with safety prompt)

### Key Configuration (app/config_common.py)

- **Database**: SQLite at `sqlite:///app.db`
- **Mail**: Gmail SMTP server (flask.boilerplate@gmail.com)
- **Secret Key**: 'houdini' (CHANGE in production!)
- **Admin**: admin/pa$$word (CHANGE in production!)
- **Timezone**: Europe/Paris

**Security Note**: Default credentials in config_common.py must be changed before production use.

### View Organization

- **main routes** (`/`, `/index`, `/map`, `/contact`): `app/views/main.py:6-27`
- **user authentication** (`/signin`, `/signup`, `/signout`, password reset): `app/views/user.py`
- **error handlers** (404, 500): `app/views/error.py`

### User Authentication Flow

The project implements email-based user registration and authentication with confirmation emails:
1. User submits signup form
2. Confirmation email sent via Flask-Mail
3. User confirms via email link
4. User can then sign in with email/password
5. Password reset via email confirmation

## Code Style and Quality

- **Linting**: Pylint configured in `.pylintrc` with max line length of 100 characters
- **Python**: Python 3.x compatible
- **Flask extensions**: Uses older Flask-SQLAlchemy and Flask-Mail syntax (`flask.ext.*`)

## Notes

- This is an older Flask project (Flask 0.10.1) - some syntax differs from modern Flask
- No test suite currently exists
- Uses legacy `flask.ext.*` import style
- Email credentials are hardcoded in config_common.py - for production, use environment variables
- SQLite database file is at `app/app.db` (checked into git per .gitignore showing it's not ignored)