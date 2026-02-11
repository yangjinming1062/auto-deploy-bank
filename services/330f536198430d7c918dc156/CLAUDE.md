# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Free GenAI/ML Tips repository containing tutorial code for building AI/ML applications. Each numbered directory (001-015) represents a standalone project demonstrating different AI agent patterns and data science workflows. The `temp/` directory contains incomplete/experimental projects.

## Architecture Pattern

Each project (001-015) follows a consistent structure:
- `NNN_project_name.ipynb` - Jupyter notebook with embedded documentation
- `NNN_project_name.py` - Standalone Python script
- `data/` - Project-specific datasets (CSV, .db files)
- `utils/` - Helper modules for parsing and data processing
- `app.py` - Streamlit web application (in app-based projects: 010, 014, 015)

Projects use `PATH_ROOT` convention to reference their own data/resources and `sys.path.append()` to import from utils.

## LLM Models

Primary models used: `gpt-4o-mini` (default) and `gpt-4o`. Initialize with:
```python
ChatOpenAI(model_name='gpt-4o-mini', temperature=0)
```

## Running Projects

### Python Scripts
Requires `credentials.yml` in the repository root:
```yaml
openai: sk-your-api-key-here
```

Run a script:
```bash
python 001_pandas_dataframe_agent/001_pandas_dataframe_agent.py
```

### Streamlit Apps
Streamlit apps accept the API key via the sidebar UI:
```bash
streamlit run 010_sql_database_agent_app/app.py
streamlit run 014_ai_exploratory_copilot_app/app.py
streamlit run 015_ai_exploratory_copilot_dtale_integration/app.py
```

### Jupyter Notebooks
Open any `.ipynb` file in VS Code with Jupyter extension or JupyterLab.

## Dependencies

Install all dependencies:
```bash
pip install langchain langchain-openai langchain-experimental langgraph openai streamlit
pip install pandas sqlalchemy pytimetk dtale sweetviz plotly matplotlib
pip install git+https://github.com/business-science/ai-data-science-team.git --upgrade
```

Individual Streamlit apps have `requirements.txt` with their specific dependencies.

## Streamlit Theme

Dark theme with magenta primary color (`#d33682`) configured in `.streamlit/config.toml`.

## Common Patterns

| Pattern | Implementation |
|---------|---------------|
| **API Key (scripts)** | `os.environ['OPENAI_API_KEY'] = yaml.safe_load(open('../credentials.yml'))['openai']` |
| **API Key (Streamlit apps)** | Entered in sidebar, stored in `st.session_state["OPENAI_API_KEY"]` |
| **Path Setup** | `PATH_ROOT = '001_pandas_dataframe_agent'` + `sys.path.append()` |
| **Pandas Agent** | `create_pandas_dataframe_agent(llm, df, agent_type=AgentType.OPENAI_FUNCTIONS)` |
| **JSON Parsing** | `parse_json_to_dataframe()` from `utils/parsers.py` (extracts JSON from markdown code blocks) |
| **Custom Agents** | `ai_data_science_team.agents.*Agent` (SQLDatabaseAgent, EDAToolsAgent, etc.) |

## Agent Reference

| Project | Agent/Module | Purpose |
|---------|-------------|---------|
| 001 | `create_pandas_dataframe_agent` | Data Q&A on DataFrames |
| 002 | Custom ML agent | Churn prediction workflow |
| 003-005 | `ai_functions/*` modules | Data cleaning, feature engineering, wrangling |
| 006 | SQL copilot | Query generation |
| 007 | Visualization agent | Plotly chart generation |
| 008 | Multi-agent team | SQL data analysis |
| 009 | H2O AutoML agent | Automated machine learning |
| 010 | `SQLDatabaseAgent` | SQL database chat (Streamlit) |
| 011 | MLflow H2O agent | Model deployment |
| 012 | Data loader agent | Data ingestion |
| 013-015 | `EDAToolsAgent` | EDA with Dtale (Streamlit) |