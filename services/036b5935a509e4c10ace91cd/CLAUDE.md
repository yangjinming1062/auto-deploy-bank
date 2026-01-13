# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Wenda (闻达) is a large-scale language model invocation platform that integrates multiple LLMs (chatGLM, RWKV, LLaMA, etc.) with knowledge bases and web UI. It supports both local model deployment and API-based services, designed for efficient content generation with resource constraints.

## Architecture

### Core Components

1. **Main Entry Point**: `wenda.py`
   - Sets up web server (FastAPI + Bottle)
   - Loads LLM adapter dynamically based on `llm_type` config
   - Loads knowledge base plugin
   - Handles WebSocket connections for chat

2. **LLM Adapters** (`llms/` directory)
   - Each model type has its own adapter: `llm_rwkv.py`, `llm_glm6b.py`, `llm_llama.py`, etc.
   - Adapters implement common interface: `load_model()`, `ask()`, `stream_out()`
   - RWKV has both torch (`llm_rwkv.py`) and C++ (`rwkvcpp/`) implementations
   - Generic transformers adapter supports GPTQ/AWQ quantized models

3. **Plugin System** (`plugins/` directory)
   - `common.py` - Configuration loader, logging, utility functions
   - Knowledge base implementations:
     - `zhishiku_rtst.py` - Sentence transformers + FAISS
     - `zhishiku_fess.py` - FESS search engine
     - `zhishiku_bing.py` - Bing search
     - `zhishiku_qdrant.py` - Qdrant vector database
   - Data generation scripts: `gen_data_st.py`, `gen_data_qdrant.py`

4. **Auto Extensions** (`autos/` directory)
   - JavaScript plugins that extend functionality via browser injection
   - Examples: `0-zsk.js` (knowledge base management), `1-draw_use_SD_api.js` (Stable Diffusion), `QQ.js` (QQ bot)
   - Provides APIs: `send()`, `add_conversation()`, `find()`, `zsk()`, etc.

5. **Frontend** (`views/` directory)
   - Web UI served by Bottle framework
   - `index.html` - Main chat interface
   - Static assets in `views/static/`

### Configuration System

- Main config: `config.yml` (copy from `example.config.yml`)
- Key sections:
  - `logging`, `port`, `library` (knowledge base settings)
  - `llm_type`, `llm_models.<model_type>` (model configuration)
- Runtime overrides via CLI: `-c config.yml -p 17860 -l True -t rwkv`

### Knowledge Base Architecture

Multiple knowledge retrieval strategies:
- **rtst mode**: sentence_transformers + FAISS for semantic search
- **fess mode**: Local FESS search engine
- **bing mode**: Bing web search
- **qdrant mode**: Qdrant vector database
- Configured via `library.strategy`: `"calc:2 rtst:5 agents:0"`

## Common Development Commands

### Installation
```bash
# Install base dependencies
pip install -r requirements/requirements.txt

# Install model-specific dependencies (as needed)
pip install -r requirements/requirements-llama.txt
pip install -r requirements/requirements-glm6b-lora.txt
```

### Running the Application

```bash
# Basic run
python wenda.py

# With custom config and parameters
python wenda.py -c config.yml -p 17860 -t rwkv

# Or use provided scripts for specific models:
bash run_rwkv.sh          # RWKV
bash run_GLM6B.sh         # GLM6B
bash run_chatglm.sh       # ChatGLM
```

### Knowledge Base Operations

```bash
# Build RTST index (Linux)
python plugins/gen_data_st.py

# Build RTST index (Windows)
plugins/buils_rtst_default_index.bat

# Build Qdrant index (Windows)
plugins/build_qdrant_data.bat
```

### Model Quantization (RWKV)

```bash
# Torch quantization
cov_torch_rwkv.bat

# C++ GGML conversion and quantization
cov_ggml_rwkv.bat
```

## Testing Notes

- No formal test suite found
- Models have basic "apitest" references but not pytest/unittest
- Knowledge base debugging available via web UI interface
- Individual components can be tested by running `python wenda.py` with specific model configuration

## Configuration Reference

See `example.config.yml` for complete configuration options. Key points:

- Model paths: `llm_models.<type>.path` (e.g., `model/rwkv-x060-3b-world-v2.pth`)
- Strategy settings: CUDA/quantization options like `"cuda fp16"`, `"Q8_0"`
- Knowledge base models: `model/m3e-base` (recommended over deprecated text2vec-large-chinese)
- Device settings: For embedding models, use `device: cuda` or `device: cpu`

## Model Recommendations

- **RWKV**: RWKV-4-Raven-7B-v11 (good performance/resource balance)
- **GLM**: chatGLM-6B or chatGLM2-6B
- **Embedding**: moka-ai/m3e-base (replaces text2vec-large-chinese)
- **Baichuan**: Use with LoRA for better results

## Development Tips

1. **Adding New LLM**: Create `llm_<name>.py` with `load_model()` and `ask()` functions
2. **Adding Knowledge Base**: Create `zhishiku_<name>.py` implementing search interface
3. **Adding Auto Feature**: Create `.js` file in `autos/` directory with async functions
4. **Configuration**: Always copy from `example.config.yml` and fill in model paths
5. **GPU Memory**: Adjust `state_source_device` for RWKV to save VRAM (set to `cpu`)

## API Endpoints

- POST `/chat/completions` - Chat completions (OpenAI-compatible)
- WebSocket - Real-time streaming chat
- GET `/llm` - LLM-specific JavaScript
- GET `/plugins` - Auto plugins list

## Important Files

- `wenda.py:31-41` - LLM loading logic
- `wenda.py:52-56` - Model loading thread
- `wenda.py:64-79` - Knowledge base loading thread
- `plugins/common.py:13-80` - Configuration loading and parsing
- `plugins/zhishiku_rtst.py` - RTST implementation
- `llms/llm_rwkv.py` - RWKV adapter (most mature implementation)