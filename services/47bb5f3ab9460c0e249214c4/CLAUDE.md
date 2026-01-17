# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LSTR (Lane Shape Prediction with Transformers) is an end-to-end lane detection model using a DETR-style transformer architecture. It directly outputs lane shape parameters as polynomial curves. The model uses:
- A ResNet backbone (configurable layers: BasicBlock or Bottleneck)
- Transformer encoder-decoder with learnable query embeddings
- Hungarian matching for loss computation (similar to DETR)
- ~765K parameters, ~574M MACs for the default config

## Commands

### Environment Setup
```bash
conda env create --name lstr --file environment.txt
conda activate lstr
pip install -r requirements.txt
```

### Training
```bash
# Train from scratch
python train.py LSTR

# Resume training from iteration
python train.py LSTR --iter 500000

# Use custom threads for data loading
python train.py LSTR --threads 8

# Freeze pretrained backbone
python train.py LSTR --freeze
```

Visualized training images are saved to `./results` and model checkpoints (every 5000 iterations) are saved to `./cache/nnet/LSTR/`.

### Evaluation
```bash
# Standard evaluation on test set
python test.py LSTR --testiter 500000 --modality eval --split testing

# With debug visualization (saves to ./results/LSTR/500000/testing/lane_debug)
python test.py LSTR --testiter 500000 --modality eval --split testing --debug

# FPS benchmarking (batch=16 for max FPS)
python test.py LSTR --testiter 500000 --modality eval --split testing --batch 16

# Visualize decoder attention maps
python test.py LSTR --testiter 500000 --modality eval --split testing --debug --debugDec

# Visualize encoder attention maps
python test.py LSTR --testiter 500000 --modality eval --split testing --debug --debugEnc

# Run inference on custom images in ./images directory
python test.py LSTR --testiter 500000 --modality images --image_root ./images --debug
```

## Architecture

### Data Flow
1. `train.py` / `test.py` - Entry points that load config and initialize components
2. `config.py` - Central `Config` class (singleton as `system_configs`) managing all hyperparameters
3. `config/LSTR.json` - Model-specific overrides (batch_size=16, learning_rate=0.0001, etc.)
4. `db/datasets.py` - Maps dataset names to dataset classes (e.g., "TUSIMPLE" → `TUSIMPLE`)
5. `db/tusimple.py` - TuSimple dataset with annotations, augmentation, and evaluation
6. `sample/tusimple.py` - `sample_data()` function generates training batches with augmentation
7. `nnet/py_factory.py` - `NetworkFactory` dynamically imports `models.{snapshot_name}` (e.g., `models.LSTR`) to get `model` and `loss` classes, then builds the network and handles training/inference loops
8. `models/LSTR.py` - Exports `model` class (ResNet + Transformer) and `loss` class (AELoss for DETR-style matching)

### Model Components (`models/py_utils/`)
- `kp.py` - Core network: ResNet backbone + Transformer encoder-decoder + query embeddings + prediction heads
- `transformer.py` - Transformer encoder layers and decoder layers with multi-head attention
- `detr_loss.py` - `SetCriterion` computes classification + curve regression losses with Hungarian matching
- `matcher.py` - Hungarian matcher for assigning predictions to ground truth lanes
- `position_encoding.py` - Sinusoidal positional embeddings for transformer

### Key Configuration Properties (from `config.py`)
- `batch_size`: Training batch size (default 16 in LSTR.json)
- `learning_rate`: Default 0.0001 (LSTR) or 0.00025 (base)
- `max_iter`: Total training iterations (default 500000)
- `snapshot`: Save checkpoint every N iterations (default 5000)
- `stepsize`: LR decay step (default 450000)
- `decay_rate`: LR decay factor (default 10)
- `num_queries`: Number of lane queries (default 7 for LSTR)
- `attn_dim`: Transformer hidden dimension (default 32)

### Directory Structure
- `./cache/` - Model checkpoints (`cache/nnet/LSTR/LSTR_500000.pkl`)
- `./results/` - Debug visualizations and evaluation logs
- `./data/` - Expected location of TuSimple dataset (not tracked in repo)
- `./config/` - Model configuration JSON files
- `./sample/` - Data sampling and visualization utilities
- `./test/` - Evaluation logic (`tusimple.py` for dataset eval, `images.py` for custom images)

### Data Loading (Training)
Training uses multiprocessing (`torch.multiprocessing.Process`) for parallel data prefetching:
- Multiple worker processes load and augment data in parallel
- Data is pinned to GPU memory via `pin_memory`
- Queue-based pipeline feeds batches to training loop

## Data Format

TuSimple expects data at `./data/TuSimple/LaneDetection/` with structure:
```
TuSimple/LaneDetection/
  clips/
  label_data_0313.json
  label_data_0531.json
  label_data_0601.json
  test_label.json
```

Lanes are represented as polynomial curves with 6 parameters (a0-a5) plus upper/lower y-coordinates.