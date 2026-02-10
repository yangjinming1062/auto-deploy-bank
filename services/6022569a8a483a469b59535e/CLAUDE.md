# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Semantic Kernel is a model-agnostic SDK for building AI agents and multi-agent systems. It's a polyglot repository with implementations in **Python**, **.NET (C#)**, and **Java**.

## Common Commands

### Python

```bash
# Install dependencies (Python 3.10-3.13 supported)
make install
make install PYTHON_VERSION=3.12  # Install with specific Python version

# Build
make build
uvx --from build pyproject-build --installer uv

# Run tests
uv run pytest tests/unit                    # Unit tests
uv run pytest tests/integration             # Integration tests
uv run pytest tests                         # All tests
uv run pytest tests/unit -k "test_name"     # Single test

# Code coverage
uv run pytest --cov=semantic_kernel --cov-report=term-missing tests/unit/

# Code quality checks
uv run pre-commit run -a                    # Run all pre-commit checks

# Format code
uv run ruff check --fix .
uv run ruff format .
```

### .NET

```bash
# Build (from dotnet directory)
dotnet build --configuration Release
dotnet build --configuration Debug

# Run all unit tests
dotnet test --configuration Release

# Run specific test project
dotnet test path/to/SomeTest.csproj

# Format code
dotnet format

# Build script (runs build + tests in Release)
./build.sh
```

## Architecture

### Python Package Structure

```
python/semantic_kernel/
├── agents/              # Agent framework - ChatCompletionAgent, OpenAIAssistantAgent,
│                       # AzureAIAgent, BedrockAgent, group chat, orchestration strategies
├── connectors/          # AI service connectors - OpenAI, Azure, HuggingFace, Anthropic, etc.
├── contents/            # Content models (ChatMessageContent, etc.)
├── core_plugins/        # Core built-in plugins
├── filters/             # Filter system for hooks (function invocation, etc.)
├── functions/           # KernelFunction definitions
├── kernel.py            # Main Kernel class - orchestrates AI services
├── memory/              # Memory implementations (vector stores, semantic memory)
├── processes/           # Process framework for structured workflows
├── prompt_template/     # Prompt template handling
├── services/            # Service abstractions
├── template_engine/     # Template engines (Handlebars, Jinja2, etc.)
└── utils/               # Utilities
```

### .NET Project Structure

```
dotnet/src/
├── Agents/              # Agent abstractions and implementations
│   ├── Abstractions/    # Core agent interfaces
│   ├── Core/            # Core agent functionality
│   ├── OpenAI/          # OpenAI Assistants integration
│   ├── AzureAI/         # Azure AI Agent integration
│   ├── Bedrock/         # Amazon Bedrock Agents
│   ├── Orchestration/   # Agent orchestration (Sequential, Concurrent, Handoffs)
│   └── Runtime/         # Agent runtime (InProcess, Core)
├── Connectors/          # AI and memory service connectors
├── Functions/           # Function definitions and plugins
├── Plugins/             # Plugin implementations (Core, Document, Web, etc.)
├── SemanticKernel.Abstractions/  # Core interfaces and types
├── SemanticKernel.Core/          # Main implementation
├── Extensions/          # Extended functionality
├── VectorData/          # Vector database support
└── InternalUtilities/   # Shared internal utilities
```

### Key Concepts

- **Kernel**: Central orchestrator that manages AI services, plugins, and function execution
- **Agents**: Autonomous entities with identity, instructions, and tools. Modalities include:
  - `ChatCompletionAgent` - LLM-based agents using local chat history
  - `OpenAIAssistantAgent` - OpenAI Assistants API based agents
  - `AzureAIAgent` - Azure AI Agent Service based agents
  - `BedrockAgent` - Amazon Bedrock Agents
- **Plugins**: Collections of functions (native code, semantic prompts, OpenAPI specs)
- **Connectors**: Abstractions for connecting to AI services (OpenAI, Azure, HuggingFace, etc.)
- **Channels**: Protocol for agent-conversation interaction (handles modality-specific state)
- **Process Framework**: Structured workflow approach for complex business processes
- **Filters**: Hook system for intercepting and modifying execution (function invocation, auto-function invocation)

### AI Service Configuration

Configure via environment variables:
- OpenAI: `OPENAI_API_KEY`, `OPENAI_CHAT_MODEL_ID`
- Azure OpenAI: `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT`

## Code Style

### Python
- **Formatter**: ruff format (line-length: 120)
- **Linter**: ruff with Google docstring convention
- **Async**: Use `async def` for asynchronous operations
- **Models**: Use Pydantic models extending `KernelBaseModel`

### .NET
- **Language**: C# 14 with nullable reference types
- **Formatter**: dotnet format
- **ImplicitUsings**: disabled - use explicit namespace imports

## Testing

- Unit tests are under `tests/unit/` (Python) or `*.UnitTests.csproj` projects (.NET)
- Integration tests require API keys and are skipped in PRs (run separately)
- Code coverage threshold: 80%