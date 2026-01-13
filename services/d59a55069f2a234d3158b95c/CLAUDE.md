# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`fastapi-admin` is a fast admin dashboard based on [FastAPI](https://github.com/tiangolo/fastapi)
and [TortoiseORM](https://github.com/tortoise/tortoise-orm/) with [tabler](https://github.com/tabler/tabler) ui,
inspired by Django admin.

## Common Commands

The following commands are available in the `Makefile`:

*   `make style`: Auto-fix style issues.
*   `make check`: Run style checks, flake8, mypy, and pylint.
*   `make test`: Run tests.
*   `make build`: Build the project.
*   `make ci`: Run all checks and tests.
*   `make babel`: Run i18n commands.

## Development

To run the example application locally:

1.  Clone the repository.
2.  Create a `.env` file with the following content:

    ```dotenv
    DATABASE_URL=mysql://root:123456@127.0.0.1:3306/fastapi-admin
    REDIS_URL=redis://localhost:6379/0
    ```

3.  Run `docker-compose up -d --build`.
4.  Visit <http://localhost:8000/admin/init> to create the first admin user.

## Code Architecture

The project is structured as follows:

*   `fastapi_admin`: The main application code.
*   `examples`: An example application demonstrating how to use `fastapi-admin`.
*   `tests`: Tests for the application.

The application uses `FastAPI` as the web framework and `TortoiseORM` for database access. The frontend is built using the `tabler` UI kit.
