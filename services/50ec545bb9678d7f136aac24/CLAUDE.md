# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

The primary entrypoint for development tasks is `manage.py`.

*   **Running the application:**
    *   **Locally:** `honcho start -e config.env -f Local`
    *   **With Docker:** `docker-compose up`
*   **Running tests:** `python manage.py test`
*   **Formatting code:** `python manage.py format`
*   **Database:**
    *   **Recreate the database:** `python manage.py recreate_db`
    *   **Set up for development:** `python manage.py setup_dev`
    *   **Add fake data:** `python manage.py add_fake_data`

## Architecture

This is a Flask application that uses a modular structure with Blueprints.

*   **Blueprints:** The application is divided into three main blueprints located in the `app/` directory:
    *   `main`: Core application logic.
    *   `account`: User registration, login, and account management.
    *   `admin`: Administrative interface.
*   **Database:** The application uses Flask-SQLAlchemy for database interactions. The models are defined in the `app/models/` directory.
*   **Forms:** Flask-WTF is used for forms, which are defined within each blueprint's `forms.py` file.
*   **Asynchronous Tasks:** Redis Queue is used for handling asynchronous tasks.
*   **Static Assets:** Flask-Assets is used for asset management, including SCSS compilation.
