# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

KwaiAgents is an AI agent system from Kuaishou Technology that includes:
- **KAgentSys-Lite**: A lightweight agent framework for information-seeking tasks with tool-use capabilities
- **KAgentLMs**: Fine-tuned LLMs with agent capabilities (Qwen-MAT, Baichuan2-MAT models)
- **KAgentBench**: An evaluation benchmark for agent capabilities (planning, tool-use, reflection, concluding, profiling)

## Development Commands

```bash
# Install the package in development mode
pip install -r requirements.txt
python setup.py develop

# Run agent with GPT-3.5-turbo (requires OPENAI_API_KEY)
export OPENAI_API_KEY=sk-xxxxx
export WEATHER_API_KEY=xxxxx  # Optional, for weather tool
kagentsys --query="Who is Andy Lau's wife?" --llm_name="gpt-3.5-turbo" --lang="en"

# Run agent with local model (requires FastChat server)
kagentsys --query="Who is Andy Lau's wife?" --llm_name="kagentlms_qwen_7b_mat" \
  --use_local_llm --local_llm_host="localhost" --local_llm_port=8888 --lang="en"

# Run benchmark evaluation
cd benchmark
python infer_qwen.py qwen_benchmark_res.jsonl
python benchmark_eval.py ./benchmark_eval.jsonl ./qwen_benchmark_res.jsonl
```

## Architecture

### Main Entry Point
- `kwaiagents/agent_start.py`: CLI entry point with `AgentService` class that handles configuration parsing and orchestrates the agent

### Core Agent (`kwaiagents/agents/kagent.py`)
- `KAgentSysLite`: Main agent class that implements the agent loop
  - `task_plan()`: Generates new tasks using smart LLM based on goal and memory
  - `tool_use()`: Executes tool calls and returns observations
  - `conclusion()`: Synthesizes final response from tool results
  - `chat()`: Main loop that iterates through planning → tool execution → conclusion

### Configuration (`kwaiagents/config.py`)
- `Config` class manages LLM settings, browser config, and chain logging
- Global `CFG` instance for runtime configuration

### Agent Profile (`kwaiagents/agents/agent_profile.py`)
- `AgentProfile`: Configures agent identity (name, bio, instructions, tools, max iterations)

### LLM Clients (`kwaiagents/llms/`)
- `OpenAIClient`: Routes to OpenAI API or Azure OpenAI (via `OPENAI_API_TYPE` env var)
- `FastChatClient`: Calls local vLLM/FastChat servers for local models
- `create_chat_completion()`: Unified interface with retry logic

### Tools (`kwaiagents/tools/`)
- Base classes: `BaseTool`, `BaseResult`
- Built-in tools: `SearchTool`, `BrowserTool`, `WeatherTool`, `CalendarTool`, `TimeDeltaTool`, `SolarTermsTool`
- `ALL_TOOLS` and `ALL_NO_TOOLS` lists for tool registration
- Custom tools must inherit `BaseTool` and return `BaseResult` subclasses

### Prompt System (`kwaiagents/agents/prompts.py`)
- `make_planning_prompt()`: Creates task planning prompts (Chinese/English)
- `make_task_conclusion_prompt()`: Creates final response synthesis prompts
- Prompt truncation handles token limits using `transformers` tokenizer

### Utilities (`kwaiagents/utils/`)
- `chain_logger.py`: Message logging for agent execution chains
- `json_fix_general.py`: JSON parsing and correction utilities
- `date_utils.py`: Date/time formatting utilities
- `function_utils.py`: Tool-to-OpenAI-function format conversion

## Key Configuration Options

```python
# Available llm_name values
"gpt-3.5-turbo", "gpt-4", "kagentlms_qwen_7b_mat", "kagentlms_baichuan2_13b_mat"

# Tool selection
--tool_names '["auto", "search", "browser", "weather", "calendar", "timedelta", "solarterms", "notool"]'
```

## Adding Custom Tools

See `examples/custom_tool_example.py`:
1. Define result class inheriting from `BaseResult`
2. Define tool class inheriting from `BaseTool`
3. Set `name`, `zh_name`, `description`, `tips` class attributes
4. Implement `__call__()` method with tool logic
5. Pass tool class to `KAgentSysLite` via `tools` parameter

## Local Model Deployment

```bash
# Terminal 1: Start controller
python -m fastchat.serve.controller

# Terminal 2: Start vLLM worker (single GPU)
python -m fastchat.serve.vllm_worker --model-path $MODEL_PATH --trust-remote-code

# Terminal 3: Start REST API
python -m fastchat.serve.openai_api_server --host localhost --port 8888
```