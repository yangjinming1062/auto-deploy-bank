# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a tutorial repository containing standalone Python scripts demonstrating various LLM (Large Language Model) application patterns. The code examples are designed to be self-contained and focused, teaching how to build LLM applications and Agents using Python with LlamaIndex, LangChain, OpenAI's Agent SDK, ChromaDB, Pinecone, and other libraries.

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run any example script
python <script_name>.py

# Run a specific example (examples are numbered by tutorial order)
python 01_qna.py
python 20_agents_tooluse.py
```

## Environment Setup

Create a `.env` file with required and optional API keys:

```env
OPENAI_API_KEY=...         # Required for most examples
SECTORS_API_KEY=...        # For financial data (used in agent examples)
GROQ_API_KEY=...

# Optional providers
HUGGINGFACEHUB_API_TOKEN=...
PINECONE_API_KEY=...
DEEPSEEK_API_KEY=...
COHERE_API_KEY=...
STABILITY_API_KEY=...
```

## Architecture Overview

### Core Patterns Demonstrated

1. **Basic Q&A with RAG** (`01_qna.py`): LangChain + ChromaDB for document Q&A using OpenAI embeddings and retrieval

2. **Website Q&A** (`06_team.py`): LlamaIndex + TrafilaturaWebReader for scraping and querying websites

3. **Agent Tool Use** (`20_agents_tooluse.py`): OpenAI Agents SDK with function tools for financial data retrieval

4. **Multi-Agent Patterns** (`19-24_agents_*.py`): Six patterns for building AI agent systems:
   - Hand-off and delegation
   - Tool-use and function calling
   - Deterministic chains
   - Judge and critic
   - Parallelization
   - Guardrails

### Library Versions

- LangChain: 0.0.209 (older version)
- LlamaIndex: 0.6.31
- OpenAI: 0.27.8
- ChromaDB: 0.3.21
- OpenAI Agents SDK: Latest (for agent examples)

### Key Data Directories

- `news/`: Sample text data for RAG examples
- `book/`: Book content for embeddings examples
- `storage/`: Persistent storage for indexes
- `agent_outputs/`: Output from agent runs

### Utility Modules

- `utils/api_client.py`: Shared API client utilities

## Code Patterns

### Loading Environment Variables
```python
from dotenv import load_dotenv
load_dotenv()
```

### Typical RAG Pipeline
1. Load documents with `DirectoryLoader` or specialized reader
2. Split text with `CharacterTextSplitter`
3. Create embeddings with `OpenAIEmbeddings`
4. Store in vector database (Chroma/Pinecone)
5. Create QA chain with `RetrievalQA`

### Agent Definition Pattern (OpenAI Agents SDK)
```python
from agents import Agent, Runner, function_tool

@function_tool
def my_tool(param: str) -> str:
    """Tool description for LLM"""
    ...

agent = Agent(
    name="agent_name",
    instructions="System prompt",
    tools=[my_tool],
    tool_use_behavior="run_llm_again"
)

result = await Runner.run(agent, user_query)
```