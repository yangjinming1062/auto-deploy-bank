# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Semantic Kernel is a multi-language SDK for building AI agents and multi-agent systems. The repository contains implementations in Python, .NET (C#), and references to a separate Java repository.

**Key Resources:**
- [Python SDK Docs](https://learn.microsoft.com/en-us/python/api/semantic-kernel/semantic_kernel)
- [.NET SDK Docs](https://learn.microsoft.com/en-us/dotnet/api/microsoft.semantickernel)
- [Getting Started Guide](https://learn.microsoft.com/en-us/semantic-kernel/get-started/quick-start-guide)

## Build Commands

### Python

```bash
# Install Python 3.10, uv, and all dependencies
make install

# Install with specific Python version (3.10, 3.11, 3.12 supported)
make install PYTHON_VERSION=3.12

# Run unit tests
uv run pytest tests/unit

# Run all tests
uv run pytest tests

# Run integration tests
uv run pytest tests/integration

# Code quality checks (ruff, mypy, bandit)
uv run pre-commit run -a

# Build the package
cd python && make build
```

### .NET

```bash
# Build all solutions
dotnet build ./dotnet/SK-dotnet.slnx -c Release

# Run tests
dotnet test ./dotnet/SK-dotnet.slnx -c Release

# Format code
dotnet format
```

## Architecture

### Core Concepts

1. **Kernel**: The main entry point (`python/semantic_kernel/kernel.py`, `dotnet/src/SemanticKernel.Core`). Manages plugins, services, and function invocation.

2. **Agents**: Build modular AI agents with tools, memory, and planning capabilities.
   - Python: `semantic_kernel.agents.ChatCompletionAgent`
   - .NET: `Microsoft.SemanticKernel.Agents.ChatCompletionAgent`

3. **Plugins**: Extend agent capabilities through:
   - Native code functions (`@kernel_function` in Python, `[KernelFunction]` in C#)
   - Prompt templates (stored in `prompt_template_samples/`)
   - OpenAPI specifications
   - Model Context Protocol (MCP)

4. **Connectors**: AI service integrations for LLM providers:
   - OpenAI, Azure OpenAI, Anthropic, Google, HuggingFace, Ollama, etc.
   - Located in `python/semantic_kernel/connectors/` and `dotnet/src/Connectors/`

5. **Memory**: Vector database support for semantic memory:
   - Azure AI Search, Elasticsearch, Chroma, Pinecone, Qdrant, Redis, etc.
   - Python: `python/semantic_kernel/memory/`
   - .NET: `dotnet/src/VectorData/`

6. **Process Framework**: Model complex business workflows with structured approaches.
   - Python: `python/semantic_kernel/processes/`
   - .NET: `dotnet/src/SemanticKernel.Core/`

### Project Structure

```
/python/
  semantic_kernel/          # Main SDK package
    agents/                 # Agent implementations
    connectors/             # AI service connectors
    contents/               # Chat/message content types
    core_plugins/           # Built-in plugins (Text, Math, Time)
    filters/                # Request/response filters
    functions/              # Function definition and invocation
    memory/                 # Vector storage and retrieval
    processes/              # Process framework
    prompt_template/        # Prompt templating engine
    template_engine/        # Template parsing and rendering
  samples/                  # Concept samples and demos
  tests/                    # Unit and integration tests

/dotnet/
  src/
    Agents/                 # Agent implementations
    Connectors/             # AI service connectors
    Functions/              # Function definitions
    Plugins/                # Built-in plugins
    SemanticKernel.Abstractions/
    SemanticKernel.Core/    # Core kernel and orchestration
    VectorData/             # Vector storage
  samples/
  test/

/prompt_template_samples/   # Example prompt templates
  ChatPlugin/, WriterPlugin/, etc.
```

### Key Patterns

**Defining a Native Plugin (Python):**
```python
from semantic_kernel.functions import kernel_function

class MyPlugin:
    @kernel_function(description="Description of what the function does")
    def my_function(self, input_param: str) -> str:
        """Function implementation."""
        return f"Result: {input_param}"
```

**Creating an Agent:**
```python
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

agent = ChatCompletionAgent(
    service=AzureChatCompletion(),
    name="MyAgent",
    instructions="You are a helpful assistant.",
    plugins=[MyPlugin()],
)
```

## Code Style

### Python
- **Linting**: ruff with Google docstring convention
- **Formatting**: ruff-format
- **Type hints**: Required for public APIs
- **Serialization**: Use `KernelBaseModel` (pydantic-based) for serializable classes
- **Async**: Most functions are async by default

### .NET
- **Style**: C# coding conventions with nullable reference types enabled
- **Analyzers**: All analyzers enabled (`AnalysisMode: AllEnabledByDefault`)
- **Language**: C# 14+ (`LangVersion: 14`)

## Testing Requirements

- All new features require tests
- Bug fixes must include a test that reproduces the issue
- Unit tests in `tests/unit/` or equivalent directories
- Integration tests in `tests/integration/` or equivalent directories
- Python coverage threshold: tracked via pytest-cov

## Environment Variables

Set these for running samples and tests:
```bash
export OPENAI_API_KEY="sk-..."          # For OpenAI
export AZURE_OPENAI_API_KEY="..."       # For Azure OpenAI
export AZURE_OPENAI_ENDPOINT="..."      # Azure endpoint URL
export AZURE_OPENAI_DEPLOYMENT="..."    # Deployment name
```

## Breaking Changes

Contributions must maintain API signature and behavioral compatibility. Breaking changes require filing an issue for discussion first.

## Contribution Workflow

1. Create an issue or find an existing one
2. Create a branch from `main`
3. Make changes following code conventions
4. Add/run tests
5. Run linting: `uv run pre-commit run -a` (Python) or `dotnet format` (.NET)
6. Create PR against `main`