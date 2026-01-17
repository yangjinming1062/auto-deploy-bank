# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Memoripy is a Python library for context-aware memory management with support for AI-driven applications. It provides short-term and long-term memory storage, embedding-based retrieval, concept extraction, and graph-based associations.

## Commands

```bash
# Install in development mode
pip install -e .

# Run main example
python memoripy/main.py

# Run specific examples
python examples/openai_example.py
python examples/ollama_example.py
python examples/openrouter.py
python examples/azure_example.py
```

## Architecture

### Core Components

**MemoryManager** (`memoripy/memory_manager.py`)
- Main orchestrator class coordinating all memory operations
- Initializes embedding dimension from the embedding model
- Standardizes embeddings to consistent dimensions
- Delegates to `MemoryStore` for memory operations

**MemoryStore** (`memoripy/memory_store.py`)
- In-memory storage for short-term and long-term interactions
- Uses FAISS `IndexFlatL2` for vector similarity search
- Integrates cosine similarity, time-based decay, and access count reinforcement
- Builds concept graph via NetworkX for spreading activation
- Performs hierarchical clustering with KMeans for semantic memory retrieval

### Abstract Base Classes

**ChatModel** and **EmbeddingModel** (`memoripy/model.py`)
- Abstract interfaces for chat and embedding functionality
- `ChatModel.invoke(messages)`: Generate response from messages list
- `ChatModel.extract_concepts(text)`: Extract key concepts as JSON
- `EmbeddingModel.get_embedding(text)`: Generate vector embedding
- `EmbeddingModel.initialize_embedding_dimension()`: Return embedding dimension

**BaseStorage** (`memoripy/storage.py`)
- Interface for persistence: `load_history()` and `save_memory_to_history(memory_store)`

### Storage Implementations

| Class | Description |
|-------|-------------|
| `InMemoryStorage` | Ephemeral in-memory dictionary storage |
| `JSONStorage` | Persistent JSON file storage (default: `interaction_history.json`) |
| `DynamoStorage` | AWS DynamoDB persistence using Pynamodb. Uses `set_id` as partition key for multi-user/multi-session isolation. Configurable via env vars: `MEMORIPY_DYNAMO_HOST`, `MEMORIPY_DYNAMO_REGION`, `MEMORIPY_DYNAMO_READ_CAPACITY`, `MEMORIPY_DYNAMO_WRITE_CAPACITY` |

### Model Implementations (`memoripy/implemented_models.py`)

**Embedding Models:**
- `OpenAIEmbeddingModel` - OpenAI text-embedding-3-small (1536 dim)
- `AzureOpenAIEmbeddingModel` - Azure OpenAI embeddings
- `OllamaEmbeddingModel` - Local Ollama models (dimension discovered dynamically)

**Chat Models:**
- `OpenAIChatModel` - OpenAI GPT models
- `AzureOpenAIChatModel` - Azure OpenAI deployment
- `OllamaChatModel` - Local Ollama models (llama3.1:8b default)
- `ChatCompletionsModel` - Generic chat completion (base for OpenRouter)
- `OpenRouterChatModel` - OpenRouter API integration

All chat models use LangChain's `JsonOutputParser` with `ConceptExtractionResponse` Pydantic model for structured concept extraction.

### Memory Retrieval Flow

1. Query is embedded using `EmbeddingModel`
2. Concepts are extracted using `ChatModel`
3. Cosine similarity computed against FAISS index
4. Time-based decay applied: `decay_factor * exp(-rate * time_diff)`
5. Reinforcement applied: `log1p(access_count)`
6. Spreading activation traverses concept graph (2 steps, 0.5 decay)
7. Hierarchical clustering via KMeans for semantic memory retrieval
8. Interactions with access_count > 10 promoted to long-term memory

## Key Data Structures

**Interaction structure**: `id`, `prompt`, `output`, `embedding`, `timestamp`, `access_count`, `concepts`, `decay_factor`

**Embedding handling**: Embeddings are stored as numpy arrays in `MemoryStore.embeddings`. When persisting to storage backends, they are flattened (`embeddings[idx].flatten().tolist()`) and converted back to numpy arrays on load.

**Concept handling**: Concepts are stored as Python `set` objects in `MemoryStore.concepts_list`. Storage implementations convert to/from lists for serialization.

## Dependencies

- **Vector operations**: faiss-cpu, numpy
- **LLM integration**: langchain, openai, ollama
- **Graph operations**: networkx
- **Clustering**: scikit-learn
- **Storage**: pynamodb (DynamoDB), orjson (JSON)