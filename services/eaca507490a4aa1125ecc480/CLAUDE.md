# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the LangSmith SDK repository containing both Python and JavaScript/TypeScript clients for the [LangSmith observability platform](https://smith.langchain.com/). The SDK enables tracing, monitoring, and evaluation of LLM applications.

## Development Commands

### Python SDK (python/ directory)

```bash
cd python

# Install dependencies (uses uv)
uv sync

# Run tests
pytest                                    # All tests
pytest -m slow                            # Slow tests only
pytest tests/unit_tests/test_client.py    # Single test file

# Linting and formatting
make format                               # Format all code
make lint                                 # Lint all code
uv run ruff check --fix .                  # Auto-fix linting
uv run mypy langsmith                     # Type checking

# Build and publish
pip install -e .                          # Editable install
```

### JavaScript SDK (js/ directory)

```bash
cd js

# Install dependencies
yarn install

# Build
yarn build                                # Builds ESM and CJS outputs
yarn build:typedoc                        # Build Typedoc API reference

# Testing
yarn test                                 # Jest unit tests
yarn test:single path/to/test.ts          # Run single test file
yarn test:integration                     # Integration tests
yarn test:vitest                          # Vitest evaluation tests
yarn test:eval:vitest                     # Eval-specific vitest tests

# Linting and formatting
yarn lint                                 # ESLint
yarn lint:fix                             # Auto-fix linting
yarn format                               # Prettier format
yarn format:check                         # Check formatting
yarn check:types                          # TypeScript type check
```

## Architecture

### Python SDK (langsmith/)

- **Client (`client.py`)**: Main API client for CRUD operations on runs, datasets, projects. Uses background threads to asynchronously post traces to the LangSmith API.
- **RunTree (`run_trees.py`)**: Core tracing primitive. Represents a trace span with parent/child relationships. Methods: `post()`, `end()`, `patch()`.
- **Tracing Decorator (`run_helpers.py`)**: Contains the `@traceable` decorator that wraps functions to automatically create RunTree spans. Manages tracing context via context variables.
- **Schemas (`schemas.py`)**: Pydantic models for API request/response types.
- **Evaluation (`evaluation/`)**: Evaluation framework with `StringEvaluator`, `LLMEnumerator`, and batch evaluation runners.
- **Wrappers (`wrappers/`)**: LLM SDK wrappers for OpenAI, Anthropic, and Gemini to auto-trace API calls.
- **Internal (`_internal/`)**: Private implementation details including background thread handling, serialization, and OpenTelemetry support.
- **Sandbox (`sandbox/`)**: Sandboxed execution environment for running code in isolated containers.
- **Integrations (`integrations/`)**: Third-party integrations (OpenAI Agents SDK, Claude Agent SDK, Google ADK, OpenTelemetry).

### JavaScript SDK (js/src/)

- **Client (`client.ts`)**: API client with batched trace uploading and retry logic.
- **RunTree (`run_trees.ts`)**: Core trace span class mirroring Python implementation.
- **Traceable (`traceable.ts`)**: Function wrapper for automatic tracing with configurable options.
- **Evaluation (`evaluation/`)**: Evaluation framework with evaluators and batch runners.
- **Wrappers (`wrappers/`)**: LLM wrappers for OpenAI (`wrapOpenAI`), Anthropic (`wrapSDK`), and Gemini.
- **Testing Integration (`jest/`, `vitest/`)**: Test reporters and utilities for running evaluations within test frameworks.
- **Experimental (`experimental/`)**: OpenTelemetry setup, Vercel AI SDK integration, and sandbox features.

### Shared Concepts

Both SDKs implement:
- **Run Trees**: Hierarchical trace spans with typed run_type (llm, chain, tool)
- **Batched Uploads**: Traces are collected and sent asynchronously in batches
- **Context Variables**: Tracing state propagates through function calls
- **Datasets**: Collections of examples for evaluation
- **Feedback**: Metrics/scores attached to runs

## Key Configuration

### Environment Variables

```
LANGSMITH_API_KEY        # API key (required)
LANGSMITH_TRACING        # Enable tracing (set to "true")
LANGSMITH_PROJECT        # Project name (default: "default")
LANGSMITH_ENDPOINT       # API URL (default: https://api.smith.langchain.com)
LANGSMITH_WORKSPACE_ID   # Workspace ID for org-scoped keys
```

### Python pyproject.toml Key Settings

- Build: `hatchling` with dynamic versioning from `langsmith/__init__.py`
- Python: `>=3.10`
- Linting: `ruff` (Google docstring convention) and `mypy` with pydantic plugin
- Testing: `pytest` with `pytest-asyncio`, `vcrpy` for cassette tests, `pytest-xdist` for parallel runs

### JavaScript package.json Key Settings

- TypeScript with ESM and CJS builds
- Jest for unit tests (with `experimental-vm-modules`)
- Vitest for evaluation tests
- Prettier + ESLint for formatting/linting
- Entry points defined via `exports` field for conditional module resolution

## Testing Patterns

### Python

- Tests use VCRpy cassettes in `tests/cassettes/` to record/replay HTTP responses
- Integration tests use `@pytest.mark.vcr()` or test against live API with `LANGSMITH_API_KEY`
- Evaluation tests in `tests/evaluation/`
- Unit tests in `tests/unit_tests/`

### JavaScript

- Jest for unit tests in `src/tests/`
- Integration tests tagged with `.int.test.ts` suffix
- Vitest for evaluation tests with custom config `ls.vitest.config.ts`
- Mock clients in `src/tests/utils/mock_client.ts`

## Code Style

### Python

- Use Pydantic v2 for data validation
- Google-style docstrings (enforced by ruff)
- Type hints required (`disallow_untyped_defs` in mypy)
- Prefer `orjson` for JSON serialization in hot paths

### JavaScript

- TypeScript strict mode
- Prettier for formatting (2-space indent)
- ESLint with TypeScript parser
- Named exports preferred over default exports

## Pre-commit Hooks

Run `pre-commit install` to set up automatic formatting/linting on commit. Hooks enforce:
- Python: ruff format, ruff check --fix, mypy type check
- JavaScript: prettier format, eslint --fix, TypeScript type check