# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Semantic Kernel is Microsoft's multi-language SDK (Python, .NET) for building AI agents and multi-agent systems. It provides model-agnostic orchestration with support for OpenAI, Azure OpenAI, Hugging Face, and 100+ LLM providers. Note: Java development has moved to [semantic-kernel-java](https://github.com/microsoft/semantic-kernel-java).

**Key features**: Agent framework, multi-agent orchestration, plugin ecosystem, vector database support, process framework, and enterprise reliability.

## Build and Test Commands

### Python

```bash
cd python

# Full setup: installs uv, Python 3.10-3.13, SK, all dependencies, and pre-commit hooks
make install

# Install with specific Python version
make install PYTHON_VERSION=3.12

# Run a single test file
uv run pytest tests/unit/test_kernel.py

# Run a specific test
uv run pytest tests/unit/test_kernel.py::test_some_function -v

# Run unit tests only (fast, no API keys needed)
uv run pytest tests/unit

# Run integration tests (requires API keys for Azure/OpenAI)
uv run pytest tests/integration

# Run tests matching a pattern
uv run pytest -k "agent" tests/

# Run tests with coverage report
uv run pytest --cov=semantic_kernel --cov-report=term-missing tests/unit/

# Run code quality checks (same as CI)
uv run pre-commit run -a

# Build the package
make build
```

### .NET

```bash
cd dotnet

# Build and run all unit tests
bash build.sh

# Run a single test project
dotnet test src/SemanticKernel.UnitTests/SemanticKernel.UnitTests.csproj

# Run a specific test
dotnet test src/SemanticKernel.UnitTests/SemanticKernel.UnitTests.csproj --filter "FullyQualifiedName~TestName"

# Linting with auto-fix
dotnet format
```

## Architecture

### Core Concept: The Kernel

The `Kernel` class is the central orchestrator. It:
- Manages plugins (collections of functions)
- Registers AI services (LLM clients, embedding generators)
- Executes functions with filtering and error handling pipelines
- Handles prompt rendering and auto function invocation

### Python Package Structure

The main `semantic_kernel/` package is organized by functional domain:

| Directory | Purpose |
|-----------|---------|
| **agents/** | Agent framework (`ChatCompletionAgent`, `AgentGroupChat`, `AgentThread`) for building modular AI agents |
| **connectors/** | AI service integrations (`OpenAI`, `Azure`, `Google`) and vector store connectors (`Qdrant`, `Redis`, `Pinecone`) |
| **core_plugins/** | Built-in plugins (`MathPlugin`, `TextMemoryPlugin`, `TimePlugin`) |
| **filters/** | Hook points for function invocation, prompt rendering, and auto function invocation |
| **functions/** | `KernelFunction`, `KernelPlugin`, and `@kernel_function` decorator for native functions |
| **memory/** | Semantic memory abstraction for embeddings |
| **processes/** | Process framework for structured workflow orchestration |
| **template_engine/** | Prompt templating using `{{$variable}}` syntax |
| **contents/** | Message content types (`ChatHistory`, `StreamingChatMessageContent`) |
| **services/** | AI service abstraction layer and selection |
| **data/** | Schema and data types for AI services |

### .NET Solution Structure (SK-dotnet.slnx)

| Folder | Purpose |
|--------|---------|
| **SemanticKernel.Abstractions** | Core interfaces and types |
| **SemanticKernel.Core** | Main implementation (Kernel, plugins, prompts) |
| **Agents/** | Agent framework (`Core`, `OpenAI`, `AzureAI`, `Orchestration`) |
| **Connectors/** | AI service integrations (OpenAI, Azure, Google, Ollama, etc.) |
| **VectorData/** | Vector storage and search abstractions and implementations |
| **Plugins/** | Built-in plugins (Core, Web, Document, MsGraph) |
| **Functions/** | gRPC, OpenAPI, and Prompty function support |
| **Experimental/** | Process framework and Flow orchestration (legacy) |
| **Extensions/** | Prompt template engines (Handlebars, Liquid) |

### Key Extension Patterns

**Plugins (Native Functions)**:
- Python: Create a class with methods decorated with `@kernel_function`
- .NET: Use `KernelPluginFactory.CreateFromType<T>()` with `[KernelFunction]` attributes

**AI Connectors**:
- Python: Extend `ChatCompletionClientBase` or `EmbeddingGeneratorBase`
- .NET: Implement `IChatCompletionService` or `IEmbeddingGeneratorService`

**Vector Stores**:
- Python: Extend `VectorStoreRecordCollection`
- .NET: Implement `IVectorStoreRecordCollection`

**Filters**:
- Python: Implement filter interfaces in `semantic_kernel/filters/`
- .NET: Use the filter abstractions in `Microsoft.SemanticKernel.Filters`

## Code Conventions

### Python

- Use `KernelBaseModel` (Pydantic v2) for serializable classes
- Google-style docstrings: one-line summary, blank line, Args/Returns/Raises sections
- Pre-commit hooks enforce: `ruff-format`, `ruff`, `bandit`, copyright headers
- Run `uv run pre-commit run -a` before committing
- Python 3.10+ required, 3.13 supported (experimental)

### .NET

- Follow [Microsoft C# coding conventions](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- Nullable reference types enabled, `Nullable` annotation in Directory.Build.props
- Target frameworks: `net10.0`, `net8.0`, `netstandard2.0`
- Run `dotnet format` before committing
- AOT compatibility required where possible (`IsAotCompatible`)

## Important Development Notes

1. **No breaking changes**: All PRs must maintain API compatibility. Breaking changes will be rejected.
2. **Issue-first workflow**: Create an issue before implementing non-trivial changes.
3. **Tests required**: New features need tests; bug fixes should include a regression test.
4. **Experimental APIs**: APIs marked with `@experimental` or `SKEXP*` warnings may change.
5. **Java development**: Java SDK has moved to a separate repository - do not modify `/java/`.

## Repository Structure

- **dotnet/** - .NET SDK implementation
- **python/** - Python SDK implementation
- **prompt_template_samples/** - Prompty template examples
- **docs/** - Project documentation
- **.github/workflows/** - CI/CD pipelines