# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

JARVIS is a research project exploring AGI through LLM-based agent systems. It contains three independent components:

1. **HuggingGPT** (`hugginggpt/`) - Collaborative system where ChatGPT orchestrates HuggingFace models
2. **EasyTool** (`easytool/`) - Method for creating structured tool instructions for LLM agents
3. **TaskBench** (`taskbench/`) - Benchmark for evaluating LLM task automation

## Common Commands

### HuggingGPT (LLM-powered collaborative system)

```bash
# Server mode (requires GPU for local models)
cd hugginggpt/server
conda create -n jarvis python=3.8
conda activate jarvis
pip install -r requirements.txt
cd models && bash download.sh  # For local model inference
python models_server.py --config configs/config.default.yaml
python awesome_chat.py --config configs/config.default.yaml --mode server  # for text-davinci-003

# CLI mode (lighter, uses HF Inference Endpoints)
python awesome_chat.py --config configs/config.default.yaml --mode cli

# Gradio demo
python run_gradio_demo.py --config configs/config.gradio.yaml

# Web UI
cd ../web && npm install && npm run dev
```

Environment variables: `OPENAI_API_KEY`, `HUGGINGFACE_ACCESS_TOKEN`

### EasyTool (Tool instruction evaluation)

```bash
cd easytool
pip install -r requirements.txt
export OPENAI_API_KEY="your_key"

# Data construction
python3 data_process.py

# ToolBench evaluation
python3 main.py --model_name gpt-3.5-turbo --task toolbench --data_type G2 --tool_root_dir ./toolenv/tools
python3 main.py --model_name gpt-3.5-turbo --task toolbench_retrieve --data_type G2

# FuncQA evaluation
python3 main.py --model_name gpt-3.5-turbo --task funcqa --data_type funcqa_mh

# RestBench evaluation
python3 main.py --model_name gpt-3.5-turbo --task restbench
```

### TaskBench (LLM evaluation benchmark)

```bash
cd taskbench
pip install -r requirements.txt

# Deploy LLM endpoint (for open-source models)
python3 -m fastchat.serve.controller
python3 -m fastchat.serve.vllm_worker --model-path lmsys/vicuna-7b-v1.3
python3 -m fastchat.serve.openai_api_server --host localhost --port 4000

# Inference
export YOUR_API_KEY=API_KEY
python inference.py --llm gpt-4 --data_dir data_multimedia

# Evaluation
python evaluate.py --data_dir data_multimedia --prediction_dir $prediction_dir --llm gpt-4 --mode add
```

## Architecture

### HuggingGPT

The system uses ChatGPT as a controller to coordinate expert models from HuggingFace Hub. The workflow consists of four stages:
1. **Task Planning**: LLM parses user intent into solvable tasks
2. **Model Selection**: LLM selects models based on HuggingFace descriptions
3. **Task Execution**: Models are invoked and executed
4. **Response Generation**: LLM integrates predictions into final response

Key files:
- `awesome_chat.py`: Main entry point, handles LLM interactions and orchestration
- `models_server.py`: Local model inference endpoints
- `run_gradio_demo.py`: Gradio web UI
- `configs/`: YAML configuration files (inference_mode: local/huggingface/hybrid)

### EasyTool

Modular evaluation framework for tool usage by LLM agents:
- `main.py`: CLI entry point with task selection
- `easytool/toolbench.py`: ToolBench evaluation
- `easytool/funcQA.py`: Functional QA evaluation
- `easytool/restbench.py`: REST API evaluation

### TaskBench

Three-stage task automation evaluation (decomposition, invocation, parameter prediction):
- `inference.py`: Runs LLM inference on user requests
- `evaluate.py`: Computes metrics (R1, R2, BsF, n-F1, e-F1, t-F1, v-F1)
- `data_engine.py`: Dataset generation via Back-Instruct
- `generate_graph.py`: Tool graph construction

Datasets: `data_huggingface/`, `data_multimedia/`, `data_dailylifeapis/`

## Configuration

HuggingGPT uses YAML config files in `server/configs/`:
- `config.default.yaml`: Full local deployment (24GB+ VRAM, 284GB+ disk)
- `config.lite.yaml`: HuggingFace Inference Endpoints only
- `config.gradio.yaml`: Gradio demo configuration

Key config parameters:
- `model`: LLM endpoint (text-davinci-003, gpt-4, etc.)
- `inference_mode`: local/huggingface/hybrid
- `local_deployment`: minimal/standard/full (local model scale)