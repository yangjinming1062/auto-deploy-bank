# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI-powered bank statement document analysis system. Extracts financial data from PDF bank statements using LLMs and RAG, stores in vector databases, and enables natural language queries for personal financial analysis.

## Commands

### Setup
```bash
# Create virtual environment
python3 -m venv venvEnvLLM
source src/activate_virual_environment.sh

# Install dependencies
pip3 install -r src/requirements.txt

# Install Tesseract OCR (Linux)
bash src/install-pytesseract-for-linux.sh
```

### Running Applications
```bash
# Google Gemini version (requires VPN for Hong Kong)
streamlit run src/gemini-version/apps.py

# Local/Open LLM version (Llama3, Gemma, Qwen, etc.)
streamlit run src/local-multimodel-version/app.py
```

### Development
- Development notebooks are in `src/dev/` - open with Jupyter to test new models/techniques
- Main development notebooks: `ai_bank_statement_dev.ipynb`, `ai_agent_dev.ipynb`, `RAG_algorthm_test.ipynb`

## Architecture

### Three Main Components
1. **Document Processing Pipeline**: PDF extraction → text chunking → embedding → vector storage
2. **RAG System**: Query retrieval from vector DB → LLM response generation
3. **AI Agents**: LangGraph/CrewAI agents for automated document analysis workflows

### Data Flow
```
PDF Upload → Text Extraction (PyMuPDF/PyPDF2) → Chunking (RecursiveCharacterTextSplitter)
          → Embedding (HuggingFace/Google) → Vector Store (ChromaDB/FAISS/Pinecone)
          → Retrieval → LLM Prompt → Response
```

### Key Classes/Configuration
- `CFG` class in notebooks manages all model/feature flags (use local LLM vs cloud, vector DB selection, evaluation tools)
- `DeepEvalFramework` class for LLM evaluation using DeepEval/RAGAS metrics
- `safety_settings` dictionary configures Google Gemini content filtering

### Vector Database Options
Configured via `CFG.USE_CHROMA`, `CFG.USE_FAISS`, `CFG.USE_PINECONE`, `CFG.USE_MILVUS`, `CFG.USE_WEAVIATE`

### LLM Configuration
- Cloud: Google Gemini (`models/embedding-001`, `gemini-pro`)
- Local: HuggingFace models (Llama-3.2-3B, Qwen, Gemma-2, DeepSeek)
- Controlled via `CFG.USE_*` flags and `CFG.model*` variables

### Evaluation Stack
- DeepEval for LLM benchmarks (MMLU, HumanEval, TruthfulQA)
- RAGAS for RAG-specific metrics
- Weights & Biases for experiment tracking (`src/dev/wandb/`)

## Environment Variables

Required in `.env` files:
- `GOOGLE_API_KEY` - Google Gemini API
- `HuggingFace` - HuggingFace access token
- `wandb_api_key` - Weights & Biases
- `PINECONE_API_KEY` - Pinecone vector DB (optional)
- `OPENROUTER_API_KEY` - OpenRouter (optional)

Each app directory has its own `.env` or `.env_test` file.

## Dependencies

Major dependencies managed in `src/requirements.txt`:
- **LLM/Embedding**: langchain, langchain-google-genai, transformers, sentence-transformers
- **VectorDB**: chromadb, faiss-cpu, pinecone-client, pymilvus, weaviate-client
- **UI**: streamlit
- **Document**: pymupdf, pypdf, pytesseract, unstructured
- **Agents**: langgraph, crewai
- **Evaluation**: deepeval, ragas, wandb
- **Vision**: ultralytics (YOLO for document layout detection)