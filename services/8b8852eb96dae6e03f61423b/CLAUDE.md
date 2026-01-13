# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-level Architecture

This repository contains the source code for Misago, a modern forum software. It is a monolithic application with a backend powered by the Django framework (located in the `misago` directory) and a frontend built with React.js (located in the `frontend` directory). The frontend assets are managed using npm and built with webpack.

## Development Setup

The recommended way to set up a development environment is by using Docker.

1.  **Initialize the environment:** Run the following command to build the necessary Docker containers, install Python and Node.js dependencies, and initialize the database:

    ```bash
    ./dev init
    ```

2.  **Start the development server:** After the initialization is complete, start the development server with:

    ```bash
    docker-compose up
    ```

The forum will then be available at `http://127.0.0.1:8000/`.

## Common Commands

### Backend

-   **Run tests:** Use the following command to run the Python test suite:

    ```bash
    pytest
    ```

-   **Run migrations:** To apply database migrations, use:

    ```bash
    docker-compose run --rm misago python manage.py migrate
    ```

-   **Create a superuser:** To create a new superuser for the forum, run:

    ```bash
    docker-compose run --rm misago python manage.py createsuperuser
    ```

### Frontend

The following commands should be run from the root of the repository.

-   **Development build:** To build the frontend assets for a development environment and watch for changes, run:

    ```bash
    npm run start
    ```

-   **Production build:** To create a minified, production-ready build of the frontend assets, use:

    ```bash
    npm run build
    ```

-   **Linting and formatting:** To lint and format the frontend code, use the following commands:

    ```bash
    npm run eslint
    npm run prettier
    ```
