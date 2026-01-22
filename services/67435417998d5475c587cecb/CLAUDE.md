# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository demonstrates 6 context engineering techniques using LangGraph, as described in Drew Breunig's ["How to Fix Your Context"](https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html). It is organized as a series of Jupyter notebooks, each implementing a specific technique.

## Commands

### Setup
This project uses [uv](https://docs.astral.sh/uv/) for Python package management.
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Running Notebooks
Launch Jupyter to view and run the notebooks in the `notebooks/` directory:
```bash
jupyter notebook
```

## Architecture

- **`notebooks/`**: Contains 6 sequential tutorials (01-rag.ipynb to 06-context-offloading.ipynb). Each notebook implements a distinct context engineering pattern using `StateGraph`.
- **`notebooks/utils.py`**: Shared utilities for visualizing agent messages and retrieval results using the `rich` library.
- **Dependencies**: `langgraph`, `langchain`, `langchain-openai`, and `langchain-anthropic` are the core frameworks.

## Context Engineering Techniques

The notebooks implement the following techniques from Breunig's post:
1. **RAG**: Augmenting prompts with retrieved context.
2. **Tool Loadout**: Selectively loading tool definitions to avoid context distraction.
3. **Context Quarantine**: Isolating contexts in separate threads/agents (Supervisor pattern).
4. **Context Pruning**: Removing irrelevant details from context before LLM processing.
5. **Context Summarization**: Compressing verbose context into summaries.
6. **Context Offloading**: Storing information outside the context window (Scratchpads/Store).