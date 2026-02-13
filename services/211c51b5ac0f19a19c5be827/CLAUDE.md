# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AutoGen is a multi-language framework for creating multi-agent AI applications. The project has separate Python and .NET implementations with shared protobuf definitions for cross-language communication via gRPC.

**Note:** AutoGen is transitioning to [Microsoft Agent Framework](https://github.com/microsoft/agent-framework). AutoGen will be maintained for bug fixes and critical security patches.

## Environment Setup

### Python (Primary)
- **Package manager:** `uv` (required, not pip/conda)
- **Python version:** 3.10+
- **Setup commands:**
  ```bash
  cd python
  uv sync --all-extras  # Creates .venv and installs dependencies
  source .venv/bin/activate
  ```

### .NET
- **SDK versions:** Requires both .NET 8.0 (runtime) and 9.0 (SDK)
- **Setup commands:**
  ```bash
  cd dotnet
  export PATH="$HOME/.dotnet:$PATH"
  dotnet restore
  dotnet build --configuration Release
  ```

## Common Commands

### Python Development
All commands run from `python/` directory with virtual environment activated.

| Command | Description |
|---------|-------------|
| `poe format` | Format code with ruff |
| `poe lint` | Lint with ruff |
| `poe mypy` | Type check with mypy (~6 min) |
| `poe pyright` | Type check with pyright (~40 sec) |
| `poe test` | Run all tests with pytest |
| `poe test-grpc` | Run gRPC tests specifically |
| `poe docs-build` | Build Sphinx documentation |
| `poe docs-check` | Check docs for warnings |
| `poe check` | Run all checks (format, lint, mypy, pyright, test, docs) |
| `poe samples-code-check` | Check samples with pyright |

**Test a single package:**
```bash
poe --directory ./packages/autogen-core test
```

### .NET Development
All commands run from `dotnet/` directory.

| Command | Description |
|---------|-------------|
| `dotnet restore` | Restore NuGet packages (~53 sec) |
| `dotnet build --configuration Release` | Build solution (~53 sec) |
| `dotnet test --filter "Category=UnitV2"` | Run unit tests (~25 sec) |
| `dotnet format --verify-no-changes` | Verify code formatting |
| `dotnet format` | Auto-format code |

**Run a sample:**
```bash
cd dotnet/samples/Hello
dotnet run
```

## Architecture

### Python Package Structure

```
python/packages/
├── autogen-core/          # Foundation: agents, runtime, messaging, models, tools
├── autogen-agentchat/     # High-level APIs: AssistantAgent, Swarm, Teams
├── autogen-ext/           # Extensions: model clients (OpenAI, Anthropic, Ollama), tools, runtimes
├── autogen-studio/        # Web-based IDE for no-code agent building
├── agbench/               # Benchmarking suite
└── magentic-one-cli/      # Multi-agent CLI application
```

### Programming Model

AutoGen uses an **event-driven, publish-subscribe architecture**:

1. **Events** - All communication uses [CloudEvents](https://cloudevents.io/) format with `id`, `source`, and `type` (reverse-DNS namespace)

2. **Agents** - Register event handlers that match specific event types (exact match or prefix patterns)

3. **Topics** - Event routing mechanism; agents subscribe to topics they care about

4. **Subscriptions** - Define which events reach which agents using type prefixes and sources

5. **Runtimes** - `AgentRuntime` is the execution environment; can be local (`SingleThreadedAgentRuntime`) or distributed via gRPC

### Cross-Language Support

- **Protocol buffers** in `protos/` define shared message types (`agent_worker.proto`, `cloudevent.proto`)
- **gRPC** runtime (`autogen_ext.runtimes.grpc`) enables Python-.NET agent communication
- Proto files are generated with: `poe gen-proto`

### Key Abstractions

- **ModelClient** - Interface for LLM interactions (defined in `autogen_core.models`)
- **Tool** - Functions agents can call (defined in `autogen_core.tools`)
- **Workbench** - Collection of tools (e.g., `McpWorkbench` for MCP servers)
- **Component** - Configurable, reusable building blocks with `Component[TConfig]`

## Code Style

### Python
- **Formatter:** ruff (with `ruff format`)
- **Linter:** ruff (select: E, F, W, B, Q, I, ASYNC, T20)
- **Type checking:** mypy (strict mode) and pyright
- **Docstrings:** Google style with Sphinx RST format; include `versionadded`/`versionchanged` tags

### .NET
- **Formatter:** dotnet format
- **Tests:** xUnit with `Category=UnitV2` filter

## Documentation

Documentation source is in `python/docs/src/` built with Sphinx.
- Build: `poe docs-build`
- Serve locally: `poe docs-serve` (auto-rebuilds on changes)

When adding new APIs, include `.. versionadded::` or `.. versionchanged::` in docstrings.

## Versioning

All `autogen-*` packages share the same version number. When changing one package, update all. Version bumps:
- Minor (0.X.0): Breaking changes
- Patch (0.0.X): New features or bug fixes