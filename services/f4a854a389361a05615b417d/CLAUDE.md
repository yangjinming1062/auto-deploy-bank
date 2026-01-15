# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LLMxMapReduce is a divide-and-conquer framework for enhancing LLMs in understanding and generating long sequences. Three versions exist:

- **V1**: Basic MapReduce framework (chunk → map → collapse → reduce)
- **V2**: Entropy-driven convolutional test-time scaling with encode→hidden→decode pipeline
- **V3**: MCP-based multi-agent system for academic survey generation

## Common Commands

### LLMxMapReduce-V2
```bash
cd LLMxMapReduce_V2
conda create -n llm_mr_v2 python=3.11
conda activate llm_mr_v2
pip install -r requirements.txt
python -m playwright install --with-deps chromium

# Download required NLTK data
python -c "import nltk; nltk.download('punkt_tab')"

# Run pipeline with topic
bash scripts/pipeline_start.sh "Your Topic" output_file_path.jsonl

# Or with input file
python ./src/start_pipeline.py --input_file input.jsonl --output_file output.jsonl --config_file ./config/model_config.json

# Evaluation
bash scripts/eval_all.sh output_data_file_path.jsonl
```

### LLMxMapReduce-V3
```bash
cd LLMxMapReduce_V3
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Configure API keys in config/unified_config.json
bash start.sh "Your Topic" "Your Description"
```

### LLMxMapReduce-V1
```bash
cd LLMxMapReduce_V1
pip install -r requirements.txt

# For self-hosted backend:
bash URLs/start_gunicorn.sh --hf-model-name=your/model/path --per-proc-gpus 2 --port=5002

# Or use OpenAI API with config in config/
python pipeline.py
```

## Environment Variables

Required for V2 (set before running):
```bash
export OPENAI_API_KEY=your_key
export OPENAI_API_BASE=your_base_url
export PROMPT_LANGUAGE="en"  # or "zh"
```

Required for V3: Edit `config/unified_config.json` with API keys.

## Architecture

### V2 Pipeline Structure
- `src/start_pipeline.py`: Entry point, orchestrates LLM_search, AsyncCrawler, and EntirePipeline
- `src/async_d/`: Async pipeline infrastructure (Pipeline, Monitor, PipelineAnalyser)
- `src/encode/`: EncodePipeline - processes input documents
- `src/hidden/`: HiddenPipeline - convolutional scaling layers for information integration
- `src/decode/`: DecodePipeline - generates final output
- `config/model_config.json`: Model configuration for each processing stage

### V3 MCP Architecture
- `src/start.py`: Entry point, runs AnalyseLLMHostInterface
- `src/mcp_host/host.py`: LLM host that orchestrates MCP servers
- `src/mcp_server/`: Separate MCP servers for each task (search, group, skeleton, digest, writing)
- `src/mcp_client/`: Client interfaces for calling MCP servers
- `config/unified_config.json`: Unified config for models, API keys, prompts, and MCP server definitions

Configuration keys for V3:
- `api_keys`: OpenAI, search engines (SerpAPI, Bing, Google)
- `models`: Default model and role-specific models
- `mcp_server_config`: Startup commands for each MCP server
- `prompts`: System prompts for each processing stage
- `tools`: MCP tool definitions exposed to LLM host

## Key Configuration Files

| File | Purpose |
|------|---------|
| `LLMxMapReduce_V2/config/model_config.json` | V2 model settings per pipeline stage |
| `LLMxMapReduce_V3/config/unified_config.json` | V3 models, API keys, prompts, MCP servers |
| `LLMxMapReduce_V1/config/*.yaml` | V1 LLM backend and execution parameters |