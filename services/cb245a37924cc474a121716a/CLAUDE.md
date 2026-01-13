# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Langflow is a graphical user interface for LangChain, designed to provide an easy way to experiment, build, and share flows.

## Common Development Commands

### Setup

To set up the development environment, install all dependencies and set up pre-commit hooks:

```bash
make init
```

### Backend

To run the backend server in development mode:

```bash
make backend
```

By default, the backend runs with autologin. To run without autologin:

```bash
make backend login=1
```

### Frontend

To run the frontend in development mode:

```bash
make frontend
```

### Linting and Formatting

To lint and format the code:

```bash
make lint
make format
```

### Building

To build the frontend and package the project:

```bash
make build
```

To build only the frontend:

```bash
make build_frontend
```

### Testing

To run the backend tests:

```bash
make tests
```

You can pass arguments to pytest using the `args` variable:

```bash
make tests args="--pdb"
```

To run the frontend tests:

```bash
make tests_frontend
```

To run the frontend tests with the UI:

```bash
make tests_frontend UI=true
```

## Code Architecture

The project is a monorepo with a `frontend` and `backend`.

### Backend

The backend is a Python application built with FastAPI. The main entry point is `src/backend/langflow/main.py`.

-   **`api/`**: Contains the FastAPI endpoints.
-   **`components/`**: Contains the custom components that can be used in the flows.
-   **`core/`**: Contains the core logic of the application.
-   **`graph/`**: Contains the logic for building and processing the flows.
-   **`interface/`**: Contains the interface for the components.
-   **`processing/`**: Contains the logic for processing the flows.
-   **`services/`**: Contains the services used by the application, such as the database service.
-   **`settings.py`**: Contains the settings for the application.

### Frontend

The frontend is a React application. The source code is in the `src/frontend` directory. The main entry point is `src/frontend/src/index.tsx`.
