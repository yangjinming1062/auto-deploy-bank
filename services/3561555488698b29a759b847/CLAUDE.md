# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Volcengine AI App Lab - a high-code Python SDK (`arkitect`) for building LLM applications on the Volcengine Ark platform, along with demo applications (`demohouse`). The SDK provides agent orchestration, tool calling, and streaming support for building complex AI applications.

## Development Commands

```bash
# Install dependencies (uses uv)
make install

# Install with lint/typing/test dependencies
make install_ci

# Build the package
make build

# Run tests (default: tests/ut/)
make test TEST_FILE=tests/ut/

# Run linting (ruff + mypy on arkitect/ and examples/)
make lint

# Format code
make format

# Spell check/fix
make spell_check
make spell_fix
```

## Architecture

### Core Components (`arkitect/core/`)

| Component | Purpose |
|-----------|---------|
| `component/context/` | **Context** - Core LLM interaction class managing state, tools, and hooks |
| `component/agent/` | **Agent** - BaseAgent, DefaultAgent, ParallelAgent for agent patterns |
| `component/runner/` | **Runner** - Orchestrates agent execution with checkpoint support |
| `component/tool/` | **Tool** - ToolPool, MCP client/server integration for function calling |
| `component/llm/` | **LLM** - LangChain-compatible chat model interface |
| `component/bot/` | **BotServer** - FastAPI server for OpenAI-compatible endpoints |
| `component/llm_event_stream/` | Event streaming with hooks and state management |
| `component/checkpoint/` | Checkpoint service for session state persistence |

### Key Classes

- **Context**: Initialize with `model`, `tools`, and `parameters`. Call `await ctx.init()` then use `ctx.completions.create()` for LLM calls.
- **Runner**: Wraps an Agent and handles execution flow. Use with `Runner(app_name="...", agent=agent)`.
- **Agent**: Define custom agents by subclassing BaseAgent or using DefaultAgent with instruction/tools.
- **BotServer**: FastAPI app that serves OpenAI-compatible `/api/v3/bots/chat/completions` endpoint.

### Hook System

Four hook interfaces allow interception at key points:
- `PreLLMCallHook` / `PostLLMCallHook` - Before/after LLM calls
- `PreToolCallHook` / `PostToolCallHook` - Before/after tool execution

Register hooks via `context.set_xxx_hook()`. Hooks receive and must return `State`.

### Tool Registration

Register tools by passing callables to Context:
```python
def calculator(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

ctx = Context(model="doubao-1.5-pro", tools=[calculator])
```

Tools support MCP clients via `build_mcp_clients_from_config()`.

### Streaming

Context.completions.create supports streaming:
- `stream=False`: Returns complete `ArkChatResponse` with usage stats
- `stream=True`: Returns async generator of `ArkChatCompletionChunk`

Handle `ContextInterruption` in streaming loops for tool errors or hook interruptions.

### Launching Servers

```python
from arkitect.launcher.local.serve import launch_serve

launch_serve(
    package_path="main",
    port=8080,
    endpoint_path="/api/v3/bots/chat/completions",
    health_check_path="/v1/ping",
)
```

## Commit Convention

This project uses Conventional Commits with custom scopes:
- Types: `docs`, `feat`, `fix`, `perf`, `refactor`, `revert`, `style`, `test`, `release`, `license`
- Scopes: `arkitect`, `demohouse/*`, `mcp/*`
- Example: `feat(arkitect): add new hook type`

## Dependencies

- Python 3.10+
- Core: langchain, fastapi, pydantic, volcanic-sdk-ark-runtime
- Dev: ruff, mypy, pytest, syrupy (snapshot testing)