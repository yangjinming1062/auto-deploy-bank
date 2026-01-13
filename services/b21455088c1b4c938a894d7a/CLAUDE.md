# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

GPT-Researcher is an autonomous LLM-based agent that conducts local and web research on any topic and generates comprehensive reports with citations. The project consists of a Python/FastAPI backend, a Next.js/TypeScript frontend, and a multi-agent research system using LangGraph.

**Key URLs:**
- Project: https://gptr.dev/
- GitHub: https://github.com/assafelovic/gpt-researcher
- Documentation: https://docs.gptr.dev/

## Common Commands

### Python Backend & Core Research
```bash
# Install dependencies
pip install -r requirements.txt
# or using Poetry:
poetry install

# Run the FastAPI server (development mode with auto-reload)
python -m uvicorn main:app --reload
# or
python main.py

# Run with custom host/port
python -m uvicorn backend.server.server:app --host=0.0.0.0 --port=8000

# Run CLI tool with various options
python cli.py "your query" --report_type detailed_report --tone objective
python cli.py "climate change impact" --report_type deep_research --query_domains "nasa.gov,noaa.gov"
python cli.py "AI trends" --report_source local --no-pdf --no-docx

# Run Python tests (all tests)
python -m pytest tests/ -v
# Run specific test files
python -m pytest tests/report-types.py -v
python -m pytest tests/vector-store.py -v
python -m pytest tests/test_mcp.py -v
# Run test-your-* integration tests
python -m pytest tests/test-your-*.py -v
```

### Docker
```bash
# Start all services (FastAPI on :8000, Next.js on :3000)
docker-compose up --build
# For newer Docker versions:
docker compose up --build

# Run specific services
docker-compose up --build gpt-researcher          # Backend only
docker-compose up --build gptr-nextjs             # Frontend only

# Run tests in container
docker-compose --profile test up gpt-researcher-tests

# With Discord bot (optional)
docker-compose --profile discord up --build
```

### Frontend (Next.js)
```bash
cd frontend/nextjs

# Install dependencies
npm install

# Development server
npm run dev

# Production build and start
npm run build
npm run start

# Linting
npm run lint

# Component library build (for standalone React component usage)
npm run build:lib
```

### Multi-Agent System (LangGraph)
```bash
cd multi_agents
python main.py
# or using langgraph CLI:
langgraph run
```

### Environment Setup
```bash
# Required API keys (export or store in .env)
export OPENAI_API_KEY={Your OpenAI API Key}
export TAVILY_API_KEY={Your Tavily API Key}  # For web search
export LANGCHAIN_API_KEY={LangChain key}     # Optional
export OPENAI_BASE_URL={Custom API base URL} # Optional, for local models

# Optional configuration
export DOC_PATH="./my-docs"                  # For local document research
export MAX_SCRAPER_WORKERS=15                # Concurrent scraper limit
export SCRAPER_RATE_LIMIT_DELAY=0            # Seconds between requests
export LOGGING_LEVEL=INFO                    # Logging verbosity
```

## Architecture Overview

This codebase implements a **multi-layered research automation system** with the following high-level architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                           │
│  ┌────────────────────┐        ┌──────────────────────────┐ │
│  │   Next.js (Prod)   │        │   FastAPI Static (Dev)   │ │
│  │   TypeScript/TS    │        │   Lightweight UI         │ │
│  └────────────────────┘        └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↕ WebSocket/HTTP
┌─────────────────────────────────────────────────────────────┐
│                    API Layer                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           FastAPI Backend Server                       │ │
│  │    - WebSocket Manager for real-time updates          │ │
│  │    - REST API endpoints                               │ │
│  │    - Report generation orchestration                  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  Core Research Engine                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │        GPTResearcher Class (planner-executor)         │ │
│  │  - Research planning & question generation            │ │
│  │  - Agent coordination                                 │ │
│  │  - Report writing                                     │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│              Data Retrieval & Processing                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │  Web     │ │  Local   │ │   MCP    │ │ Vector Store │  │
│  │ Scraper  │ │Documents │ │  Data    │ │  (FAISS)     │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│              Multi-Agent System (Optional)                   │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐  │
│  │Browser │ │Research│ │ Review │ │  Write │ │ Publisher│  │
│  │ Agent  │ │ Agent  │ │ Agent  │ │ Agent  │ │  Agent   │  │
│  └────────┘ └────────┘ └────────┘ └────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Key Design Patterns:**

1. **Planner-Executor Pattern**: The core research system separates planning (generating research questions) from execution (gathering information)

2. **Multi-Agent Orchestration**: LangGraph coordinates specialized agents for complex research workflows

3. **Retrieval Strategy Pattern**: Multiple retrieval methods (web search, local docs, MCP, vector stores) can be combined

4. **Real-Time Updates**: WebSocket implementation provides live research progress to the frontend

5. **Template-Based Report Generation**: Jinja2 templates enable flexible, consistent report formatting across multiple output formats

## Backend Components

**Core Research System (`/gpt_researcher/`)**
- `agent.py` - Main research orchestration
- `prompts.py` - LLM prompt templates and configurations
- `retrievers/` - Data retrieval implementations (Tavily, DuckDuckGo, ArXiv, etc.)
- `scraper/` - Web scraping modules with JavaScript support
- `llm_provider/` - LLM integration (OpenAI, Ollama, LiteLLM)
- `vector_store/` - Vector storage and embedding management
- `document/` - Local document processing (PDF, DOCX, etc.)
- `mcp/` - Model Context Protocol support

**Server (`/backend/server/`)**
- `app.py` - FastAPI application with WebSocket support
- `websocket_manager.py` - Real-time communication handling
- `server_utils.py` - Server utility functions

**Report Generation (`/backend/`)**
- `report_type/` - Report type implementations (DetailedReport, etc.)
- Template-based report structuring using Jinja2
- Multiple output formats: PDF (md2pdf), Markdown (mistune), DOCX (python-docx)

**Multi-Agent System (`/multi_agents/`)**
LangGraph-based multi-agent research system inspired by the STORM paper. Features 7 specialized agents working in coordination:

- **orchestrator.py** - Coordinates the entire research workflow and task distribution
- **researcher.py** - Conducts actual research and information gathering
- **writer.py** - Generates comprehensive report content and structure
- **reviewer.py** - Reviews and validates research findings for accuracy
- **revisor.py** - Revises content based on reviewer feedback and quality checks
- **editor.py** - Performs final editing, formatting, and polish
- **publisher.py** - Handles final report publication in multiple formats (PDF, DOCX, MD)

The system uses `langgraph.json` for configuration and implements parallel agent processing for improved performance. An average run generates a 5-6 page research report.

Entry point: `multi_agents/main.py`

### Frontend Components

**Two versions available:**
1. **Static FastAPI version** (`/frontend/`) - Lightweight deployment
2. **Next.js version** (`/frontend/nextjs/`) - Production-ready with enhanced features
   - TypeScript + Tailwind CSS
   - Real-time progress tracking
   - Interactive research findings display

### Key Configuration

**Environment Variables (`.env`):**
- `OPENAI_API_KEY` - OpenAI API key (required)
- `TAVILY_API_KEY` - Tavily search API key (required)
- `OPENAI_BASE_URL` - Custom OpenAI-compatible API endpoint
- `DOC_PATH` - Path to local documents for research
- `MAX_SCRAPER_WORKERS` - Concurrent scraper limit (default: 15)
- `SCRAPER_RATE_LIMIT_DELAY` - Seconds between requests (default: 0)

**Python Configuration (`pyproject.toml`):**
- Python 3.11+ required
- Uses Poetry for dependency management
- LangChain v1 ecosystem (langchain, langgraph >= 0.2.76)
- Test configuration with pytest-asyncio

## Development Workflow

**Branch Strategy:**
- Branch from `master` (or `main`) for features/fixes
- Feature branches following conventional naming

**Testing Strategy:**
- **Location**: `/tests/` directory
- **Framework**: pytest with `asyncio_mode = "strict"`
- **Categories**:
  - Unit tests: Individual component testing
  - Integration tests: Agent interactions, LLM providers
  - End-to-end tests: Complete research workflows
  - MCP tests: Model Context Protocol integration
  - Vector store tests: Database and search functionality
  - Report type tests: Different research report formats
- **Test Files**: `research_test.py`, `vector-store.py`, `test_mcp.py`, `report-types.py`, `test-your-*.py`
- **Running Tests**:
  - All tests: `python -m pytest tests/ -v`
  - Specific file: `python -m pytest tests/report-types.py -v`
  - Docker tests: `docker-compose --profile test up gpt-researcher-tests`

**Code Standards (from .cursorrules):**
- **Python**: Follow PEP 8, use type hints for better code clarity
- **Frontend**: TypeScript strict mode, ESLint and Prettier configured, responsive and accessible components
- **Styling**: Tailwind CSS following project design system
- **Comments**: Minimize AI-generated comments; prefer self-documenting code
- **Documentation**: Document all public APIs and complex logic
- **Error Handling**: Research failure recovery, API rate limiting, network timeouts, input validation
- **Performance**: Parallel processing, caching, memory management, response streaming
- **Security**: Validate all inputs and API responses, no sensitive data in code or commits

## Language Model Configuration

**Default Models:**
- Primary: `gpt-4-turbo`
- Alternatives: `gpt-3.5-turbo`, `claude-3-opus`
- Local: `ollama` (via langchain-ollama)

**Configuration Options:**
- Temperature settings per task type
- Context window management
- Token limit handling
- Cost optimization strategies

## API Usage

### CLI Interface (`cli.py`)
```bash
# Basic usage
python cli.py "Explain quantum computing trends" --report_type detailed_report --tone analytical

# Advanced usage with custom domains
python cli.py "Climate change impact on agriculture" \
  --report_type deep_research \
  --tone objective \
  --query_domains "nasa.gov,noaa.gov,ipcc.ch"

# Local document research
python cli.py "Research findings" --report_source local --no-pdf

# Generate specific output formats
python cli.py "Market analysis" --report_type detailed_report --no-docx
```

**Tone Options**: objective, formal, analytical, informal, formal, persuasive, creative

### Python API Usage

**Basic Example:**
```python
from gpt_researcher import GPTResearcher
import asyncio

async def research_example():
    researcher = GPTResearcher(
        query="Why is Nvidia stock going up?",
        report_type="detailed_report",
        tone="objective"
    )

    # Conduct research
    research_result = await researcher.conduct_research()

    # Write the report
    report = await researcher.write_report()

    return report
```

**With Local Documents:**
```python
researcher = GPTResearcher(
    query="Summarize the key findings",
    report_source="local",  # Uses DOC_PATH environment variable
    report_type="detailed_report"
)
```

**With MCP Integration:**
```python
import os

os.environ["RETRIEVER"] = "tavily,mcp"  # Enable hybrid web + MCP research

researcher = GPTResearcher(
    query="Top open source research agents",
    mcp_configs=[
        {
            "name": "github",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")}
        }
    ]
)

research_result = await researcher.conduct_research()
report = await researcher.write_report()
```

**Report Types:**
- `research_report` - Summary, short and fast (~2 min)
- `detailed_report` - In-depth analysis (~5 min)
- `resource_report` - Resource-focused output
- `outline_report` - Structured outline format
- `custom_report` - User-defined format
- `subtopic_report` - Deep dive on specific subtopic
- `deep_research` - Advanced recursive research with tree-like exploration (~5 min, ~$0.40 with o3-mini)
  - Features: concurrent processing, smart context management, configurable depth and breadth
  - Explores topics with agentic depth and breadth using a tree-like pattern

**Report Sources:**
- `web` - Web search and scraping
- `local` - Local documents (PDF, DOCX, CSV, etc.)
- `hybrid` - Combined web and local sources
- `mcp` - Model Context Protocol data sources

## Core Workflows

**Research Pipeline:**
1. Create task-specific agent based on query
2. Generate research questions for objective coverage
3. Crawl and gather information (Browser agent)
4. Research each question (Researcher agents)
5. Review and validate sources (Reviewer agent)
6. Write comprehensive report (Writer agent)
7. Publish in multiple formats (Publisher agent)

**Error Handling:**
- Research failure recovery with retry logic
- API rate limiting and quota management
- Network timeout handling
- Invalid input validation
- Source credibility verification

**Performance Optimization:**
- Parallel agent processing (LangGraph)
- Caching mechanisms for embeddings and documents
- Memory management for large documents
- Response streaming for real-time updates

## MCP (Model Context Protocol) Integration

Enable hybrid research combining web search with specialized data sources:
```bash
export RETRIEVER=tavily,mcp
```

Example with GitHub MCP server:
```python
researcher = GPTResearcher(
    query="open source research agents",
    mcp_configs=[{
        "name": "github",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")}
    }]
)
```

## Important Notes

**File Outputs:**
- Reports saved to: `/outputs/{uuid}.md`
- PDFs generated via: `md2pdf` library
- DOCX generated via: `python-docx`
- Logs written to: `/logs/` directory

**MCP Server Integration:**
GPT Researcher can be integrated with AI assistants via a separate MCP server repository: https://github.com/assafelovic/gptr-mcp

This enables:
- Deep research capabilities for Claude Desktop and other MCP-compatible assistants
- Integration with specialized data sources alongside web search
- Enhanced context management for better LLM reasoning

**Code Quality Standards (from .cursorrules):**
- **Python**: Follow PEP 8, use type hints for better code clarity
- **TypeScript/React**: Use strict mode, follow React 18 best practices and hooks guidelines
- **Frontend**: Follow ESLint and Prettier configurations, ensure responsive and accessible components
- **Styling**: Use Tailwind CSS following the project's design system
- **Comments**: Minimize AI-generated comments; prefer self-documenting code
- **Error Handling**: Implement proper error handling for AI responses, handle rate limiting, maintain context window limits
- **Security**: Validate all user inputs and API responses, no sensitive data in code or commits
- **Performance**: Use parallel processing strategies, implement caching mechanisms, monitor memory usage

**Dependencies:**
- Excluded from package: selenium, webdriver, fastapi, uvicorn, jinja2, langgraph
- Optional dependencies: playwright, scrapy, selenium for advanced scraping

**Version:**
- Current: 0.14.5 (defined in `setup.py` and `pyproject.toml`)
- Python support: 3.11, 3.12, 3.13

## Development Tips

- Use `DOC_PATH` environment variable to research local documents
- Configure scraper workers via `MAX_SCRAPER_WORKERS` for rate-limited APIs
- WebSocket endpoint for real-time progress updates at `/ws`
- Logs directory auto-created on startup
- All API keys should be set in `.env` file (copy from `.env.example`)