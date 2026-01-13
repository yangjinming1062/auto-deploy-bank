# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains **two main components**:

1. **TigerBot** - A family of large language models (7B, 13B, 70B, 180B parameters) with training, inference, and fine-tuning capabilities
2. **OpenCompass** - A comprehensive evaluation platform for LLM benchmarking, integrated into this repository under `/opencompass/`

## Environment Setup

### OpenCompass Installation

```bash
# Create conda environment
conda create --name opencompass python=3.10 pytorch torchvision pytorch-cuda -c nvidia -c pytorch -y
conda activate opencompass

# Install OpenCompass
cd opencompass
pip install -e .

# Download datasets
wget https://github.com/InternLM/opencompass/releases/download/0.1.0/OpenCompassData.zip
unzip OpenCompassData.zip
```

### TigerBot Installation

```bash
# From repository root
conda create --name tigerbot python=3.8
conda activate tigerbot
conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia

pip install -r requirements.txt
```

## Common Commands

### TigerBot Inference

```bash
# CLI inference (interactive)
python infer.py --model_path tigerbot-13b-chat --max_input_length 1024 --max_generate_length 1024

# Web demo
export PYTHONPATH='./' && export CUDA_VISIBLE_DEVICES=0
streamlit run apps/web_demo.py -- --model_path tigerbot-13b-chat

# ExLlamaV2 web demo (for quantized models)
streamlit run apps/exllamav2_web_demo.py -- --model_path TigerResearch/tigerbot-70b-chat-v4-4bit-exl2

# Quantized inference
python other_infer/quant_infer.py --model_path ${MODEL_DIR} --wbit 8
```

**Key Parameters:**
- `--model_path`: Model repository or path
- `--model_type`: 'chat' or 'base'
- `--max_input_length`: Maximum input tokens (default: 1024)
- `--max_generate_length`: Maximum generation length (default: 1024)
- `--rope_scaling`: Length extrapolation method ('yarn' or 'dynamic')
- `--rope_factor`: Extrapolation factor (default: 8.0)

### TigerBot Training

**Prerequisites:** Install DeepSpeed with GPU architecture support

```bash
# Install DeepSpeed
git clone git@github.com:microsoft/DeepSpeed.git
cd DeepSpeed
rm -rf build
TORCH_CUDA_ARCH_LIST="8.0" DS_BUILD_CPU_ADAM=1 DS_BUILD_UTILS=1 pip install . \
  --global-option="build_ext" --global-option="-j8" --no-cache -v \
  --disable-pip-version-check
```

**Pre-training (CLM):**
```bash
deepspeed \
  --include="localhost:0,1,2,3" \
  ./train_clm.py \
  --deepspeed ./ds_config/ds_config_zero3.json \
  --model_name_or_path TigerResearch/tigerbot-7b-base \
  --dataset_name TigerResearch/dev_pretrain \
  --do_train \
  --output_dir ./ckpt-clm \
  --overwrite_output_dir \
  --num_train_epochs 5 \
  --learning_rate 1e-5 \
  --bf16 True \
  --per_device_train_batch_size 2
```

**SFT (Instruction Fine-tuning):**
```bash
deepspeed \
  --include="localhost:0,1,2,3" \
  ./train_sft.py \
  --deepspeed ./ds_config/ds_config_zero3.json \
  --model_name_or_path TigerResearch/tigerbot-7b-base \
  --dataset_name TigerResearch/dev_sft \
  --do_train \
  --output_dir ./ckpt-sft \
  --num_train_epochs 5 \
  --learning_rate 1e-5 \
  --bf16 True \
  --per_device_train_batch_size 2
```

**QLoRA Fine-tuning (single GPU):**
```bash
python train_with_qlora.py \
  --model_name_or_path TigerResearch/tigerbot-7b-base \
  --data_pathTigerResearch/dev_sft \
  --output_dir ./ckpt-qlora \
  --per_device_train_batch_size 4
```

### OpenCompass Evaluation

```bash
# From opencompass directory
cd opencompass

# Debug mode (sequential execution)
python run.py configs/eval_demo.py -w outputs/demo --debug

# Parallel evaluation
python run.py configs/eval_demo.py -w outputs/demo

# Evaluate TigerBot model
python run.py configs/eval_tigerbot_13b.py -w outputs/tigerbot-13b-base

# Specific evaluation modes
python run.py configs/eval_demo.py --mode infer  # Only inference
python run.py configs/eval_demo.py --mode eval   # Only evaluation
python run.py configs/eval_demo.py --mode viz    # Visualize results
```

**Key Options:**
- `-w, --work-dir`: Output directory for results
- `-m, --mode`: 'all', 'infer', 'eval', or 'viz'
- `--debug`: Run in debug mode (sequential, logs to console)
- `--dry-run`: Show commands without executing
- `--slurm`: Run on SLURM cluster
- `--dlc`: Run on Alibaba Cloud DLC
- `-r, --reuse`: Reuse previous results

## Code Style and Quality

The codebase follows **PEP8** standards and uses:

- **flake8**: Linting
- **yapf**: Code formatting
- **isort**: Import sorting
- **codespell**: Spell checking
- **mdformat**: Markdown formatting
- **docformatter**: Docstring formatting

### Pre-commit Hook

```bash
pip install -U pre-commit
pre-commit install
```

After installation, the hook automatically runs on every commit to check and format code.

### Running Tests

```bash
# Run all tests (from opencompass directory)
pytest tests/

# Run specific test file
pytest tests/openicl/test_prompt_template.py

# Run with coverage
pytest --cov=opencompass tests/
```

## High-Level Architecture

### TigerBot Structure

```
/
├── apps/                      # Applications (web demo, etc.)
├── infer.py                   # Main inference script for TigerBot
├── other_infer/               # Alternative inference methods (quantization)
├── train/                     # Training scripts
│   ├── train_clm.py          # Pre-training (Causal LM)
│   ├── train_sft.py          # Instruction fine-tuning
│   ├── train_with_qlora.py   # QLoRA fine-tuning
│   └── ds_config/            # DeepSpeed configurations
├── utils/                     # Utility modules
│   ├── modeling_hack.py      # Model loading utilities
│   └── streaming.py          # Streaming generation
└── requirements.txt           # TigerBot dependencies
```

### OpenCompass Structure

```
opencompass/
├── run.py                     # Main entry point for evaluation
├── setup.py                   # Package installation
├── opencompass/
│   ├── models/                # Model implementations
│   │   ├── huggingface.py    # HuggingFace models
│   │   ├── openai_api.py     # OpenAI API models
│   │   ├── base.py           # Base model interface
│   │   └── ...
│   ├── datasets/             # Dataset implementations (60+ datasets)
│   │   ├── mmlu.py          # MMLU benchmark
│   │   ├── gsm8k.py         # GSM8K math
│   │   ├── humaneval.py     # Code evaluation
│   │   └── ...
│   ├── openicl/              # In-Context Learning framework
│   │   ├── icl_inferencer/   # Inference strategies
│   │   ├── icl_evaluator/    # Evaluation methods
│   │   ├── icl_retriever/    # Retrieval strategies
│   │   └── icl_prompt_template.py
│   ├── tasks/                # Task definitions
│   │   ├── openicl_infer.py  # Inference tasks
│   │   ├── openicl_eval.py   # Evaluation tasks
│   │   └── llm_eval.py       # LLM evaluation tasks
│   ├── partitioners/         # Task partitioning strategies
│   ├── runners/              # Execution backends (local, SLURM, DLC)
│   └── utils/                # Utilities
├── configs/                   # Evaluation configurations
│   ├── eval_*.py             # Model evaluation configs
│   ├── models/               # Model configurations
│   ├── datasets/             # Dataset configurations
│   └── summarizers/          # Result summarizers
└── tests/                     # Unit tests
```

### Key Design Patterns

1. **OpenCompass Configuration System**
   - Uses `mmengine.config` for hierarchical configuration
   - Configs are composable via `read_base()`
   - Example: `configs/eval_tigerbot_13b.py` imports models and datasets separately

2. **Model Abstraction**
   - Base class in `opencompass/models/base.py`
   - HuggingFace models: `HuggingFaceCausalLM`
   - API models: `OpenAIAPI`, `OpenAIChatAPI`
   - Each model implements standard inference interface

3. **Evaluation Paradigms**
   - **PPL (Perplexity)**: Discriminative tasks (classification, multiple choice)
   - **GEN (Generation)**: Generative tasks (open-ended问答, code generation)
   - Defined per dataset in `configs/datasets/*/`

4. **Distributed Execution**
   - Task partitioning based on dataset size
   - Support for local, SLURM, and DLC runners
   - Automatic retry and failure handling

5. **TigerBot Model Loading**
   - Custom `get_model()` function in `utils/modeling_hack.py`
   - Supports base/chat models with different prompt formats
   - Handles RoPE scaling for long context

## Important Files to Know

### TigerBot
- **infer.py**: Main TigerBot inference entry point
- **utils/modeling_hack.py**: Model loading and initialization
- **utils/streaming.py**: Streaming generation utilities
- **train/train_clm.py**: Pre-training script
- **train/train_sft.py**: SFT fine-tuning script
- **train/train_with_qlora.py**: QLoRA fine-tuning (memory-efficient)

### OpenCompass
- **opencompass/run.py**: Main evaluation orchestrator
- **opencompass/openicl/**: In-context learning core
- **opencompass/models/huggingface.py**: HuggingFace model integration
- **opencompass/datasets/**: Individual dataset implementations
- **configs/eval_*.py**: Ready-to-use evaluation configs
- **opencompass/tasks/openicl_infer.py**: Inference task logic
- **opencompass/tasks/openicl_eval.py**: Evaluation task logic

## Development Notes

### Adding New Datasets

1. Create dataset file in `opencompass/opencompass/datasets/`
2. Implement dataset class following existing patterns
3. Create config in `opencompass/configs/datasets/[dataset_name]/`
4. Export dataset list in config's `__init__.py`

### Adding New Models

1. Create model class in `opencompass/opencompass/models/`
2. Inherit from `BaseModel`
3. Implement required methods: `get_ppl()`, `get_gen()`
4. Add model config in `opencompass/configs/models/`

### Memory Requirements

- **TigerBot-7B**: 1x A100 40GB minimum
- **TigerBot-13B**: 1x A100 40GB minimum
- **TigerBot-70B**: 4x A100 40GB minimum
- **TigerBot-180B**: 16x A100 40GB minimum
- **QLoRA fine-tuning**: Single RTX 3090 possible

## Configuration System

OpenCompass uses a hierarchical configuration system:

```python
# Example: configs/eval_tigerbot_13b.py
from mmengine.config import read_base

with read_base():
    # Import model configuration
    from .models.hf_tigerbot_13b_base import models

    # Import dataset configurations
    from .datasets.humaneval.humaneval_gen import humaneval_datasets
    from .datasets.gsm8k.gsm8k_gen import gsm8k_datasets

    # Combine datasets
    datasets = [*humaneval_datasets, *gsm8k_datasets]
```

This system allows easy composition and reuse of configurations across different evaluation scenarios.