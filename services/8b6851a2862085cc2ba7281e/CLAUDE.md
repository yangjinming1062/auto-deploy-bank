# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Easy-RAG is a Retrieval-Augmented Generation (RAG) system that integrates with Ollama for local LLM inference. It supports multiple vector databases (Chroma, FAISS, Elasticsearch), knowledge graph extraction (Neo4j), and AI-powered web search via SearxNG.

## Common Commands

### Environment Setup
```bash
# Create conda environment
conda create -n Easy-RAG python=3.10.9
conda activate Easy-RAG

# Install dependencies
pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
```

### Running the Application
```bash
# Main RAG WebUI
python webui.py

# Knowledge Graph Extraction Tool
python graph_demo_ui.py
```

### Dependencies
- **Ollama**: Required for LLM and Embedding models. Must be running locally (`http://localhost:11434`).
- **SearxNG**: Required for the "AI Web Search" feature. Must be running at `http://localhost:8080`.
- **Neo4j**: Optional. Used for the Knowledge Graph feature if `VECTOR_DB` is configured for it or if using `graph_demo_ui.py` with persistence.

## Architecture

### Core Components
- **Web Interface (`webui.py`)**: Gradio-based UI handling chat, knowledge base management (upload/vectorize/delete), and web search.
- **RAG Logic (`rag/rag_class.py`)**: Implements `RAG_class` which orchestrates retrieval and generation. Supports three retrieval strategies:
  - `simple_chain`: Direct retrieval and answer generation.
  - `rerank_chain`: Retrieval followed by re-ranking using a cross-encoder model.
  - `rag_chain` (Complex): Decomposes questions into sub-questions for improved recall.
- **Vector Databases (`embeding/`)**: Abstraction layer over `ChromaDB`, `FAISS`, and `ElasticsearchStore`. Selected via `Config/config.py`.
- **Configuration (`Config/config.py`)**: Central configuration for vector database selection (`VECTOR_DB`), directory paths, and Neo4j settings.

### Data Flow
1. **Ingestion**: Files are uploaded via UI, parsed using `unstructured` (PDF, DOCX, etc.) or `funasr` (Audio/Video), chunked, and embedded using Ollama embeddings, then stored in the selected vector DB.
2. **Chat**: User query $\rightarrow$ Retrieve relevant chunks $\rightarrow$ Rerank (optional) $\rightarrow$ Generate response with LLM.
3. **Web Search**: Query $\rightarrow$ SearxNG search $\rightarrow$ LLM summarization.

## Configuration
- **Vector DB Selection**: Edit `Config/config.py` to switch between `1` (Chroma), `2` (FAISS), or `3` (Elasticsearch).
- **Model Settings**: Models are fetched dynamically from the running Ollama instance. Default expected models include `qwen2:7b` (LLM) and `mofanke/acge_text_embedding:latest` (Embedding).
- **Re-ranking**: The `rag/rerank.py` script loads `BAAI/bge-reranker-large`. Update the `tokenizer` and `model` paths if not using the default Windows path `E:\model\bge-reranker-large`.