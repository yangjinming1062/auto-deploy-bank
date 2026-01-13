# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dash is a Python framework for building machine learning and data science web applications. It is built on top of Plotly.js, React, and Flask.

## Architecture

The Dash architecture consists of three main parts:

1.  **Dash Backend (Python/R):** The backend is responsible for defining the app layout and handling callbacks.
2.  **Dash Frontend (React):** The frontend is a React application that renders the UI components and communicates with the backend.
3.  **Dash Components:** These are reusable UI components that can be used to build Dash applications.

The core of Dash is the `dash` Python package, which provides the framework for building applications. The `dash-renderer` package is the frontend component that renders the application in the browser. The `dash-core-components`, `dash-html-components`, and `dash-table` packages provide a set of pre-built components for building user interfaces.

## Common Development Tasks

### Setting up the development environment

To set up the development environment, you will need to have Python, Node.js, and npm installed.

1.  Clone the repository and create a virtual environment:
    ```bash
    git clone https://github.com/plotly/dash.git
    cd dash
    python3 -m venv .venv/dev
    source .venv/dev/bin/activate
    ```
2.  Install the required Python and Node.js dependencies:
    ```bash
    pip install -e .[ci,dev,testing,celery,diskcache]
    npm ci
    ```

### Building the project

To build the project, run the following command:

```bash
npm run build
```

This will build the `dash-renderer` and all of the component packages.

### Running tests

To run the Python tests, use `pytest`:

```bash
pytest
```

To run a specific test file:

```bash
pytest tests/unit/test_some_feature.py
```

To run the renderer unit tests:

```bash
cd dash/dash-renderer && npm run test
```

### Linting

To run the linters, use the following commands:

```bash
npm run lint
```
