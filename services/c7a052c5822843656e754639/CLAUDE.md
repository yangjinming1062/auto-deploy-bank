# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-level Architecture

TimeTagger is a web-based time-tracking application.

*   **Backend:** The server is written in Python and runs on `uvicorn`. It uses `asgineer` for the web framework and `itemdb` (SQLite) for data storage.
*   **Frontend:** The client-side code is written in Python and compiled to JavaScript using `PScript`.
*   **Deployment:** The application can be run directly using `python -m timetagger` or deployed using Docker. Docker-compose files are provided in the `deploy/` directory.
*   **Authentication:** Authentication is supported through credentials (username/password) or a reverse proxy.

## Common Commands

The following commands are commonly used during development:

*   **Install for development:**
    ```bash
    pip install -e .
    ```
*   **Install developer dependencies:**
    ```bash
    pip install invoke black flake8 pytest pytest-cov requests
    ```
*   **Run the application:**
    ```bash
    python -m timetagger
    ```
*   **Run tests:**
    ```bash
    invoke tests
    ```
*   **Lint the code:**
    ```bash
    invoke lint
    ```
*   **Format the code:**
    ```bash
    invoke format
    ```
*   **Clean temporary files:**
    ```bash
    invoke clean
    ```
