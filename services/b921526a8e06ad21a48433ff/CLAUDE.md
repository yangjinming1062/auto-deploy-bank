# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Deep Snake is a real-time instance segmentation algorithm (CVPR 2020). The core idea uses a snake algorithm where polygon contours are iteratively deformed to segment objects, with a deep network predicting the deformation.

## Common Commands

### Installation
```bash
# Create conda environment
conda create -n snake python=3.7
conda activate snake

# Install dependencies
pip install torch==1.1.0 -f https://download.pytorch.org/whl/cu90/stable
pip install Cython==0.28.2
pip install -r requirements.txt

# Install NVIDIA apex (specific commit)
git clone https://github.com/NVIDIA/apex.git
cd apex
git checkout 39e153a3159724432257a8fc118807b359f4d1c8
python setup.py install --cuda_ext --cpp_ext

# Compile CUDA extensions
cd lib/csrc/dcn_v2 && python setup.py build_ext --inplace
cd ../extreme_utils && python setup.py build_ext --inplace
cd ../roi_align_layer && python setup.py build_ext --inplace
```

### Training
```bash
# Single-GPU training
python train_net.py --cfg_file configs/city_rcnn_snake.yaml model rcnn_snake det_model rcnn_det

# Multi-GPU training (set gpus in config)
python train_net.py --cfg_file configs/kins_snake.yaml model kins_snake
python train_net.py --cfg_file configs/sbd_snake.yaml model sbd_snake
```

### Testing & Evaluation
```bash
# Evaluate with COCO evaluator
python run.py --type evaluate --cfg_file configs/city_rcnn_snake.yaml

# Evaluate with dataset-specific evaluator
python run.py --type evaluate --cfg_file configs/city_rcnn_snake.yaml test.dataset CityscapesVal
python run.py --type evaluate --cfg_file configs/kins_snake.yaml test.dataset KinsVal
python run.py --type evaluate --cfg_file configs/sbd_snake.yaml test.dataset SbdVal

# Speed test (throughput only, no evaluation)
python run.py --type network --cfg_file configs/city_rcnn_snake.yaml
```

### Visualization & Demo
```bash
# Visualize on test/val set
python run.py --type visualize --cfg_file configs/city_rcnn_snake.yaml test.dataset CityscapesTest ct_score 0.3

# Run demo on images
python run.py --type demo --cfg_file configs/sbd_snake.yaml demo_path demo_images ct_score 0.3
```

### Monitor Training
```bash
tensorboard --logdir data/record/<task>/<model>
# e.g., tensorboard --logdir data/record/rcnn_snake/long_rcnn
```

## Architecture

### Configuration System (`lib/config/`)
Uses **yacs** CfgNode for configuration. Configs are YAML files that specify:
- `model`: Model name (affects save directory)
- `network`: Backbone architecture (e.g., `rcnn_34`, `dla_34`)
- `task`: Task name (snake, rcnn_snake, ct_rcnn) - determines which network module to load
- `heads`: Output heads for detection/segmentation
- `train`/`test`: Training and testing parameters

Configuration is loaded via `make_cfg(args)` in `config.py`.

### Data Pipeline (`lib/datasets/`)
- `make_data_loader()` creates PyTorch DataLoaders
- Datasets inherit from base dataset classes for each task type (snake, ct_rcnn, rcnn_snake)
- Each dataset has corresponding augmentation in `augmentation.py`
- `lib/datasets/dataset_catalog.py` maps dataset names to classes

### Network Factory (`lib/networks/`)
Networks are organized by **task**:
- `snake/` - Snake-only model
- `ct_rcnn/` - CenterNet-style detector
- `rcnn_snake/` - R-CNN detector + snake (two-stage)

Each task's `__init__.py` defines `_network_factory` mapping architecture names to `get_network()` functions. `make_network()` dynamically imports the task module and calls its `get_network()`.

### Training (`lib/train/`)
- `make_trainer()` creates task-specific trainers
- `make_optimizer()` / `make_lr_scheduler()` configure optimization
- `make_recorder()` handles tensorboard logging
- Training loop in `train_net.py` handles epochs, saving, and evaluation

### CUDA Extensions (`lib/csrc/`)
Custom CUDA operations that must be compiled:
- `dcn_v2/` - Deformable convolution v2
- `extreme_utils/` - NMS and other utilities
- `roi_align_layer/` - ROIAlign implementation

## Key Configuration Patterns

Override config values via command line:
```bash
python train_net.py --cfg_file configs/city_rcnn_snake.yaml model new_model train.lr 0.0001
```

Model checkpoints saved to: `data/model/<task>/<model>/<epoch>.pth`
Tensorboard logs at: `data/record/<task>/<model>/`