# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Azure AI Studio Copilot Sample - A deprecated reference implementation demonstrating how to build a copilot enterprise chat API that uses custom Python code to ground responses in company data. Uses RAG (Retrieval Augmented Generation) with Azure AI Search and Azure OpenAI.

## Development Commands

```bash
# Set up environment (copy .env.sample to .env and fill in Azure credentials)
cp .env.sample .env

# Install dependencies
pip install -r requirements.txt

# Build Azure AI Search index from product data
python src/run.py --build-index

# Run copilot with a sample question (default: "which tent is the most waterproof?")
python src/run.py --question "your question here"

# Test different implementations
python src/run.py --question "..." --implementation promptflow  # or langchain, aisdk

# Evaluate copilot responses against ground truth
python src/run.py --evaluate --implementation aisdk

# Deploy to Azure AI Studio
python src/run.py --deploy

# Test deployed endpoint
python src/run.py --invoke-deployment --stream  # for streaming responses

# Run tests
pytest src/tests/
```

## Architecture

### Three Copilot Implementations

This project demonstrates three approaches to building the same copilot functionality:

1. **`copilot_aisdk/`** - Direct Azure AI SDK implementation
   - `chat.py`: Async function that retrieves documents from Azure AI Search using vector embeddings, then calls Azure OpenAI with context
   - Uses Jinja2 templates for system message composition
   - Returns responses with search context attached

2. **`copilot_langchain/`** - LangChain-based implementation
   - `chat.py`: Uses LangChain's RetrievalQA chain with AzureChatOpenAI
   - Converts conversation history to LangChain memory
   - Loads MLIndex as a LangChain retriever

3. **`copilot_promptflow/`** - Prompt Flow implementation
   - `flow.dag.yaml`: YAML-defined flow with LLM nodes, document retrieval, and response generation
   - Uses PFClient to execute flows locally and for deployment
   - Includes customer lookup and documentation retrieval nodes

### Core Entry Point

- **`src/run.py`**: Main CLI for all operations - handles argument parsing, calls specific implementations, manages evaluation and deployment

### Data Flow

1. User question → Search index (vector similarity search in Azure AI Search)
2. Retrieved documents → Combined with system prompt
3. Augmented prompt → Azure OpenAI chat completions
4. Response + context → Returned to user

### Key Environment Variables

Required in `.env`:
- `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_KEY` - OpenAI credentials
- `AZURE_AI_SEARCH_ENDPOINT`, `AZURE_AI_SEARCH_KEY` - Search credentials
- `AZURE_OPENAI_CHAT_DEPLOYMENT` - Chat model deployment name
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` - Embedding model deployment name
- `AZURE_AI_SEARCH_INDEX_NAME` - Index to query

### Evaluation Dataset

`src/tests/evaluation_dataset.jsonl` contains test questions and ground truth answers for copilot evaluation. Each line: `{"question": "...", "truth": "..."}`.

## Azure SDK Clients

All implementations use `AIClient.from_config(DefaultAzureCredential())` for Azure authentication. The `DefaultAzureCredential` automatically attempts multiple authentication methods including environment variables, managed identity, and Azure CLI login.