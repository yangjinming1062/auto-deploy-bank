# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-level code architecture

`pyspider` is a web crawler framework with a modular architecture. The key components are:

*   **`pyspider/run.py`**: The main entry point for the application.
*   **`pyspider/webui/`**: A Flask-based web interface for managing and monitoring crawl jobs.
*   **`pyspider/scheduler/`**: Schedules and manages the crawl queue.
*   **`pyspider/fetcher/`**: Fetches web pages.
*   **`pyspider/processor/`**: Processes the fetched content and extracts data.
*   **`pyspider/database/`**: Provides a database abstraction layer for storing results. It supports multiple backends like MySQL, MongoDB, and Redis.
*   **`tests/`**: Contains the test suite.

## Common Commands

*   **Running tests**:
    *   To run the full test suite for all supported Python versions, use `tox`.
    *   To run tests for a specific environment, use `python setup.py test`.
*   **Installation**:
    *   Install the package and its dependencies using `pip install .`
    *   To install with all optional backends, use `pip install .[all]`
*   **Running pyspider**:
    *   The command `pyspider` starts the web interface and all components.
