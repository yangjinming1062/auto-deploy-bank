# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the LangSmith SDK repository containing both Python and JavaScript/TypeScript client libraries for the [LangSmith observability platform](https://smith.langchain.com/). The SDK enables tracing, evaluating, and monitoring LLM applications.

## Development Commands

### Python (in `python/` directory)

```bash
# Install dependencies (uses uv)
cd python && uv sync

# Run unit tests (uses pytest with auto-parallelization, socket disabled)
make tests                    # All unit tests
make tests TEST=path/to/test  # Specific test file
make tests_watch              # Watch mode with pytest-watch

# Run integration tests
make integration_tests
make integration_tests_fast   # Parallelized with -n auto
make integration_tests_watch  # Watch mode

# Run evaluation tests
make evals

# Lint and format
make lint        # ruff check + mypy
make format      # ruff format + ruff check --fix

# Build package
make build

# Run doctests
make doctest

# Run benchmarks
make benchmark         # Rigorous benchmark
make benchmark-fast    # Fast benchmark
```

### JavaScript/TypeScript (in `js/` directory)

```bash
# Install dependencies
cd js && yarn install

# Build (compiles TypeScript to dist/, generates entrypoints)
yarn build

# Run tests
yarn test                    # Unit tests (jest)
yarn test:integration        # Integration tests
yarn test:single path/to/test.ts  # Single test file
yarn watch:single path/to/test.ts  # Watch mode for single test
yarn test:vitest             # Vitest runner
yarn test:eval:vitest        # Evaluation vitest tests

# Lint and format
yarn lint        # ESLint
yarn lint:fix    # ESLint with auto-fix
yarn format      # Prettier
yarn format:check

# Type check
yarn check:types
```

### Root-level commands

```bash
make format    # Format both Python and JS
make lint      # Lint both Python and JS
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks manually
pre-commit run --all-files
```

## Architecture

### Python SDK (`python/langsmith/`)

**Core Components:**
- `client.py` (~380KB) - Main synchronous `Client` class for API interactions (datasets, runs, projects)
- `async_client.py` (~72KB) - Async `AsyncClient` counterpart
- `run_trees.py` (~46KB) - `RunTree` class for creating and managing trace runs
- `run_helpers.py` (~76KB) - `@traceable` decorator and tracing utilities
- `schemas.py` (~44KB) - Pydantic models for API data structures
- `evaluation/` - Evaluation framework and evaluators

**Utilities:**
- `_internal/` - Internal utilities (`_background_thread.py`, `_orjson.py`, `_uuid.py`, etc.)
- `wrappers/` - LLM SDK wrappers (OpenAI, Anthropic, etc.) for automatic tracing
- `integrations/` - Third-party framework integrations (LangChain, OpenAI Agents, Claude Agent SDK)
- `testing/` - Testing utilities including pytest plugin (`pytest_plugin.py`)

**Pattern:** The SDK uses lazy imports in `__init__.py` for faster module loading. Public API is exposed via `__getattr__` for most major classes.

### JavaScript/TypeScript SDK (`js/src/`)

**Core Components:**
- `client.ts` (~172KB) - Main `Client` class
- `run_trees.ts` (~36KB) - `RunTree` class
- `traceable.ts` (~39KB) - `traceable` function and run management
- `schemas.ts` - Type definitions for API responses

**Integration Points:**
- `wrappers/` - OpenAI, Anthropic, Gemini SDK wrappers
- `jest/` and `vitest/` - Testing framework integrations
- `langchain.ts` - LangChain integration
- `experimental/` - Experimental features (OpenTelemetry, Vercel, Sandbox)

**Build Output:** Compiled to `dist/` (ESM) and `dist-cjs/` (CommonJS), then merged with entrypoint generation scripts.

## Key Concepts

### Tracing
- `@traceable` decorator / `traceable()` function - Wrap functions to automatically trace their execution
- `RunTree` - Manual run tree construction for advanced use cases
- `Client` - Create projects, list runs, manage datasets

### Evaluation
- `evaluate()` / `aevaluate()` - Run evaluations against datasets
- `RunEvaluator` - Base class for custom evaluators
- String, threshold, and label evaluators provided

### Environment Variables
- `LANGSMITH_TRACING` - Enable tracing
- `LANGSMITH_API_KEY` - API authentication
- `LANGSMITH_PROJECT` - Default project name
- `LANGSMITH_ENDPOINT` - API endpoint (defaults to https://api.smith.langchain.com)
- `LANGSMITH_WORKSPACE_ID` - Required for org-scoped API keys

### Testing with VCR Cassettes

Integration tests use VCR.py to record and replay HTTP interactions to avoid hitting live APIs:
- Python cassettes: `tests/cassettes/` and `tests/integration_tests/test_data/`
- When modifying API request/response formats, delete and regenerate cassettes:
  ```bash
  # Regenerate cassettes (requires API keys)
  uv run pytest tests/integration_tests/ --record-mode=all
  ```
- Tests are marked with `slow` for long-running tests: `pytest -m slow`