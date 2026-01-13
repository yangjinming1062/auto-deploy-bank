# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

httpbin is a simple HTTP Request & Response Service written in Python using Flask. It provides various HTTP endpoints that echo back request data, making it useful for testing HTTP clients and debugging HTTP interactions.

## Common Commands

### Installation
```bash
pipenv install
```

### Running Tests
```bash
# Run all tests
python test_httpbin.py

# Run tests with tox (tests against Python 2.7, 3.6, 3.7)
tox

# Run a specific test
python -m unittest test_httpbin.TestHttpBin.test_get
```

### Running the Application

**Local development:**
```bash
gunicorn httpbin:app -k gevent
```

**Docker:**
```bash
docker run -p 80:80 kennethreitz/httpbin
```

**Using docker-compose:**
```bash
docker-compose up
```

### Building and Packaging
```bash
python setup.py sdist bdist_wheel
```

### Code Quality
```bash
# Using tox for multi-version testing
tox -e py36
```

## High-Level Architecture

### Core Structure

- **httpbin/core.py** - Main Flask application and HTTP endpoint handlers. Contains:
  - Flask app configuration and initialization (line 85)
  - All route handlers (/get, /post, /anything, /status codes, /redirect, etc.)
  - JSON response helpers and CORS handling

- **httpbin/helpers.py** - Utility functions for:
  - Authentication (basic, digest, bearer)
  - Header processing
  - Status code handling
  - Cookie management
  - Encoding/decoding utilities

- **httpbin/utils.py** - Helper utilities like weighted choice selection

- **httpbin/structures.py** - Custom data structures (CaseInsensitiveDict)

- **httpbin/filters.py** - Content filtering and transformation logic

- **httpbin/templates/** - Jinja2 HTML templates for web endpoints

- **httpbin/static/** - Static assets (favicon.ico)

### Key Application Patterns

- **Flask Routes**: Defined as `@app.route()` decorators throughout httpbin/core.py
- **Testing**: Uses Python's unittest framework in test_httpbin.py at project root
- **JSON Responses**: Custom `jsonify()` wrapper ensures trailing newline (httpbin/core.py:72)
- **CORS**: Automatically added via `before_request()` and `set_cors_headers()` (httpbin/core.py:201, 217)
- **Authentication**: Handlers in helpers.py (check_basic_auth, check_digest_auth)
- **Response Echoing**: Most endpoints echo back request data (headers, args, form, JSON, etc.)

### Dependencies

- **Flask** - Web framework
- **gunicorn + gevent** - WSGI server for production
- **brotlipy** - Brotli compression support
- **flasgger** - Swagger UI integration
- **six** - Python 2/3 compatibility
- **werkzeug** - WSGI utilities

### Deployment

- **Docker**: Containerized with Dockerfile (Python 3.6)
- **Heroku**: Procfile configured for gunicorn
- **CI**: Travis CI configuration for Python 2.7, 3.6, 3.7