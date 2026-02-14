# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GraphRAG is a data pipeline and transformation suite that extracts meaningful, structured data from unstructured text using LLMs. It builds a knowledge graph from documents and supports multiple query strategies (local, global, drift, basic) for RAG-enhanced LLM responses.

## Common Commands

```bash
# Install dependencies
uv sync

# Run CLI commands
uv run poe index --root <path>       # Build knowledge graph index
uv run poe query --root <path> "<query>"  # Query the index
uv run poe prompt_tune --root <path> # Generate custom prompts

# Run tests
uv run poe test                      # All tests with coverage
uv run poe test_unit                 # Unit tests only
uv run poe test_integration          # Integration tests only
uv run poe test_smoke                # Smoke tests only
uv run poe test_notebook             # Notebook tests
uv run poe test_only -k "<pattern>"  # Run matching tests

# Code quality
uv run poe check                     # Format, lint, type-check
uv run poe fix                       # Auto-fix formatting/linting
uv run poe format                    # Format code only

# Documentation
uv run poe serve_docs                # Serve MkDocs documentation
uv run poe build_docs                # Build documentation

# Version management (required for PRs)
uv run semversioner add-change -t patch -d "<description>"
```

## Architecture

### Monorepo Structure

```
packages/
├── graphrag              # Main package, depends on all others
├── graphrag-chunking     # Text chunking logic
├── graphrag-common       # Shared utilities
├── graphrag-input        # Input processing (loading documents)
├── graphrag-llm          # LLM wrapper (completion + embeddings)
├── graphrag-storage      # Storage backends (File, Azure Blob)
├── graphrag-cache        # LLM response caching
└── graphrag-vectors      # Vector store implementations
```

### Core Modules (in packages/graphrag/graphrag/)

- **cli/main.py**: Typer-based CLI entry point with subcommands: `init`, `index`, `update`, `prompt-tune`, `query`
- **index/**: Indexing engine with workflow-based pipeline
  - **workflows/**: Sequential workflow definitions (create_base_text_units, extract_graph, create_communities, etc.)
  - **operations/**: Individual indexing operations (extract_graph, cluster_graph, embed_text, etc.)
- **query/**: Query engine supporting 4 search methods:
  - **local_search**: Entity/relationship-focused context building
  - **global_search**: Community report-based map-reduce queries
  - **drift_search**: Iterative drifting search with local context
  - **basic_search**: Simple vector similarity search
- **config/**: Configuration management via Pydantic models
- **data_model/**: Domain objects (Entity, Relationship, Community, TextUnit, etc.)

### Design Patterns

- **Factory Pattern**: Most modules use `factory.py` files for extensible instantiation (cache, logger, storage, vector stores, query engines). Register custom implementations by extending the factory registry.
- **Workflow Pattern**: Indexing uses configurable workflows defined in YAML/config, allowing pipeline customization.

### Configuration

Configuration is loaded from YAML files in the project root. Key config sections:
- `completion_models` / `embedding_models`: LLM settings
- `input`: Document loading configuration
- `chunking`: Text splitting parameters
- `output_storage`: Index output storage
- `vector_store`: Vector database settings
- Search-specific configs (local_search, global_search, drift_search, basic_search)

## Development Notes

- **Python Version**: Requires 3.11-3.13
- **Package Manager**: uv (not pip)
- **Type Checking**: pyright (configured in pyproject.toml include paths)
- **Formatting/Linting**: ruff with numpy docstring convention
- **Testing**: pytest with asyncio mode, timeout = 1000s
- **Versioning**: semversioner-required. Run `semversioner add-change` before committing
- **Azure Testing**: Some tests use Azurite. Start with `./scripts/start-azurite.sh`