# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ImaginAIry is a Python library for AI-powered image and video generation using stable diffusion. It provides a command-line interface (`aimg`) for generating and manipulating images and videos, as well as a Python API for programmatic access.

## Common Commands

The following `make` commands are available for common development tasks:

*   `make init`: Sets up the development environment by installing the correct Python version and dependencies.
*   `make test`: Runs the full test suite.
*   `make test-fast`: Runs only the tests that do not require a GPU.
*   `make lint`: Lints the codebase using `ruff`.
*   `make autoformat`: Automatically formats the code using `ruff`.
*   `make type-check`: Runs the `mypy` type checker.
*   `make check-fast`: Runs the autoformatter, linter, type-checker, and fast tests.
*   `make build-pkg`: Builds the Python package.
*   `make docs`: Serves the documentation website locally.

## High-level Code Architecture

The `imaginairy/` directory contains the core source code for the project. Here's a breakdown of the key subdirectories:

*   `api/`: Contains the public Python API for `imaginairy`.
*   `cli/`: Implements the command-line interface (`aimg`).
*   `configs/`: Contains configuration files for various models and features.
*   `enhancers/`: Includes modules for enhancing images, such as upscaling and face correction.
*   `http_app/`: The web server and API for the StableStudio web interface.
*   `img_processors/`: Contains image processing utilities.
*   `modules/`: Core modules for stable diffusion and other models.
*   `samplers/`: Houses different sampling methods for the diffusion process.
*   `schema.py`: Defines the data structures and schemas used in the project.
*   `utils/`: Contains various utility functions.
*   `vendored/`: Holds third-party libraries that are included directly in the project.

## Development Environment Setup

To set up a local development environment, run the following command:

```bash
make init
```

This will:
1. Install the correct Python version using `pyenv`.
2. Create a virtual environment.
3. Install all necessary development dependencies.
