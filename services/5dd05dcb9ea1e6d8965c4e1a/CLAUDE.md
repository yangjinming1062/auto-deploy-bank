# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

NLPer-Arsenal-Code is a PyTorch-based NLP toolkit that provides baseline implementations for common NLP tasks and various competition strategies ("tricks"). The project is designed to help both beginners (through examples) and experienced practitioners (through competition strategies).

## Repository Structure

```
.
├── codes/                          # Main source code directory
│   ├── examples/                   # Baseline implementations for NLP tasks
│   │   ├── text_classification.py  # Text classification (multi-class)
│   │   └── text_generation.py      # Text generation
│   ├── tricks/                     # Competition strategies
│   │   ├── center_controller.py    # Main entry point for running tricks
│   │   ├── default_configs/        # YAML configurations for tasks
│   │   ├── fgm/                    # Adversarial training strategy
│   │   ├── eight_bit/              # 8-bit quantization for faster training
│   │   ├── unsup_simcse/           # Unsupervised contrastive learning
│   │   └── train.sh                # Batch training script
│   ├── nlper/                      # Core framework
│   │   ├── mini_pytorch_lightning/ # Simplified PyTorch Lightning implementation
│   │   ├── models/                 # Model implementations
│   │   ├── modules/                # Reusable modules (metrics, trainer, etc.)
│   │   └── utils/                  # Utilities (data loading, format conversion)
│   ├── data/                       # Dataset storage
│   └── assets/                     # Additional resources
├── README.md                       # Project overview (Chinese)
└── codes/developer.md              # Developer guide (Chinese)
```

## Core Architecture

The project uses a custom lightweight training framework (`nlper/mini_pytorch_lightning/`) instead of full PyTorch Lightning. Key components:

- **Models** (`nlper/models/`): Task-specific model implementations (BertCLF, Bert2Transformer)
- **Modules** (`nlper/modules/`): Reusable components (metrics, trainer, MLP, decoder)
- **Utils** (`nlper/utils/`): Data utilities, format converters, dataset loaders
- **Tricks** (`tricks/`): Competition strategies with plug-and-play implementations

## Quick Start

### Installation

```bash
cd codes
pip install -r requirements.txt
```

Requirements:
- Python >= 3.8
- PyTorch >= 1.6
- Transformers >= 4.5
- scikit-learn, pandas, matplotlib, seaborn, etc.

### Running Examples

Text Classification:
```bash
cd codes/examples
python text_classification.py
```

Text Generation:
```bash
cd codes/examples
python text_generation.py
```

### Running Competition Tricks

Use `center_controller.py` with YAML configuration:

```bash
cd codes/tricks
python center_controller.py \
    --whole_model BertCLF \
    --trick_name fgm \
    --task_config default_configs/text_clf_smp2020_ewect_usual.yaml
```

Available tricks:
- `fgm`: Adversarial training (Faster Gradient Sign Method)
- `eight_bit`: 8-bit quantization for faster training
- `unsup_simcse`: Unsupervised contrastive learning

Batch training using the provided script:
```bash
cd codes/tricks
bash train.sh
```

### Configuration

Tricks use YAML configuration files in `tricks/default_configs/`:

```yaml
task_name: 'text_clf'
dataset_name: 'text_clf/smp2020-ewect-usual'
model_type: 'bert'
pretrained_model: 'bert-base-chinese'
whole_model: 'BertCLF'
max_len: 140
train_batch_size: 8
lr: 3e-5
target_metric: 'F1'
trainer_args:
  gpus: [0]
  max_epochs: 100
  early_stop: true
  patience: 3
```

## Data Format Standards

### Text Classification
Format: `[[text1, label1], [text2, label2], ...]` where label is numeric
Example: See `codes/data/examples/text_clf.txt`

### Text Generation
Format: `[[src1, tgt1], [src2, tgt2], ...]` where both are strings
Example: See `codes/data/examples/text_gen.txt`

For non-standard datasets:
1. Create a converter function in `codes/nlper/utils/format_convert.py`
2. Add the dataset to `codes/nlper/utils/corpus.py`
3. Set `use_convert: true` in the YAML config

## Key Files

- `codes/examples/text_classification.py`: Complete text classification pipeline with BertCLF
- `codes/tricks/center_controller.py`: Main controller for running tricks with configs
- `codes/tricks/text_clf_handler.py`: Task handler for text classification
- `codes/nlper/mini_pytorch_lightning/trainer.py`: Custom training loop implementation
- `codes/nlper/modules/trainer.py`: Trainer wrapper for examples
- `codes/nlper/modules/metrics.py`: Metric implementations (Precision, Recall, F1)

## Available Competition Strategies

| Trick | Purpose | Description | Supported Tasks |
|-------|---------|-------------|-----------------|
| fgm | Robustness | Adversarial training with embedding perturbation | Text CLF |
| eight_bit | Speed | 8-bit quantization to reduce memory usage | Text CLF |
| unsup_simcse | Semantics | Unsupervised contrastive learning for better representations | Text CLF |

Each trick has:
- `specialModels.py`: Implementation of the strategy
- `README.md`: Detailed explanation and ablation studies

## Development Workflow

### Adding a New Model

1. Implement model in `codes/nlper/models/` for the appropriate task
2. Import in `codes/nlper/models/__init__.py`
3. Update YAML config `whole_model` parameter
4. Model must accept `**iter(dataloader)` as input

### Adding a New Trick

1. Create directory `codes/tricks/trick_name/`
2. Implement in `specialModels.py` (follow existing tricks as reference)
3. Create `README.md` with:
   - PyTorch implementation (pseudo-code)
   - Performance impact explanation
   - References
4. Create or update task handler if needed
5. Submit PR

### Running on Custom Data

For `examples/`:
- Modify data loading and preprocessing directly in the example file
- Or use the format converter utility

For `tricks/`:
- Add dataset to `codes/nlper/utils/corpus.py` for auto-download
- Create converter in `codes/nlper/utils/format_convert.py` if needed
- Create or modify YAML config in `codes/tricks/default_configs/`

## Key Utilities

- `codes/nlper/utils/corpus.py`: Auto-download datasets from standard repositories
- `codes/nlper/utils/format_convert.py`: Convert custom datasets to standard format
- `codes/nlper/utils/datasets.py`: Dataset classes for different tasks
- `codes/nlper/modules/metrics.py`: Evaluation metrics with macro/micro averaging

## Training Features

- Automatic dataset downloading (when dataset in registry)
- Early stopping based on target metric
- Learning rate scheduling with warmup
- Mixed precision support through eight_bit trick
- GPU/CPU support (single GPU only)
- System monitoring during training

## Notes

- All documentation is in Chinese
- Project focuses on Chinese NLP tasks (BERT-based models)
- Uses custom mini-framework rather than PyTorch Lightning
- Designed for reproducibility and quick experimentation
- Single GPU support only (no distributed training)