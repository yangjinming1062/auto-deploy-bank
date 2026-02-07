# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Minima is an on-premises RAG (Retrieval-Augmented Generation) system for local document search and AI chat. It supports multiple deployment modes:
- **Fully Local (Ollama)**: All models run on-premises via Ollama containers
- **Custom LLM**: OpenAI-compatible API endpoints (vLLM, TGI, Ollama server, etc.)
- **ChatGPT Integration**: Custom GPT integration for document search
- **Anthropic Claude**: MCP integration for Claude Desktop app

Supported document types: PDF, XLS, DOCX, TXT, MD, CSV.

## Development Commands

### Backend Services (Docker)

```bash
# Interactive menu with all options
./run.sh

# Manual Docker Compose commands
docker compose -f docker-compose-[mode].yml --env-file .env up --build
```

Docker compose modes: `ollama`, `custom-llm`, `chatgpt`, `mcp`

### Frontend (React Web App)
```bash
cd chat
npm install
npm start       # Development server at http://localhost:3000
npm test        # Run tests
npm run build   # Production build
```

### Desktop App (Electron)
```bash
cd electron
npm install
npm start
```

### MCP Server (Standalone)
Requires Python >= 3.10 and `uv` installed.
```bash
uv --directory mcp-server run minima
```

## Architecture

### Services

| Service | Path | Port | Purpose |
|---------|------|------|---------|
| indexer | `/indexer` | 8001 | Document ingestion, embedding storage (Qdrant) |
| llm | `/llm` | 8002 | LLM interactions, streaming responses via WebSocket |
| linker | `/linker` | - | Service discovery and routing coordination |

### Technology Stack

- **Backend**: Python (FastAPI, LangChain, Qdrant, Unstructured)
- **Frontend**: React (TypeScript, Create React App), Material UI
- **Desktop**: Electron
- **Vector Database**: Qdrant
- **Protocol**: MCP (Model Context Protocol) for AI assistant integration

### Key Source Files

- `indexer/app.py` - FastAPI entry point, handles `/query` and `/files/add` endpoints
- `llm/ollama_chain.py`, `llm/openai_chain.py` - LLM chain implementations
- `mcp-server/minima/` - MCP server implementation for Claude Desktop integration

### Service Communication

- Indexer ↔ LLM: REST APIs
- LLM ↔ Frontend: WebSocket for streaming responses
- Linker: Coordinates inter-service discovery

## Environment Variables

Required variables (copy from `.env.sample`):
- `LOCAL_FILES_PATH` - Root folder for document indexing
- `EMBEDDING_MODEL_ID` - Sentence Transformer model (e.g., `sentence-transformers/all-mpnet-base-v2`)
- `EMBEDDING_SIZE` - Embedding dimension (768 for mpnet-base-v2)

Mode-specific variables:
- **Ollama**: `OLLAMA_MODEL`, `RERANKER_MODEL`
- **Custom LLM**: `LLM_BASE_URL`, `LLM_MODEL`, `LLM_API_KEY`
- **ChatGPT**: `USER_ID`, `PASSWORD`

## MCP Integration

### Claude Desktop
Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "minima": {
      "command": "uv",
      "args": ["--directory", "/path/to/minima/mcp-server", "run", "minima"]
    }
  }
}
```

### GitHub Copilot
Configure `.vscode/mcp.json`:
```json
{
  "servers": {
    "minima": {
      "type": "stdio",
      "command": "run_in_copilot.sh",
      "args": ["/path/to/minima"]
    }
  }
}
```