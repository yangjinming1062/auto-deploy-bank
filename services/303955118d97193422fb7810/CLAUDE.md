# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is the **MT-DNN** (Multi-Task Deep Neural Network) repository for Natural Language Understanding. It's a PyTorch-based library that implements multi-task learning on top of pre-trained language models (BERT, RoBERTa, DeBERTa, T5) to solve various NLP tasks including classification, regression, question answering, and sequence labeling.

## High-Level Architecture

The codebase follows a modular architecture with clear separation of concerns:

### Core Components

1. **`mt_dnn/`** - Main model package containing:
   - `model.py:28` - **MTDNNModel** class: High-level model wrapper that manages training, inference, and multi-task setup
   - `matcher.py:17` - **SANBertNetwork**: Core neural network architecture based on BERT with task-specific output heads
   - `batcher.py` - Data loading, batching, and collation for single/multi-task training
   - `loss.py` - Loss functions (Cross-Entropy, MSE, KL divergence, etc.)
   - `optim.py` - Optimizer configurations (AdamaxW, RAdam support)
   - `inference.py` - Model inference and evaluation utilities
   - `perturbation.py` - Adversarial training perturbations (SMART)

2. **`module/`** - Low-level neural network components:
   - `san.py` - Self-Attentive Networks (SAN) classifier implementation
   - `pooler.py` - Pooling layers for sequence representations
   - `sub_layers.py` - Transformer sub-layers
   - `dropout_wrapper.py` - Dropout wrappers
   - `similarity.py` - Similarity computation utilities

3. **`data_utils/`** - Data processing utilities:
   - `tokenizer_utils.py` - Tokenizer creation and management (HuggingFace Transformers integration)
   - `task_def.py:1` - Task type definitions (Classification, Regression, QA, SequenceLabeling)
   - `metrics.py` - Evaluation metrics (ACC, F1, Pearson, Spearman, MCC)
   - `vocab.py` - Vocabulary management
   - `mrc_eval.py`, `squad_eval.py` - QA task evaluators

4. **`experiments/`** - Task-specific configurations and scripts:
   - `glue/` - GLUE benchmark tasks (MNLI, QQP, RTE, etc.)
   - `superglue/` - SuperGLUE benchmark tasks
   - `ner/` - Named Entity Recognition
   - `squad/` - SQuAD question answering
   - `domain_adaptation/` - Domain adaptation experiments
   - `exp_def.py:52` - **TaskDefs**: Loads YAML task definitions and creates TaskDef objects

5. **`tasks/`** - Task-specific implementations:
   - Custom task objects with `train_build_task_layer()` methods for constructing task-specific output layers

### Key Configuration Files (YAML)

Task configurations are defined in YAML files under `experiments/*/`:
- `experiments/glue/glue_task_def.yml` - GLUE tasks (MNLI, MRPC, QQP, RTE, SST, STS-B, etc.)
- `experiments/ner/ner_task_def.yml` - NER task
- `experiments/squad/squad_task_def.yml` - SQuAD QA task
- `experiments/superglue/superglue_task_def.yml` - SuperGLUE tasks

Each task definition includes:
- `task_type`: Classification, Regression, or other types
- `data_format`: PremiseOnly, PremiseAndOneHypothesis, etc.
- `n_class`: Number of classes
- `metric_meta`: Evaluation metrics
- `loss`: Loss function (CeCriterion, MseCriterion, etc.)
- `dropout_p`: Dropout probability
- `enable_san`: Whether to use SAN classifier

## Common Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Download data and models
bash download.sh
```

### Quick Start
```bash
# Run a toy example (RTE task)
bash run_toy.sh
```

### Data Preprocessing
```bash
# Preprocess GLUE data for all PLMs
bash experiments/glue/prepro.sh

# Or manually for specific model
python prepro_std.py \
  --model bert-base-uncased \
  --root_dir data/canonical_data \
  --task_def experiments/glue/glue_task_def.yml \
  --workers 32
```

### Training
```bash
# Single-task training
python train.py \
  --data_dir <data-path> \
  --init_checkpoint <bert-model> \
  --train_dataset <task-name> \
  --test_dataset <task-name> \
  --task_def <task-def-yml> \
  --output_dir <output-path>

# Multi-task training example
python train.py \
  --data_dir data/canonical_data \
  --init_checkpoint bert-base-uncased \
  --train_dataset cola,mrpc,sst \
  --test_dataset cola,mrpc,sst \
  --task_def experiments/glue/glue_task_def.yml \
  --epochs 3 \
  --batch_size 16 \
  --learning_rate 5e-5
```

### Advanced Training Options
```bash
# With gradient accumulation (for small GPUs)
python train.py ... --grad_accumulation_step 4

# FP16 training (requires apex)
python train.py ... --fp16

# Adversarial training (SMART)
python train.py ... --adv_train --adv_opt 1

# Distributed training
python train.py ... --local_rank 0 --world_size 4
```

### Running Tests
```bash
# Run full test suite
bash tests/test.sh

# Run specific test
python tests/test_prepro.py
```

### Inference and Embedding Extraction
```bash
# Extract embeddings
python experiments/dump_embedding/extractor.py \
  --do_lower_case \
  --finput input_examples/pair-input.txt \
  --foutput input_examples/pair-output.json \
  --bert_model bert-base-uncased \
  --checkpoint mt_dnn_models/mt_dnn_base.pt
```

## Development Workflow

### Adding a New Task

1. Create a task definition YAML file in `experiments/<task_name>/<task_name>_task_def.yml`:
   ```yaml
   mytask:
     task_type: Classification
     data_format: PremiseAndOneHypothesis
     n_class: 2
     metric_meta: [ACC, F1]
     loss: CeCriterion
     dropout_p: 0.1
     enable_san: false
   ```

2. Create a preprocessing script at `experiments/<task_name>/<task_name>_prepro.py` if custom data loading is needed

3. Run preprocessing:
   ```bash
   python prepro_std.py --model bert-base-uncased --root_dir data/<task-data> --task_def experiments/<task_name>/<task_name>_task_def.yml
   ```

4. Train the model:
   ```bash
   python train.py --data_dir data/<preprocessed-data> --train_dataset mytask --test_dataset mytask --task_def experiments/<task_name>/<task_name>_task_def.yml
   ```

### Training from Checkpoint
```bash
python train.py ... --resume --model_ckpt <checkpoint-path>
```

### Key Command-Line Arguments for train.py

- `--data_dir`: Path to preprocessed data
- `--init_checkpoint`: Pre-trained model checkpoint (bert-base-uncased, path to .pt file, etc.)
- `--train_dataset`: Comma-separated list of training tasks
- `--test_dataset`: Comma-separated list of test tasks
- `--task_def`: Path to task definition YAML
- `--output_dir`: Where to save model checkpoints
- `--batch_size` / `--batch_size_eval`: Training and evaluation batch sizes
- `--learning_rate`: Learning rate
- `--epochs`: Number of epochs
- `--grad_accumulation_step`: Gradient accumulation steps
- `--optimizer`: Optimizer (adamax, adam, radam)
- `--fp16`: Enable FP16 training
- `--adv_train`: Enable adversarial training
- `--local_rank`: For distributed training

## Model Architecture Details

The MT-DNN model consists of:

1. **Shared Encoder**: Pre-trained transformer (BERT/RoBERTa/DeBERTa/T5)
2. **Task-Specific Heads**: Multiple output layers, one per task (created in `matcher.py:54-73`)
3. **SAN Classifier**: Optional Self-Attentive Networks for certain tasks
4. **Multi-Task Learning**: Shared representations with task-specific heads

## Important Files

- `train.py` - Main training script with extensive configuration options
- `prepro_std.py` - Data preprocessing pipeline for converting raw data to MT-DNN format
- `predict.py` - Inference script for making predictions
- `pretrained_models.py:1` - MODEL_CLASSES mapping for supported pre-trained models
- `module/san.py:1` - SAN (Self-Attentive Networks) classifier implementation
- `experiments/exp_def.py:52` - TaskDefs class for loading task configurations

## Environment Requirements

- Python 3.6+
- PyTorch 1.5.0
- transformers==4.20.0
- Other dependencies in requirements.txt

**Note**: Experiments typically require 4 V100 GPUs for base models. Reduce batch size for smaller GPUs or use gradient accumulation.

## Key Papers Implemented

1. **MT-DNN** (ACL 2019): Multi-task learning on GLUE benchmark
2. **MT-DNN-KD** (arXiv 2019): Knowledge distillation for MT-DNN
3. **SMART** (ACL 2020): Adversarial training for robust fine-tuning
4. **Posterior Differential Regularization** (NAACL 2021): f-divergence based robustness

For detailed information, see the full README.md.