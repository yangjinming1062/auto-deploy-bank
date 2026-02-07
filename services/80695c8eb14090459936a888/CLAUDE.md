# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Codefuse-ChatBot (DevOps-ChatBot) is a Multi-Agent AI chatbot framework for DevOps tasks. It supports isolated sandbox code execution, LLM integration (OpenAI, fastchat, Chinese APIs), vector-based knowledge retrieval, and an extensible Multi-Agent framework.

## Common Commands

```bash
# Setup configuration (required before first run)
cd configs
cp model_config.py.example model_config.py
cp server_config.py.example server_config.py

# Configure environment variables
export OPENAI_API_KEY="sk-xxx"
export API_BASE_URL="https://api.openai.com/v1"

# Start the complete service (includes sandbox, API, and web UI)
cd examples
python start.py

# Start individual services
python examples/llm_api.py          # LLM API service (port 8888)
python examples/api.py              # API server (port 7861)
streamlit run examples/webui.py     # Web UI (port 8501)
```

## Architecture

### Core Components

- **muagent/coagent**: The main Multi-Agent framework module providing:
  - `BasePhase`: Pre-configured agent execution chains (baseGroupPhase, baseTaskPhase, codeReactPhase, docChatPhase, etc.)
  - `BaseAgent`: Individual agent instances with role configurations
  - `BaseChain`: Multi-agent chained execution
  - Connector modules for LLM, embedding, memory, and prompt management

- **examples/model_workers**: LLM adapter implementations extending `ApiModelWorker`:
  - OpenAI, Azure, Qwen, ZhiPu, XingHuo, Spark, QianFan, BaiChuan, MiniMax, FangZhou, TianGong
  - Each worker implements `do_chat()` for API integration

- **examples/api.py**: FastAPI server exposing:
  - `/chat/chat` - LLM chain conversations
  - `/chat/knowledge_base_chat` - Knowledge base Q&A
  - `/chat/search_engine_chat` - Web search Q&A
  - `/chat/code_chat` - Code base conversations
  - Knowledge base management endpoints

### Configuration

Configuration files in `configs/`:
- **model_config.py**: LLM models, embedding models, vector database settings, knowledge base paths
- **server_config.py**: Service ports, Docker settings, sandbox configuration

### Data Paths

- **data/**: Vector database (chroma_data) and graph database (nebula_data)
- **nltk_data/**: NLTK tokenization data
- **jupyter_work/**: Sandbox working directory for code execution

### Web UI

The Streamlit-based web UI (`examples/webui.py`) provides:
- Chat interface with streaming responses
- Knowledge base management
- Code base management
- Configuration via `examples/webui_config.py`

## LLM Integration

To add a new LLM provider:
1. Create a worker in `examples/model_workers/` extending `ApiModelWorker`
2. Implement `do_chat()` method returning `{"error_code": int, "text": str}`
3. Register in `examples/model_workers/__init__.py`
4. Configure in `configs/model_config.py` under `ONLINE_LLM_MODEL`

## Multi-Agent Development

Use `BasePhase` to create agent execution chains:
```python
from coagent.connector.phase import BasePhase
from coagent.connector.schema import Message

phase = BasePhase("codeReactPhase", llm_config=llm_config, embed_config=embed_config)
query = Message(role_name="human", role_type="user", role_content="...")
output_message, output_memory = phase.step(query)
```

## Commit Format

Follow the convention: `[<type>](<scope>) <subject>`

Types: fix, feature, feature-wip, improvement, style, typo, refactor, optimize, test, deps, community

Scopes: connector, codechat, sandbox, etc.