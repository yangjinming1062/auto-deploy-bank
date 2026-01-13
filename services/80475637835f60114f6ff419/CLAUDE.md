# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

- To run the tests:
  - `make test` or `python runtests.py tests`
  - To run a subset of tests: `python -m unittest tests.test_django_json_widget`
  - To run tests for all supported Python and Django versions: `make test-all` or `tox`
- To check code style: `make lint` or `flake8 django_json_widget tests`
- To check code coverage: `make coverage`
- To build the project: `python setup.py sdist bdist_wheel`

## High-level Code Architecture

- This project is a Django widget for `JSONField`.
- The main application logic is located in the `django_json_widget/` directory.
- The project is configured for testing with `tox` against multiple Django and Python versions. The configuration is in `tox.ini`.
- The `Makefile` contains shortcuts for common development tasks like testing, linting, and building.
- The `example/` directory contains a sample Django project that uses the widget.
