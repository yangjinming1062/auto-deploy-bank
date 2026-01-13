# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

- `make install-requirements`: Install all requirements needed for development.
- `make lint`: Run lint checks and format the code.
- `make test`: Run unit tests.
- `make test-integration`: Run integration tests.
- `make build`: Build all artifacts, including Docker images and the Python wheel.
- `make docker-images`: Build all Docker images.
- `make package-wheel`: Build the Python package wheel.

## High-Level Code Architecture

The project is a monolithic repository containing both the MLRun client-side library and the server-side components.

- **`mlrun/`**: This is the main Python package for the MLRun client. It contains all the core logic for interacting with the MLRun service, defining and running ML tasks, and managing data and models.
- **`server/`**: This directory contains the server-side components of MLRun, including the API server and other services.
- **`tests/`**: This directory contains the tests for the project, including unit, integration, and system tests.
- **`docs/`**: This directory contains the documentation for the project.
- **`dockerfiles/`**: This directory contains the Dockerfiles for building the various MLRun images.
- **`pyproject.toml`**: This file defines project metadata and dependencies, as well as linting and testing configurations. The project uses `ruff` for linting and `importlinter` to enforce import rules.
- **`Makefile`**: This file contains a variety of commands for developing and building the project.
