# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

h2oGPT is an Apache V2 open-source large language model (LLM) platform by H2O.ai that provides a **private, offline chatbot with document querying capabilities**. It supports multiple models (LLaMa2, Mistral, Falcon, Vicuna, WizardLM) with GPTQ, 4-bit/8-bit quantization, and LoRA fine-tuning. Features include a Gradio UI, CLI, and OpenAI-compliant API proxy.

## Common Commands

### Development Setup
```bash
# Create virtual environment
make venv

# Install dependencies (installs main requirements + all optional extras)
pip install -e .

# Install from wheel
make install

# Install specific extras (cpu, cuda, training, etc.)
pip install -e .[cpu]    # CPU-only dependencies
pip install -e .[cuda]   # GPU dependencies
pip install -e .[TRAINING]  # Fine-tuning dependencies
pip install -e .[WIKI_EXTRA]  # Wikipedia processing
```

### Building & Packaging
```bash
# Build Python wheel
make clean dist
# or
python setup.py bdist_wheel

# Build Docker images
make docker_build

# Push to container registry
make docker_push
```

### Testing
```bash
# Run all tests (excludes tests requiring tokens or GPU by default)
make test

# Run import tests only
make test_imports

# Run specific test file
pytest tests/test_langchain_units.py -s -v

# Run full test suite including GPU tests
GPT_H2O_AI=0 CONCURRENCY_COUNT=1 pytest --instafail -s -v tests

# Run OpenAI server tests (requires running local server)
pytest -s -v -n 4 openai_server/test_openai_server.py::test_openai_client

# Run tests on 4 GPUs
bash tests/test4gpus.sh
```

**Test markers:**
- `need_tokens` - tests requiring API tokens or external services
- `need_gpu` - tests requiring GPU hardware

### Running the Application

**CLI Entrypoints:**
```bash
h2ogpt_finetune    # Fine-tuning CLI (setup.py entry point)
h2ogpt_generate    # Generation CLI (setup.py entry point)

# Or directly:
python generate.py --base_model=... --prompt_type=chat
```

**Application Modes:**
```bash
# CLI chat mode
python generate.py --base_model=h2oai/h2ogpt-70b --prompt_type=chat

# Gradio UI
python gradio_runner.py
# or
python generate.py --base_model=... --gradio=True --share=False

# OpenAI API proxy server
python openai_server/server.py
```

## High-Level Architecture

The codebase follows a modular architecture with these key components:

### Core Package (h2ogpt/)

**Entry Points:**
- `generate.py` → `src.gen:main()` (line 113) - Main CLI entry point
- `finetune.py` → `h2ogpt.finetune:entrypoint_main` - Fine-tuning CLI
- `gradio_runner.py` - Gradio web UI launcher (40,000+ LOC)

**Main Components:**
- **gen.py** (~306KB) - Core generation logic, prompt handling, model orchestration
- **gradio_runner.py** (~443KB) - Gradio UI implementation with streaming, voice, vision
- **model_utils.py** (~94KB) - Model loading, inference server integration, client management
- **gpt_langchain.py** (~497KB) - LangChain document processing and Q/A
- **prompter.py** (~130KB) - Prompt templates and formatting
- **utils.py** - General utilities
- **eval.py** - Evaluation and reward model functions
- **db_utils.py** - Database utilities for document stores

**Specialized Modules:**
- `llm_exllama.py` - ExLLaMa integration
- `gpt4all_llm.py` - GPT4All integration
- `image_*.py` - Image processing and generation (Stable Diffusion, SDXL, etc.)
- `audio_langchain.py`, `stt.py`, `tts.py` - Speech-to-text and text-to-speech
- `vision/` - Vision model support (LLaVa, Claude-3, GPT-4-Vision)

### API Server (openai_server/)

- **server.py** - FastAPI-based OpenAI-compliant REST API
  - Chat completions (streaming and non-streaming)
  - Embedding generation
  - Function tool calling with auto-selection
  - Audio transcription (STT) and generation (TTS)
  - Image generation
  - Authentication and state preservation
- **client_test.py** - Client integration tests
- **test_*.py** - Comprehensive test suites

### Supporting Directories

- **src/** - Redirect/symlink to actual source location (h2ogpt/)
- **tests/** - 40+ test files covering unit, integration, GPU, and API tests
- **docs/** - Comprehensive documentation (20+ files)
- **gradio_utils/** - Gradio UI utilities and components
- **spaces/** - Hugging Face Spaces configuration
- **models/** - Model-related utilities
- **reqs_optional/** - Optional dependency groups by feature
- **ci/** - GitHub Actions and Jenkins CI/CD configs
- **helm/** - Kubernetes Helm chart for deployment
- **cloud/** - Cloud deployment configurations

### Key Dependencies

**Core:** gradio==4.44.0, torch, transformers>=4.45.1, accelerate, peft, bitsandbytes
**Training:** loralib, datasets, sentencepiece, einops
**Databases:** chromadb, weaviate, faiss (optional extras)
**Audio:** whisper (STT), multiple TTS engines
**Testing:** pytest, pytest-xdist, evaluate, rouge_score, sacrebleu

### Key Integration Points

- **Inference Servers:** vLLM, HF TGI, oLLaMa, ExLLaMa, OpenAI, Anthropic, Google, MistralAI, Groq
- **Databases:** Chroma (persistent), Weaviate, FAISS (in-memory)
- **Models:** LLaMa2, Mistral, Falcon, Vicuna, WizardLM, LLaVa (vision), Stable Diffusion, GPT-4-Vision
- **Document Formats:** 20+ types (PDF, Excel, Word, Images, Video, Audio, Code, Text, Markdown)
- **Features:** HYDE retrieval, semantic chunking, parallel summarization, attention sinks

## Testing Strategy

**Framework:** pytest with pytest-xdist for parallel execution (up to 4+ processes)

**Test Coverage:**
- Unit tests for individual components (40+ test files)
- Integration tests for full workflows
- Tests for different model backends and inference servers
- LangChain document processing tests
- OpenAI API proxy server tests
- Speech/Audio processing tests
- Performance benchmarks
- Multi-GPU tests (see `tests/test4gpus.sh`)

**Specialized Test Commands:**
```bash
# Install test dependencies
pip install requirements-parser pytest-instafail pytest-random-order playsound==1.3.0

# Ubuntu/Debian audio testing
sudo apt-get install gstreamer-1.0
# Or conda
conda install -c conda-forge gst-python -y
```

## Development Environment Setup

See `docs/INSTALL.md` for detailed GPU setup instructions.

**Prerequisites:**
- Python 3.10+
- CUDA 11.8+ or 12.1+ for GPU support
- For A100/H100 systems: NVIDIA GPU Manager and Fabric Manager

**Quick Setup:**
```bash
# Create venv and install
make venv
pip install -e .  # Installs all dependencies

# Optional: Install specific extras
pip install -e .[cpu,cuda,TRAINING]
```

## Version & Build Information

- **Version:** Read from `version.txt` (current: 0.2.1)
- **Build System:** Python wheel via `python setup.py bdist_wheel`
- **CI/CD:**
  - GitHub Actions: Python wheel publishing to PyPI
  - Jenkins: Multi-stage pipeline (see `ci/jenkinsfile`)
  - Docker: Multi-stage build (CUDA 12.1, Ubuntu 20.04)

**Makefile Targets:**
```bash
make venv          # Create virtual environment
make clean         # Clean build artifacts
make dist          # Build Python wheel
make install       # Install from wheel
make test          # Run test suite (excludes GPU/token tests)
make test_imports  # Test imports only
make docker_build  # Build Docker images
make docker_push   # Push to GCR
```

## Configuration Files

- **requirements.txt** - Core dependencies (gradio, torch, transformers, etc.)
- **reqs_optional/** - Optional dependency groups:
  - `requirements_optional_*.txt` - Feature-specific deps (agents, audio, GPU, training, etc.)
  - `requirements_optional_langchain*.txt` - Document processing extras
- **Makefile** - Build automation and common tasks
- **Dockerfile** - Multi-stage Docker build (CUDA 12.1, Ubuntu 20.04)
- **docker-compose.yml** - Service orchestration
- **setup.py** - Package configuration with entry points

## Important Implementation Notes

1. **Environment Variables** - Extensive use of env vars (HF_HUB_* for model downloads, CUDA settings, authentication, etc.)

2. **Model Locking** - Uses `filelock` for managing concurrent model access

3. **Torch Settings** - Aggressive thread limiting to avoid resource contention on multi-GPU systems

4. **Optional Dependencies** - Heavy use of optional/extra dependencies - check `reqs_optional/` for feature-specific requirements

5. **Platform Support** - Linux (full), macOS (limited), Windows (limited), Docker (full capability)

6. **Performance** - Parallel processing throughout (document ingestion, summarization, generation)

## Key Documentation

- **README.md** - Main project overview and quick start
- **docs/INSTALL.md** - Development environment setup with GPU drivers
- **docs/FAQ.md** - Common issues, troubleshooting, and usage tips
- **docs/README_ui.md** - Gradio UI documentation
- **docs/README_CLIENT.md** - OpenAI-compliant API client docs
- **docs/README_LangChain.md** - Document processing integration
- **docs/README_InferenceServers.md** - Inference server support (vLLM, TGI, etc.)
- **docs/FINETUNE.md** - Fine-tuning instructions
- **docs/README_*.md** - Platform-specific guides (Linux, Windows, macOS, Docker)