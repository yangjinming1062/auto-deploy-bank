# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DynaSaur is a dynamic LLM-based agent framework that uses Python as a universal representation of actions. At each step, the agent generates Python code that calls existing actions or creates new ones when the action set is insufficient. These new actions are saved to disk and indexed in a vector database for future retrieval.

## Development Commands

```bash
# Setup environment
conda create -n dynasaur python=3.12
conda activate dynasaur
pip install -r requirements.txt

# Configure environment (required before running)
# Create .env file with Azure API keys - see README.md for template

# Download GAIA benchmark data
mkdir data
git clone https://huggingface.co/datasets/gaia-benchmark/GAIA
mv GAIA/2023 data/gaia/
rm -rf GAIA

# Run agent on validation set
python dynasaur.py --set validation

# Run agent on test set (disables action accumulation)
python dynasaur.py --set test --model_name gpt-4o-2024-08-06
```

## Architecture

### Core Components

**`dynasaur.py`** - Entry point that:
- Loads GAIA dataset from HuggingFace
- Initializes the execution environment (`Env`)
- Creates the agent with tools and LLM engine
- Runs evaluation via `answer_questions()`

**`agents.py`** - Agent hierarchy:
- `UnrestrictedReactCodeAgent`: Extends transformers ReAct agent with metrics tracking
- `DynamicActionSpaceAgent`: Adds dynamic tool generation and vector database retrieval
- `StructuredOutputDynamicActionSpaceAgent`: Uses structured output (thought/code JSON) from LLM

**`env.py`** - Code execution environment:
- `PythonJupyterEnv`: Executes Python code via IPython kernel
- `Env`: Wrapper that manages the execution state and output collection

**`actions.py`** - Tool definitions:
- Web browsing: `SearchInformationTool`, `VisitTool`, `DownloadTool`, `FinderTool`, etc.
- File handling: `TextInspectorTool` for PDF/DOCX/images
- Tool retrieval: `ToolRetrievalTool` queries ChromaDB for relevant generated tools

**`scripts/llm_engines.py`** - LLM integrations:
- `AzureOpenAIEngine`: Primary engine using Azure API
- `StructuredOutputAzureOpenAIEngine`: Enforces structured response format (ThoughtCodeFormat)
- `OpenAIEngine`, `AnthropicEngine`: Alternative backends

**`utils.py`** - AST utilities:
- `parse_generated_tools()`: Extracts function definitions from LLM-generated code
- `extract_function_calls()`: Analyzes which functions code uses
- `add_parent_pointers()`: Enables AST tree traversal with parent references

### Execution Flow

1. Agent receives question with file paths
2. LLM generates structured output: `{"thought": "...", "code": "..."}`
3. Code executes in `PythonJupyterEnv`
4. New function definitions are parsed and saved to `generated_actions/<model>/`
5. Generated tools are indexed in ChromaDB (`<generated_tool_dir>/vectordb`)
6. Agent can retrieve past tools via `get_relevant_tools(query)`
7. Final answer submitted via `submit_final_answer(answer)`

### Key Configuration

- `GENERATED_ACTION_DIR`: Where generated tools are saved (env var set by dynasaur.py)
- `MODEL_NAME`: LLM model identifier (default: `gpt-4o-2024-08-06`)
- Embedding model for tool retrieval: configured via `EMBED_MODEL_TYPE` env var (AzureOpenAI by default)

## Code Patterns

- Generated tools use `@track_num_calls` decorator for metrics
- Tool retrieval uses semantic similarity via ChromaDB and embeddings
- Agent maintains `generated_toolbox` separate from initial tools
- `disable_accum=True` for test set prevents saving new actions