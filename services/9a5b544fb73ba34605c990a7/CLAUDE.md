# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ThinkRAG is a LLM RAG (Retrieval Augmented Generation) application built on LlamaIndex and Streamlit. It enables Q&A with a local knowledge base and is optimized for Chinese users.

## Commands

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the application
streamlit run app.py

# The app runs at http://localhost:8501
```

## Environment Variables

```bash
OPENAI_API_KEY=your-key      # For OpenAI API models
DEEPSEEK_API_KEY=your-key    # For DeepSeek API
MOONSHOT_API_KEY=your-key    # For Moonshot API
ZHIPU_API_KEY=your-key       # For ZhiPu API
THINKRAG_ENV=production      # Switch to production mode (default: development)
```

## Architecture

### Application Structure

```
app.py                 # Main entry point, Streamlit page routing
config.py              # Global configuration (models, paths, defaults)
frontend/              # Streamlit UI pages
  Document_QA.py       # Query interface (chat with knowledge base)
  KB_File.py           # File upload and indexing
  KB_Web.py            # Web URL ingestion
  KB_Manage.py         # Knowledge base management
  Model_*.py           # Model configuration pages
  state.py             # Streamlit session state initialization
server/                # Backend RAG components
  engine.py            # Query engine creation with retrieval
  index.py             # IndexManager class for index operations
  ingestion.py         # AdvancedIngestionPipeline for document processing
  retriever.py         # Hybrid retriever (vector + BM25)
  models/              # LLM and embedding model factories
  stores/              # Storage backends (chat, config, doc, index, vector)
  splitters/           # Chinese text splitters
  readers/             # Web content readers
```

### Data Flow

1. **Document Ingestion** (`IndexManager.load_files`/`load_websites`):
   - Documents → `AdvancedIngestionPipeline` → text splitting → embedding → nodes
   - Nodes stored in vector store and doc store

2. **Query Processing** (`Document_QA.perform_query`):
   - User query → `SimpleFusionRetriever` (vector + BM25) → optional reranking
   - Retrieved nodes → LLM response using Chinese prompt templates

3. **Storage Context** (`server/stores/strage_context.py`):
   - **Dev mode**: Local JSON files in `storage/` directory
   - **Production mode**: Redis + LanceDB/Chroma

### Key Components

- **Hybrid Retrieval**: Combines vector search (semantic) with BM25 (keyword) using distance-based score fusion
- **Chinese Optimization**: Uses jieba for BM25 tokenization, custom Chinese text splitters
- **Model Abstraction**: All LLM/embedding interactions go through LlamaIndex APIs
- **Configuration Persistence**: `LocalKVStore` in `config_store.py` saves user settings

### Model Configuration

Models are defined in `config.py`:
- `LLM_API_LIST`: LLM API providers (OpenAI-compatible)
- `EMBEDDING_MODEL_PATH`: BGE models from BAAI
- `RERANKER_MODEL_PATH`: BGE reranking models

Adding a new model provider requires:
1. Add API config to `LLM_API_LIST` in `config.py`
2. Create model creation function in `server/models/`
3. Add UI page in `frontend/` if configuration UI needed