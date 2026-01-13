# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Minima is an on-premises RAG (Retrieval-Augmented Generation) system that allows querying local documents using various AI integrations (ChatGPT, Anthropic Claude, or fully local LLMs).

The project is structured as a set of microservices orchestrated via Docker Compose, with Python backends (FastAPI) and Node.js frontends.

## Architecture

The system consists of several independent services that communicate via HTTP/WebSocket:

1.  **Indexer** (`indexer/`): Scans `LOCAL_FILES_PATH` for documents (PDF, DOCX, etc.), chunks them, and stores embeddings in Qdrant.
2.  **LLM** (`llm/`): Handles RAG queries. It retrieves relevant chunks from Qdrant via the Indexer, reranks them, and generates answers using an LLM (Ollama).
3.  **Linker** (`linker/`): Bridges external AI providers (ChatGPT Custom GPTs) with the internal Minima services. It polls Firestore for requests and submits results.
4.  **MCP Server** (`mcp-server/`): A Python MCP server allowing AI assistants (like Claude Desktop) to query the local Minima instance.
5.  **Chat UI** (`chat/`): A React application for local chat interactions.
6.  **Electron App** (`electron/`): A desktop wrapper for the Chat UI.

### Data Flow

- **Local Mode**: Electron/Chat UI -> `llm` (WebSocket) -> `indexer` (HTTP).
- **ChatGPT Mode**: ChatGPT Custom GPT -> Firestore -> `linker` -> `indexer`/`llm` -> Firestore.
- **MCP Mode**: Claude Desktop -> `mcp-server` -> `indexer` (HTTP).

## Commands

### Running the System

The primary way to run the system is using Docker Compose. A helper script `run.sh` is provided for interactive selection.

```bash
# Select deployment mode
./run.sh
```

Or run directly with docker compose:

```bash
# Fully local (Ollama + Qdrant + Indexer + LLM + Chat UI)
docker compose -f docker-compose-ollama.yml --env-file .env up --build

# ChatGPT Integration (Linker + Indexer + LLM)
docker compose -f docker-compose-chatgpt.yml --env-file .env up --build

# MCP Integration (MCP Server + Indexer)
docker compose -f docker-compose-mcp.yml --env-file .env up --build
```

### Frontend Development

**Chat UI (React):**

```bash
cd chat
npm install
npm start
```

**Electron App:**

```bash
cd electron
npm install
npm start
```

### MCP Server (Python)

Requires Python >= 3.10 and `uv`.

```bash
cd mcp-server
uv run minima
```
Or use the helper script for Copilot integration:
```bash
./run_in_copilot.sh <path_to_project>
```

## Configuration

- Root `.env` file is required for container deployments (see `.env.sample`).
- **Critical Variables**:
  - `LOCAL_FILES_PATH`: The directory to index.
  - `OLLAMA_MODEL`: The LLM to use (for local mode).
  - `EMBEDDING_MODEL_ID` / `EMBEDDING_SIZE`: For vectorization.