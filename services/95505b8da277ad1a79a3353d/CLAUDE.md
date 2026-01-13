# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-level Architecture

HTTPX is a next-generation HTTP client for Python, designed to be a successor to `requests`. Key architectural features include:

- **Sync and Async APIs:** It provides both a standard synchronous client (`httpx.Client`) and an asynchronous client (`httpx.AsyncClient`) for modern Python applications.
- **HTTP/1.1 and HTTP/2 Support:** HTTPX can handle both major versions of HTTP, enabling features like multiplexing over a single connection with HTTP/2.
- **Transport Layer:** It is built on top of the `httpcore` library, which provides a low-level transport layer for handling HTTP requests and connection pooling.
- **Extensibility:** The client can be extended with custom transports, authentication classes, and content decoders.
- **Command-Line Client:** An optional CLI is available with `httpx[cli]`, providing command-line access to its features.

## Common Commands

This repository uses scripts in the `/scripts` directory to standardize development tasks.

- **Install dependencies:**
  ```bash
  scripts/install
  ```

- **Run tests:**
  The test suite is run using `pytest`.
  ```bash
  # Run all tests
  scripts/test

  # Run a specific test file
  scripts/test tests/test_client.py
  ```

- **Run linting and code checks:**
  The project uses `black`, `isort`, and `mypy`.
  ```bash
  # Auto-format the code
  scripts/lint

  # Run static analysis and type checking
  scripts/check
  ```

- **Build documentation:**
  The documentation is built using `mkdocs`.
  ```bash
  # Serve the documentation locally
  scripts/docs
  ```
