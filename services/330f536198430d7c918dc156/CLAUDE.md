# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of **Generative AI/ML tutorials and applications** by Business Science. The repository contains 15+ standalone data science examples demonstrating AI-powered workflows including customer churn prediction, SQL database agents, exploratory data analysis, and automated feature engineering.

## Running Applications

**Streamlit Apps** (most examples):
```bash
streamlit run <directory>/app.py
```

Example:
```bash
streamlit run 010_sql_database_agent_app/app.py
```

**Standalone Python Scripts**:
```bash
python <directory>/<script_name>.py
```

Example:
```bash
python 002_customer_churn_ai_ml/customer_churn_ai_ml.py
```

**Jupyter Notebooks**:
```bash
jupyter notebook temp/<notebook_name>.ipynb
```

## Dependencies

Most apps share common dependencies defined in `requirements.txt` files:

- `streamlit` - Web app framework
- `openai` - OpenAI API client
- `langchain`, `langchain-openai`, `langgraph` - LLM orchestration
- `pandas`, `sqlalchemy` - Data manipulation and SQL
- `ai-data-science-team` - Custom agent library (install via `pip install git+https://github.com/business-science/ai-data-science-team.git`)

Install all dependencies for an app:
```bash
pip install -r <directory>/requirements.txt
```

## Common Architecture Patterns

### Streamlit Apps

All Streamlit apps follow a consistent pattern:

1. **Configuration section** - Set page title, config options
2. **Sidebar** - API key input, model selection, data upload
3. **Session state** - Store dataframes, messages, API keys
4. **Chat interface** - Chat input with `st.chat_message` and `StreamlitChatMessageHistory`
5. **Agent integration** - Async agent invocation using `ai_data_science_team` agents

Example model list for OpenAI apps:
```python
MODEL_LIST = ['gpt-4o-mini', 'gpt-4o']
```

### Database Apps

SQL-based apps use SQLAlchemy connections:
```python
sql_engine = sql.create_engine(st.session_state["PATH_DB"])
conn = sql_engine.connect()
```

Default database: Northwind SQLite database at `data/northwind.db`

### Data Science Workflows

Typical patterns:
1. Load data (CSV via `pd.read_csv()` or database via SQLAlchemy)
2. Generate LLM summaries / text embeddings
3. Feature engineering (LabelEncoder, embedding expansion to DataFrame)
4. ML model training (XGBoost, scikit-learn)
5. Model interpretation (feature importance plots)

### API Key Handling

Apps require OpenAI API key via `st.sidebar.text_input` with `type="password"`. Key validation:
```python
client = OpenAI(api_key=api_key)
models = client.models.list()  # Validate key
```

## Key Directories

- `00X_*` - Numbered example directories (1-15+)
- `data/` - Shared datasets (churn_data.csv, northwind.db)
- `.streamlit/` - Streamlit theming (dark theme configured)
- `temp/002_csv_semantic_search/` - Alternative implementation path

## Editor Configuration

VS Code settings in `.vscode/settings.json`:
- Jupyter notebooks use interactive window with selection execution
- Notebook root: workspace folder

## Streamlit Theme

Dark theme configured in `.streamlit/config.toml`:
- Primary color: #d33682 (magenta)
- Dark background (#000000)
- Sans-serif font