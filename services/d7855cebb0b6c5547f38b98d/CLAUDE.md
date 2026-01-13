# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a **Discover Flask** tutorial project - a full-stack web application built with Flask. It's a simple blog/messaging system with user authentication, demonstrating best practices for Flask development including blueprints, SQLAlchemy ORM, migrations, and testing.

## Technology Stack

- **Python 2.7** (note: very outdated, requires Python 2.7)
- **Flask 0.10.1** - Web framework
- **SQLAlchemy 0.9.4** - Database ORM (PostgreSQL)
- **Flask-Migrate** - Database migration management
- **Flask-Login** - User session management
- **Flask-Bcrypt** - Password hashing
- **Flask-WTF** - Form handling and CSRF protection
- **Gunicorn** - WSGI server for production
- **Coverage.py** - Test coverage reporting

## Development Commands

### Running the Application

```bash
# Development server (auto-reload enabled)
python run.py

# Production server (Heroku)
gunicorn run:app
```

### Database Management

```bash
# Create database tables
python db_create.py

# Create users table
python db_create_users.py

# Run database migrations (Flask-Migrate)
python manage.py db upgrade
python manage.py db downgrade
python manage.py db history
python manage.py db current
```

### Testing

```bash
# Run all tests
python manage.py test

# Run tests with coverage report
python manage.py cov

# Run tests manually
python -m unittest discover tests
```

The coverage report generates HTML in `coverage/` directory and prints a summary to console.

## Project Structure

```
/
├── manage.py                 # Flask-Script manager (commands for running, testing, migrations)
├── run.py                    # Application entry point for development
├── config.py                 # Configuration classes (Dev, Test, Prod)
├── requirements.txt          # Python dependencies
├── Procfile                  # Heroku deployment config
├── .travis.yml              # CI configuration
│
├── project/                  # Main application package
│   ├── __init__.py          # App factory, blueprint registration, login manager
│   ├── models.py            # SQLAlchemy models (User, BlogPost)
│   │
│   ├── users/               # Users blueprint
│   │   ├── views.py         # /login, /logout, /register routes
│   │   └── forms.py         # LoginForm, RegisterForm (WTForms)
│   │
│   ├── home/                # Home blueprint
│   │   ├── views.py         # /, /welcome routes
│   │   └── forms.py         # MessageForm (WTForms)
│   │
│   ├── static/              # CSS, JS, images
│   └── templates/           # Jinja2 templates
│
├── tests/                    # Unit tests
│   ├── base.py              # BaseTestCase (test setup/teardown)
│   ├── test_users.py        # User tests (registration, login, logout)
│   ├── test_blog.py         # Blog post tests
│   └── test_basic.py        # Basic functionality tests
│
└── migrations/               # Database migration scripts
    └── versions/            # Alembic migration files
```

## Architecture

### Application Factory Pattern
The application is created in `project/__init__.py`:
- Flask app instance initialized with config from environment
- SQLAlchemy database instance
- Bcrypt password hashing
- LoginManager configured
- Blueprints registered: `users_blueprint`, `home_blueprint`

### Blueprint Organization
The app uses **Blueprints** for modular architecture:

1. **users Blueprint** (`project/users/views.py`):
   - `/login` - User authentication
   - `/logout` - Session termination
   - `/register/` - User registration

2. **home Blueprint** (`project/home/views.py`):
   - `/` - Main dashboard (requires login) - create/view blog posts
   - `/welcome` - Public welcome page

### Models (`project/models.py`)

Two main models:
- **User**: Stores user data with password hashing via bcrypt
- **BlogPost**: Blog entries with foreign key to User

Both models implement Flask-Login required methods (`is_authenticated`, `is_active`, `is_anonymous`, `get_id`).

### Configuration (`config.py`)
Three configuration classes:
- **BaseConfig**: Base configuration
- **TestConfig**: In-memory SQLite for testing
- **DevelopmentConfig**: Debug enabled
- **ProductionConfig**: Debug disabled

Configuration loaded from `APP_SETTINGS` environment variable.

### Testing Strategy
Tests extend `BaseTestCase` which:
- Sets up in-memory SQLite database
- Creates test user and blog post in `setUp()`
- Tears down database in `tearDown()`

Tests cover:
- User registration and validation
- Login/logout functionality
- Password hashing
- Blog post creation
- CSRF protection via Flask-WTF

## Database Setup

The app uses PostgreSQL in production (DATABASE_URL environment variable).

Local development options:
1. **SQLite** (via DATABASE_URL=sqlite:///:memory: or sqlite:///database.db)
2. **PostgreSQL** (via PostgreSQL DATABASE_URL)

Example DATABASE_URL formats:
```
# SQLite
export DATABASE_URL=sqlite:///database.db
export APP_SETTINGS=config.DevelopmentConfig

# PostgreSQL
export DATABASE_URL=postgresql://user:password@localhost/database_name
export APP_SETTINGS=config.DevelopmentConfig

# Test
export DATABASE_URL=sqlite:///:memory:
export APP_SETTINGS=config.TestConfig
```

## Key Features

### Authentication Flow
1. User registers at `/register/` with username, email, password
2. User logs in at `/login` with username and password
3. Session managed by Flask-Login
4. Passwords hashed using bcrypt
5. Protected routes require `@login_required` decorator

### Blog/Messaging System
- Authenticated users can create posts with title and description
- All posts displayed on home dashboard
- Posts linked to author via foreign key

### Form Handling
All forms use Flask-WTF with CSRF protection:
- `LoginForm` - username and password
- `RegisterForm` - username, email, password, confirm password
- `MessageForm` - title and description (max 140 chars)

## Deployment

Configured for **Heroku deployment**:
- `Procfile`: `web: gunicorn run:app`
- Uses Gunicorn WSGI server
- Requires environment variables: `APP_SETTINGS`, `DATABASE_URL`

## Important Notes

⚠️ **This is a tutorial project (not production-ready)**:
- Python 2.7 (end-of-life)
- Very old Flask version (0.10.1 from 2014)
- Security configurations may be outdated
- For production use, upgrade to Python 3.x and modern Flask

The codebase serves as a learning reference for Flask best practices including blueprints, migrations, testing, and authentication.