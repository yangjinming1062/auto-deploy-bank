# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`django-allauth` is a reusable Django app that provides a comprehensive solution for authentication, registration, and account management, including social media authentication.

## Common Commands

- `make test`: Run the test suite using pytest.
- `make qa`: Perform quality assurance checks, including flake8, isort, black, and djlint.
- `make black`: Auto-format Python code.
- `make isort`: Sort imports.
- `make po`: Regenerate `.po` files for internationalization.
- `make mo`: Compile `.po` files into `.mo` files.

## Architecture

The project is structured into several Django apps:

- `allauth/account`: Handles local account management (e.g., sign up, login, email verification).
- `allauth/socialaccount`: Manages social media authentication and connections.
- `allauth/mfa`: Implements multi-factor authentication.
- `allauth/usersessions`: Manages user sessions.

Key modules:

- `allauth/models.py`: Contains the core data models.
- `allauth/urls.py`: Defines the URL patterns for the authentication views.
- `allauth/app_settings.py`: Defines the app's settings.
- `allauth/templates/`: Contains the templates for the authentication views.
