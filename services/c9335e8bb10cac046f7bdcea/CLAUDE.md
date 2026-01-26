# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GenAI Career Assistant is a multi-agent job search application built with LangGraph and Streamlit. It uses a Supervisor pattern where a central supervisor agent routes queries to specialized worker agents based on user intent.

## Commands

### Setup and Installation
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
streamlit run app.py
```

### Required Secrets
Create `.streamlit/secrets.toml` with:
```toml
OPENAI_API_KEY = "your-openai-api-key"
SERPER_API_KEY = "serper-api-key"
FIRECRAWL_API_KEY = "firecrawl-api-key"
GROQ_API_KEY = "groq-api-key"  # optional, for fallback LLM
LANGCHAIN_API_KEY = ""  # optional, for tracing
LANGCHAIN_TRACING_V2 = "true"  # optional
LANGCHAIN_PROJECT = "JOB_SEARCH_AGENT"  # optional
```

## Architecture

### Multi-Agent Supervisor Pattern (LangGraph)

The application uses a StateGraph workflow with a **Supervisor** node that routes to worker agents:

```
Supervisor → routes to one of:
  ├─ ResumeAnalyzer → extracts and summarizes resume content
  ├─ CoverLetterGenerator → creates tailored cover letters
  ├─ JobSearcher → searches LinkedIn for job listings
  ├─ WebResearcher → performs web searches and scraping
  └─ ChatBot → handles general conversational queries
```

### State Management (`agents.py`)
- `AgentState` TypedDict: Contains `user_input`, `messages`, `next_step`, `config`, `callback`
- Each node receives state, performs work, appends message to history, returns state
- Supervisor uses `RouteSchema` (Pydantic) to determine next agent via `with_structured_output()`

### Agent Creation Pattern
Agents are created using `create_agent(llm, tools, system_prompt)` which:
1. Builds a `ChatPromptTemplate` with system prompt and message placeholders
2. Uses `create_openai_tools_agent` to create an agent executor
3. Workers always report back to Supervisor (edges: `worker → Supervisor`)

### Key Files by Responsibility

| File | Responsibility |
|------|----------------|
| `app.py` | Streamlit UI, session state, API key handling, callback setup |
| `agents.py` | Graph definition, all node functions, `create_agent()` factory |
| `chains.py` | Supervisor chain (`get_supervisor_chain`), finish chain |
| `tools.py` | LangChain tools: job search, resume extraction, web search, web scraping |
| `prompts.py` | Prompt templates for each agent type |
| `search.py` | LinkedIn job search (web scraping or API), async job detail fetching |
| `utils.py` | `SerperClient` (Google search), `FireCrawlClient` (website scraping) |
| `schemas.py` | `RouteSchema` for supervisor routing, `JobSearchInput` for tool args |
| `data_loader.py` | PDF resume loading (PyMuPDF), DOCX cover letter writing |
| `members.py` | Team member definitions shown to supervisor for routing decisions |

### Tool Patterns

**Job Search** (`tools.py`):
- `get_job_search_tool()` → `StructuredTool` wrapping `linkedin_job_search()`
- Uses `search.py`'s `get_job_ids()` + `fetch_all_jobs()` (async)

**Web Research** (`tools.py`):
- `get_google_search_results()` → Serper API via `utils.SerperClient`
- `scrape_website()` → FireCrawl via `utils.FireCrawlClient`

**Resume/Cover Letter**:
- `ResumeExtractorTool` (BaseTool) → `load_resume()` (PyMuPDF)
- `generate_letter_for_specific_job()` and `save_cover_letter_for_specific_job()` → `write_cover_letter_to_doc()`

## Model Configuration

LLM is configured at runtime via `app.py` with `settings` dict:
- `model`: "gpt-4o-mini", "gpt-4o", "llama-3.1-70b-versatile"
- `model_provider`: "openai" or "groq"
- `temperature`: 0.3

Passed to `init_chat_model(**state["config"])` in each node.

## Routing Logic

The supervisor (`chains.py`) uses structured output to select the next agent based on `RouteSchema`:
```python
RouteSchema.next_action: Literal[
    "ResumeAnalyzer", "CoverLetterGenerator",
    "JobSearcher", "WebResearcher", "ChatBot", "Finish"
]
```

Agents return results as `HumanMessage` with their name, allowing context accumulation in the message history.