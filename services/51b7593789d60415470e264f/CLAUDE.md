# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-level code architecture

This project is a Python implementation of Google's Agent-to-Agent (A2A) protocol. The library allows for building interoperable AI agent ecosystems.

The main components are:
*   **`python_a2a`**: The core Python package.
*   **`examples/`**: Contains example usage of the library.
*   **`docs/`**: Contains the documentation.
*   **`tests/`**: Contains the tests for the library.

The library is structured around a few key concepts:
*   **Agents**: Independent AI services that can communicate with each other.
*   **Skills**: Specific capabilities of an agent.
*   **Agent Networks**: A collection of agents that can be managed and discovered.
*   **Workflows**: Complex interactions between multiple agents.
*   **MCP (Model Context Protocol)**: A protocol for agents to access external tools and data sources.

The library also provides a command-line interface (CLI) for interacting with agents and a UI for visualizing and managing agent workflows.

## Common Commands

The `Makefile` provides several useful commands for development:

*   **`make setup`**: Sets up the development environment using `uv`.
*   **`make format`**: Formats the code using `black` and `isort`.
*   **`make lint`**: Lints the code using `flake8` and `mypy`.
*   **`make test`**: Runs the tests using `pytest`.
*   **`make build`**: Builds the distribution packages.
*   **`make docs`**: Builds the documentation.
*   **`make run-example`**: Runs a simple example agent.

To run a single test, you can use the following command:

```bash
pytest tests/test_file.py::test_function
```
