# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CSV-AI is a Streamlit web application that uses LangChain and OpenAI to interact with, summarize, and analyze CSV files. It provides a chat interface for exploring CSV data through AI.

## Commands

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run the application:**
```bash
streamlit run app.py
```

**Required environment:**
- OpenAI API key (set via `.env` file as `OPENAI_API_KEY` or entered in the sidebar)

## Architecture

The application is a single-file Streamlit app (`app.py`) with three main features:

1. **Chat with CSV** - RAG-based chat using FAISS vector store. CSV data is loaded, split into chunks, embedded with OpenAI embeddings, and stored in FAISS for similarity search.

2. **Summarize CSV** - Uses LangChain's `load_summarize_chain` with map_reduce strategy to generate summaries of CSV content.

3. **Analyze CSV** - Uses LangChain's `create_pandas_dataframe_agent` to allow natural language querying of pandas DataFrames.

**Key functions:**
- `retriever_func()` - Cached function that loads CSV, creates embeddings, and builds FAISS retriever
- `chat()` - RAG chat interface with conversation memory
- `summary()` - Summary generation with map_reduce chain
- `analyze()` - Pandas DataFrame agent for data analysis

**Dependencies:** Streamlit, LangChain, OpenAI, FAISS, Pandas, python-dotenv