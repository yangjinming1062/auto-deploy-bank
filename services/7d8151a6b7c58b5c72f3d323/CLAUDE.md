# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

EasyPortrait is a large-scale face parsing and portrait segmentation dataset with 40,000 RGB images (~92GB). Built on PyTorch and MMSegmentation v0.30.0 (OpenMMLab ecosystem). Two task configurations:
- **Portrait segmentation (PS)**: 2 classes (background + person)
- **Face parsing (FP)**: 9 classes (background, person, skin, left brow, right brow, left eye, right eye, lips, teeth)

## Architecture

**Config-driven** project following OpenMMLab patterns. Model architecture, datasets, and training schedules are all defined in Python config files.

### Key Directories
- `pipelines/mmseg/` - Vendored MMSegmentation 0.30.0 (datasets, models, core utilities)
- `pipelines/local_configs/` - Experiment configurations
- `pipelines/tools/` - Training and testing CLI scripts
- `pipelines/demo/` - Inference scripts

### Configuration System
- `__base__/models/` - Base model definitions (SegFormer, BiSeNet, FPN, FCN, DeepLab, DANet, etc.)
- `__base__/datasets/` - Dataset configurations (EasyPortrait with various input sizes)
- `__base__/schedules/` - Training schedules (AdamW, different iteration counts)
- `easyportrait_experiments_v2/<model>-<ps|fp>/` - Model-specific configs

### Dataset Classes
Custom datasets registered via `@DATASETS.register_module()` in `pipelines/mmseg/datasets/easy_portrait.py`:
- `EasyPortraitDataset` - 9-class face parsing
- `EasyPortraitPSDataset` - 2-class portrait segmentation

## Commands

### Installation
```bash
pip install -r pipelines/requirements.txt
pip install -v -e pipelines/
```

### Training
Single GPU:
```bash
python ./pipelines/tools/train.py <config_path> --gpu-id <GPU_ID>
```

Distributed (8 GPUs):
```bash
./pipelines/tools/dist_train.sh <config_path> <NUM_GPUS>
```

### Evaluation
Single GPU:
```bash
python ./pipelines/tools/test.py <config_path> <checkpoint_path> --gpu-id <GPU_ID> --eval mIoU
```

Distributed:
```bash
./pipelines/tools/dist_test.sh <config_path> <checkpoint_path> <NUM_GPUS> --eval mIoU
```

### Inference Demo
```bash
python ./pipelines/demo/image_demo.py <img_path> <config_path> <checkpoint_path> --palette=easy_portrait --out-file=<out_path>
```

### Linting and Formatting
```bash
# Code formatting with yapf
yapf -i <path> ...

# Import sorting with isort
isort <path> ...

# Spell checking
codespell

# Flake8 linting
flake8 <path>
```

### Tests
```bash
pytest pipelines/
```

### Common Config Paths
- Portrait segmentation: `pipelines/local_configs/easyportrait_experiments_v2/<model>-ps/<model>-ps.py`
- Face parsing: `pipelines/local_configs/easyportrait_experiments_v2/<model>-fp/<model>-fp.py`

Example models: segformer, bisenet, fpn, fcn, deeplab, danet, fastscnn