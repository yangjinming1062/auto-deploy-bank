# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AgentFlow is a **trainable, tool-integrated agentic framework** for in-the-flow agentic system optimization using **Flow-GRPO** (Flow-based Group Refined Policy Optimization). It features a modular architecture with four specialized agent modules that coordinate through evolving memory and integrated tools.

## Build & Development Commands

```bash
# Setup environment
bash setup.sh
source .venv/bin/activate

# Test all tools (run from agentflow/agentflow directory)
bash ./tools/test_all_tools.sh

# Test LLM engines
python agentflow/scripts/test_llm_engine.py

# Run quick start demo
python quick_start.py

# Prepare training data
python data/get_train_data.py      # train data (NQ + DeepMath-103K)
python data/aime24_data.py         # validation data

# Training (requires tmux)
tmux new-session -s agentflow
bash train/serve_with_logs.sh      # Window 0: vLLM server
bash train/train_with_logs.sh      # Window 1: training

# Benchmark evaluation
bash scripts/serve_vllm.sh         # Serve planner model with vLLM
cd test/bamboogle && bash run.sh   # Run specific benchmark
```

**Key Configuration Files:**
- `agentflow/pyproject.toml` - Package metadata and dependencies
- `agentflow/requirements.txt` - Python dependencies
- `train/config.yaml` - Training hyperparameters (model, tools, RL params)
- `agentflow/.env.template` - Environment variables template

## Architecture

```
AgentFlow/
├── agentflow/agentflow/
│   ├── engine/              # LLM engine adapters (OpenAI, DashScope, vLLM, etc.)
│   │   └── factory.py       # create_llm_engine() - central factory for all engines
│   ├── models/              # Four specialized agent modules
│   │   ├── planner.py       # Plans actions, generates next steps, final outputs
│   │   ├── executor.py      # Executes tool commands (generates + runs code)
│   │   ├── verifier.py      # Verifies memory completeness, decides STOP/CONTINUE
│   │   ├── memory.py        # Stores action-history pairs across turns
│   │   └── initializer.py   # Loads/enumerates available tools
│   ├── tools/               # Tool implementations (BaseTool subclasses)
│   │   ├── base.py          # BaseTool abstract class
│   │   ├── python_coder/    # Generates/executes Python code
│   │   ├── google_search/   # Web search via Google
│   │   ├── wikipedia_search/# Wikipedia RAG search
│   │   ├── web_search/      # General web search
│   │   └── base_generator/  # General response generation
│   └── solver.py            # Main orchestration loop (coordination layer)
├── agentflow/trainer.py     # Multi-worker RL trainer (Trainer class)
├── agentflow/verl/          # VERL integration for RL training
└── quick_start.py           # Demo entry point
```

## Core Abstractions

### Agent Modules (in `agentflow/models/`)

All four agents share a common pattern: they use `llm_engine_fixed` (typically Qwen-2.5-7B) for deterministic operations, and a configurable `llm_engine` for trainable/generation operations.

1. **Planner** - Main reasoning agent
   - `analyze_query()` - Initial query analysis
   - `generate_next_step()` - Determines next action + tool
   - `generate_final_output()` / `generate_direct_output()` - Final responses

2. **Executor** - Tool command execution
   - `generate_tool_command()` - LLM generates code to call tool
   - `execute_tool_command()` - Runs generated code with timeout protection

3. **Verifier** - Context verification
   - `verificate_context()` - Evaluates if memory is complete enough
   - Returns STOP/CONTINUE signals to control the main loop

4. **Memory** - Action-history storage
   - `add_action()` - Records step, tool, sub_goal, command, result
   - `get_actions()` - Returns formatted history for LLM context

### Tool System (`agentflow/tools/`)

Tools inherit from `BaseTool` and must define:
- `TOOL_NAME` - External name constant
- `require_llm_engine` - Boolean flag
- `execute(query, **kwargs)` - Main implementation method

Execution model: Planner decides tool → Executor generates command → `tool.execute()` is called via `exec()` with timeout.

### LLM Engine Factory (`agentflow/engine/factory.py`)

```python
from agentflow.engine.factory import create_llm_engine

# Supported prefixes: azure-, gpt-, dashscope-, claude-, deepseek-, gemini-,
#                     grok-, vllm-, litellm-, together-, ollama-
engine = create_llm_engine(model_string="gpt-4o", temperature=0.7)
response = engine(prompt)
```

### Solver Orchestration (`agentflow/solver.py`)

The `Solver` class runs the main loop:
1. Query analysis
2. For each step (up to `max_steps`):
   - Planner generates next step (context, sub_goal, tool)
   - Executor generates and runs tool command
   - Memory stores action/result
   - Verifier checks completeness → STOP or CONTINUE
3. Generate final/direct outputs

## Flow-GRPO Training

The `Trainer` class manages distributed rollouts:
- Uses `AgentFlowClient` to communicate with vLLM server
- Supports multi-worker parallel execution via multiprocessing
- Integrates with VERL for RL training
- Tracer system for logging (AgentOps, custom)

Key files:
- `agentflow/trainer.py` - Trainer class for worker orchestration
- `agentflow/client.py` - AgentFlowClient for vLLM communication
- `agentflow/runner.py` - AgentRunner for execution loop

## Configuration Patterns

### Solver Configuration (`solver.py:construct_solver`)

```python
model_engine=[planner_main, planner_fixed, verifier, executor]
# "trainable" = use llm_engine_name (the model being trained)
# Specific engine name = use that engine
```

### Tool Configuration

Tools can use different engines per tool via `tool_engine` list in `Initializer`:
- "Default" - Tool's default model
- "self" - Use main model_string
- Specific name - Use that engine (e.g., "gpt-4o-mini")

## Key Files for Extension

- `agentflow/engine/factory.py` - Add new LLM engines here
- `agentflow/tools/base.py` - Base class for new tools
- `agentflow/models/planner.py` - Modify prompts for planning behavior
- `agentflow/models/formatters.py` - Pydantic response formats
- `agentflow/solver.py` - Main loop logic