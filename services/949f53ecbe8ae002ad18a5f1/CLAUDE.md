# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Chat-with-Git-Repo is a chatbot application that allows users to ask questions about any Git repository. It uses:
- **Streamlit** for the web UI
- **OpenAI GPT-3.5-turbo** for generating responses
- **Activeloop Deep Lake** as the vector database for semantic search

The application works by cloning a repository, processing its files into embeddings, storing them in Deep Lake, then using RAG (retrieval-augmented generation) to answer questions.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r dev-requirements.txt

# Run linter
flake8 src

# Format code
black src
```

## CLI Usage

```bash
# Process a repository (creates embeddings in Deep Lake)
python src/main.py process --repo-url <repository_url>

# Start the chat UI (requires an existing dataset)
python src/main.py chat --activeloop-dataset-name <dataset_name>
```

## Architecture

- **`src/main.py`**: CLI entry point with `process` and `chat` subcommands. Handles argument parsing and delegates to other modules.
- **`src/utils/process.py`**: Repository processing pipeline:
  - `clone_repository()` - Clones git repos locally
  - `load_docs()` - Loads files, respects `.gitignore` patterns via `pathspec`
  - `split_docs()` - Chunks documents into 1000-char segments
  - `create_deeplake_dataset()` - Initializes Deep Lake with tensors for ids, metadata, embeddings, text
  - `process()` - Main orchestration function
- **`src/utils/chat.py`**: Streamlit web application:
  - `run_chat_app()` - Main UI rendering with session state for conversation history
  - `search_db()` - RAG retriever with cosine similarity and MMR
  - `generate_response()` - Calls OpenAI ChatCompletion API

## Environment Variables

Required in `.env`:
- `OPENAI_API_KEY` - OpenAI API key
- `ACTIVELOOP_TOKEN` - Deep Lake/Activeloop authentication token
- `ACTIVELOOP_USERNAME` - Activeloop account username

## Code Style

- Line length: 88 characters
- Black reads configuration from `pyproject.toml`
- Flake8 configured to ignore E501 (line too long) and W503 (line break before binary operator)