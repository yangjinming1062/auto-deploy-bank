# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GraphRAG is a graph-based Retrieval-Augmented Generation (RAG) system from Microsoft Research. It extracts structured knowledge from unstructured text using LLMs to build a knowledge graph that enhances LLM reasoning over private data.

## Commands

```bash
# Install dependencies
uv sync

# Initialize a GraphRAG project
uv run poe init --root <path>

# Run the indexing pipeline
uv run poe index --root <path>

# Update an existing index
uv run poe update --root <path>

# Run queries
uv run poe query --root <path> --query "<question>"

# Prompt tuning
uv run poe prompt_tune --root <path>

# Run all tests with coverage
uv run poe test

# Run specific test categories
uv run poe test_unit        # Unit tests only
uv run poe test_integration # Integration tests only
uv run poe test_smoke       # Smoke tests only
uv run poe test_notebook    # Notebook tests only
uv run poe test_verbs       # Verb tests only

# Run a single test
uv run pytest -s -k "<test_pattern>" ./tests  # or use: uv run poe test_only -k "<pattern>"

# Static checks (format, lint, type-check)
uv run poe check

# Auto-format and fix issues
uv run poe fix          # Safe fixes
uv run poe fix_unsafe   # Includes unsafe fixes
uv run poe format       # Explicitly run formatter and import sorter

# Build all packages
uv run poe build        # Sequence: copy assets, build packages

# Release workflow (version bump, changelog, sync)
uv run poe release

# Serve documentation locally
uv run poe serve_docs

# Version management
uv run semversioner add-change -t <major|minor|patch> -d "<description>"
```

## Architecture

### Monorepo Structure

```
packages/
├── graphrag           # Main package (aggregator)
├── graphrag-chunking  # Text chunking strategies
├── graphrag-common    # Shared utilities and types
├── graphrag-input     # Input readers (text, CSV, JSON, etc.)
├── graphrag-llm       # LLM abstraction layer (LiteLLM-based)
├── graphrag-storage   # Storage providers (file, blob, CosmosDB)
├── graphrag-cache     # LLM response caching
└── graphrag-vectors   # Vector store integration (LanceDB, Azure AI Search, etc.)
```

### Indexing Pipeline (6 Phases)

1. **Compose TextUnits**: Split documents into chunks (default 1200 tokens)
2. **Document Processing**: Link documents to their text units
3. **Graph Extraction**: Extract entities, relationships, and claims via LLM
4. **Graph Augmentation**: Leiden hierarchical community detection
5. **Community Summarization**: Generate reports for each community
6. **Text Embedding**: Vectorize entities, text units, and reports

### Core Data Model

Key entities in `graphrag/data_model/`:
- `Document` - Input documents
- `TextUnit` - Analysis chunks
- `Entity` - Extracted entities (people, places, events)
- `Relationship` - Connections between entities
- `Covariate` - Time-bound claims about entities
- `Community` - Hierarchical cluster structure
- `Community Report` - Summarized community content

### Factory Pattern

Multiple subsystems use factories for extensibility in `graphrag/*/factory.py`:
- Language models (LLM/embedding)
- Input readers
- Cache providers
- Loggers
- Storage providers
- Vector stores
- Workflows

Each factory supports custom implementations via string registration.

### Query Types

Located in `graphrag/query/`:
- **Local Search**: Entity-focused, uses community reports and text units
- **Global Search**: Community-report focused, for broad reasoning
- **Global Search (DRIFT)**: Iterative multi-hop reasoning

### Key Files

- `graphrag/cli/main.py` - CLI entrypoint (Typer-based)
- `graphrag/index/run/run.py` - Indexing execution
- `graphrag/query/factory.py` - Query engine creation
- `graphrag/config/` - Configuration models and defaults
- `graphrag/prompts/` - System prompts for LLM operations

## Configuration

Use `graphrag init --root <path>` to generate a default configuration. Configuration is YAML-based with settings for:
- LLM providers (via LiteLLM)
- Chunking parameters
- Vector store settings
- Extraction prompts
- Storage backends

Run `uv run poe index --root <path> --repopulate` to re-index after config changes.

## Development Notes

- Python 3.11-3.13 required
- Azurite used for some integration tests (`./scripts/start-azurite.sh` or run `azurite` if installed)
- Semantic versioning via semversioner - all PRs need a change file
- Run `uv run poe format` before committing to ensure code style
- Tests use pytest-asyncio with `.env` file for environment variables
- Default pytest timeout is 1000 seconds

## Code Style

| Tool | Purpose |
|------|---------|
| ruff format | Code formatting (preview mode) |
| ruff | Linting (extensive rules configured) |
| pyright | Type checking |
| pydocstyle | Docstring convention (numpy) |

Target Python version is py310 for compatibility checks, though py311-py313 are supported.