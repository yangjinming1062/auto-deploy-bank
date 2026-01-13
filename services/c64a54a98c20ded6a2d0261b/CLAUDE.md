# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**memary** is a long-term memory system for autonomous agents that emulates human memory patterns. It integrates knowledge graphs, memory streams, and entity knowledge stores to enable agents to maintain and utilize contextual information over time.

- **Python version requirement**: `<= 3.11.9`
- **Package name**: `memary`
- **License**: MIT

## Quick Start

### Development Setup

1. Create virtual environment with Python <= 3.11.9
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

The project includes a Streamlit web interface:

```bash
cd streamlit_app
streamlit run app.py
```

### Package Installation

To install the package:

```bash
pip install memary
```

## Architecture Overview

The codebase is organized into three main modules under `src/memary/`:

### 1. Agent (`src/memary/agent/`)
- **`base_agent.py`**: Core `Agent` class that manages:
  - LLM/Vision model initialization (supports Ollama and OpenAI)
  - Graph database integration (FalkorDB or Neo4j)
  - Knowledge Graph RAG retriever
  - ReAct agent with custom tools
  - Memory system integration

- **`chat_agent.py`**: Extends `Agent` with chat-specific functionality:
  - Chat message handling
  - Memory persistence
  - Entity tracking

- **`llm_api/tools.py`**: Custom tools for the ReAct agent
- **`data_types.py`**: Data structures (`Context`, `Message`)

### 2. Memory (`src/memary/memory/`)
- **`memory_stream.py`**: Records all entities with timestamps (breadth of knowledge)
- **`entity_knowledge_store.py`**: Tracks entity frequency/recency (depth of knowledge)
- **`types.py`**: Memory data structures (`MemoryItem`, `KnowledgeMemoryItem`)
- **`base_memory.py`**: Base memory class

### 3. Synonym Expansion (`src/memary/synonym_expand/`)
- Custom synonym expansion for knowledge graph retrieval

## Core Concepts

### Knowledge Graph Integration
- Uses **LlamaIndex** for graph operations
- Supports **FalkorDB** (preferred, enables multi-tenant) or **Neo4j**
- Implements recursive and multi-hop retrieval for efficient querying
- Stores agent responses and extracts entities for graph updates

### Memory System
- **Memory Stream**: Timeline-based entity tracking (JSON file)
- **Entity Knowledge Store**: Frequency/recency-based ranking (JSON file)
- Both persist to disk and sync with graph database

### Default Agent Tools
- `search`: Knowledge graph queries with Perplexity fallback
- `vision`: LLaVA (Ollama) or GPT-4 Vision
- `locate`: Google Maps integration
- `stocks`: Alpha Vantage API

## Development Workflow

### Testing

Tests are located in `dev/KG_memory_stream/tests/`:
```bash
cd dev/KG_memory_stream
python -m pytest tests/memory/test_memory_stream.py -v
python -m pytest tests/memory/test_entity_knowledge_store.py -v
```

### Configuration

Required environment variables (in `.env`):
```bash
# Required for OpenAI models
OPENAI_API_KEY="your_key"

# Database (choose one)
FALKORDB_URL="falkor://[[username]:[password]]@[host]:port"
NEO4J_PW="your_password"
NEO4J_URL="your_url"

# Optional APIs
PERPLEXITY_API_KEY
GOOGLEMAPS_API_KEY
ALPHA_VANTAGE_API_KEY
```

### Model Configuration

**LLM Models** (default: `llama3` via Ollama):
- `llama3` (Ollama) - recommended
- `gpt-3.5-turbo` (OpenAI)

**Vision Models** (default: `llava` via Ollama):
- `llava` (Ollama) - recommended
- `gpt-4-vision-preview` (OpenAI)

### Custom Tools

```python
from memary.agent.chat_agent import ChatAgent

def custom_tool(x):
    """Custom tool documentation"""
    return x

agent = ChatAgent(...)
agent.add_tool({"custom_tool": custom_tool})
agent.remove_tool("custom_tool")
```

## Key Files and Directories

- **`pyproject.toml`**: Package metadata and dependencies
- **`streamlit_app/app.py`**: Web interface entry point
- **`streamlit_app/data/`**: Default persona files and JSON storage
  - `user_persona.txt`: User profile template
  - `system_persona.txt`: System behavior configuration
  - `memory_stream.json`: Initial memory state
  - `entity_knowledge_store.json`: Initial knowledge state
  - `past_chat.json`: Chat history seed
- **`dev/`**: Experimental features and benchmarks
  - `recursive_retrieval/`: Recursive KG retrieval experiments
  - `KG_memory_stream/`: Memory system tests
  - `query_decomposition/`: Query processing research
  - `reranking/`: Result ranking experiments

## Usage Examples

### Basic Agent

```python
from memary.agent.chat_agent import ChatAgent

chat_agent = ChatAgent(
    agent_name="Personal Agent",
    memory_stream_json="data/memory_stream.json",
    entity_knowledge_store_json="data/entity_knowledge_store.json",
    system_persona_txt="data/system_persona.txt",
    user_persona_txt="data/user_persona.txt",
    past_chat_json="data/past_chat.json",
    user_id="user_a"  # For FalkorDB multi-tenancy
)
```

### Query Agent

```python
response = chat_agent.get_routing_agent_response("What do you know about machine learning?")
```

### Memory Management

```python
# Add chat with entities
chat_agent.add_chat(
    role="user",
    content="I'm interested in transformers",
    entities=["transformers", "attention mechanism"]
)

# Clear all memory
chat_agent.clearMemory()
```

## Common Operations

### Multi-Graph Setup (FalkorDB)

Create separate agents for different users by using unique `user_id` values:

```python
agent_a = ChatAgent(..., user_id="user_a")
agent_b = ChatAgent(..., user_id="user_b")
```

### Debugging

Enable debug mode to log ReAct agent execution steps:

```python
agent = ChatAgent(..., debug=True)
# Check data/routing_response.txt for execution trace
```

### Memory Token Management

Agent automatically manages context window with:
- **Context length limit**: 4096 tokens
- **Eviction rate**: 70%
- **Chat history summarization**: When approaching limits

## Important Notes

- Graph database connection is initialized in `Agent.__init__()` - FalkorDB takes precedence if both URLs are present
- Memory is automatically persisted after each chat addition
- Entity extraction happens during LLM processing for graph updates
- The ReAct agent is used for planning/execution but will be removed in future versions to support arbitrary agent types
- Custom synonym expansion function can be provided to `KnowledgeGraphRAGRetriever`