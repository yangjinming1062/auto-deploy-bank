# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multi-language sample repository demonstrating Azure AI Search vector search capabilities across Python, .NET, JavaScript, and Java. Each language folder contains standalone samples demonstrating different vector search patterns including:

- Basic vector indexing and querying
- Hybrid search (combining text and vectors)
- Integrated vectorization (chunking and embedding during indexing)
- Semantic ranking
- Data quantization and storage optimization

## Common Commands

### Python (Jupyter Notebooks)

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies (per notebook folder)
pip install -r requirements.txt

# Run: Open ipynb file in VS Code and execute cells
```

### JavaScript/Node.js

```bash
cd demo-javascript/code
npm install
node azure-search-vector-sample.js --upload    # Upload sample data
node azure-search-vector-sample.js --query "query text"  # Query
node azure-search-vector-sample.js --embed     # Regenerate embeddings
```

### .NET

```bash
cd demo-dotnet/{ProjectName}  # DotNetVectorDemo, DotNetIntegratedVectorizationDemo, etc.
dotnet build
dotnet run -- --setup-index              # Setup index with sample data
dotnet run -- --query "query text"       # Run query
dotnet run -- -h                         # Show all options
```

### Java (Maven)

```bash
cd demo-java/demo-vectors  # or demo-integrated-vectorization
mvn compile exec:java      # Build and run
```

## Configuration

Each demo requires Azure credentials configured via environment variables or config files:

- `AZURE_SEARCH_SERVICE_ENDPOINT` - Azure AI Search endpoint
- `AZURE_SEARCH_ADMIN_KEY` or `AZURE_SEARCH_INDEX_KEY` - Search API key
- `AZURE_OPENAI_ENDPOINT` - Azure OpenAI endpoint
- `AZURE_OPENAI_API_KEY` - OpenAI API key
- `AZURE_OPENAI_EMBEDDING_DEPLOYED_MODEL` - Embedding model deployment name (e.g., "text-embedding-3-large")

Environment templates: `.env-sample` files are provided in each demo directory.

## Architecture Patterns

All samples follow similar Azure AI Search patterns:

1. **Connect to services** using Azure Identity (DefaultAzureCredential) or API keys
2. **Create index** with vector and non-vector fields using the search index SDK
3. **Generate embeddings** via Azure OpenAI embedding API for text fields
4. **Upload documents** containing both text content and vector representations
5. **Execute queries** that can be pure vector, text-only, or hybrid (combining both)

For integrated vectorization demos, indexing uses Azure Blob Storage as data source with Azure OpenAI called via a custom skill during the indexing pipeline.

## Key Dependencies

| Language | Key Packages |
|----------|-------------|
| Python | `azure-search-documents`, `azure-openai`, `azure-identity`, `python-dotenv` |
| JavaScript | `@azure/search-documents`, `@azure/openai`, `@azure/identity`, `commander` |
| .NET | `Azure.Search.Documents`, `Azure.AI.OpenAI`, `Azure.Identity` |
| Java | `azure-search-documents`, `azure-identity`, `azure-ai-openai` |

## Sample Data

- `demo-dotnet/data/` - JSON files with pre-generated embeddings
- `demo-javascript/data/` - Sample text data
- `demo-java/demo-vectors/src/main/resources/` - Sample JSON data
- `demo-python/code/{subfolder}/` - Sample data alongside notebooks