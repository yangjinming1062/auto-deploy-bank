# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BioReason is a multimodal AI system integrating DNA foundation models (NucleotideTransformer, Evo2) with LLMs (Qwen3) for biological reasoning tasks like KEGG pathway prediction and variant effect prediction. Uses PyTorch Lightning + HuggingFace Transformers.

## Development Commands

```bash
# Installation
pip install -e .              # Standard install
pip install -e ".[dev]"       # With dev dependencies (pytest, black, isort, mypy)

# Code quality
black bioreason/              # Format (line-length: 88)
isort bioreason/              # Sort imports (black profile)
mypy bioreason/               # Strict type checking (python_version = "3.11")

# Testing
pytest                         # Run tests
```

## Architecture

### Directory Structure
```
bioreason/
├── dataset/           # Data loading (kegg.py, variant_effect.py, utils.py)
├── models/            # Model implementations
│   ├── dna_llm.py     # Main DNA+LLM integration
│   ├── dna_only.py    # DNA-only classifier
│   ├── dl/            # Deep learning utilities (processing, config, chat_template)
│   └── evo2_tokenizer.py
├── dna_modules/       # DNA-specific modules (dna_module.py, nucleotide_module.py)
├── trainer/           # Training logic (grpo_config.py, grpo_trainer.py)
└── utils/             # DNA utilities

Root scripts: train_dna_qwen.py, train_dna_only.py, reason.py
```

### Core Patterns

**Model Architecture (PyTorch Lightning):**
- DNA encoder (NucleotideTransformer/Evo2) → projection layer → Qwen3 LLM
- Special tokens: `<|dna_start|>`, `<|dna_pad|>`, `<|dna_end|>`
- LoRA for parameter-efficient fine-tuning via `peft` library
- DeepSpeed ZeRO-2/3 for distributed training

**Training Methods:**
- Supervised Fine-Tuning (SFT) via `pl.LightningModule`
- GRPO (Group Relative Policy Optimization) reinforcement learning in `trainer/grpo_trainer.py`

**Data Processing:**
- Custom datasets in `bioreason/dataset/` with collate functions
- Chat templates for Qwen conversation formatting
- DNA truncation strategies (left/right truncation)

**Hardware:**
- Multi-GPU training via SLURM (see `sh_train_dna_qwen.sh`)
- BitsAndBytes quantization support
- Weights & Biases for logging

## Key Dependencies
- torch, transformers, accelerate, pytorch_lightning
- peft (LoRA), trl (RL), datasets, wandb
- deepspeed, bitsandbytes
- nucleotide-transformer, evo2, qwen3

## Code Style
- Strict mypy type checking enabled
- Black formatter (line length 88)
- isort with black profile
- Comprehensive docstrings with Args/Returns sections