# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the source code for the Alibaba Cloud Large Model ACP (Advanced Professional Certification) course. It contains a series of Jupyter Notebooks and Python modules demonstrating how to build an intelligent Q&A system (RAG application) using LLMs, specifically focusing on Alibaba Cloud's DashScope (Bailian) services.

## Commands

**Setup & Installation**

```bash
pip install -r requirements.txt
```

**Environment Configuration**

You must set the `DASHSCOPE_API_KEY` environment variable to use the LLM features. This can be done by:
1. Creating a `Key.json` file in the root or course directory with `{"DASHSCOPE_API_KEY": "your-key"}`.
2. Or setting it directly in your environment: `export DASHSCOPE_API_KEY="your-key"`.

The course tutorials often import `config.load_key` to handle this interactively.

**Running Notebooks**

The primary learning format is Jupyter Notebooks (`.ipynb` files). To run them:
```bash
jupyter notebook <notebook_file>.ipynb
```

## Architecture

The core logic for the Q&A bot is located in `LLM_ACP_EN/p2_Build LLM Q&A System/`.

### Core Components (`chatbot/`)

- **`llm.py`**: Wrapper for LLM calls. Currently uses the DashScope API (compatible with OpenAI interface).
  - Key function: `invoke(user_message, model_name)`
- **`rag.py`**: Implements RAG (Retrieval-Augmented Generation) logic using LlamaIndex.
  - Functions: `create_index()`, `load_index()`, `create_query_engine()`.
  - Stores knowledge base in `./docs`.
- **`agent.py`**: Agent implementation using AgentScope (optional advanced module).

### Utilities (`utils/`)

- **`ragas_evaluate.py`**: Contains logic for evaluating the RAG system using RAGAS metrics.
- **`security/`**: Modules for content moderation and security checks (text, image, audio, video).

### Configuration (`config/`)

- **`load_key.py`**: Utility to load the DashScope API key from `Key.json` or prompt for it.

## Key Dependencies

- **DashScope**: The primary LLM provider (`dashscope` SDK).
- **Llama-Index**: For building RAG pipelines (`llama-index-core`, `llama-index-llms-dashscope`, etc.).
- **AgentScope**: For Agent development.
- **Gradio**: For building the web UI.
- **Ragas**: For automated evaluation.