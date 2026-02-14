# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

JARVIS is a collaborative AI system exploring AGI, consisting of three main components:

1. **HuggingGPT** (`/hugginggpt/`) - An LLM-based controller that orchestrates expert models from HuggingFace for solving complex AI tasks through a 4-stage pipeline: Task Planning → Model Selection → Task Execution → Response Generation
2. **EasyTool** (`/easytool/`) - A method for creating concise, structured tool instructions from documentation to improve LLM-based agents
3. **TaskBench** (`/taskbench/`) - A benchmark for evaluating task automation capability of LLMs across three domains

## Environment Setup

### HuggingGPT (Server)
```bash
cd hugginggpt/server
conda create -n jarvis python=3.8
conda activate jarvis
conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
pip install -r requirements.txt
cd models && bash download.sh  # Required for local/hybrid inference mode
```

### HuggingGPT (Web)
```bash
cd hugginggpt/web
npm install
npm run dev
```

### EasyTool
```bash
cd easytool
pip install -r requirements.txt
export OPENAI_API_KEY="your_key"
export RAPIDAPI_KEY="your_key"
```

### TaskBench
```bash
cd taskbench
conda create -n taskbench python=3.8
conda activate taskbench
pip install -r requirements.txt
```

## Running Applications

### HuggingGPT Server (with API endpoints)
```bash
cd hugginggpt/server
python models_server.py --config configs/config.default.yaml
python awesome_chat.py --config configs/config.default.yaml --mode server
```
- Configure `OPENAI_API_KEY` and `HUGGINGFACE_ACCESS_TOKEN` env vars or update `config.default.yaml`
- API endpoints: `/hugginggpt` (full), `/tasks` (Stage 1), `/results` (Stages 1-3)

### HuggingGPT CLI Mode
```bash
cd hugginggpt/server
python awesome_chat.py --config configs/config.default.yaml --mode cli
```

### HuggingGPT Gradio Demo
```bash
cd hugginggpt/server
python models_server.py --config configs/config.gradio.yaml
python run_gradio_demo.py --config configs/config.gradio.yaml
```

### EasyTool Inference
```bash
export OPENAI_API_KEY=""
python main.py --model_name gpt-3.5-turbo --task funcqa --data_type funcqa_mh

python main.py --model_name gpt-3.5-turbo --task toolbench --data_type G2 --tool_root_dir ./toolenv/tools
python main.py --model_name gpt-3.5-turbo --task restbench
```

### TaskBench Inference & Evaluation
```bash
# Generate predictions
export YOUR_API_KEY=API_KEY
python inference.py --llm gpt-4 --data_dir data_multimedia --api_addr localhost --api_port 4000

# Evaluate metrics
python evaluate.py --data_dir data_multimedia --prediction_dir $prediction_dir --llm gpt-4
```

## Architecture Notes

### HuggingGPT Server
- `awesome_chat.py` - Main chat interface (45KB), handles CLI/Server modes
- `models_server.py` - Model inference server (31KB)
- `configs/config.*.yaml` - Configuration files controlling inference mode (`local`/`huggingface`/`hybrid`) and local deployment scale (`minimal`/`standard`/`full`)
- `requirements.txt` - Dependencies include diffusers, transformers, gradio, flask, speechbrain, espnet, etc.

### TaskBench Data Format
Each dataset directory contains:
- `data.json` - Samples
- `graph_desc.json` - Tool graph description
- `user_requests.json` - User requests
- `tool_desc.json` - Tool descriptions

### EasyTool Tasks
Supports: `funcqa`, `toolbench`, `toolbench_retrieve`, `restbench` with various data types (`G2`, `G3`, `funcqa_mh`, `funcqa_oh`)