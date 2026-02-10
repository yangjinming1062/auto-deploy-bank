# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of 15+ Streamlit applications demonstrating AI/ML-powered data science workflows using LLMs (OpenAI GPT models). Each numbered directory (001-015) is a standalone project demonstrating a specific use case like SQL querying, data cleaning, feature engineering, EDA, and ML automation.

## Common Commands

**Run a Streamlit app:**
```bash
streamlit run <project_directory>/app.py
# Example: streamlit run 010_sql_database_agent_app/app.py
```

**Install dependencies (per project):**
```bash
pip install -r <project_directory>/requirements.txt
```

**Install the core ai-data-science-team library (used across most apps):**
```bash
pip install git+https://github.com/business-science/ai-data-science-team.git --upgrade
```

## Architecture

Each project follows a consistent structure:
- `app.py` or `<project_name>.py` - Main entry point (Streamlit app or standalone script)
- `requirements.txt` - Project-specific dependencies (not all projects have this)
- `data/` - SQLite databases or sample datasets
- `ai_functions/` - AI agent logic modules (in some projects)
- `utils/` - Utility functions (in some projects)

Most apps use the `ai-data-science-team` library which provides agents like `SQLDatabaseAgent`, `DataVisualizationAgent`, and multi-agent workflows. They follow a pattern of:
1. Setup LLM with OpenAI API key (via sidebar or environment/credentials.yml)
2. Initialize agent with connection/config
3. Handle user input async
4. Display results (dataframes, plots, SQL queries)

## Key Dependencies

- **streamlit** - UI framework
- **openai** - OpenAI API client
- **langchain / langchain-openai** - LLM orchestration
- **ai-data-science-team** - Custom AI agent library
- **pandas** - Data handling
- **sqlalchemy** - Database connections

## Configuration

Streamlit theme is configured in `.streamlit/config.toml` (dark theme with purple accents). Some apps load credentials from `../credentials.yml` using `yaml.safe_load()`.

## API Keys

Apps requiring OpenAI API keys accept them via:
- Environment variable: `os.environ['OPENAI_API_KEY']`
- YAML file: `../credentials.yml`
- Streamlit sidebar text input (type="password")