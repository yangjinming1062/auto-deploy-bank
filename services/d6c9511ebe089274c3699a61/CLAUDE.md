# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

### Docker (Recommended)

*   **Run development server:** `docker compose up flask-dev`
*   **Run production server:** `docker compose up flask-prod`
*   **Run Flask CLI commands:** `docker compose run --rm manage <<COMMAND>>`
*   **Run tests:** `docker compose run --rm manage test`
*   **Run linter:** `docker compose run --rm manage lint`
*   **Database migrations:**
    *   `docker compose run --rm manage db migrate` (generates migration)
    *   `docker compose run --rm manage db upgrade` (applies migration)

### Local Development (without Docker)

*   **Installation:**
    *   If using pipenv: `pipenv install --dev` then `pipenv shell`
    *   Otherwise: `pip install -r requirements/dev.txt`
*   **Run development server:** `npm start`
*   **Run tests:** `flask test`
*   **Run linter:** `flask lint`
*   **Database migrations:**
    *   `flask db migrate` (generates migration)
    *   `flask db upgrade` (applies migration)

## High-level code architecture and structure

This is a cookiecutter template for creating a Flask project. It uses a modular structure with Blueprints and an Application Factory pattern.

Key features include:

*   **Authentication:** Flask-Login for user authentication and Flask-Bcrypt for password hashing.
*   **Database:** Flask-SQLAlchemy for database interactions and Flask-Migrate for database migrations.
*   **Frontend:** Bootstrap 5, Font Awesome 6, and webpack for asset management.
*   **Testing:** pytest and Factory-Boy for testing.
*   **Configuration:** Environment variables for configuration, following the Twelve-Factor App methodology.
*   **Deployment:** Supports deployment via Docker and Heroku.
