# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AppAgentX is an LLM-based GUI agent framework that evolves high-level actions for smartphone automation. It uses LangChain/LangGraph for agent orchestration, Neo4j for graph-based memory, Pinecone for vector storage, and Dockerized backend services for screen parsing.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Launch Gradio demo UI (requires ADB-connected Android device/emulator)
python demo.py
# or
gradio demo.py

# Clear databases (Neo4j and Pinecone)
python utils.py

# Backend services (Docker required with GPU support)
cd backend && docker-compose up --build
# Services:
# - Image Feature Extraction: http://localhost:8001
# - Screen Parsing Service: http://localhost:8000
```

## Configuration

All configuration is in `config.py`:
- LLM settings (OpenAI-compatible API, base URL, model)
- Neo4j connection (URI, credentials)
- Pinecone API key
- Backend service URIs (Feature extraction port 8001, OmniParser port 8000)

## Architecture

### Agent Modes (in `demo.py`)
1. **Automatic Exploration** (`explor_auto.py`): Uses LangGraph ReAct agent to autonomously complete tasks
2. **Human-Guided Exploration** (`explor_human.py`): Records human demonstrations for learning
3. **Chain Evolution** (`chain_evolve.py`): Evolves recorded operation chains into reusable high-level actions using LLM evaluation
4. **Chain Understanding** (`chain_understand.py`): Stores and analyzes chain data in Neo4j

### Deployment Flow (`deployment.py`)
1. Match user task to high-level actions via LLM
2. Retrieve element sequences and shortcuts from Neo4j
3. Match screen elements using vector similarity (Pinecone)
4. Execute templates or fall back to ReAct agent

### Database Layer (`data/`)
- **`graph_db.py`**: Neo4j node management (Page, Element, Action) with relationships:
  - `Page-HAS_ELEMENT->Element`: Elements on a page
  - `Element-LEADS_TO->Page`: Navigation paths
  - `Action-COMPOSED_OF->Element`: High-level action composition
- **`vector_db.py`**: Pinecone for visual embedding similarity search (2048-dim vectors)

### Backend Services (`backend/`)
- **OmniParser**: Screen parsing via Docker (port 8000) using Microsoft's UI element detection
- **ImageEmbedding**: Feature extraction service (port 8001) for visual embeddings

### Tool Layer (`tool/`)
- **`screen_content.py`**: ADB operations, screen element parsing
- **`img_tool.py`**: Image processing and manipulation

### State Management
- **`State.py`**: Defines two TypedDicts:
  - `State`: For learning/exploration mode
  - `DeploymentState`: For task execution mode