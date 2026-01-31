# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Setup and Installation
```bash
make install-dev    # Create venv and install all dependencies (recommended)
make uv-venv        # Create virtual environment only
uv sync --all-extras  # Install dependencies with test/evaluation extras
make pre-commit-install  # Install pre-commit hooks
```

### Running Tests
```bash
make test           # Run all tests (skips external service tests)
uv run pytest tests/ -v --tb=short  # Alternative with uv
uv run pytest tests/test_cli.py -v  # Run single test file
uv run pytest tests/tools/test_edit_tool.py::test_name -v  # Run specific test
SKIP_OLLAMA_TEST=true SKIP_OPENROUTER_TEST=true SKIP_GOOGLE_TEST=true make test  # Skip specific provider tests
```

### Linting and Formatting
```bash
make fix-format              # Auto-fix formatting
ruff format .                # Format code
ruff check --fix .           # Auto-fix linting issues
uv run pre-commit run --all-files  # Run all pre-commit hooks
```

### CLI Usage
```bash
uv run trae-cli run "your task" --config-file trae_config.yaml
uv run trae-cli interactive
uv run trae-cli show-config
```

## Architecture

### Codebase Overview
Trae Agent is an LLM-based agent for software engineering with a modular, research-friendly architecture. The project uses Python 3.12+ with async/await patterns throughout. Key features include multi-LLM provider support, trajectory recording for debugging, MCP integration, and Docker sandbox execution.

### Execution Flow
1. CLI parses arguments → loads YAML config → instantiates Agent
2. Agent initializes `LLMClient` and tools from registry
3. Main loop (up to `max_steps`):
   - Send conversation history to LLM
   - LLM returns tool calls or completion signal
   - `ToolExecutor` executes calls sequentially or in parallel
   - Reflection on failures via `reflect_on_result()`
4. `TrajectoryRecorder` logs all steps for analysis
5. Task completion detected via `task_done` tool or completion indicators

### Agent Execution States
- `THINKING`: Waiting for LLM response
- `CALLING_TOOL`: Executing tool calls
- `REFLECTING`: Processing tool results with failure reflection
- `COMPLETED`: Step finished successfully
- `ERROR`: Step encountered an error

### Directory Structure
```
trae_agent/
├── agent/          # Agent logic and execution loop
├── tools/          # Tool implementations and registry
├── utils/
│   ├── llm_clients/    # LLM provider clients (OpenAI, Anthropic, Azure, etc.)
│   ├── cli/            # Console interfaces (simple/rich modes)
│   └── config.py       # YAML-based configuration
├── prompt/         # System prompts
└── cli.py          # CLI entry point
```

### Core Architecture Layers

**1. CLI Layer (`cli.py`)**
- Entry point using Click framework
- Commands: `run`, `interactive`, `show-config`, `tools`
- Handles config file resolution (YAML/JSON), Docker mode setup, and console type selection

**2. Agent Layer (`agent/`)**
- `BaseAgent`: Abstract base class managing the agent loop
  - LLM interaction via `LLMClient`
  - Tool execution via `ToolExecutor` (or `DockerToolExecutor`)
  - Step-by-step execution with state management
  - Trajectory recording for debugging
- `TraeAgent`: Concrete implementation for software engineering
  - Loads configured tools from `tools_registry`
  - Supports MCP server integration
  - Handles project context (path, commits, patches)

**3. Tool System (`tools/`)**
- All tools inherit from `Tool` base class (abstract)
- Registry pattern in `__init__.py`: `tools_registry` dict mapping names to classes
- Built-in tools: `bash`, `str_replace_based_edit_tool`, `json_edit_tool`, `sequentialthinking`, `task_done`, `ckg`
- Each tool implements: `get_name()`, `get_description()`, `get_parameters()`, `execute()`
- MCP tools can be dynamically loaded and added to the agent

**4. LLM Client Layer (`utils/llm_clients/`)**
- Factory pattern via `LLMClient` class in `llm_client.py`
- Routes to provider-specific clients based on config
- Clients: `OpenAIClient`, `AnthropicClient`, `AzureClient`, `OpenRouterClient`, `DoubaoClient`, `OllamaClient`, `GoogleClient`
- All inherit from `BaseLLMClient` for common interface
- `LLMMessage` and `LLMResponse` dataclasses for communication

**5. Configuration (`utils/config.py`)**
- YAML-based config with environment variable overrides
- Priority: CLI args > config file > env vars > defaults
- Dataclasses: `Config`, `ModelConfig`, `ModelProvider`, `TraeAgentConfig`
- Supports MCP server configuration

**6. Docker Support**
- `DockerManager`: Container lifecycle management
- `DockerToolExecutor`: Routes specific tools to container execution
- Pre-built tools in `trae_agent/dist/` for containerized use
- Build with `pyinstaller` for standalone binaries

### Key Design Patterns
- **Registry Pattern**: Tools and model providers registered in dictionaries for dynamic lookup
- **Factory Pattern**: `LLMClient` factory, `ConsoleFactory` for UI
- **Template Method**: `BaseAgent` defines skeleton; subclasses override specific behavior
- **Strategy Pattern**: Interchangeable tool executors (local vs Docker)
- **Abstract Base Classes**: `Tool`, `BaseAgent`, `BaseLLMClient` define interfaces

### Adding New Components

**Adding a Tool:**
1. Create class inheriting from `Tool` in `trae_agent/tools/`
2. Implement: `get_name()`, `get_description()`, `get_parameters()`, `execute()`
3. Register in `tools_registry` dict in `trae_agent/tools/__init__.py`

**Adding an LLM Provider:**
1. Create client class inheriting from `BaseLLMClient`
2. Implement `chat()` method returning `LLMResponse`
3. Add provider case in `LLMClient.__init__()` factory match statement

**Adding Configuration:**
1. Add dataclass in `trae_agent/utils/config.py`
2. Update `Config.create()` parsing logic
3. Update `Config.resolve_config_values()` if CLI overrides needed

### Important Files
- `trae_agent/tools/__init__.py`: Tool registry definition
- `trae_agent/utils/llm_clients/llm_client.py`: LLM provider factory
- `trae_agent/agent/base_agent.py`: Core execution loop
- `trae_agent/cli.py`: Command-line interface
- `trae_agent/utils/trajectory_recorder.py`: Execution logging for debugging

### Testing Patterns
- Tests use `pytest` with `asyncio_mode = "auto"` for async tests
- Test markers: `slow`, `integration`, `unit` (see `pyproject.toml`)
- Mock external services with environment variables: `SKIP_OLLAMA_TEST`, `SKIP_OPENROUTER_TEST`, `SKIP_GOOGLE_TEST`

### Code Standards
- Python 3.12+ required
- License header required: `SPDX-License-Identifier: MIT` (see existing files)
- Type hints required for function signatures
- Ruff linting configured in `pyproject.toml` (B, SIM, C4, E4/E9/F, I rules)
- Pre-commit hooks enforce formatting and type checking (mypy)
- Use `contextlib.suppress(Exception)` for cleanup, not bare `except:`