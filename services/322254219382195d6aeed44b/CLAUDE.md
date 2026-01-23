# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

vLLM CLI is a command-line interface tool for serving Large Language Models using vLLM. It provides interactive terminal menus, CLI commands, and a multi-model proxy server for managing LLM deployments.

## Development Commands

```bash
# Install in development mode
pip install -e .

# Run tests
pytest tests/ -v --tb=short

# Run a single test file
pytest tests/test_config_manager.py -v

# Run tests with coverage
pytest tests/ --cov=src/vllm_cli --cov-report=term-missing

# Format code (black + isort)
make format

# Check formatting without changes
make format-check

# Linting with flake8
flake8 src/vllm_cli --count --select=E9,F63,F7,F82 --show-source

# Type checking with mypy
mypy src/vllm_cli --python-version 3.9 --ignore-missing-imports

# Full CI/CD check
make ci-test
```

## Architecture

### Directory Structure

```
src/vllm_cli/
├── cli/           # Argument parsing and CLI command handlers
├── config/        # Configuration, profiles, shortcuts, and persistence
├── errors/        # Error handling and recovery strategies
├── models/        # Model discovery, caching, and management
├── proxy/         # Multi-model proxy server (experimental)
├── server/        # vLLM server process management and monitoring
├── system/        # GPU, memory, and system capability detection
├── ui/            # Rich terminal interface (menus, components, display)
├── validation/    # vLLM parameter validation framework
└── schemas/       # JSON schemas for configuration validation
```

### Key Entry Points

- **`__main__.py`**: Main entry point. Handles both CLI arguments (via `cli/parser.py`) and interactive mode (via `ui/menu.py`)
- **CLI flow**: `__main__` → `cli/parser.py` → `cli/handlers.py` → `server/manager.py`
- **Interactive flow**: `__main__` → `ui/menu.py` → various UI modules → config/server modules

### Configuration System

- **Main config**: `~/.config/vllm-cli/config.yaml` (YAML)
- **User profiles**: `~/.config/vllm-cli/user_profiles.json`
- **Shortcuts**: `~/.config/vllm-cli/shortcuts.json`

The `config/` module uses `ConfigManager` as the facade, delegating to:
- `ProfileManager`: Built-in and user profiles
- `ShortcutManager`: Saved model+profile combinations
- `PersistenceManager`: YAML/JSON file I/O
- `SchemaManager`: vLLM argument metadata

### Validation Framework

The `validation/` module provides comprehensive vLLM parameter validation:
- `ValidationRegistry`: Central registry of validation rules
- `CompatibilityValidator`: Validates parameter combinations
- Factory functions: `create_vllm_validation_registry()`, `create_compatibility_validator()`

### Server Management

`server/manager.py` handles vLLM server lifecycle:
- Process spawning and monitoring
- Log parsing for server readiness
- GPU and resource cleanup

### Proxy Server (Experimental)

The `proxy/` module enables serving multiple models through a unified API:
- `ProxyManager`: Coordinates multiple vLLM server instances
- `ProxyRouter`: HTTP routing to model servers
- `ProxyRuntime`: Live model addition/removal

## Important Patterns

### Error Handling
Custom error types defined in `errors/`: `ConfigurationError`, `ServerError`, `ModelError`, etc. Use exception handlers from `errors/handlers.py`.

### Type Hints
The project uses Python 3.9+ type hints. Run `mypy` before committing.

### Pydantic Models
Configuration schemas use Pydantic v2. See `config/schemas.py` for validation patterns.

### Rich UI Components
UI modules use `rich` library for terminal rendering. Custom components are in `ui/components.py`.

## Dependency Notes

- **vLLM is NOT installed by default**: The package lists it as optional (`[vllm]` extra)
- **hf-model-tool**: External dependency for model discovery
- **Test dependencies**: Install with `pip install -e ".[test]"`