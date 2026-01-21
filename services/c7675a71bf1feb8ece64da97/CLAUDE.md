# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AgentForge is a low-code Python framework for building AI-powered autonomous agents and multi-agent cognitive architectures. It provides declarative YAML-based configuration for agents and workflows (called "Cogs"), with integrated memory management using ChromaDB.

## Common Commands

**Installation:**
```bash
pip install -e .  # Install in development mode
```

**Running Tests:**
```bash
pytest                    # Run unit tests (integration tests excluded by default)
pytest -m integration     # Run integration tests only
pytest tests/path/to/test_file.py::test_name  # Run specific test
pytest --co -q            # List all available tests
```

**Project Setup:**
```bash
python -m agentforge.init_agentforge  # Initialize .agentforge config directory in current project
agentforge                           # Same as above (after CLI installation)
```

## Architecture

### Core Components

**Agent (`src/agentforge/agent.py`):** Base class for individual AI agents. Agents follow a workflow: `load_data` → `process_data` → `render_prompt` → `run_model` → `parse_result` → `post_process_result` → `build_output`. Extensible via method override hooks.

**Cog (`src/agentforge/cog.py`):** Workflow orchestrator that chains multiple agents together based on YAML-defined transitions. Handles flow control, memory management, and state tracking between agent executions. Supports branching logic with decision transitions and loop detection via `max_visits`.

**Config (`src/agentforge/config.py`):** Singleton that loads and manages all YAML configurations from `.agentforge/` directory. Provides access to agents, cogs, models, and settings. Supports on-the-fly reloading when `settings.system.misc.on_the_fly: true`.

**Memory (`src/agentforge/storage/memory.py`):** Base memory class using ChromaDB for vector storage. Partitions data by cog and persona. Supports query/update operations with template-based key extraction.

### Configuration Structure

Configurations live in `.agentforge/` directory with this structure:
- `settings/system.yaml` - System settings (debug, logging, audio, personas)
- `settings/models.yaml` - LLM model definitions and API configurations
- `settings/storage.yaml` - ChromaDB storage settings
- `prompts/<agent_name>.yaml` - Agent prompt templates (system and user)
- `cogs/<cog_name>.yaml` - Workflow definitions with agents, memory, and transitions
- `personas/<persona_name>.yaml` - Agent persona definitions
- `custom_apis/<api_name>.py` - Custom API implementations

### APIs and Models

LLM APIs are implemented in `src/agentforge/apis/` with a `BaseModel` class providing common retry logic, prompt building, and response handling. Supported APIs: OpenAI, Anthropic, Gemini, Groq, Ollama, LMStudio, OpenRouter. Each API uses a modular class structure (e.g., `openai_api.GPT`, `openai_api.STT`, `openai_api.TTS`).

### Configuration Loading

Config discovers project root by walking up directories looking for `.agentforge/`. Can be overridden via `AGENTFORGE_ROOT` environment variable or `root_path` parameter. YAML files are parsed using ruamel.yaml to preserve formatting and comments.

### Memory System

Memory nodes are declared in Cog YAML files under `memory:` section with `query_before` and `update_after` operations. Data is extracted from context/state using key-based lookup with dot notation support (e.g., `_ctx.user_input`, `_state.analysis.choice`).

### Testing

Tests use `tests/conftest.py` fixtures with automatic environment bootstrapping. Tests stub Agent.run to prevent external LLM calls. Use `bootstrap_test_env(use_fakes=True)` in test utilities for consistent test setup. FakeChromaStorage provides in-memory storage for tests.