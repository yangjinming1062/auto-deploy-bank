# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Notion Question-Answering system** built with LangChain that allows querying a Notion database using natural language. It uses a RAG (Retrieval-Augmented Generation) architecture with OpenAI embeddings and FAISS for vector search.

The system exports data from Notion, processes it into a vector database, and provides both CLI and Streamlit interfaces for asking questions.

## Core Architecture

The application follows a simple three-stage pipeline:

1. **Data Ingestion** (`ingest.py`): Processes Notion markdown exports
   - Reads `.md` files from `Notion_DB/` directory
   - Splits text into chunks (1500 character limit)
   - Creates embeddings using OpenAIEmbeddings
   - Stores vectors in FAISS database
   - Outputs: `docs.index` (FAISS index) + `faiss_store.pkl` (metadata)

2. **Query Interface** (`qa.py` and `main.py`): Answers questions
   - Loads FAISS index and metadata
   - Uses RetrievalQAWithSourcesChain for context-aware answers
   - Returns answer + source files

3. **Data Storage**:
   - `docs.index`: FAISS vector index
   - `faiss_store.pkl`: Serialized LangChain FAISS store with metadata

## Key Files

- **main.py** - Streamlit web interface (port 8501 by default)
- **qa.py** - Command-line interface (`python qa.py "question"`)
- **ingest.py** - Data ingestion script
- **Notion_DB/** - Directory containing Notion export (markdown files)
- **requirements.txt** - Dependencies: langchain, openai, faiss-cpu, streamlit, streamlit-chat, tiktoken

## Common Development Tasks

### Setup Environment
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your_api_key_here
```

### Ingest New Notion Data
```bash
# 1. Export Notion database as Markdown & CSV
unzip Export-*.zip -d Notion_DB
# 2. Process the data
python ingest.py
```

### Run the Application
```bash
# Streamlit web interface
streamlit run main.py

# CLI interface
python qa.py "is there food in the office?"
```

## Example Data

The repository includes example data from Blendle's Employee Handbook (exported October 18th). This serves as a sample dataset for testing and demonstration purposes.

## Dependencies

All dependencies are listed in `requirements.txt`:
- langchain (v0.0.170) - Core framework
- openai - OpenAI API client
- faiss-cpu - Vector database
- streamlit - Web UI framework
- streamlit-chat - Chat UI components
- tiktoken - Tokenizer for OpenAI models

## Important Notes

- **Required Environment Variable**: `OPENAI_API_KEY` must be set
- **Data Format**: Notion exports must be in Markdown & CSV format
- **Vector Store**: Both `docs.index` and `faiss_store.pkl` must exist for queries to work
- **Chunking**: Text is split into 1500-character chunks with newline separators for optimal LLM context handling
- **Model**: Uses OpenAI embeddings for vectorization and ChatOpenAI for question answering (temperature=0 for deterministic responses)