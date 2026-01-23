# Ollama Projects - Codebase Guide

A multi-project repository containing 20 AI-powered applications built with Ollama's open-source models, created for the NarimanCodes YouTube channel.

## Project Overview

This is a **Python-based multi-project repository** featuring AI applications across various domains:

- **Document Processing**: Chat with PDF, Hybrid RAG, Multimodal RAG
- **Voice/Audio**: Voice RAG, AI Podcaster
- **Research & Agents**: AI Researcher, Multi-Agent AI Researcher, Multi-Agent Investment Advisor, ACP Agents, Agent with Memory, GPT-OSS Agent with MCP
- **Vision & Media**: Image Search, OCR, Object Detection, Emotion Detection, Video Summarization
- **Utilities**: AI Scraper, Text to SQL

## Architecture & Organization

### Directory Structure
```
/home/ubuntu/deploy-projects/e92c55559356cb9a9b6438ad/
├── .gitignore                  # Comprehensive Python gitignore
├── LICENSE                     # MIT License
├── README.md                   # Main project listing
├── CLAUDE.md                   # This file
├── chat-with-pdf/              # PDF RAG application
├── ai-researcher/              # Single-agent research workflow
├── multi-agent-researcher/     # Multi-agent supervisor architecture
├── multi-agent-investment-advisor/ # Swarm architecture
├── voice-rag/                  # Audio transcription & RAG
├── ai-podcaster/               # Text-to-speech generation
├── video-summarization/        # Video frame analysis & summarization
├── ocr/                        # Invoice OCR extraction
├── image-search/               # Image similarity search
├── object-detection/           # Computer vision object detection
├── emotion-detection/          # Facial emotion recognition
├── text-to-sql/                # Natural language to SQL
├── ai-scraper/                 # Web scraping agent
├── hybrid-retrieval-rag/       # Hybrid search RAG system
├── multi-modal-rag/            # Multimodal document RAG
├── gpt-oss-agent-with-mcp/     # MCP integration agent
├── agent-with-memory/          # Memory-equipped agent
├── acp-agents/                 # ACP agent framework
└── [other projects...]
```

### Common Project Structure
Each project typically contains:
- `[project_name].py` - Main application file
- `requirements.txt` - Project dependencies
- `README.md` - Project-specific documentation
- Data directories (e.g., `pdfs/`, `audios/`, `images/`, `frames/`, `videos/`)

## Technology Stack

### Core Frameworks
- **Streamlit** - Web UI framework (all projects use this for user interface)
- **LangChain** - LLM orchestration and chains
- **LangGraph** - Workflow and agent state management
- **LangChain Community** - Integration utilities (DuckDuckGo, Tavily search, etc.)

### Key Dependencies
```python
streamlit                          # Web application framework
langchain_core                     # Core LangChain abstractions
langchain_community                # Community integrations & tools
langchain_ollama                   # Ollama LLM & embedding integrations
langgraph                          # Agent workflow orchestration
langgraph_supervisor               # Supervisor/multi-agent patterns
```

### Additional Libraries (Project-Specific)
- **Document Processing**: pdfplumber, langchain_text_splitters
- **Audio/Video**: opencv-python, whisper, kokoro, soundfile, numpy
- **Vision**: (project-specific CV libraries)
- **Data**: pydantic (data validation), (pandas/scikit-learn in some projects)

### LLM Models Used
- **Primary**: deepseek-r1:8b (most common)
- **Secondary**: qwen3:8b, llama3.2-vision

## Build & Run Commands

### Standard Application Run
```bash
streamlit run [project_name].py
```

### Dependency Installation
```bash
pip install -r requirements.txt
```

### Requirements Pattern
Each project has minimal dependencies (~4-6 packages):
```txt
streamlit
langchain_core
langchain_community
langchain_ollama
[project-specific packages]
```

## Code Patterns & Conventions

### Common Patterns

1. **Text Cleaning Function**
   - Every project uses a `clean_text()` function to remove LLM reasoning traces
   - Removes content between `` tags
   ```python
   def clean_text(text: str):
       cleaned_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
       return cleaned_text.strip()
   ```

2. **Prompt Templates**
   - Uses `ChatPromptTemplate.from_template()` for LLM prompts
   - Templates stored as multi-line strings with placeholders

3. **LangGraph State Management**
   - TypedDict classes define state structure
   - StateGraph builder pattern for workflow definitions
   - Nodes: search, summarize, generate_response, etc.

4. **Streamlit UI Pattern**
   - Simple file upload interface
   - Chat-style input/output
   - State management via Streamlit session

5. **Ollama Integration**
   - `OllamaEmbeddings` for vector embeddings
   - `OllamaLLM` or `ChatOllama` for LLM calls
   - Model specification in constructor: `model="deepseek-r1:8b"`

### File & Directory Naming
- Python files: lowercase with underscores (snake_case)
- Requirements: `requirements.txt` per project
- Subdirectories: descriptive names (pdfs/, audios/, images/, frames/, videos/)
- No `src/` or `tests/` directories in individual projects

### Imports Structure
```python
import streamlit as st
from langchain_community.tools import [specific_tool]
from langchain_ollama import ChatOllama
from langgraph.graph import START, END, StateGraph
from typing_extensions import TypedDict
import re  # For clean_text function
```

## Configuration Files

### .gitignore
Comprehensive Python .gitignore covering:
- Byte-compiled files (`__pycache__/`, `*.pyc`)
- Distribution artifacts (`build/`, `dist/`, `*.egg`)
- Virtual environments (`.venv/`, `venv/`)
- Test coverage (`.coverage`, `htmlcov/`)
- IDE files (`.idea/`, `.vscode/`)
- Environment variables (`.env`)

### Project-Specific README.md
Each project includes:
- Brief description
- Video reference (YouTube link)
- Prerequisites (Ollama installation, model pulls)
- Installation instructions
- Run instructions

## Development Guidelines

### Running Applications
```bash
cd /home/ubuntu/deploy-projects/e92c55559356cb9a9b6438ad/[project-directory]
streamlit run [project_name].py
```

### Setting Up Ollama
Required before running most projects:
```bash
ollama pull deepseek-r1:8b    # Most common model
ollama pull qwen3:8b          # Alternative model
ollama pull llama3.2-vision   # For vision tasks
```

### Adding a New Project
1. Create project directory
2. Create `requirements.txt` with core dependencies:
   ```
   streamlit
   langchain_core
   langchain_community
   langchain_ollama
   ```
3. Create main Python file
4. Add README.md with setup instructions
5. Follow existing patterns (clean_text, prompt templates, etc.)

### Testing Approach
- No formal test framework configured (pytest, unittest)
- Manual testing via Streamlit UI
- Testing typically done through interactive use

## Key Projects Overview

### Multi-Agent Architectures
- **multi-agent-researcher**: Supervisor pattern with query_refiner and research agents
- **multi-agent-investment-advisor**: Swarm architecture for investment analysis
- **agent-with-memory**: Memory-equipped agent implementation

### RAG Systems
- **chat-with-pdf**: Basic PDF document RAG
- **hybrid-retrieval-rag**: Hybrid search approach
- **multi-modal-rag**: Multimodal document handling
- **voice-rag**: Audio transcription + RAG

### Vision & Media
- **ocr**: Invoice text extraction with structured output
- **image-search**: Similarity-based image search
- **object-detection**: Computer vision object detection
- **emotion-detection**: Facial emotion recognition
- **video-summarization**: Frame extraction and summarization

### Specialized Applications
- **ai-podcaster**: Text-to-speech with Kokoro
- **ai-researcher**: Web research with Tavily search
- **ai-scraper**: AI-powered web scraping
- **text-to-sql**: Natural language to SQL conversion
- **gpt-oss-agent-with-mcp**: MCP integration

## Important Notes

1. **No Build Scripts**: All projects are run directly with Streamlit
2. **No Test Framework**: Manual testing only
3. **No Linting Config**: No ESLint, PyLint, or similar configured
4. **Minimal Configuration**: Each project is self-contained
5. **Single-File Focus**: Most projects are single Python files
6. **Ollama Required**: All projects assume local Ollama installation
7. **Model Persistence**: Models are pulled and cached by Ollama
8. **Interactive Only**: Primarily designed for interactive web UI use

## Additional Resources

- YouTube Channel: https://www.youtube.com/@NarimanCodes
- Ollama: https://ollama.com/
- LangChain: https://python.langchain.com/
- Streamlit: https://streamlit.io/
- LangGraph: https://langchain-ai.github.io/langgraph/
