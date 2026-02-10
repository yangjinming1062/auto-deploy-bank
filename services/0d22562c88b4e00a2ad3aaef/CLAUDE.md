# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AppAgentX is an evolving GUI agent framework that controls Android devices (via ADB) to perform tasks. It uses LLM-based agents with LangChain/LangGraph, stores learned operation chains in Neo4j graph database, and uses Pinecone for vector storage. Screen parsing is handled by Microsoft's OmniParser via Docker containers.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Start backend services (OmniParser + ImageEmbedding)
cd backend && docker-compose up --build -d

# Run Gradio demo UI
python demo.py

# Stop backend services
cd backend && docker-compose down
```

## Architecture

### Frontend (Gradio)
- **demo.py**: Main web interface with 5 tabs:
  1. Initialization - Configure ADB device and task
  2. Auto Exploration - LLM agent automatically explores and learns workflows
  3. User Exploration - Human demonstrates operations manually
  4. Chain Understanding & Evolution - Convert learned chains into reusable high-level actions
  5. Action Execution - Execute tasks using learned shortcuts

### Agent Modes (LangGraph StateGraph)
- **explor_auto.py**: Automatic exploration using `create_react_agent` with tools
  - Nodes: `tsk_setting` → `page_understand` → `perform_action` → (loop)
  - Uses `screen_action` tool for ADB operations
  - Uses `screen_element` for OmniParser screen parsing

- **explor_human.py**: Human-guided exploration for recording demonstrations

### Memory & Evolution System
- **chain_evolve.py**: Evaluates if a chain can be templated, generates high-level action nodes
- **chain_understand.py**: Analyzes operation paths and extracts reasoning
- **deployment.py**: Task execution with shortcut matching from learned actions

### Data Layer
- **data/graph_db.py** (Neo4jDatabase): Graph operations for Page, Element, Action nodes
  - Relationships: `HAS_ELEMENT`, `LEADS_TO`, `COMPOSED_OF`
- **data/vector_db.py**: Pinecone vector store for visual embeddings
- **data/State.py**: TypedDict state schemas for exploration and deployment
- **data/data_storage.py**: JSON state persistence in `./log/json_state`

### Tool Layer (ADB via LangChain tools)
- **tool/screen_content.py**:
  - `list_all_devices()`: List ADB-connected devices
  - `get_device_size()`: Get screen resolution
  - `take_screenshot()`: Capture device screen via ADB
  - `screen_element()`: Call OmniParser API for UI parsing
  - `screen_action()`: Perform tap, back, text, swipe, long_press operations

### Backend Services (Docker)
- **backend/OmniParser/**: Screen parsing service (port 8000) - parses UI into structured elements
- **backend/ImageEmbedding/**: Feature extraction service (port 8001)

## Configuration

All configuration is in `config.py`:
- `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` - LLM endpoint (supports OpenAI-compatible APIs like DeepSeek)
- `Neo4j_URI`, `Neo4j_AUTH` - Graph database connection
- `Feature_URI` - Image embedding service (default: http://127.0.0.1:8001)
- `Omni_URI` - Screen parser service (default: http://127.0.0.1:8000)
- `PINECONE_API_KEY` - Vector database key

## Key Patterns

- State is passed through the graph as TypedDict with annotated messages
- Tools are decorated with `@tool` from langchain_core.tools
- Neo4j stores pages, elements, and actions with relationships forming operation chains
- High-level actions are composite actions stored in Action nodes with `COMPOSED_OF` relationships to elements
- Frontend callbacks receive current State and node name for real-time progress updates