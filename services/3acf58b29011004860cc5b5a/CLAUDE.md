# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

### Installation

This project uses `uv` for dependency management.

To install dependencies:
```bash
pip install uv
uv sync
```

### Running the bot

You can run the bot using the following command:

```bash
uv run main.py
```

Alternatively, you can use the installed script:

```bash
astrbot
```

### Linting

This project uses `ruff` for linting. To check the code for linting errors, run:

```bash
ruff check .
```

To automatically fix linting errors, run:
```bash
ruff check --fix .
```

## High-level Code Architecture

AstrBot is a modular and extensible chatbot framework with the following key components:

*   **Core:** The core of the bot, handling event dispatching, message processing, and plugin management.
*   **LLM Integration:** It supports a wide range of Large Language Models (LLMs) like OpenAI, Gemini, and local models via Ollama.
*   **Platform Support:** The bot can connect to various messaging platforms like QQ, WeChat, Telegram, and more. Each platform has its own adapter.
*   **Plugin System:** Functionality can be extended through a plugin system. Plugins can be developed to add new commands and features.
*   **Web Dashboard:** A web-based UI for configuration, plugin management, and direct interaction with the bot.
*   **Agent Capabilities:** The bot has built-in agent-like features, including a code executor, web search, and natural language to-do lists.
