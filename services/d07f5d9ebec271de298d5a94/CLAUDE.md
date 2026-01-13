# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **Milvus Bootcamp** - a comprehensive collection of tutorials, demonstrations, and real-world applications for the Milvus vector database. The repository showcases various AI use cases including:

- **RAG (Retrieval-Augmented Generation)** systems
- **Semantic/Image Search** applications
- **Hybrid Search** combining dense and sparse vectors
- **Recommendation Systems**
- **Question Answering** systems
- **Multimodal Search** (text + images)

## Repository Structure

```
/home/ubuntu/deploy-projects/d07f5d9ebec271de298d5a94/
├── applications/          # Complete production-ready applications
│   ├── image/            # Image search and computer vision apps
│   │   ├── reverse_image_search/    # Milvus + Towhee image search
│   │   └── biological_multifactor_authentication/
│   └── nlp/              # Natural language processing apps
│       ├── OpenAI/       # OpenAI-powered text search
│       ├── HuggingFace/  # HuggingFace transformers
│       └── question_answering_system/
│
├── tutorials/            # Quickstart tutorials and demos
│   └── quickstart/apps/  # Standalone applications
│       ├── rag_search_with_milvus/
│       ├── image_search_with_milvus/
│       ├── hybrid_demo_with_milvus/
│       ├── multimodal_rag_with_milvus/
│       └── cir_with_milvus/
│
├── bootcamp/             # Core bootcamp materials
│   ├── RAG/             # RAG-specific examples and notebooks
│   ├── Retrieval/       # Vector retrieval examples
│   ├── Evaluation/      # RAG evaluation methodologies
│   ├── Integration/     # Third-party integrations
│   ├── workshops/       # Workshop materials
│   └── *.ipynb          # Jupyter notebooks for learning
│
├── evaluation/           # RAG evaluation tools and datasets
├── integration/          # Integration examples
└── blog/                # Blog posts and articles
```

## Common Development Commands

### Running Applications

**Most applications follow this pattern:**

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   - Copy `.env.example` to `.env` and configure
   - Common variables:
     - `OPENAI_API_KEY` (for LLM features)
     - `MILVUS_ENDPOINT` (Milvus server URI)
     - `MILVUS_TOKEN` (authentication, if needed)
     - `COLLECTION_NAME` (Milvus collection name)

3. **Deploy with Docker Compose (full-stack apps):**
   ```bash
   docker-compose up -d
   ```

4. **Run from source (development):**
   - Start Milvus server (via Docker or standalone)
   - Start dependent services (MySQL, etc.)
   - Run the application:
     ```bash
     python app.py
     # or
     streamlit run app.py
     # or
     python src/main.py
     ```

### Testing

Some applications include pytest tests:

```bash
pytest test_main.py
```

Or test individual modules:
```bash
python -m pytest server/src/test_main.py
```

### Code Quality

**Linting with Pylint:**
```bash
pylint --rcfile=pylint.conf <path_to_code>
```

The repository uses a custom pylint configuration (`pylint.conf`) with relaxed rules suitable for tutorials and examples.

**Code Formatting:**
- Black formatter is used for `tutorials/` and `integration/` directories
- CI runs `black --check --diff --verbose` on pull requests

**Max line length:** 150 characters (configured in pylint.conf)

## Key Architecture Patterns

### 1. Application Structure

Most applications follow this pattern:

```
app_name/
├── app.py              # Main entry point (Streamlit/FastAPI)
├── encoder.py          # Text/image embedding logic
├── milvus_utils.py     # Milvus database operations
├── insert.py           # Data loading script
├── requirements.txt    # Python dependencies
├── .env                # Environment configuration
└── docker-compose.yaml # Full-stack deployment
```

### 2. Common Tech Stack

- **Vector Database:** Milvus (or Zilliz Cloud for managed)
- **Embedding Models:**
  - OpenAI embeddings (`text-embedding-ada-002`)
  - HuggingFace transformers
  - Towhee operators (ResNet50, etc.)
- **LLM Integration:**
  - OpenAI GPT models
  - HuggingFace transformers
- **Web Framework:**
  - Streamlit (for interactive demos)
  - FastAPI (for REST APIs)
- **Metadata Storage:** MySQL or file-based (for simplicity)
- **Deployment:** Docker Compose for multi-service apps

### 3. Data Flow Patterns

**RAG Applications:**
1. Document ingestion → chunking → embedding → store in Milvus
2. Query → embedding → similarity search in Milvus → LLM generation
3. Response with source citations

**Image Search Applications:**
1. Image → CNN feature extraction → vector → store in Milvus
2. Query image → feature extraction → similarity search → return results

### 4. Milvus Configuration

**Common Collection Schema:**
- Primary key (int64)
- Vector field (float32 vector, dimension varies by model)
- Metadata fields (TEXT/VARCHAR)

**Index Types:**
- HNSW (default for search)
- IVF_FLAT (for large datasets)
- AutoIndex (automatic optimization)

**Milvus Deployment Options:**
1. **Milvus Lite** - File-based, for development
2. **Standalone Docker** - Single-node deployment
3. **Cluster** - Distributed production deployment
4. **Zilliz Cloud** - Fully managed cloud service

## Important Notes

### Version Compatibility

- **Milvus versions:** Examples primarily target v2.2.x - v2.4.x
- **Python version:** CI runs on Python 3.8+
- **pymilvus version:** Must match Milvus server version

### Environment Setup

**For local development:**
- Install Docker and Docker Compose
- For Milvus standalone: Use provided docker-compose.yml
- Set up virtual environment for Python dependencies

**For cloud deployment:**
- Use Zilliz Cloud (managed Milvus)
- Update `MILVUS_ENDPOINT` and `MILVUS_TOKEN` in `.env`

### CI/CD Quality Checks

The repository has automated quality checks:

1. **Pylint workflow** (`.github/workflows/pylint.yml`):
   - Runs on pull requests to main branch
   - Checks `solutions/` and `benchmark_test/` directories
   - Uses custom `pylint.conf` configuration

2. **Black formatter** (`.github/workflows/black.yml`):
   - Runs on push and PR to tutorials/ and integration/
   - Checks code formatting with Black
   - Supports Jupyter notebook formatting

3. **Docker Compose CI** (`.github/workflows/docker_compose_ci.yml`):
   - Tests Docker Compose configurations

4. **Jupyter CI** (`.github/workflows/jupyter_ci.yml`):
   - Validates Jupyter notebooks

### Dataset Dependencies

Some applications require external datasets:

- **Image search:** PASCAL VOC dataset (~2GB)
  - Download: https://drive.google.com/file/d/1n_370-5Stk4t0uDV1QqvYkcvyV8rbw0O/view
- **RAG examples:** Milvus documentation (200+ docs, 4000+ chunks)
  - Download via `wget` and `unzip` commands in README files

### Example: Running a Quickstart App

**RAG Search Example:**
```bash
cd tutorials/quickstart/apps/rag_search_with_milvus

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your OPENAI_API_KEY

# Prepare data
wget https://github.com/milvus-io/milvus-docs/releases/download/v2.4.6-preview/milvus_docs_2.4.x_en.zip
unzip -q milvus_docs_2.4.x_en.zip -d milvus_docs
python insert.py milvus_docs/en

# Run application
streamlit run app.py
# Access at http://localhost:5005
```

## Key Resources

- **Milvus Documentation:** https://milvus.io/docs
- **Milvus Cheat Sheet:** `bootcamp/MilvusCheatSheet.md`
- **Tutorials Overview:** https://milvus.io/docs/tutorials-overview.md
- **API Reference:** https://milvus.io/api-reference
- **Community:** https://discord.gg/milvus (Discord)