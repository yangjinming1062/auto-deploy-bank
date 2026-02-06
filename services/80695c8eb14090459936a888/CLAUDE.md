# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CodeFuse-ChatBot is an AI intelligent assistant for the full software development lifecycle (DevOps), covering design, coding, testing, deployment, and operations. It uses Retrieval Augmented Generation (RAG), Tool Learning, and sandbox execution environments.

## Development Setup

**Environment:**
- Python 3.9.18 recommended
- CUDA 11.7 for GPU support
- Tested on Windows, Linux (X86), and macOS with Apple Silicon (M-series)

**Install dependencies:**
```bash
cd codefuse-chatbot
pip install -r requirements.txt
```

**Configure the project:**
```bash
cd examples
cp ../configs/model_config.py.example ../configs/model_config.py
cp ../configs/server_config.py.example ../configs/server_config.py
```

## Running the Application

**Quick start (web UI configuration):**
```bash
cd examples
bash start.sh
# Or directly: streamlit run webui_config.py --server.port 8510
```

**Start services manually:**
```bash
cd examples
python start.py
# This starts: API server (7861), WebUI (8501), SDFILE_API (7862), LLM API (8888), Sandbox (5050)
```

**Stop all services:**
```bash
python stop.py
```

**Run a single test:**
```bash
python -m pytest tests/torch_test.py
python tests/file_test.py
```

## Architecture

```
codefuse-chatbot/
├── examples/
│   ├── webui/              # Streamlit UI pages
│   │   ├── dialogue.py     # Main chat interface with multiple modes
│   │   ├── knowledge.py    # Knowledge base management
│   │   ├── code.py         # Code knowledge base management
│   │   └── utils.py        # UI utilities
│   ├── api.py              # FastAPI backend (port 7861)
│   ├── llm_api.py          # FastChat OpenAI-compatible API (port 8888)
│   ├── sdfile_api.py       # File storage API (port 7862)
│   ├── webui.py            # Main UI entry point
│   ├── start.py            # Service orchestration script
│   └── stop.py             # Service shutdown script
├── configs/
│   ├── default_config.py   # Default paths (logs, sources, knowledge_base, etc.)
│   ├── model_config.py     # LLM/embedding model configurations
│   └── server_config.py    # Server ports and Docker settings
├── web_crawler/
│   ├── utils/
│   │   ├── WebCrawler.py   # Web content crawling (requests/selenium)
│   │   ├── Html2Text.py    # HTML to text extraction
│   │   └── WebHtmlExtractor.py  # HTML content extraction
│   └── main_test.py        # Crawler usage example
├── sources/                # Static assets, documentation images
├── tests/                  # Unit tests
└── nltk_data/              # NLTK model data
```

## Key Components

### Multi-Modal Chat Modes (dialogue.py)
1. **LLM Chat** - Direct LLM conversation
2. **Knowledge Base Chat** - RAG with document retrieval (FAISS vector store)
3. **Code Base Chat** - Code repository Q&A with graph-based retrieval
4. **Search Engine Chat** - Web search-augmented responses
5. **Agent Chat** - Multi-Agent orchestration with tool usage

### Backend APIs (api.py)
- `/chat/chat` - LLM chain conversation
- `/chat/knowledge_base_chat` - Knowledge base Q&A
- `/chat/code_chat` - Code base Q&A
- `/knowledge_base/*` - Knowledge base management CRUD
- `/code_base/*` - Code base management

### Service Ports
| Service | Port |
|---------|------|
| WebUI | 8501 |
| API Server | 7861 |
| SDFILE_API | 7862 |
| FastChat OpenAI API | 8888 |
| Sandbox (Jupyter) | 5050 |
| Nebula Graph | 9669 |

### Configuration Points
- **LLM models**: `configs/model_config.py` - `llm_model_dict` and `ONLINE_LLM_MODEL`
- **Embedding models**: `configs/model_config.py` - `embedding_model_dict`
- **Vector store type**: `configs/default_config.py` - `DEFAULT_VS_TYPE` (faiss, milvus, pg)
- **Chunk settings**: `CHUNK_SIZE=500`, `OVERLAP_SIZE=50` in default_config.py

## Dependencies

Key dependencies from requirements.txt:
- `torch<=2.0.1` - ML framework
- `fschat==0.2.33` - FastChat for model serving
- `streamlit*` - Web UI framework
- `muagent` - Multi-agent orchestration (external package)
- `unstructured[all-docs]` - Document parsing
- `duckduckgo-search` - Web search
- `nltk~=3.8.1` - NLP tools

## Web Crawler Usage

```python
from web_crawler.utils.WebCrawler import WebCrawler

wc = WebCrawler()
# Single URL
wc.webcrawler_single(
    html_dir="data/html/output.jsonl",
    text_dir="data/text/output.jsonl",
    base_url="https://example.com",
    reptile_lib="requests",  # or "selenium"
    time_sleep=4
)

# Batch crawling from page links
wc.webcrawler_1_degree(
    html_dir="data/html/output.jsonl",
    text_dir="data/text/output.jsonl",
    base_url="https://example.com",
    target_url_prefix="https://example.com",  # limit to same domain
    reptile_lib="requests"
)
```

## Commit Format

When contributing, follow the project's commit format:
```
[<type>](<scope>) <subject> (#pr)
```

Types: `fix`, `feature`, `feature-wip`, `improvement`, `style`, `typo`, `refactor`, `performance/optimize`, `test`, `deps`, `community`