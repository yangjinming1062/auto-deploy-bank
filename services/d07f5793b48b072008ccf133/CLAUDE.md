# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GAM (General Agentic Memory) is a dual-agent memory framework for AI agents that combines long-term retention with dynamic reasoning. It follows a Just-in-Time (JIT) memory optimization principle, performing deep research at runtime to build adaptive, high-utility context.

**Core Architecture:**
- **MemoryAgent**: Constructs structured memory from raw text/sessions using `memorize(message)` → `MemoryUpdate`
- **ResearchAgent**: Performs iterative retrieval, reflection, and summarization to answer questions

## Commands

### Installation
```bash
pip install -r requirements.txt
pip install -e .
```

### Development
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_ttl_memory.py -v

# Linting and formatting
black gam/
flake8 gam/
mypy gam/
```

### Running Examples
```bash
cd examples/quickstart
python basic_usage.py
python model_usage.py
```

### Evaluation (requires downloaded datasets)
```bash
# Set API key
export OPENAI_API_KEY="your-key"

# Run evaluations
bash scripts/eval_hotpotqa.sh
bash scripts/eval_narrativeqa.sh
bash scripts/eval_locomo.sh
bash scripts/eval_ruler.sh

# Or directly
python eval/hotpotqa_test.py --data data/hotpotqa/eval_400.json --outdir ./results/hotpotqa --memory-api-key $OPENAI_API_KEY --memory-model gpt-4o-mini
```

## Core Architecture

```
gam/
├── agents/               # Dual-agent system
│   ├── memory_agent.py  # MemoryAgent: memory construction via memorize()
│   └── research_agent.py # ResearchAgent: iterative research via research()
├── generator/            # LLM backends
│   ├── openai_generator.py  # OpenAI API + compatible endpoints
│   └── vllm_generator.py    # Local vLLM inference
├── retriever/            # Retrieval strategies
│   ├── dense_retriever.py   # Semantic search (FlagEmbedding + FAISS)
│   ├── bm25.py              # Keyword search (pyserini)
│   └── index_retriever.py   # Direct index access
├── schemas/              # Data models
│   ├── memory.py         # MemoryState, MemoryStore
│   ├── page.py           # Page, PageStore
│   ├── ttl_memory.py     # TTL-enabled stores for production
│   └── result.py         # ResearchOutput, Result schemas
├── config/               # Configuration classes
└── prompts/              # LLM prompt templates
```

### Key Data Flow

1. **Memory Construction**: `MemoryAgent.memorize()` → generates abstract → stores in `MemoryStore` + `PageStore`
2. **Research**: `ResearchAgent.research(query)` → multi-iteration retrieval → reflection → integrated answer

### Store Types

- `InMemoryMemoryStore` / `InMemoryPageStore`: Ephemeral in-memory storage
- `TTLMemoryStore` / `TTLPageStore`: Persistent with automatic expiration (for production)

### Retriever Types

- `DenseRetriever`: Semantic/vector search (requires FlagEmbedding, FAISS)
- `BM25Retriever`: Keyword search (requires pyserini)
- `IndexRetriever`: Direct page lookup

Optional retrievers are lazy-loaded and set to `None` if dependencies are missing.

## Dependencies Note

Some retrievers require optional dependencies:
- BM25Retriever: needs `pyserini>=0.22.0`
- DenseRetriever: needs `FlagEmbedding>=1.2.0`, `faiss-cpu>=1.7.4`

The main `pip install -r requirements.txt` installs core dependencies only.