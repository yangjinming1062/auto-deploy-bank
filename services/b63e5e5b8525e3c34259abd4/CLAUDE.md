# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

### Setup

To set up the development environment, install the required dependencies:

```bash
pip install -r requirements.txt
pip install -r requirements.development.txt
```

### Running the development server

To run the development server, use the following command:

```bash
python manage.py runserver
```

### Running tests

To run the tests, use the following command:

```bash
python manage.py test
```

To run a single test, you can specify the path to the test class or method:

```bash
python manage.py test bugsink.tests.StreamsTestCase
```

### Linting

This project uses `flake8` for linting. The configuration can be found in `tox.ini`. To run the linter, you can use the following command:

```bash
flake8 .
```

## High-level code architecture and structure

Bugsink is a self-hosted error tracking application built with Django. It is designed to be compatible with the Sentry SDK, allowing you to monitor your applications in real-time.

The main application logic is located in the `bugsink` directory. This directory contains the Django project, including settings, URLs, and views. The other directories in the root of the project are individual Django apps that provide specific functionalities, such as `api`, `events`, `issues`, and `users`.

The project follows a standard Django architecture:

- **`bugsink/settings/`**: Contains the Django settings for different environments (e.g., `development.py`, `production.py`).
- **`bugsink/urls.py`**: The main URL configuration for the project.
- **`manage.py`**: The command-line utility for administrative tasks.
- **Templates**: The HTML templates are located in the `templates` directory.
- **Static files**: The static files (CSS, JavaScript, images) are located in the `static` directory.

The application is composed of several Django apps, each responsible for a specific domain:

- **`alerts`**: Handles alert notifications.
- **`api`**: Provides the API endpoints for ingesting events.
- **`bsmain`**: The main application for the Bugsink UI.
- **`events`**: Manages the storage and processing of error events.
- **`issues`**: Groups similar events into issues.
- **`projects`**: Manages projects and their settings.
- **`teams`**: Manages teams and user access.
- **`users`**: Manages user authentication and accounts.
