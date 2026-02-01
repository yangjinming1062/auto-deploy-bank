# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Seed-OSS is an open-source 36B parameter causal language model developed by ByteDance Seed Team. It features:
- **512K native long context**
- **Flexible thinking budget control** - dynamically adjust reasoning length (use multiples of 512: 512, 1K, 2K, 4K, 8K, 16K)
- **Agent capabilities** - tool calling and function execution
- **International (i18n) focus** - optimized primarily for English

## Setup

```bash
pip install -r requirements.txt
# For vLLM inference:
pip install vllm>=0.10.2
```

## Inference Commands

### Basic Transformers Inference
```bash
python inference/generate.py --model_path /path/to/model --thinking_budget 512
```

Key parameters:
- `--model_path`: Path to model directory (required)
- `--prompts`: Input prompts as Python list string
- `--max_new_tokens`: Generation limit (default: 4096)
- `--thinking_budget`: Token limit for chain-of-thought (default: -1 for unlimited)
- `--load_in_4bit`/`--load_in_8bit`: Enable quantization

### vLLM Server
```bash
bash inference/vllm_serve.sh
# Or manually:
python3 -m vllm.entrypoints.openai.api_server \
    --host localhost \
    --port 4321 \
    --enable-auto-tool-choice \
    --tool-call-parser seed_oss \
    --trust-remote-code \
    --model ./Seed-OSS-36B-Instruct \
    --chat-template ./Seed-OSS-36B-Instruct/chat_template.jinja \
    --tensor-parallel-size 8 \
    --dtype bfloat16 \
    --served-model-name seed_oss
```

### vLLM Chat Client
```bash
# Non-streaming
python inference/vllm_chat.py --max_new_tokens 4096 --thinking_budget -1
# Streaming
python inference/vllm_chat.py --max_new_tokens 4096 --thinking_budget -1 --stream
```

### vLLM Tool Calling
```bash
# Non-streaming
python inference/vllm_tool_call.py --max_new_tokens 4096 --thinking_budget -1
# Streaming
python inference/vllm_tool_call.py --max_new_tokens 4096 --thinking_budget -1 --stream
```

## Architecture

The repository contains inference utilities only (model weights are downloaded from Hugging Face):

| File | Purpose |
|------|---------|
| `inference/generate.py` | Basic Transformers-based inference script |
| `inference/vllm_chat.py` | OpenAI-compatible chat client |
| `inference/vllm_tool_call.py` | Tool/function calling demonstration |
| `inference/vllm_output_parser.py` | Parses streaming and non-streaming vLLM output |

## Thinking Budget Pattern

The model uses `<seed:think>` and `</seed:think>` tags for chain-of-thought, with optional `<seed:cot_budget_reflect>` tokens that track budget consumption:

```
<seed:think>
Reasoning steps here...
<seed:cot_budget_reflect>I have used 129 tokens, and there are 383 tokens remaining.</seed:cot_budget_reflect>
...
<seed:cot_budget_reflect>I have exhausted my token budget, and now I will start answering.</seed:cot_budget_reflect>
</seed:think>
Final answer...
```

## Recommended Sampling Settings
- Temperature: 1.1
- Top-p: 0.95

## Model Download
Models are available on Hugging Face:
- `ByteDance-Seed/Seed-OSS-36B-Base`
- `ByteDance-Seed/Seed-OSS-36B-Base-woSyn`
- `ByteDance-Seed/Seed-OSS-36B-Instruct`