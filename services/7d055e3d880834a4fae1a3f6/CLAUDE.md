# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**DeerFlow** (Deep Exploration and Efficient Research Flow) is a multi-agent research framework built on LangGraph. It orchestrates AI agents to conduct deep research, generate reports, and create content like podcasts and presentations.

## Development Commands

### Backend (Python)
```bash
uv sync                           # Install dependencies
uv run server.py --reload         # Start FastAPI dev server (localhost:8000)
uv run main.py                    # Run console UI
make test                         # Run pytest
make coverage                     # Run tests with coverage report
make lint                         # Ruff linting
make format                       # Ruff formatting
make langgraph-dev                # Start LangGraph Studio for graph debugging
```

### Frontend (Web UI)
```bash
cd web && pnpm install            # Install dependencies
pnpm dev                          # Start Next.js dev server (localhost:3000)
pnpm build                        # Production build
pnpm typecheck                    # TypeScript checking
pnpm lint                         # ESLint
pnpm test:run                     # Jest tests
```

### Full Stack
```bash
./bootstrap.sh -d                 # macOS/Linux: run both backend and frontend
bootstrap.bat -d                  # Windows
```

## Architecture

### Multi-Agent Workflow (LangGraph)

The main research workflow is defined in `src/graph/builder.py`:

```
coordinator → background_investigator → planner → research_team (router)
                                              ↓
                        ┌─────────────────────┼─────────────────────┐
                        ↓                     ↓                     ↓
                    researcher              analyst              coder
                        └─────────────────────┼─────────────────────┘
                                              ↓
                                           reporter → END
```

**Node functions** are in `src/graph/nodes.py`:
- `coordinator_node`: Entry point managing workflow lifecycle
- `background_investigation_node`: Initial context gathering
- `planner_node`: Decomposes research objectives into structured plans
- `research_team_node`: Router directing to specialized agents
- `researcher_node`: Web search and information gathering
- `analyst_node`: Data analysis and evaluation
- `coder_node`: Python code execution and analysis
- `reporter_node`: Synthesizes findings into reports
- `human_feedback_node`: Interactive plan modification/approval

**State management** is defined in `src/graph/types.py`. Use `src/graph/checkpoint.py` for MongoDB/PostgreSQL checkpointing.

### Secondary Graphs

Additional LangGraph workflows for post-processing:
- `src/podcast/graph/builder.py`: Podcast script and TTS generation
- `src/ppt/graph/builder.py`: PowerPoint presentation generation
- `src/prose/graph/builder.py`: Report editing (continue, fix, improve, shorter, longer)
- `src/prompt_enhancer/graph/builder.py`: Query enhancement

### Key Directories

| Directory | Purpose |
|-----------|---------|
| `src/agents/` | Agent definitions and tool interceptors |
| `src/graph/` | LangGraph workflow definitions and nodes |
| `src/tools/` | External tools (search, crawl, TTS, Python REPL, retriever) |
| `src/prompts/` | Agent prompt templates with i18n support |
| `src/crawler/` | Web content extraction (Jina, InfoQuest) |
| `src/llms/` | LLM provider integrations |
| `src/server/` | FastAPI endpoints and WebSocket handling |
| `src/rag/` | RAG integrations (Qdrant, Milvus, RAGFlow, VikingDB, Dify, MOI) |
| `web/src/app/` | Next.js pages and API routes |
| `web/src/components/` | React UI components (Radix-based design system) |

### External Integrations

- **Search**: Tavily, InfoQuest, DuckDuckGo, Brave Search, Arxiv, Searx (configured via `.env` SEARCH_API)
- **Crawling**: Jina, InfoQuest (configured via `conf.yaml`)
- **TTS**: Volcengine TTS API (`/api/tts` endpoint)
- **Checkpoint**: MemorySaver (default), MongoDB, PostgreSQL (`LANGGRAPH_CHECKPOINT_DB_URL`)
- **MCP**: Model Context Protocol servers (dynamic loading from config)

## Adding New Features

### New Agent
1. Create agent in `src/agents/agents.py`
2. Add node function in `src/graph/nodes.py`
3. Register node in `src/graph/builder.py._build_base_graph()`
4. Add edge in conditional routing logic

### New Tool
1. Implement in `src/tools/`
2. Register in agent's prompt template in `src/prompts/`
3. Add configuration in `src/config/tools.py` if needed

### New LangGraph Workflow
1. Create graph builder in `src/[feature]/graph/builder.py`
2. Define state in `src/[feature]/graph/state.py`
3. Add nodes in `src/[feature]/graph/[node]_node.py`
4. Register API endpoint in `src/server/`

### Frontend Component
1. Add React component to `web/src/components/`
2. Add API client to `web/src/core/api/`
3. Export types alongside components