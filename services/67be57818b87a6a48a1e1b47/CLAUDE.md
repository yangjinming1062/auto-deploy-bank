# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

QA-Pilot is an interactive chat application that uses LLMs (local or cloud) to answer questions about GitHub code repositories. It features a **FastAPI backend** and **Svelte SPA frontend**, with support for multiple LLM providers via LangChain integrations.

## Common Commands

### Backend (Python/FastAPI)
```bash
# Run the main application
python qa_pilot_run.py

# Test PostgreSQL connection
python check_postgresql_connection.py
```

### Frontend (Svelte)
```bash
cd svelte-app
npm install                    # Install dependencies
npm run dev                    # Development server (port 5001)
npm run build                  # Production build with Rollup
```

### Go CodeGraph Parser
```bash
go build -o parser parser.go   # Compile the Go parser
./parser /path/to/file.go      # Parse a Go file (outputs JSON)
```

## Architecture

### Backend Stack (`app.py` is main entry)
- **FastAPI** on port 5000 with CORS middleware
- **PostgreSQL** for session/messages storage (session-per-table pattern)
- **ChromaDB** for vector embeddings storage (`VectorStore/` directory)
- **LangChain** for LLM orchestration (v0.2.6)

### Data Flow
1. User provides GitHub URL via Svelte UI (`NewSourceModal`)
2. Backend clones repo to `projects/` via `DataHandler.git_clone_repo()`
3. Files are loaded and chunked (`DataHandler.load_files()`, `split_files()`)
4. Chunks embedded and stored in ChromaDB (`store_chroma()`)
5. Chat queries use `ConversationalRetrievalChain` with:
   - Similarity retrieval (configurable k=3)
   - Optional FlashRank reranking (`rr:` prefix)
   - Custom prompt templates

### LLM Provider Support (`qa_model_apis.py`)
- **ollama**: local models via HTTP (default: http://localhost:11434)
- **openai**: GPT models (API key in `.env`)
- **anthropic**: Claude models
- **mistralai**, **zhipuai**, **nvidia**, **tongyi**, **moonshot**: cloud APIs
- **localai**: LocalAI Docker containers
- **llamacpp**: Local GGUF models via llama-cpp-python

### Embedding Models
- **huggingface**: sentence-transformers (default: all-MiniLM-L6-v2)
- **ollama**: nomic-embed-text, mxbai-embed-large

### CodeGraph Visualization
- **Python**: `utils/codegraph.py` uses AST parsing to extract classes/methods/functions/calls
- **Go**: `parser.go` is a standalone Go binary that parses Go AST and outputs JSON

### Session Management
- Sessions stored in PostgreSQL `sessions` table
- Messages stored in dynamic `session_{id}` tables
- Current session tracked globally in `app.py::current_session`

## Key Configuration Files

- `config/config.ini`: Model providers, database, directories, chunk settings
- `config/prompt_templates.ini`: Custom QA and code analysis prompts
- `.env`: API keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.)

## Special Input Prefixes

- `rsd:`: Return source documents with answer
- `rr:`: Use FlashRank reranker for retrieval