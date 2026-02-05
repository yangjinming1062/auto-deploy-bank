# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NagaAgent is a multi-service intelligent conversation assistant system with multi-agent collaboration, voice interaction, and knowledge graph memory. The system uses a multi-process microservices architecture running independent servers on different ports.

## Build and Run Commands

```bash
# Initial setup (auto-installs dependencies, creates venv)
python setup.py

# Run development environment check
python main.py --check-env --force-check
python main.py --quick-check

# Run application
python main.py

# Update application
./update.sh  # Linux/macOS
update.bat   # Windows

# Build standalone package
python build.py
```

## Architecture Overview

### Multi-Service Architecture (ports: 8000, 8001, 8003, 5048)

```
UI Layer (PyQt5)
    ↓
API Server (:8000) → Agent Server (:8001) → MCP Server (:8003)
    ↓                    ↓                      ↓
Memory System       Task Scheduler         Tools (MCP Protocol)
                    Game/Theory System
    ↓
GRAG Memory System (Neo4j optional)
```

### Core Components

| Directory | Purpose |
|-----------|---------|
| `apiserver/` | REST API server, conversation management, streaming responses, document processing |
| `agentserver/` | Agent task scheduling, computer control, tool management |
| `mcpserver/` | Model Context Protocol tools (crawl4ai, vision, online search, etc.) |
| `game/` | Multi-agent game theory system with RoleGenerator, SignalRouter, DynamicDispatcher |
| `summer_memory/` | GRAG knowledge graph memory system (Neo4j-based) |
| `voice/` | Voice I/O (ASR, TTS, realtime voice with WebRTC) |
| `ui/` | PyQt5 GUI with Live2D avatar support |

### Game System Architecture (game/)

The `game/` module implements multi-agent collaboration based on game theory:

```
NagaGameSystem
├── RoleGenerator → generates agent roles via LLM
├── SignalRouter → builds agent communication paths
├── DynamicDispatcher → routes messages between agents
├── UserInteractionHandler → processes user requests
└── GameEngine → self-game loop (Actor → Criticizer → PhilossChecker)
```

### Configuration

- Main config: `config.json` (copy from `config.json.example`)
- API key and model settings in `config.api` section
- Neo4j for knowledge graph: set `config.grag.enabled=true` and configure connection
- Ports: API (8000), Agent (8001), MCP (8003), TTS (5048)

## Key Patterns

### Tool Calling Format (HANDOFF)

LLM responses use `<<<[HANDOFF]>>>` format for tool calls:
```python
<<<[HANDOFF]>>>
tool_name: 「始」service_name「末」
param1: 「始」value1「末」
<<<[END_HANDOFF]>>>
```

### Game System Flow
```python
from game import NagaGameSystem, Task

game = NagaGameSystem()
task = Task(task_id="x", description="task", domain="领域", requirements=[])
result = await game.execute_full_game_flow(task, expected_agent_count=(3, 6))
```

### API Server Usage
```python
# Stream response with tool call extraction
POST /chat/stream
# Returns SSE with markers: [SENTENCE], [TOOL_CALL], [TOOL_RESULT], [TOOL_ERROR]
```

### Agent Server Endpoints
- `POST /analyze_and_execute` - Intent analysis and execution
- `GET /tasks?session_id=xxx` - Task management

## Critical Implementation Details

1. **Conversation core migrated**: `conversation_core` deleted, functionality moved to `apiserver/`

2. **PyInstaller compatibility**: `main.py` checks `sys.frozen` and `_MEIPASS` for packaged builds

3. **nagaagent-core dependency**: Core vendored in local `nagaagent-core/` directory, takes precedence over system-installed version

4. **Async event loop**: Services run in background threads with dedicated event loops via `ServiceManager`

5. **Port availability checking**: Pre-check ports before launching servers to avoid crashes

6. **Proxy settings**: Controlled by `config.api.applied_proxy` - if false, clears HTTP_PROXY environment variables

7. **GRAG memory**: Optional Neo4j-based memory system; falls back gracefully if unavailable