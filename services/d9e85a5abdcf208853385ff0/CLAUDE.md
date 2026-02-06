# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

KwaiAgents is an AI Agent system from Kuaishou Technology (KuaikeG). It includes:
- **KAgentSys-Lite**: A lite agent system with planning, reflection, tool-use, and concluding capabilities
- **KAgentLMs**: Fine-tuned LLMs (Qwen, Baichuan2) with agent capabilities via meta-agent tuning
- **KAgentInstruct**: 200k+ agent-related instruction fine-tuning data
- **KAgentBench**: 3,000+ human-edited evaluation data for testing agent capabilities

## Build & Test Commands

```bash
# Install dependencies
conda create -n kagent python=3.10
conda activate kagent
pip install -r requirements.txt

# Install package in development mode
python setup.py develop

# Run agent with GPT models (requires OPENAI_API_KEY)
kagentsys --query="Who is Andy Lau's wife?" --llm_name="gpt-3.5-turbo" --lang="en"

# Run agent with local model (requires vLLM service running)
kagentsys --query="Who is Andy Lau's wife?" --llm_name="kagentlms_qwen_7b_mat" \
  --use_local_llm --local_llm_host="localhost" --local_llm_port=8888 --lang="en"

# Run benchmark evaluation
cd benchmark
python infer_qwen.py qwen_benchmark_res.jsonl
python benchmark_eval.py ./benchmark_eval.jsonl ./qwen_benchmark_res.jsonl
```

## Architecture

```
agent_start.py          # CLI entry point, parses arguments, runs AgentService
agents/
  ├── kagent.py         # KAgentSysLite - core agent loop (planning, tool use, conclusion)
  ├── agent_profile.py  # AgentProfile - agent name, bio, instructions, tools config
  └── prompts.py        # Prompt templates for planning and conclusion
llms/
  ├── clients.py        # OpenAIClient, FastChatClient for LLM API calls
  └── __init__.py       # create_chat_completion() - unified LLM interface
tools/
  ├── base.py           # BaseTool, BaseResult abstract classes
  ├── search.py         # WebSearch tool (DuckDuckGo)
  ├── browser.py        # BrowserTool (Selenium/chromedriver)
  ├── weather.py        # WeatherTool
  ├── calendars.py      # CalendarTool
  ├── timedelta.py      # TimeDeltaTool
  ├── solarterms.py     # SolarTermsTool
  └── commons.py        # NoTool, FinishTool (task signaling)
utils/
  ├── chain_logger.py   # ChainMessageLogger for logging agent thought chain
  ├── json_fix_general.py  # JSON parsing utilities
  └── ...               # Other utilities (date, HTML, NLP, Selenium)
```

### Agent Execution Flow (KAgentSysLite.chat)

1. **Planning Phase**: Uses `smart_llm_model` to generate task plan from goal + memory + tools
2. **Tool Use Phase**: Executes tasks using `fast_llm_model`, calls tools from `name2tools` dict
3. **Conclusion Phase**: Synthesizes final response using `smart_llm_model`

The loop iterates up to `max_iter_num` with a `SingleTaskListStorage` queue managing tasks.

### LLM Clients

- `OpenAIClient`: For GPT-3.5/GPT-4 via OpenAI API (uses `OPENAI_API_KEY` env var)
- `FastChatClient`: For local models served via vLLM/FastChat (OpenAI-compatible API at `localhost:8888`)

The client selects the appropriate prompt format based on model type (Qwen uses `<|im_start|>/<|im_end|>`, Baichuan uses `<reserved_106>/<reserved_107>`).

### Tool Development

Tools inherit from `BaseTool` and return `BaseResult`:
- Define `name` and `zh_name` class attributes
- Implement `__call__(self, **kwargs)` returning a `BaseResult`
- Override `answer` and `answer_md` properties for text/markdown output

See `examples/custom_tool_example.py` for a complete example (GithubTrendingTool).

## Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `OPENAI_API_KEY` | For GPT models | OpenAI API authentication |
| `WEATHER_API_KEY` | Optional | Weather tool (weatherapi.com) |
| `http_proxy` / `https_proxy` | Optional | Network proxy for DuckDuckGo search |
| `OPENAI_API_TYPE` | Optional | Set to "azure" for Azure OpenAI |
| `OPENAI_API_VERSION` | Azure only | Azure API version |
| `OPENAI_API_BASE` | Azure only | Azure endpoint URL |

## Key Configuration (Config class)

- `fast_llm_model`: Model for tool use (default: gpt-3.5-turbo)
- `smart_llm_model`: Model for planning/conclusion (default: gpt-4)
- `use_local_llm`: Whether to use FastChatClient instead of OpenAIClient
- `local_llm_host`/`local_llm_port`: Local model server address
- `max_tokens_num`: LLM context window limit
- `llm_max_retries`: Retry attempts for LLM calls (default: 5)

## Useful Links

- Paper: http://arxiv.org/abs/2312.04889
- Models: https://huggingface.co/collections/kwaikeg/kagentlms-6551e685b5ec9f9a077d42ef
- Dataset: https://huggingface.co/datasets/kwaikeg/KAgentInstruct
- Benchmark: https://huggingface.co/datasets/kwaikeg/KAgentBench