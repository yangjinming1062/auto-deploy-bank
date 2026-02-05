# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SNIPER (Scale Normalization for object Detection with efficient multi-sPace tRaining) is an efficient multi-scale training approach for instance-level recognition tasks like object detection. It selectively processes context regions (chips) around ground-truth objects instead of entire image pyramids. AutoFocus is the complementary efficient multi-scale inference algorithm.

This is a deep learning computer vision project built on MXNet with Python/C++ for performance.

## Build & Installation

```bash
# Clone with submodules (includes custom MXNet fork)
git clone --recursive https://github.com/mahyarnajibi/SNIPER.git

# Compile C++ extensions
bash scripts/compile.sh

# Install Python dependencies
pip install -r requirements.txt

# Build custom MXNet fork (required for training)
cd SNIPER-mxnet
make -j [NUM_CPUS] USE_CUDA_PATH=[CUDA_PATH] USE_CUDNN=1
cd ..
```

## Common Commands

```bash
# Run demo on sample image
python demo.py

# Run demo on custom image
python demo.py --im_path [PATH_TO_IMAGE]

# Train SNIPER detector (uses default config)
python main_train.py

# Train with custom config
python main_train.py --cfg configs/faster/sniper_res101_e2e.yml

# Override config values at command line
python main_train.py --cfg configs/faster/sniper_res101_e2e.yml --set TRAIN.BATCH_IMAGES 8

# Evaluate trained model
python main_test.py --cfg [CONFIG_USED_FOR_TRAINING]

# Download pretrained models
bash scripts/download_pretrained_models.sh
bash scripts/download_sniper_autofocus_detectors.sh
bash scripts/download_sniper_neg_props.sh
```

## Architecture

### Directory Structure
- `lib/` - Core library code
- `symbols/faster/` - Neural network symbol definitions (ResNet-101/50, MobileNetV2, ResNeXt)
- `configs/faster/` - YAML configuration files for different model variants
- `SNIPER-mxnet/` - Custom MXNet fork with optimized operators
- `lib/inference.py` - Main inference/testing module

### Configuration System
Configs are split between YAML files in `configs/faster/` and Python defaults in `lib/configs/faster/default_configs.py`. YAML configs override defaults and are loaded via `update_config()`. Override individual values with `--set key value` at command line.

Key config sections:
- `dataset` - Dataset paths, image sets, number of classes
- `TRAIN` - Training parameters (scales, batch size, chip generation)
- `TEST` - Inference parameters
- `network` - Anchor settings, pretrained model path, fixed layers

### Data Flow
1. `load_proposal_roidb()` in `lib/data_utils/load_data.py` - Loads dataset annotations
2. `MNIteratorE2E` in `lib/iterators/` - Creates training mini-batches with chips
3. Symbol definition in `symbols/faster/` - Builds the network graph
4. `mx.mod.Module` - Executes training/inference on GPU(s)

### Supported Datasets
- COCO (`dataset: coco`)
- PASCAL VOC (`dataset: PascalVOC`)

Configure paths via `dataset.dataset_path` and `dataset.root_path` in config.

## Key Files

| File | Purpose |
|------|---------|
| `main_train.py` | Training entry point |
| `main_test.py` | Evaluation/inference entry point |
| `demo.py` | Single image demo |
| `lib/inference.py` | `Tester` class for multi-scale inference |
| `lib/iterators/MNIteratorE2E.py` | Training data iterator with chip generation |
| `lib/train_utils/metric.py` | Evaluation metrics |