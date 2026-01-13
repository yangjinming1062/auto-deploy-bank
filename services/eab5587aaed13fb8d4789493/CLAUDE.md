# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Running the application

The primary way to run the application is by using `docker-compose`:

```bash
docker-compose up
```

The application will be available at http://localhost:8080.

### Rebuilding the application

To rebuild the Docker containers from scratch, use the following script:

```bash
./recreate.sh
```

### Stopping the application

To stop the application, run:

```bash
docker-compose down
```

### Managing Dependencies

The Python dependencies are listed in `requirements.txt` and can be installed using `pip`:

```bash
pip install -r requirements.txt
```

## Code Architecture

This is a Python web application built with `aiohttp`. The project is intentionally vulnerable for educational purposes (Damn Vulnerable Python Web Application - DVPWA).

The main application logic is located in the `sqli/` directory.

-   **`run.py`**: The entry point for the application.
-   **`sqli/app.py`**: Initializes the `aiohttp` application, sets up routes, and configures templates.
-   **`sqli/routes.py`**: Defines the application's URL routes.
-   **`sqli/views.py`**: Contains the view handlers for the different routes.
-   **`sqli/dao/`**: Data Access Object layer. This directory contains modules for interacting with the database tables (e.g., `user.py`, `student.py`).
-   **`sqli/services/`**: Contains services for interacting with external components like the database (`db.py`) and Redis (`redis.py`).
-   **`sqli/templates/`**: Contains the Jinja2 templates used for rendering the HTML pages.
-   **`config/`**: Contains configuration files. `dev.yaml` is used for development.
-   **`migrations/`**: Contains SQL scripts for database schema initialization and data seeding.
