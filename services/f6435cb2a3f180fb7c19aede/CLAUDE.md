# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a monorepo containing multiple LLM/AI chatbot projects. Each project is self-contained with its own configuration, dependencies, and entry point.

### Projects
- **WebGPT** - Streamlit UI chatbot with web search via DuckDuckGo and OpenAI function calling
- **RAG-GPT** - Gradio UI chatbot for document Q&A using LangChain, ChromaDB, OpenAI
- **WebRAGQuery** - Chainlit UI combining WebGPT and RAG-GPT capabilities
- **LLM-Fine-Tuning** - Full fine-tuning pipeline with Chainlit UI (Pythia, dLite, Open-LLaMA)
- **HUMAIN-advanced-multimodal-chatbot** - Gradio UI multimodal chatbot (GPT + LLaVA + Stable Diffusion + Whisper)
- **Hidden-Technical-Debt-Behind-AI-Agents** - LangGraph agent with Docker (PostgreSQL + ChromaDB)
- **RAGMaster-LlamaIndex-vs-Langchain** - Comparison of RAG techniques across both frameworks
- **Open-Source-RAG-GEMMA** - Open-source RAG using Google Gemma 7B + BAAI embeddings

## Common Commands

### Setup
```bash
# Create virtual environment (Python 3.11 recommended)
conda create --name projectenv python=3.11
conda activate projectenv

# Install dependencies
cd <project-directory>
pip install -r requirements.txt
```

### Environment Variables
Create `.env` file in project root with:
```env
OPENAI_API_KEY=<your-key>
# Optional for Azure:
OPENAI_API_TYPE=azure
OPENAI_API_VERSION=2023-05-15
OPENAI_API_BASE=<azure-endpoint>
gpt_deployment_name=<deployment-name>
```

### Running Projects

| Project | Command |
|---------|---------|
| WebGPT | `streamlit run src/webgpt_app.py` |
| RAG-GPT | `python src/raggpt_app.py` (Gradio) |
| WebRAGQuery | `chainlit run src/app.py` |
| LLM-Fine-Tuning | `chainlit run src/chatbot/app.py` |
| HUMAIN | `./run_chatbot.sh` (uses tmux) or `python src/app.py` |
| Technical-Debt | `python src/app.py` (or `docker-compose up` for containers) |

## Architecture Patterns

### Common Directory Structure
```
Project/
├── configs/           # YAML configuration files
├── data/              # Documents and vector databases
│   ├── docs/          # Source documents (PDFs, etc.)
│   └── vectordb/      # ChromaDB persistence
├── src/               # Application code
│   ├── app.py         # Main entry point
│   └── utils/         # Utility modules
├── images/            # UI screenshots and diagrams
├── .env               # API keys (not committed)
└── requirements.txt   # Python dependencies
```

### Key Configuration (app_config.yml)
- `embedding_model_config.engine`: Embedding model (e.g., `text-embedding-ada-002`)
- `llm_config.engine`: LLM deployment name (e.g., `gpt-35-turbo`, `gpt-4`)
- `splitter_config.chunk_size`: Text chunk size for RAG (typically 1000-2000)
- `splitter_config.chunk_overlap`: Overlap between chunks (typically 200-500)
- `retrieval_config.k`: Number of documents to retrieve

### Vector Database
Most projects use ChromaDB for vector storage:
- Local: `data/vectordb/processed/chroma/`
- Uploaded docs: `data/vectordb/uploaded/chroma/`
- HTTP client (docker): `chromadb.HttpClient(host="chroma", port=8000)`

## Tech Stack

**LLM Providers:** OpenAI (GPT-3.5/4), Azure OpenAI, HuggingFace (Gemma, LLaVA, Stable Diffusion, Whisper)

**Frameworks:** LangChain, LlamaIndex, LangGraph

**Vector Stores:** ChromaDB

**UI Frameworks:** Streamlit, Gradio, Chainlit

**Other:** DuckDuckGo Search, BeautifulSoup4, Tiktoken

## Port Management

If ports are in use:
```bash
# Linux/macOS
sudo lsof -i :<port>
sudo kill -9 <PID>

# Windows
netstat -ano | findstr :<port>
taskkill /PID <PID> /F
```

## Sample Prompts (WebRAGQuery/RAG-GPT)

- `"Prepare this link for q and a <url>"` - Index website for RAG
- `"summarize this website for me <url>"` - Summarize website
- `"I am looking for videos that explain..."` - Web search
- Debug code: `"debug the following code <code>"`

## Docker Projects

**Hidden-Technical-Debt-Behind-AI-Agents** uses Docker Compose:
```bash
# Start services
docker-compose up --build

# Build vector DB inside container
docker exec -it chatbot python src/prepare_vectordb_container.py

# Stop services
docker-compose down
```

Required `.env` for containers:
```env
DATABASE_URI_CONTAINER=postgresql://postgres:postgres@postgres:5432/postgres
```