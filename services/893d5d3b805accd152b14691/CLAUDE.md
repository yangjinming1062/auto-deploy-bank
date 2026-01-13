# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Install Dependencies

To install all dependencies, run:

```bash
uv sync
```

### Linting and Static Analysis

This project uses `pre-commit` to run linting and static analysis checks.

To install the pre-commit hooks:

```bash
uv run pre-commit install
```

To run the linters manually:

```bash
uv run ruff format .
uv run flake8
uv run djlint --check templates
```

To reformat files with `djlint`:

```bash
uv run djlint --reformat .
```

### Running Tests

To run the test suite:

```bash
sh scripts/run-test.sh
```

Tests are located in the `tests/` directory and configured in `pytest.ci.ini`.

### Running the Application Locally

1.  Create a `.env` file from the example:
    ```bash
    cp example.env .env
    ```
2.  Run the Postgres database in Docker:
    ```bash
    docker run -e POSTGRES_PASSWORD=mypassword -e POSTGRES_USER=myuser -e POSTGRES_DB=simplelogin -p 15432:5432 postgres:13
    ```
3.  Run the application:
    ```bash
    alembic upgrade head && flask dummy-data && python3 server.py
    ```

The application will be available at http://localhost:7777.

### Database Migrations

Database migrations are handled by `alembic`. To create a new migration, run:

```bash
sh scripts/new-migration.sh
```

## Architecture

The backend consists of two main components:

*   **`webapp`**: The main Flask application that serves the web interface, API, and OAuth endpoints. The entry point is `server.py`.
*   **`email handler`**: Handles email forwarding and sending. The entry point is `email_handler.py`.

### Directory Structure

-   `app/`: The main Flask application, structured into packages by feature (e.g., `oauth`, `api`, `dashboard`).
-   `static/`: Static assets like CSS, JavaScript, and images.
-   `templates/`: Jinja2 templates for HTML pages and emails.
-   `migrations/`: Alembic database migration scripts.
-   `tests/`: Test files.
-   `scripts/`: Helper scripts for development tasks.
