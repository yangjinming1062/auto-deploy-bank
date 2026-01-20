# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LLMBox is a comprehensive library for implementing Large Language Models, consisting of two main components:
- **Training** (`training/`): Unified training pipeline for SFT, PT, PPO, and DPO
- **Utilization** (`utilization/`): Model evaluation and inference with 60+ datasets

## Common Commands

### Installation
```bash
pip install -r requirements.txt
```

### Evaluation/Utilization
```bash
# Basic evaluation
python inference.py -m model_name -d dataset_name

# With specific parameters
python inference.py -m meta-llama/Llama-2-7b-hf -d mmlu -shots 5 --vllm True

# OpenAI models
python inference.py -m gpt-3.5-turbo -d copa
```

### Training
```bash
cd training
bash bash/run_7b_ds3.sh  # SFT with DeepSpeed
bash bash/run_7b_pt.sh   # Pre-training
bash bash/run_ppo.sh     # PPO training
bash bash/run_dpo.sh     # DPO training
```

### Testing
```bash
# Run all tests
pytest

# Run specific test group (for CI)
pytest --splits 12 --group 1

# Run with coverage
pytest --cov utilization

# Rerun failures
pytest --reruns 3
```

### Code Formatting
```bash
# Check formatting
isort --check-only --diff --settings-path .isort.cfg
yapf --style .style.yapf --exclude '**/training/**' --diff

# Apply formatting
isort --settings-path .isort.cfg
yapf --style .style.yapf --exclude '**/training/**' --in-place
```

## Architecture

### Utilization Pipeline (`utilization/`)

Entry point: `inference.py` → calls `utilization.get_evaluator()` → `Evaluator` class

**Key components:**
- `evaluator.py`: Main `Evaluator` class that orchestrates model loading, dataset loading, and evaluation
- `model/` Model backends extending the base `Model` class:
  - `huggingface_model.py`: Local HF models with transformers
  - `vllm_model.py`: vLLM for fast inference
  - `openai_model.py`: OpenAI API (GPT-4, davinci-002)
  - `anthropic_model.py`, `dashscope_model.py`, `qianfan_model.py`: Other API providers
- `dataset/`: Dataset implementations inheriting from `Dataset` base class:
  - `multiple_choice_dataset.py`: For MMLU, ARC, etc.
  - `generation_dataset.py`: For GSM8K, HumanEval, etc.
  - 60+ specific dataset files (e.g., `mmlu.py`, `gsm8k.py`)
- `load_model.py`: Factory for loading models via `register_model` decorator
- `load_dataset.py`: Factory for loading datasets via `register_dataset` decorator
- `metric/`: Evaluation metrics (accuracy, BLEU, perplexity, etc.)

**Evaluation flow:**
1. Parse arguments via `parse_argument()` → returns `ModelArguments`, `DatasetArguments`, `EvaluationArguments`
2. `load_model()` creates model instance based on backend
3. `load_datasets()` creates dataset instance with evaluation type (get_ppl, generation, etc.)
4. `Evaluator.evaluate()` iterates over dataloader, calls model methods, computes metrics

### Training Pipeline (`training/`)

- `train.py`: Main SFT/PT trainer using HuggingFace Transformers
- `ppo.py`: PPO trainer for RLHF
- `dpo.py`: DPO trainer for preference optimization
- `dataset/`: Training dataset classes (SFTDataset, PTDataset, etc.)
- `configs/`: DeepSpeed configuration files
- `bash/`: Preset training scripts for common configurations

### Key Configuration Files
- `.style.yapf`: Python formatting style
- `.isort.cfg`: Import sorting configuration
- `requirements.txt`: Core dependencies
- `tests/requirements-tests.txt`: Test dependencies

## Development Notes

- Python 3.8+ required
- The `utilization/` module avoids early torch imports for lightweight API-only usage
- Datasets and models use registry patterns (`@register_dataset`, `@register_model`)
- Use `--dry_run` to test evaluation pipeline without calling models
- Evaluation results saved to `evaluation_results/` by default