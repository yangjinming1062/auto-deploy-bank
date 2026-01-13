# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MaxText is a high-performance, highly scalable, open-source LLM library written in pure Python/JAX, targeting Google Cloud TPUs and GPUs for training. It provides reference implementations of popular models (Gemma, Llama, DeepSeek, Qwen, Mistral, GPT-OSS) with support for pre-training (up to tens of thousands of chips) and scalable post-training (SFT, GRPO/GSPO).

## Quick Start

### Installation

```bash
# Install in development mode
pip install -e .

# Install with TPU dependencies
pip install -e ".[tpu]"

# Install with CUDA 12 dependencies
pip install -e ".[cuda12]"
```

### Running Training

```bash
# Basic training
python3 src/MaxText/train.py --config=src/MaxText/configs/base.yml --base_output_directory=gs://your-bucket/ --run_name=your-run

# Train a specific model
python3 src/MaxText/train.py --config=src/MaxText/configs/models/llama2-7b.yml --model_name=llama2 --base_output_directory=gs://your-bucket/ --run_name=llama2-7b
```

### Running Inference/Decoding

```bash
# Decode with a prompt
python3 src/MaxText/decode.py --config=src/MaxText/configs/inference.yml --model_name=llama2 --prompt="Your prompt here" --load_parameters_path=gs://your-bucket/checkpoints/1000
```

### Running Tests

```bash
# Run all tests
python3 -m pytest

# Run CPU-only tests
python3 -m pytest -m cpu_only

# Run TPU-only tests
python3 -m pytest -m tpu_only

# Run GPU-only tests
python3 -m pytest -m gpu_only

# Run integration tests
python3 -m pytest -m integration_test

# Run a specific test file
python3 -m pytest tests/attention_test.py

# Run with verbose output
python3 -m pytest -v

# Skip scheduled-only tests
python3 -m pytest -m "not scheduled_only"
```

### Code Quality & Linting

```bash
# Run pre-commit hooks on all files
pre-commit run --all-files

# Run only pylint
pylint src/MaxText/

# Format code with pyink
pyink --pyink-indentation=2 --line-length=122 src/MaxText/
```

## High-Level Architecture

### Core Components

**Entry Points:**
- `src/MaxText/train.py` - Main training script for pre-training and post-training
- `src/MaxText/decode.py` - Main inference/decode script
- `src/MaxText/maxengine.py` - Core inference engine implementing JetStream Engine API
- `src/MaxText/maxengine_server.py` - Server for serving models

**Model Layer Architecture (`src/MaxText/layers/`):**
- `models.py` - Top-level Transformer model definition (`TransformerLinenPure`)
- `decoders.py` - Decoder layers and transformer blocks
- `attentions.py` - Attention implementations (dot product, flash, chunked, MLA)
- `embeddings.py` - Token embeddings and positional encodings
- `encoders.py` - Vision encoders for multimodal models
- `linears.py` - Linear layers with quantization support
- `moe.py` - Mixture of Experts implementations
- `multi_token_prediction.py` - MTP auxiliary loss layer
- Model family implementations:
  - `llama2.py`, `llama4.py` - Llama architectures
  - `gemma.py`, `gemma2.py`, `gemma3.py` - Gemma architectures
  - `deepseek.py` - DeepSeek architectures
  - `qwen3.py` - Qwen3 architectures
  - `mixtral.py` - Mixtral architectures
  - `gpt3.py`, `gpt_oss.py` - GPT architectures
  - `mistral.py` - Mistral architectures

**Key Infrastructure:**
- `pyconfig.py` - YAML-based configuration system with parameter merging
- `sharding.py` - Model and tensor sharding for distributed training
- `checkpointing.py` - Orbax-based checkpointing with multi-tier support
- `max_utils.py` - Core utilities (cross-entropy, device mesh, etc.)
- `maxtext_utils.py` - JAX-specific utilities and helpers
- `train_utils.py` - Training utilities (optimizer setup, learning rate schedules)

**Data Input Pipeline (`input_pipeline/`):**
- TFDS pipeline support (`tfds_input_pipeline.py`)
- HuggingFace dataset support (`hf_input_pipeline.py`)
- Grain data loader (`grain_input_pipeline.py`)
- Pre-tokenized data support

**Post-Training:**
- `sft_trainer.py` - Supervised Fine-Tuning
- `rl/` - Reinforcement Learning (GRPO/GSPO)
- `dpo_utils.py` - Direct Preference Optimization
- `rl/train_rl.py` - RL training entry point

**Inference:**
- `inference/` - Inference utilities and JetStream integration
- `inference_utils.py` - General inference utilities
- `decode_multi.py` - Multi-stream decoding

**Quantization & Optimization:**
- `layerwise_quantization.py` - Post-training quantization
- `quantizations.py` - Quantization configuration
- `vocabulary_tiling.py` - Memory optimization for vocabulary operations

### Configuration System

MaxText uses a hierarchical YAML-based configuration system:

1. **Base config** (`src/MaxText/configs/base.yml`) - Contains all possible parameters with defaults
2. **Model-specific configs** (`src/MaxText/configs/models/`) - Model architecture parameters
3. **Task configs** - Training tasks (SFT, RL, DPO)
4. **Hardware configs** - Hardware-specific optimizations (v4, v5e, v5p, v6e, trillium)
5. **Command-line overrides** - Parameters can be overridden via CLI

Key configuration files:
- `base.yml` - Main configuration template
- `inference.yml` - Inference configuration
- `sft.yml`, `dpo.yml`, `rl.yml` - Post-training configurations
- `gpu_smoke_test.yml`, `tpu_smoke_test.yml` - Smoke test configs
- `models/` - Individual model configurations

### JAX Ecosystem Integration

MaxText integrates with Google's JAX AI libraries:
- **Flax** - Neural network library (model definitions)
- **Orbax** - Checkpointing and parameter management
- **Optax** - Optimization (AdamW, SGD)
- **Grain** - High-performance data loading
- **Tunix** - Post-training framework

### Parallelism & Sharding

MaxText supports multiple parallelism strategies:
- **Data Parallelism (DP)** - Batch splitting across devices
- **Tensor Parallelism (TP)** - Sharding individual tensors
- **Pipeline Parallelism (PP)** - Layer pipelining across stages
- **Expert Parallelism (EP)** - Distributing experts in MoE models
- **Context Parallelism** - Sequence-level sharding
- **Shardy/GSPMD** - Automatic sharding via JAX

The `data_sharding` parameter controls how tensors are partitioned across mesh axes (`['data', 'stage', 'fsdp', 'fsdp_transpose', 'sequence', 'context', 'expert']`).

### Checkpointing

Uses Orbax for robust checkpointing:
- **Async/Sync modes** - Configurable via `async_checkpointing`
- **Multi-tier checkpointing** - Local + GCS for fast recovery
- **Parameter-only checkpoints** - For inference loading
- **Full state checkpoints** - Include optimizer state for resumption
- **Format conversion** - Support for HF/Safetensors conversion

## Common Development Tasks

### Adding a New Model

1. Create model layer implementation in `src/MaxText/layers/`
2. Add model config in `src/MaxText/configs/models/`
3. Update `src/MaxText/layers/models.py` to register the model
4. Add tests in `tests/`
5. Update documentation

### Running End-to-End Tests

```bash
# TPU end-to-end test
python3 -m pytest tests/train_smoke_test.py -m tpu_only

# GPU end-to-end test
python3 -m pytest tests/train_gpu_smoke_test.py -m gpu_only

# Integration tests
python3 -m pytest tests/ -m integration_test
```

### Debugging Training Issues

```bash
# Enable detailed logging
python3 src/MaxText/train.py --config=... --jax_debug_log_modules=jax

# Profile training
python3 src/MaxText/train.py --config=... --profiler=xplane --profiler_steps=5

# Enable stack trace collection
python3 src/MaxText/train.py --config=... --collect_stack_trace=True

# Compile ahead of time
python3 src/MaxText/train_compile.py --config=... --compile_topology=v5e-256
```

### Working with Checkpoints

```bash
# Load parameters for inference
python3 src/MaxText/decode.py --config=... --load_parameters_path=gs://bucket/checkpoint/

# Convert checkpoint formats
python3 src/MaxText/utils/ckpt_conversion/to_huggingface.py --src_path=gs://bucket/checkpoint/ --dst_path=./hf_model/

# Generate parameter-only checkpoint
python3 src/MaxText/generate_param_only_checkpoint.py --config=... --load_full_state_path=gs://bucket/checkpoint/
```

## Important Environment Variables

- `XLA_PYTHON_CLIENT_MEM_fraction` - JAX memory usage limit (e.g., "0.75")
- `TF_FORCE_GPU_ALLOW_GROWTH` - Allow GPU memory growth ("true"/"false")
- `LIBTPU_INIT_ARGS` - TPU initialization flags
- `DECOUPLE_GCLOUD` - Run in decoupled mode without GCP dependencies
- `JAX_CACHE_DIR` - JAX compilation cache directory

## Key Files & Directories

- **Source:** `src/MaxText/` - Main codebase
- **Tests:** `tests/` - Unit and integration tests
- **Configs:** `src/MaxText/configs/` - YAML configuration files
- **Benchmarks:** `benchmarks/` - Performance benchmarking tools
- **Docs:** `docs/` - Documentation (Sphinx/Markdown)
- **End-to-end:** `end_to_end/` - End-to-end example scripts
- **Dependencies:** `dependencies/` - Dockerfiles and requirements
- **Tools:** `tools/` - Utility scripts

## Pre-commit Hooks

The repository uses pre-commit hooks for code quality:
- **codespell** - Spell checking
- **pylint** - Static analysis (configured via `pylintrc`)
- **pyink** - Code formatting (2-space indent, 122 char line length)

Install and activate:
```bash
pip install pre-commit
pre-commit install
```

## CI/CD

GitHub Actions workflows (`.github/workflows/`):
- **RunTests.yml** - Main test workflow (TPU/GPU/CPU)
- **build_and_test_maxtext.yml** - Build and test pipeline
- **CodeQuality.yml** - Code quality checks

Tests are categorized by markers:
- `cpu_only`, `tpu_only`, `gpu_only` - Hardware-specific tests
- `integration_test` - End-to-end integration tests
- `scheduled_only` - Tests run only on schedule
- `external_*` - Tests requiring external services

## Python Version & Dependencies

- **Python:** 3.12+ (officially supported)
- **Build system:** hatchling (configured in `pyproject.toml`)
- **Dependencies:** Located in `dependencies/requirements/generated_requirements/`
  - `tpu-requirements.txt` - TPU dependencies
  - `cuda12-requirements.txt` - CUDA 12 dependencies

## Documentation

- **Main docs:** https://maxtext.readthedocs.io
- **Local build:** `cd docs && sphinx-build -b html . _build/html`
- **Tutorials:** `docs/tutorials/` - Getting started guides
- **Guides:** `docs/guides/` - Detailed guides for various features
- **Reference:** `docs/reference/` - API and architecture reference

## Model Families Supported

MaxText implements reference JAX versions of popular models:
- **Google:** Gemma (1, 2, 3) - 2B to 27B parameters
- **Alibaba:** Qwen3 (Dense 0.6B-32B, MoE 30B-480B)
- **DeepSeek:** V2 (16B, 236B), V3/R1 (671B)
- **Meta:** Llama 2/3/3.1/3.3/4 - 7B to 405B (including Maverick 400B)
- **OpenAI:** GPT-OSS (20B, 120B), GPT3 variants
- **Mistral:** Mistral (7B), Mixtral (8x7B, 8x22B)
- **Multimodal:** Gemma 3, Llama 4 Vision models

## Performance Features

- **Ahead-of-time compilation** - Pre-compile for faster startup
- **Quantization** - INT8, FP8, mixed precision support
- **Vocabulary tiling** - Memory optimization for large vocabularies
- **Ragged attention** - Efficient long sequence handling
- **Paged attention** - Memory-efficient KV cache management
- **Multi-Token Prediction (MTP)** - Auxiliary loss for training efficiency
- **Custom kernels** - JAX/Flax-optimized attention implementations