# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About the Project

MetaGPT is a multi-agent framework that uses Large Language Models (LLMs) to form a collaborative entity for complex tasks. It takes a one-line requirement as input and outputs user stories, competitive analysis, requirements, data structures, APIs, and documents. The project simulates a software company with roles like product managers, architects, project managers, and engineers.

## Common Commands

### Setup

1.  **Create a virtual environment** (recommended):
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install dependencies**:
    For regular use:
    ```bash
    pip install --upgrade metagpt
    ```
    For development (editable install from a cloned repo):
    ```bash
    pip install -e .
    ```

3.  **Install development and test dependencies**:
    ```bash
    pip install -e ".[dev,test]"
    ```
    This will install `pytest` for testing, and `ruff`, `black`, and `isort` for code formatting and linting.

4. **Initialize Configuration**:
    ```bash
    metagpt --init-config
    ```
    This creates a `config2.yaml` file in `~/.metagpt/` for you to add your LLM provider details.

### Running the application
```bash
metagpt "your one line requirement"
```
For example:
```bash
metagpt "Create a 2048 game"
```

### Testing

The project uses `pytest` for testing.

*   **Run all tests**:
    ```bash
    pytest
    ```
*   **Run tests with coverage**:
    ```bash
    pytest --cov=metagagpt
    ```

### Linting and Formatting

The project uses `ruff` for linting and `black` for formatting.

*   **Check for linting errors**:
    ```bash
    ruff check .
    ```
*   **Format code with black**:
    ```bash
    black .
    ```

## Code Architecture

*   **Core Logic**: The main source code is located in the `metagpt/` directory. It implements the multi-agent system, with different roles, actions, and the environment for them to interact.
*   **Entry Point**: The main CLI entry point is `metagpt.software_company:app`, as defined in `setup.py`.
*   **Configuration**: The application is configured through `~/.metagpt/config2.yaml`. This file is created by running `metagpt --init-config`. It's used to configure the LLM provider, API keys, etc.
*   **Testing**: The tests are in the `tests/` directory. They use `pytest` and heavily rely on mocking external services like LLM APIs and web requests. The mocks can be found in `tests/mock/`. The `ALLOW_OPENAI_API_CALL` environment variable can be used to control whether tests make real API calls.
*   **Dependencies**: Project dependencies are listed in `requirements.txt`. Optional dependencies for features like testing, selenium, and different search engines are in `setup.py` under `extras_require`.
