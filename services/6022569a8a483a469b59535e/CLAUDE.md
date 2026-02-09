# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Semantic Kernel is a model-agnostic SDK for building intelligent AI agents and multi-agent systems. The repository contains implementations in three languages:
- **Python** (`python/`): Primary implementation, uses `uv` for package management
- **.NET** (`dotnet/`): C# implementation with NuGet packages
- **Java** (`java/`): Moved to separate repository (microsoft/semantic-kernel-java)

## Build and Test Commands

### Python

```bash
# Install dependencies (uv, Python 3.10-3.13, SK, pre-commit hooks)
make install

# Install SK only (without uv/python installation)
make install-sk

# Run a single test file
uv run pytest tests/unit/test_kernel.py

# Run unit tests
uv run pytest tests/unit

# Run integration tests
uv run pytest tests/integration

# Build the package
cd python && make build

# Run all tests with coverage
uv run pytest --cov=semantic_kernel --cov-report=term-missing tests/unit/

# Lint and format check
uv run ruff check .
uv run ruff format --check .

# Auto-fix linting issues
uv run ruff check --fix .

# Run all pre-commit checks
uv run pre-commit run -a
```

### .NET

```bash
# Build (Release configuration)
./build.sh

# Run tests (coverage threshold: 80%)
dotnet test --configuration Release --no-build --no-restore

# Format code
dotnet format

# Run specific test project
dotnet test --project src/Connectors/Connectors.OpenAI.UnitTests/Connectors.OpenAI.UnitTests.csproj
```

## Architecture

### Core Concepts

**Kernel**: The central orchestration component that manages AI services, plugins, and filters. All operations flow through the Kernel instance.

**Agents**: Modular AI entities with identity, behavior, and interaction patterns. Main types:
- `ChatCompletionAgent`: LLM-based agents using chat completions
- `OpenAIAssistantAgent`: Agents using OpenAI's Assistant API
- `AggregatorAgent`: Wraps multiple agents as one

**Plugins**: Extend agent capabilities through:
- Native functions (code-based tools)
- Semantic functions (prompt-based)
- OpenAPI specs
- Model Context Protocol (MCP)

**Connectors**: abstractions for LLM and service integrations (OpenAI, Azure OpenAI, HuggingFace, Google, etc.)
- Base classes: `ChatCompletionClientBase`, `EmbeddingGeneratorBase`, `TextCompletionClientBase`
- Each connector implements service-specific logic for the AI provider

**Process Framework**: Structured workflow modeling for complex business processes with steps, steps with steps (nested processes), and user-defined functions.

### Key File Patterns

- **Python**: `semantic_kernel/` contains core packages. Connectors are in `semantic_kernel/connectors/`, agents in `semantic_kernel/agents/`. Memory stores are in `semantic_kernel/connectors/memory_stores/`.
- **.NET**: Solution organized by feature (Agents, Connectors, Plugins, VectorData). Each connector has a matching UnitTests project with `.UnitTests` suffix.

### Pydantic Migration (Python)

New serializable classes should extend `KernelBaseModel` for consistency:
```python
from semantic_kernel.kernel_pydantic import KernelBaseModel

class MyClass(KernelBaseModel):
    field: str
```

### Kernel Extension Pattern (Python)

The Kernel class uses multiple inheritance via extension mixins:
- `KernelFilterExtension`: Adds filter management (function invocation, prompt rendering, auto function invocation)
- `KernelFunctionExtension`: Adds plugin/function management
- `KernelServicesExtension`: Adds AI service management
- `KernelReliabilityExtension`: Adds reliability/retry handling

Example: `class Kernel(KernelFilterExtension, KernelFunctionExtension, KernelServicesExtension, KernelReliabilityExtension)`

### Configuration

For local development, API keys are loaded from `.env` files using Pydantic settings. Create an `openai.env` file:
```env
OPENAI_API_KEY=""
OPENAI_CHAT_MODEL_ID="gpt-4o-mini"
```
Then pass `env_file_path="openai.env"` to connector constructors.

## Code Style

### Python
- Use `ruff` for formatting (line length: 120), configured in `pyproject.toml`
- Follow Google docstring conventions
- Use `async def` for asynchronous operations (pytest uses `asyncio_mode = "auto"`)
- Prefer type annotations and generics
- Use `OneOrMany`, `OptionalOneOrMany` type utilities from `kernel_types.py`

### .NET
- C# 14+ with nullable reference types enabled
- ImplicitUsings disabled (explicit imports required)
- XML documentation required for public APIs
- Use `Kernel.CreateBuilder()` pattern for initialization

### Kernel Functions

Native functions use the `@kernel_function` decorator (Python) or `[KernelFunction]` attribute (C#):
```python
from semantic_kernel.functions import kernel_function

class MyPlugin:
    @kernel_function(description="What this function does")
    def my_function(self, input: str) -> str:
        return result
```

## Important Notes

- Java code is maintained in a separate repository
- Breaking changes require issue discussion before PR
- All PRs must pass CI checks before merge
- Pre-commit hooks enforce code quality