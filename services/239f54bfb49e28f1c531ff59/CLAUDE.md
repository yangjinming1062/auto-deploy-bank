# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Running the Hub

*   **Start the Hub server**: `jupyterhub`
*   **Start the Hub with a test configuration**: `jupyterhub -f testing/jupyterhub_config.py`

### Testing

JupyterHub uses `pytest` for its tests.

*   **Run all tests**: `pytest -v jupyterhub/tests`
*   **Run tests with coverage**: `pytest -v --cov=jupyterhub jupyterhub/tests`
*   **Run tests from one file**: `pytest -v jupyterhub/tests/<test-file-name>`
*   **Run a single test**: `pytest -v jupyterhub/tests/<test-file-name>::<test-name>`

### Code Formatting and Linting

To automatically format code locally, you can install and use `pre-commit`.

*   **Install pre-commit**: `pip install pre-commit`
*   **Install git hooks**: `pre-commit install --install-hooks`
*   **Run manually on unstaged changes**: `pre-commit run`
*   **Run manually on all files**: `pre-commit run --all-files`

## Architecture

JupyterHub is a multi-user Hub that spawns, manages, and proxies multiple instances of the single-user Jupyter notebook server.

The three main components are:

*   **Hub**: A Tornado process that manages users and their notebook servers.
*   **Proxy**: A configurable HTTP proxy that routes requests to the Hub and the single-user notebook servers.
*   **Single-user Jupyter notebook servers**: The individual Jupyter notebook instances that users interact with.
