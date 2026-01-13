# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

- **Install dependencies**: `poetry install`
- **Run tests**: `poetry run pytest`
- **Run a single test file**: `poetry run pytest tests/unit/tasks/test_tool_task.py`
- **Linting**: `poetry run ruff .`
- **Formatting**: `poetry run black .`
- **Type checking**: `poetry run pyright`

## High-level Architecture

Griptape is a modular Python framework for building AI applications. Its architecture is centered around a few key concepts:

- **Structures**: These are the main entry points for creating applications. The primary structures are `Agent`, `Pipeline`, and `Workflow`, located in `griptape/structures`.
- **Tasks**: Tasks are the building blocks of structures. They define the work to be done and can be chained together in various ways. You can find them in `griptape/tasks`.
- **Drivers**: Drivers are responsible for communicating with external services. This includes prompt drivers for LLMs (e.g., `OpenAiChatPromptDriver`), vector store drivers for databases (e.g., `PineconeVectorStoreDriver`), and embedding drivers. The drivers are located in `griptape/drivers`.
- **Tools**: Tools are components that Griptape agents can use to perform specific actions, such as scraping a website (`WebScraper`) or managing files (`FileManager`). The available tools are in `griptape/tools`.
- **Memory**: Memory components are used to store and retrieve information during the execution of a structure. This includes conversation history and tool outputs. Memory-related code is in `griptape/memory`.
