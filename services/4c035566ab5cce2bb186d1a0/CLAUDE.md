# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AgentScope is a flexible and robust multi-agent platform designed for building LLM applications. It emphasizes transparency, model agnosticism, and a modular, LEGO-style approach to agent building. It is designed for multi-agent applications, with explicit message passing and workflow orchestration.

## Common Commands

### Installation

To install the project and its dependencies, use the following commands:

```bash
# Pull the source code from GitHub
git clone https://github.com/modelscope/agentscope.git

# Install the package in editable mode
cd agentscope
pip install -e .
```

To install all dependencies for development, including testing tools, use:

```bash
pip install -e ".[dev]"
```

### Testing

The project uses `pytest` for testing. To run the test suite, use the following command:

```bash
pytest
```

## High-level Architecture

The core logic of AgentScope resides in the `src/agentscope` directory. The project is structured into several key components:

-   `agents/`: Contains the core agent implementations, such as `DialogAgent` and `UserAgent`.
-   `models/`: Handles interactions with various language models.
-   `service/`: Provides tools and services that agents can use, such as code execution and web search.
-   `memory/`: Manages the memory of agents.
-   `message/`: Defines the message structure used for communication between agents.
-   `msghub.py`: A central component for message broadcasting in multi-agent setups.
-   `pipelines/`: Facilitates the creation of sequential and other types of workflows.
-   `prompt/`: Manages and formats prompts.
-   `rpc/`: Handles distributed communication between agents.
-   `server/`: Contains the server implementation for hosting agents.
-   `web/`: Contains web ui related code.

This structure allows for a clear separation of concerns, making it easier to extend and maintain the platform.
