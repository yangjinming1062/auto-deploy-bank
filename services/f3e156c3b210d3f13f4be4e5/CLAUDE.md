# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

- **Install dependencies:** `pip install -r requirements/requirements_test.txt`
- **Run linter:** `flake8`

## High-level Code Architecture

This project is a Django application that provides AJAX utilities for pagination, tabbing, and delayed content loading.

- **`django_ajax/`**: The main application directory.
  - **`pagination.py`**: Contains the core logic for paginating querysets and other iterables.
  - **`templatetags/`**: Contains the template tags for pagination, tabbing, and xhr.
  - **`static/`**: Contains the JavaScript and CSS files for the AJAX functionality.
  - **`templates/`**: Contains the HTML templates for the utilities.

The `README` file provides a good overview of how to use the different utilities.
