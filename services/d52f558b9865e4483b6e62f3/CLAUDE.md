# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LLamaTuner is an efficient, flexible, and full-featured toolkit for fine-tuning Large Language Models (LLMs) including Llama3, Phi3, Qwen, Mistral, and many others. It supports various fine-tuning methods (LoRA, QLoRA, full fine-tuning, freeze tuning) and training stages (pre-training, SFT, reward modeling, PPO, DPO, KTO, ORPO).

## Development Commands

### Installation
```bash
pip install -r requirements.txt
```

### Training (using CLI)
```bash
# Single GPU training
llamatuner-cli train --model_name_or_path meta-llama/Llama-2-7b-hf --dataset alpaca --template llama2 --output_dir work_dir/lora

# Multi-GPU distributed training (auto-selected for >1 GPU)
llamatuner-cli train --model_name_or_path meta-llama/Llama-2-7b-hf --dataset alpaca --template llama2 --output_dir work_dir/lora

# Force torchrun for multi-GPU
FORCE_TORCHRUN=1 llamatuner-cli train --model_name_or_path meta-llama/Llama-2-7b-hf --dataset alpaca --template llama2

# Using DeepSpeed
torchrun --nnodes 1 --nproc_per_node 4 --master_port 29500 llamatuner/train/sft/train_lora.py --deepspeed examples/deepspeed/ds_z2_config.json ...
```

### Using Configuration Files
```bash
# YAML config
llamatuner-cli train config.yaml

# JSON config
llamatuner-cli train config.json
```

### Training Stages (`--stage`)
- `pt`: Pre-training (causal language modeling)
- `sft`: Supervised Fine-Tuning (instruction following)
- `rm`: Reward Modeling (preference pairs)
- `ppo`: PPO (Reinforcement Learning from Human Feedback)
- `dpo`: Direct Preference Optimization
- `kto`: Kahneman-Tversky Optimization
- `orpo`: Odds Ratio Preference Optimization

### Fine-tuning Methods (`--finetuning_type`)
- `lora`: Low-Rank Adaptation (memory-efficient)
- `full`: Full parameter fine-tuning
- `freeze`: Partial-parameter freezing (train only specific layers)

### Quantization Options
- `--use_qlora`: Enable QLoRA with 4-bit/8-bit quantization
- `--quant_bit 4`: 4-bit quantization (via bitsandbytes)
- `--quant_bit 8`: 8-bit quantization
- `--quant_type nf4` or `fp4`: NF4 or FP4 data type

### Example Training Scripts
```bash
# QLoRA fine-tuning (scripts/qlora_finetune/qlora-finetune.sh)
python llamatuner/train/sft/train_lora.py \
    --model_name_or_path facebook/opt-125m \
    --dataset alpaca \
    --use_qlora \
    --output_dir work_dir/lora-finetune

# Full fine-tuning with DeepSpeed
bash scripts/full_finetune/full-finetune_ds.sh

# LoRA fine-tuning
bash scripts/lora_finetune/lora-finetune.sh
```

### DeepSpeed ZeRO Stages
- **Stage 0**: No optimization (DDP only)
- **Stage 1**: ZeRO optimizer state partitioning
- **Stage 2**: + gradient partitioning
- **Stage 3**: + parameter partitioning (requires `--force_torchrun`)

### Code Quality
```bash
# Run pre-commit hooks
pre-commit run --all-files

# Install pre-commit hooks
pre-commit install
```

## Architecture

### Core Modules

**`llamatuner/cli.py`**: Entry point for CLI commands. Supports `train`, `env`, `version`, `help` commands. Automatically uses `torchrun` for multi-GPU training or when `FORCE_TORCHRUN=1`.

**`llamatuner/launcher.py`**: Entry point for distributed training via torchrun. Receives args from CLI and calls `run_exp()`.

**`llamatuner/train/tuner.py`**: Main training dispatcher. Routes to appropriate training pipeline based on `stage` argument (`pt`/`sft`/`rm`/`ppo`/`dpo`/`kto`/`orpo`).

**`llamatuner/configs/parser.py`**: Argument parsing using Hugging Face `HfArgumentParser`. Supports YAML/JSON config files. Key argument classes:
- `ModelArguments`: Model path, adapters, quantization settings
- `DataArguments`: Dataset, template, cutoff length, packing
- `FinetuningArguments`: Stage, method, LoRA/quantization/RLHF config
- `GeneratingArguments`: Inference settings (max tokens, temperature, etc.)
- `EvaluationArguments`: Evaluation settings for benchmarking

**`llamatuner/configs/`**: Configuration dataclasses:
- `model_args.py`: Model loading, quantization, device settings
- `data_args.py`: Dataset paths, templates, cutoff length, streaming
- `finetuning_args.py`: Stage, finetuning type, LoRA/quant/RLHF hyperparameters
- `eval_args.py`: Evaluation batch size, tasks, few-shot settings
- `generating_args.py`: Generation config for inference

### Training Pipelines

**`llamatuner/train/sft/`**: SFT implementations:
- `train_full.py`: Full parameter fine-tuning (supports DeepSpeed)
- `train_lora.py`: LoRA/QLoRA fine-tuning with bitsandbytes quantization

**`llamatuner/train/pt/`**: Pre-training (`train_pt.py`)

**`llamatuner/train/rm/`**: Reward modeling (`trainer.py`)

**`llamatuner/model/callbacks/`**: Custom callbacks:
- `save_peft_model_callback.py`: Saves adapters properly
- `wandb_callback.py`: Weights & Biases logging
- `metrics.py`: ComputeMetrics for generation evaluation
- `perplexity.py`: PPL computation for language modeling

### Model Architecture Support

**Default LoRA targets** (`--lora_target`):
- LLaMA/Llama2/Llama3: `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`
- BLOOM/Falcon/ChatGLM: `query_key_value`, `dense`, `dense_h_to_4h`, `dense_4h_to_h`
- Baichuan: `W_pack`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`
- Qwen: `c_attn`, `attn.c_proj`, `w1`, `w2`, `mlp.c_proj`
- InternLM2: `wqkv`, `wo`, `w1`, `w2`, `w3`
- Use `--lora_target all` to auto-detect all linear modules

### Data Pipeline

**`llamatuner/data/`**: Data processing components:
- `data_loader.py`: `get_dataset()` loads datasets from HF hub, ModelScope, or local files
- `dataset_factory/`: Dataset classes:
  - `sft_dataset.py`: `SupervisedDataset2` for SFT
  - `sharegpt_dataset.py`: For ShareGPT format conversations
  - `reward_dataset.py`: For preference/reward modeling
  - `pt_dataset.py`: For pre-training
- `template.py`: `Template` class for formatting conversations into token IDs
- `formatter.py`: `Formatter` classes for role-specific formatting
- `data_parser.py`: `DatasetAttr` and `get_dataset_attr_list()` for parsing dataset configs

**`data/dataset_info.yaml`**: Dataset registry. Defines available datasets with HF/ModelScope URLs, formatting type, and column mappings.

### Templates System

Templates define how conversations are encoded for each model family. Registered in `data/template.py` via `get_template_and_fix_tokenizer()`. Each template defines:
- `format_user`, `format_assistant`, `format_system`, `format_function`, `format_observation`
- `default_system`, `stop_words`, `efficient_eos`

Supported templates: `llama2`, `llama3`, `qwen`, `chatglm3`, `mistral`, `vicuna`, `baichuan`, `intern2`, `gemma`, `deepseek`, `yi`, `falcon`, `codeqwen`, `phi`, `starcoder2`, etc.

### Model Support

**`llamatuner/model/`**: Model utilities and callbacks:
- `callbacks/`: Custom callbacks including `ComputeMetrics`, `SavePeftModelCallback`, `WandbCallback`, `PerplexityCallback`

### Server/Inference

**`server/`**: Gradio-based web interfaces for model chat/inference:
- `gradio_webserver.py`: Basic chat interface
- `gradio_qlora_webserver.py`: For quantized LoRA models
- `single_chat.py`: Single model inference
- `multi_chat.py`: Multi-model comparison

## Dataset Format

Datasets use either **Alpaca** or **ShareGPT** format, configured in `data/dataset_info.yaml`:

### Alpaca Format (supervised)
```json
{"instruction": "...", "input": "...", "output": "...", "system": "...", "history": [...]}
```

### ShareGPT Format (conversations)
```json
{"conversations": [{"from": "human", "value": "..."}, {"from": "gpt", "value": "..."}], "system": "...", "tools": "..."}
```

### Preference Datasets (DPO/RM/PPO/KTO)
```json
{"instruction": "...", "input": "...", "chosen": "...", "rejected": "..."}
```

## Training Workflow

1. **Argument Parsing** (`parser.py`): Parse CLI args or YAML/JSON config
2. **Model Loading** (`train_lora.py` / `train_full.py`):
   - Load base model with optional quantization (4-bit/8-bit bitsandbytes)
   - Apply LoRA config if using lora/qlora method
   - Load tokenizer with appropriate chat template
3. **Dataset Preparation** (`data_loader.py`):
   - `get_dataset()` loads dataset from HF/ModelScope/local
   - Apply template formatting via `template.py`
   - Tokenize with `model_max_length` cutoff
4. **Training**: HuggingFace Trainer with custom callbacks
5. **Checkpointing**: Save adapter weights (LoRA) or full model (full/pt)

## Key Configuration Files

- `data/dataset_info.yaml`: Dataset registry with column mappings
- `.pre-commit-config.yaml`: Code quality hooks (flake8, isort, yapf)
- `.flake8`: Flake8 configuration (max-line-length: 79)
- `examples/deepspeed/`: DeepSpeed config templates (ds_z0, ds_z2, ds_z3 with optional offload)

## Code Style

- **Python**: 3.9+
- **Code style**: black (with .flake8 max-line-length: 79 override)
- **Import sorting**: isort
- **Formatting**: yapf
- Pre-commit hooks: flake8, isort, yapf, trailing-whitespace, double-quote-string-fixer

## Important Notes

- Use `--template` to match your model (e.g., `llama2`, `llama3`, `qwen`, `mistral`, `chatglm3`)
- LoRA requires `--lora_target` for target modules or use `all` to auto-detect
- QLoRA requires `--finetuning_type lora` and `--quant_bit 4` or `8`
- Resume training: set `--resume_from_checkpoint` or rely on auto-detection
- 4-bit QLoRA can fine-tune 7B models on a single 8GB GPU
- Use `--wandb_project` and `--wandb_run_name` for experiment tracking