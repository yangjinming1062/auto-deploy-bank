# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ChatDB is a research project (arXiv:2306.03901) that augments LLMs with SQL databases as external symbolic memory. The LLM generates SQL instructions to manipulate MySQL databases for complex multi-hop reasoning.

## Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment (required)
cp .env.template .env
# Edit .env with OPENAI_API_KEY and MYSQL_PASSWORD
```

### Running
```bash
# Run the fruit shop CLI demo
python chatdb.py

# Interactive mode - type queries like:
# "Who bought 100kg apple on 2010-03-27?"
# "Customer named 'John' bought 10kg banana"
```

### MySQL Requirement
MySQL server must be running locally (default: localhost:3306). The demo automatically creates a database named "try1024" and populates it with sample data from CSVs.

## Architecture

### Core Flow (chatdb.py)
1. User input → `generate_chat_responses()`
2. LLM generates step-by-step SQL plan using `prompt_ask_steps` template
3. Parse response with regex (`Step\d+:` pattern) into structured steps
4. Execute SQL via `chain_of_memory()` which handles `<placeholder>` substitution
5. Dynamic SQL population via `call_ai_function.py` for multi-step dependencies

### Key Components

| File | Purpose |
|------|---------|
| `chatdb.py` | Main orchestration: parses LLM SQL plans, executes step chains |
| `chat.py` | Token-aware chat wrapper for OpenAI API with message history |
| `mysql.py` | `MySQLDB` class wrapping PyMySQL with CRUD helpers |
| `config.py` | Singleton `Config` class loading `.env` variables |
| `call_ai_function.py` | Dynamic function calling pattern for SQL population |
| `chatgpt.py` | Low-level OpenAI API wrapper with retry logic |
| `fruit_shop_schema.py` | Table definitions (fruits, customers, sales, etc.) |
| `tables.py` | Database init: creates tables, loads CSVs via SQLAlchemy |
| `chatdb_prompts.py` | LangChain `PromptTemplate` for SQL generation |
| `sql_examples.py` | Example Q&A pairs shoting multi-step SQL patterns |

### Two-Model Strategy
- **FAST_LLM_MODEL** (gpt-3.5-turbo): SQL generation, faster/cheaper
- **SMART_LLM_MODEL** (gpt-4): Complex function calling (populate_sql_statement)

### Dynamic SQL Pattern
SQL queries use `<placeholder>` syntax for values from previous results. For example:
```sql
SELECT fruit_id, quantity_sold FROM sale_items WHERE sale_id = <sale_id>;
```

The `populate_sql_statement()` function uses GPT to extract and substitute these placeholders with actual values from prior query results.

### Data Flow
1. `tables.py:init_database()` creates MySQL tables and loads `csvs/*.csv` via SQLAlchemy
2. `chatdb.py:chain_of_memory()` iterates through steps, executing each SQL
3. Results accumulated in `sql_results_history` for downstream step substitution