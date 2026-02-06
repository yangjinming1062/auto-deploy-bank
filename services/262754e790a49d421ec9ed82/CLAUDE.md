# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is the **DAMO-ConvAI** repository from Alibaba Research - a monorepo containing multiple independent research projects focused on conversational AI, NLP, and machine learning. Each top-level directory represents a separate research project with its own README, dependencies, and training/inference scripts.

## Common Commands

### Setup
```bash
# For projects with requirements.txt (most projects)
cd <project-directory>
pip install -r requirements.txt

# For Poetry-based projects (Sotopia, graphix/picard)
cd <project-directory>
poetry install
poetry install -E examples  # with optional dependencies

# For LLaMA-Factory based projects (EPO, SDPO)
cd <project>/LLaMA-Factory && pip install -e .

# For Makefile-based projects (Graphix)
cd graphix && make pull-train-image  # Uses Docker
```

### Training (project-specific)
```bash
# SPACE1.0 style (uses run.py with argparse)
python run.py --do_train=true --model=UnifiedTransformer --data_name=multiwoz ...

# BIRD fine-tuning style (uses shell scripts)
sh ./finetuning/run/run_bird_large.sh

# LLaMA-Factory style (EPO, SDPO)
llamafactory-cli train examples/train_epo/llama3_sotopia_pi_rl.yaml
```

### Inference/Evaluation
```bash
# SPACE1.0 style
python run.py --do_infer=true ...

# BIRD evaluation
sh ./llm/run/run_evaluation.sh

# Sotopia benchmark evaluation (EPO, SDPO)
sotopia benchmark --models <MODEL_NAME> --partner-model <PARTNER> --evaluator-model gpt-4o --task all
```

### Data Preprocessing
```bash
# SPACE1.0 preprocessing
sh scripts/pre_train/preprocess.sh

# Project-specific scripts typically in scripts/ directory
```

### Testing
```bash
# Poetry projects (Sotopia)
poetry run pytest

# Project-specific evaluation scripts
sh ./llm/run/run_evaluation.sh
```

## Architecture

### Project Structure Patterns

**requirements.txt projects** (most common):
```
<project>/
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies
├── run.py             # Main entry point for training/inference
├── scripts/           # Shell scripts for specific tasks
│   ├── <task>/train.sh
│   └── <task>/infer.sh
├── galaxy/ or src/    # Core implementation
│   ├── args.py        # Argument parsing
│   ├── data/          # Dataset handling
│   ├── models/        # Model definitions
│   ├── trainers/      # Training logic
│   └── utils/         # Utility functions
├── data/              # Dataset files (not in git)
└── model/             # Model checkpoints (not in git)
```

**Poetry projects** (Sotopia, graphix/picard):
```
<project>/
├── pyproject.toml     # Poetry configuration with extras
├── poetry.lock        # Locked dependencies
├── tests/             # Test files (pytest)
├── <project>/         # Source code package
└── scripts/           # Utility scripts
```

### Common Dependencies
- **PyTorch**: Core ML framework (versions vary by project, typically 1.8+)
- **transformers**: Hugging Face model library (v3.x or v4.x)
- **numpy/scipy**: Numerical computing
- **nltk**: Natural language toolkit
- **spaCy**: Tokenization (some older projects)
- **scikit-learn**: Machine learning utilities

### Training Patterns
1. **Argument-based config**: Most projects use argparse with configuration files
2. **GPU configuration**: `CUDA_VISIBLE_DEVICES` or `--gpu` flag
3. **Checkpointing**: Models saved in `outputs/` or `save_dir/`
4. **Distributed training**: Some support multi-GPU via DataParallel

## Key Projects

| Project | Focus Area | Main Framework |
|---------|------------|----------------|
| SPACE1.0/2.0/3.0 | Task-oriented dialog | Custom GALAXY framework |
| BIRD-SQL | Text-to-SQL | T5 fine-tuning, OpenAI ICL |
| S²SQL / R²SQL | Text-to-SQL | Sequence-to-sequence |
| Graphix | Text-to-SQL | T5 with graph-aware layers, Docker |
| PROTON | Text-to-SQL parsing | Graph neural networks |
| Sotopia | Social simulation | Multi-agent dialogue, Poetry |
| EPO | Strategic reasoning in LLMs | LLaMA-Factory, RL |
| SDPO | Segment-level preference optimization | LLaMA-Factory, DPO |
| IOPO | Offline-to-online RL | LLaMA-Factory |
| MMEvol | Multimodal LLMs with Evol-Instruct | LLaVA-based |
| OmniCharacter | Character-based dialogue | LLM agents |
| OpenOmni | Open-domain omnimodal conversation | Multimodal LLMs |
| Loong | Long context language models | Extended context LLMs |
| metaretriever | Information retrieval | Dense retrieval |

## Working with Specific Projects

### For SPACE-style projects (galaxy/ module)
- Entry point: `run.py`
- Datasets: MultiWOZ, CamRest, In-Car Assistant
- Models: UnifiedTransformer with DA classification head
- Requires SpaCy: `python -m spacy download en_core_web_sm`

### For BIRD
- Two modes: Fine-tuning (T5) and In-Context Learning (GPT)
- Evaluation requires: Execution accuracy (EX) and Valid Efficiency Score (VES)
- Database files in `./data/dev_databases/`

### For LLaMA-Factory based projects (EPO, SDPO)
- Training: `llamafactory-cli train <config.yaml>`
- Inference: `bash inference.sh` with vLLM
- Requires: Redis for some data pipeline operations

### For Sotopia (Poetry-based)
- Install: `poetry install && poetry install -E examples`
- Run tests: `poetry run pytest`
- CLI: `sotopia benchmark --models <MODEL> --task all`

### For Graphix (Docker-based)
- Uses Docker for environment isolation
- Preprocess: `make pre_process`
- Train: `make train`
- Evaluate: `make eval`
- Image: `eyuansu62/graphix-text-to-sql:v2`

## Environment Setup Notes

1. **Python version**: Projects vary (3.7+ to 3.10+)
2. **CUDA versions**: Projects may require specific PyTorch CUDA versions
3. **External data**: Most require downloading data/models from Google Drive, HuggingFace, or provided links
4. **External APIs**: Some evaluation scripts require OpenAI API keys

## Repository Root

- MIT License
- Each project has its own license notation (check individual READMEs)
- Papers accepted at major venues: NeurIPS, ACL, EMNLP, SIGIR, AAAI, KDD