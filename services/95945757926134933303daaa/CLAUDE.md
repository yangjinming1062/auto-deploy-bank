# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CrewAI Studio is a Streamlit-based GUI application for creating and running CrewAI agent crews without coding. It provides a visual interface for defining agents, tasks, crews, and knowledge sources, then executing them with various LLM providers.

## Commands

### Running the Application

```bash
# Using virtual environment (Linux/MacOS)
./run_venv.sh

# Using Conda environment
./run_conda.sh

# Direct Python execution
pip install -r requirements.txt
streamlit run ./app/app.py

# Using Docker
docker-compose up --build
```

### Database

Default: SQLite (`sqlite:///crewai.db`)
PostgreSQL: Set `DB_URL` environment variable to PostgreSQL connection string.

## Architecture

### Entry Point
- `app/app.py`: Main Streamlit application; initializes database, loads session data, manages page navigation via sidebar

### Core Domain Models
- `app/my_agent.py`: `MyAgent` class - wraps CrewAI Agent with role, backstory, goal, tools, LLM config
- `app/my_crew.py`: `MyCrew` class - orchestrates agents and tasks, supports sequential/hierarchical processes
- `app/my_task.py`: `MyTask` class - task definitions with context dependencies
- `app/my_knowledge_source.py`: `MyKnowledgeSource` class - RAG knowledge sources for agents/crews

### LLM Configuration
- `app/llms.py`: LLM provider abstraction; supports OpenAI, Groq, Ollama, Anthropic, LM Studio, XAI (Grok)
- `create_llm(provider_and_model, temperature)` factory function parses "Provider: Model" format
- Environment variables: `OPENAI_API_KEY`, `GROQ_API_KEY`, `ANTHROPIC_API_KEY`, `OLLAMA_HOST`, `LMSTUDIO_API_BASE`, `XAI_API_KEY`, `OPENAI_PROXY_MODELS`, `OLLAMA_MODELS`

### Tools System
- `app/my_tools.py`: Tool wrapper classes (`My*Tool`) implementing `MyTool` base; each wraps a `crewai_tools` class
- `TOOL_CLASSES` registry maps tool names to wrapper classes for dynamic instantiation
- Custom tools in `app/tools/` directory extend base tool functionality

### Data Persistence
- `app/db_utils.py`: SQLAlchemy-based ORM using single `entities` table with entity_type polymorphism
- Entity types: `agent`, `task`, `crew`, `tool`, `knowledge_source`, `result`, `tools_state`
- All entities serialized to JSON; auto-creates tables on startup
- Uses upsert pattern (`ON CONFLICT`) for inserts

### UI Page Groups
- `pg_agents.py`: Agent creation/editing UI
- `pg_tasks.py`: Task creation/editing with agent assignment and context dependencies
- `pg_crews.py`: Crew composition with agent/task selection, process/manager config
- `pg_tools.py`: Tool configuration (add, delete, configure parameters)
- `pg_knowledge.py`: Knowledge source management (PDF, DOCX, CSV, websites, etc.)
- `pg_crew_run.py`: Crew execution with threaded runs, placeholder inputs, result display
- `pg_results.py`: Historical results viewing
- `pg_export_crew.py`: JSON export/import for crews

### Key Patterns

1. **Session State Management**: Streamlit session state (`st.session_state`) is used heavily for edit modes and cross-page state. Each model uses keys like `edit_{id}`, `name_{id}`, etc.

2. **Model `draw()` Pattern**: Each domain model (`MyAgent`, `MyCrew`, `MyTask`, etc.) implements a `draw()` method that renders its UI component, supporting both view and edit modes.

3. **Database Loader Pattern**: Functions like `load_agents()`, `load_crews()` populate session state on startup and are called from `app.py`.

4. **CrewAI Conversion**: Models implement `get_crewai_*()` methods to convert to native CrewAI objects (`get_crewai_agent()`, `get_crewai_task()`, `get_crewai_crew()`).

5. **LLM Provider Switching**: Uses environment switching (`switch_environment`/`restore_environment` in `llms.py`) for API key isolation between providers.

6. **Cascade Deletion**: `MyCrew.analyze_dependencies()` identifies conflicts before deletion, preventing orphaned entities.

7. **Threaded Execution**: `pg_crew_run.py` runs crews in background threads with console capture for real-time output.

### Important Files for Reference

- `app/db_utils.py` - All database operations, entity serialization/deserialization, export/import
- `app/llms.py` - LLM provider factory, environment variable handling
- `app/my_crew.py` - Crew creation, validation, knowledge sources, cascade delete handling
- `app/pg_crew_run.py` - Threaded crew execution, result serialization, console capture