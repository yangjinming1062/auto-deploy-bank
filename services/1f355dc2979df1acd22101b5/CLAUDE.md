# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

- **Run tests:** `py.test flask_user/tests/`

## High-level Code Architecture

This project is a Flask extension for user authentication and management. It follows a modular architecture with different components for handling specific responsibilities:

- **`flask_user/`**: The main package directory.
- **`db_adapters/`**: Contains database adapters for different database backends (e.g., SQL, MongoDB).
- **`email_adapters/`**: Contains email adapters for sending emails.
- **`*_manager.py`**: Several manager modules (`db_manager.py`, `email_manager.py`, `password_manager.py`, `token_manager.py`, `user_manager.py`) are responsible for handling specific aspects of user management.
- **`user_manager.py`**: This appears to be the central component, orchestrating the user management functionality.
