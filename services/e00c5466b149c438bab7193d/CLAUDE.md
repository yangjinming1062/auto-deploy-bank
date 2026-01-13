# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

### Development Environment Setup

1.  **Install Dependencies:** The project uses `uv` and a `pyproject.toml` file for dependency management. Install the dependencies using `uv`:
    ```bash
    uv pip install -r requirements.txt
    ```
2.  **Database Setup:** The application requires a database. The `jms` script handles database migrations.

### Running the Application

To run the application, use the `jms` script:

```bash
python jms start all
```

This will start all the necessary services.

### Running Tests

To run the tests, use the following command:

```bash
python apps/manage.py test
```
**Note:** The test command is inferred from the project being a standard Django application.

### Linting

There is no information about a linting command in the project documentation.

## High-level Code Architecture

JumpServer is a monolithic Django application with a modular structure. The core logic is located in the `apps` directory, with each subdirectory representing a different Django app.

*   **`apps/jumpserver`**: The main Django project, containing the settings and base configuration.
*   **`apps/users`**: Manages users and authentication.
*   **`apps/assets`**: Manages assets, such as servers and devices.
*   **`apps/perms`**: Handles permissions and access control.
*   **`apps/audits`**: Contains the audit and logging functionality.
*   **`jms`**: A wrapper script for managing the application services, which calls Django's `manage.py` commands.
*   **`pyproject.toml`**: Defines the project dependencies.
