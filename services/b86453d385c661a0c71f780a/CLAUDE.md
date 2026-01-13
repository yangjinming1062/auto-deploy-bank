# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-level Architecture

This project, `sqlite-web`, is a web-based SQLite database browser built with Python.

-   **Framework**: It uses the [Flask](http://flask.pocoo.org) web framework.
-   **Main Application**: The core application logic, including URL routing and views, is located in `sqlite_web/sqlite_web.py`.
-   **Database Interaction**: The application uses the [peewee](http://docs.peewee-orm.com) ORM for database interactions.
-   **Frontend**:
    -   HTML templates are located in the `sqlite_web/templates/` directory.
    -   Static assets (CSS, JavaScript, images) are in the `sqlite_web/static/` directory.
-   **Entry Point**: The application is launched via the `main` function in `sqlite_web/sqlite_web.py`, which is set up as a console script in `setup.py`.

## Common Commands

### Installation

To set up the development environment, install the dependencies using pip:

```sh
pip install -r requirements.txt
```

Alternatively, you can install the package in editable mode:

```sh
pip install -e .
```

### Running the Application

To run the web server, use the `sqlite_web` command followed by the path to a SQLite database file:

```sh
sqlite_web /path/to/database.db
```

Several command-line options are available for changing the port, host, enabling debug mode, etc. For a full list, see the "Command-line options" section in `README.md`.

### Building and Running with Docker

To build and run the application using Docker:

```sh
cd docker/
docker build -t coleifer/sqlite-web .
docker run -it --rm \
    -p 8080:8080 \
    -v /path/to/your-data:/data \
    -e SQLITE_DATABASE=db_filename.db \
    coleifer/sqlite-web
```

### Testing

No automated test suite (e.g., using `pytest` or `unittest`) was found in the repository. Manual testing by running the application is required.
