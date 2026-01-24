# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Advanced-RAG-Series is a multi-project repository containing LLM-based chatbots for Retrieval Augmented Generation (RAG) and Q&A systems. Each project demonstrates different approaches using LangChain/LangGraph with OpenAI models and various databases.

## Repository Structure

```
/home/ubuntu/deploy-projects/c4665093af648861ae72bb17/
├── LangGraph_1o1_Agentic_Customer_Support/      # LangGraph agent with 18 tools
├── AgentGraph-Intelligent-Q&A-and-RAG-System/   # Multi-database RAG + SQL agent
├── Q&A-and-RAG-with-SQL-and-TabularData/        # SQL/CSV/XLSX Q&A with GPT-3.5
├── KnowledgeGraph-Q&A-and-RAG-with-TabularData/ # Neo4j graph-based RAG
├── RAG-Evolution-8-SOTA-Techniques/             # 8 state-of-the-art RAG techniques
├── README.md                                     # Main documentation
└── Presentation.pptx                             # Project presentation
```

## Tech Stack

- **Language:** Python 3.10+
- **LLM:** OpenAI GPT-4o-mini/GPT-4/GPT-3.5-turbo (configurable per project)
- **Agent Framework:** LangChain + LangGraph
- **Vector DB:** ChromaDB
- **Monitoring:** LangSmith tracing
- **UI:** Gradio web interface
- **Config:** YAML files with `pyprojroot` for path resolution

## Common Commands

All projects follow the same setup pattern:

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API keys (edit .env)
# Required: OPEN_AI_API_KEY, TAVILY_API_KEY, LANGCHAIN_API_KEY

# 4. Prepare databases
python data_preparation/download_data.py
python data_preparation/prepare_vector_db.py

# 5. Run the application
python src/app.py
```

**Database refresh (after testing):**
```bash
python data_preparation/update_db_date.py
```

## Architecture Patterns

Each project follows a consistent structure:

```
Project-folder/
├── README.md              # Project-specific docs
├── HELPER.md              # Additional execution info
├── .env                   # Environment variables (gitignored)
├── .env.example           # Template for .env
├── .here                  # Marker for project root
├── configs/config.yml     # Runtime configuration
├── requirements.txt       # Python dependencies
├── data/                  # SQLite, CSV, XLSX data files
├── data_preparation/      # Database prep scripts
├── src/
│   ├── app.py             # Gradio UI entry point
│   ├── chatbot.py         # Chatbot logic
│   ├── agent_graph/       # LangGraph state machines
│   ├── tools/             # Tool implementations
│   └── utils/             # Utilities and config loader
└── documentation/         # System design docs
```

**Configuration Pattern:** All projects use YAML configs with a `LoadConfig` class pattern. Key settings:
- Model selection (`openai_models.model`)
- Vector database paths (`RAG.vectordb`)
- Collection names (`RAG.collection_name`)
- LangSmith tracing (`langsmith.tracing`)

**Entry Points:**
- `src/app.py` - Gradio Blocks UI with `demo.launch()`
- `src/prepare_vector_db.py` - Vector database initialization
- `data_preparation/download_data.py` - Download SQLite/database files

## Key Implementation Notes

- **Tool Calling:** Uses OpenAI function calling via `langchain-openai`
- **State Management:** LangGraph checkpoints for conversation state
- **Vector Storage:** ChromaDB with HNSW index for semantic search
- **Database Access:** Use READ-ONLY mode for production; write permissions enabled for demo/testing
- **Path Resolution:** Uses `pyprojroot` with `.here` marker for project-relative paths

## Important Notes from Documentation

1. Informative column names in databases help LLM agents navigate more effectively
2. For sensitive databases, use READ-only access to prevent data manipulation
3. The LangGraph_1o1_Agentic_Customer_Support project includes a backup database for safe testing
4. Each project can use either AzureOpenAI or OpenAI API (configured in YAML)

## Development Workflow

1. Configure `.env` with API keys
2. Run data preparation scripts
3. Launch app with `python src/app.py`
4. Access Gradio UI at `http://localhost:7860`
5. Monitor LangSmith traces for debugging
6. Refresh database with `update_db_date.py` after testing