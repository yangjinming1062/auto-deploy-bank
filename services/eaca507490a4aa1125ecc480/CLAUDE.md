# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the LangSmith SDK monorepo containing Python and JavaScript/TypeScript client libraries for the LangSmith observability and evaluation platform. LangSmith helps debug, evaluate, and monitor LLM applications and agents.

## Build & Test Commands

### Python SDK (`python/`)

```bash
cd python

# Install dependencies (uses uv)
uv sync

# Run unit tests (sets PYTHONDEVMODE, disables network access by default)
make tests

# Run specific test file
TEST=tests/unit_tests/test_client.py make tests

# Run all pytest options directly
uv run python -m pytest tests/unit_tests -x -v

# Integration tests (requires API keys)
make integration_tests
make integration_tests_fast  # Uses pytest-xdist for parallel execution

# Eval tests
make evals

# Doctests
make doctest

# Format code
make format

# Lint and type check
make lint

# Build package
make build
```

### JavaScript SDK (`js/`)

```bash
cd js

# Install dependencies
yarn install

# Build the package (generates ESM, CJS, and type definitions)
yarn build

# Run unit tests (Jest)
yarn test

# Run integration tests
yarn test:integration

# Run a single test file
yarn test:single --testPathPattern=traceable.test.ts

# Watch mode for a single test
yarn watch:single --testPathPattern=traceable.test.ts

# Type check
yarn check:types

# Format code
yarn format

# Lint
yarn lint
```

### Root Level

```bash
# Format both Python and JS
make format

# Lint both Python and JS
make lint
```

## Architecture

### Python SDK Structure (`python/langsmith/`)

**Core Modules:**

- **client.py**: Main `Client` class for API interactions (datasets, examples, runs, projects). Uses `requests` with automatic retry and batching.
- **async_client.py**: Async version using `httpx`
- **run_trees.py**: `RunTree` class for creating and managing trace runs hierarchically. Implements the post/end/patch lifecycle pattern.
- **run_helpers.py**: Core tracing logic including `@traceable` decorator, context management, and helper functions (`trace`, `tracing_context`)
- **schemas.py**: Pydantic v2 models for API requests/responses
- **evaluation/**: Evaluation framework:
  - `_runner.py`: Synchronous evaluation orchestrator
  - `_arunner.py`: Async evaluation orchestrator
  - `evaluator.py`: `RunEvaluator` abstract base class and `EvaluationResult`
  - `llm_evaluator.py`: LLM-based evaluators using the `evaluate()` function
- **wrappers/**: Third-party SDK auto-instrumentation:
  - `_openai.py`: OpenAI SDK wrapper with token usage tracking
  - `_anthropic.py`: Anthropic SDK wrapper
  - `_gemini.py`: Google Gemini SDK wrapper
- **integrations/**: Framework-specific integrations:
  - `otel/`: OpenTelemetry SDK instrumentation
  - `claude_agent_sdk/`: Claude Agent SDK tracing
  - `openai_agents_sdk/`: OpenAI Agents SDK tracing
  - `google_adk/`: Google Agent Development Kit tracing
- **_internal/**: Internal utilities (private module):
  - `_background_thread.py`: Asynchronous buffered uploads with thread pool
  - `_operations.py`: Retry logic, backoff, and operation utilities
  - `_serde.py`: orjson-based serialization helpers
  - `_aiter.py`: Async iteration utilities
  - `_patch.py`: Monkey patching utilities
  - `_embedding_distance.py`: Embedding-based evaluation metrics
- **prompt_cache.py**: Prompt caching functionality with configurable global cache
- **anonymizer.py**: Data anonymization for PII handling
- **pytest_plugin.py**: Pytest plugin for LangSmith datasets as tests
- **beta/**: Experimental/preview features

### JavaScript SDK Structure (`js/src/`)

- **client.ts**: Main `Client` class using `fetch` with retry logic
- **run_trees.ts**: `RunTree` class mirroring Python implementation
- **traceable.ts**: Core `traceable()` function for decorating traced functions
- **schemas.ts**: TypeScript interfaces for API data
- **langchain.ts**: LangChain integration utilities
- **evaluation/**: Evaluation utilities
- **wrappers/**: Third-party SDK wrappers (OpenAI, Anthropic, Gemini)
- **jest/**: Jest reporter for LangSmith evaluation integration
- **vitest/**: Vitest reporter for LangSmith evaluation integration
- **utils/**: Utility functions (prompt cache, anonymization)
- **singletons/**: Singleton instances (fetch, traceable)
- **experimental/**: Experimental features:
  - `otel/`: OpenTelemetry setup and exporters
  - `vercel/`: Vercel AI SDK integration
  - `anthropic/`: Claude SDK integration
  - `sandbox/`: Sandboxed execution tracing

### Shared Concepts

Both SDKs implement the same core patterns:

1. **Tracing Lifecycle** (post → end → patch):
   - `post()`: Register run initially with inputs
   - `end()`: Finalize run with outputs or error
   - `patch()`: Upload to LangSmith API

2. **Hierarchical Runs**:
   - Parent `RunTree` creates child runs via `create_child()`
   - Automatically propagates context and trace IDs

3. **@traceable decorator / traceable() function**:
   - Wraps functions to auto-capture inputs, outputs, errors, timing
   - Manages RunTree creation and lifecycle
   - Supports metadata, tags, and callbacks

4. **Client API**:
   - High-level operations on projects, datasets, examples, runs
   - List, create, update, delete operations

5. **Wrappers**:
   - Wrap third-party LLM SDKs (OpenAI, Anthropic, Gemini)
   - Auto-trace with token usage tracking

## Key Configuration

### Environment Variables

```bash
LANGSMITH_TRACING=true        # Enable tracing
LANGSMITH_API_KEY=ls_...      # API key
LANGSMITH_ENDPOINT=https://api.smith.langchain.com  # API URL
LANGSMITH_PROJECT=MyProject   # Project name (defaults to "default")
LANGSMITH_WORKSPACE_ID=...    # Required for org-scoped keys
```

### Pre-commit Hooks

The project uses pre-commit hooks for automated formatting and linting. Install with:
```bash
pip install pre-commit && pre-commit install
```

## Code Style

- **Python**: ruff for formatting (Google docstring convention), mypy for type checking
- **JavaScript**: prettier for formatting, eslint with TypeScript support

## Testing Patterns

### Python Tests
- **Unit tests**: Use VCR.py to record/replay HTTP interactions (`cassettes/` directory)
- **Integration tests**: Live API calls, require environment variables
- **Custom request matcher**: OpenAI calls match on hashed request bodies (model, messages, tools)

### JavaScript Tests
- **Unit tests**: Jest with mock service worker (msw) for HTTP mocking
- **Integration tests**: Live API calls
- **Evaluation tests**: Vitest-based with specialized config (`ls.vitest.config.ts`)