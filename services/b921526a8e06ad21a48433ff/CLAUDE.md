# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DeepSnake is a real-time instance segmentation algorithm (CVPR 2020). The codebase uses a modular factory pattern with four main components:
- **Dataset**: Provides data for training/testing (`lib/datasets/$dataset_id/$task.py`)
- **Network**: Model architecture (`lib/networks/$task/`)
- **Trainer**: Defines loss functions (`lib/train/trainers/$task.py`)
- **Evaluator**: Defines evaluation metrics (`lib/evaluators/$dataset_id/$task.py`)

## Build & Installation

```bash
# Create conda environment
conda create -n snake python=3.7
conda activate snake

# Install PyTorch (must match system CUDA version, e.g., CUDA 9.0)
pip install torch==1.1.0 -f https://download.pytorch.org/whl/cu90/stable

# Install dependencies
pip install Cython==0.28.2
pip install -r requirements.txt

# Install NVIDIA apex
git clone https://github.com/NVIDIA/apex.git
cd apex
git checkout 39e153a3159724432257a8fc118807b359f4d1c8
python setup.py install --cuda_ext --cpp_ext

# Compile CUDA extensions
cd lib/csrc/dcn_v2 && python setup.py build_ext --inplace
cd ../extreme_utils && python setup.py build_ext --inplace
cd ../roi_align_layer && python setup.py build_ext --inplace
```

## Common Commands

### Training
```bash
# Train a model (replace config, model, task as needed)
python train_net.py --cfg_file configs/city_rcnn_snake.yaml model long_rcnn task rcnn_snake det_model long_rcnn_det

# Key training parameters: train.epoch, train.lr, train.batch_size, train.milestones, train.gamma
python train_net.py --cfg_file configs/city_rcnn_snake.yaml train.epoch 140 eval_ep 5
```

### Testing & Evaluation
```bash
# Evaluate using COCO evaluator
python run.py --type evaluate --cfg_file configs/city_rcnn_snake.yaml

# Evaluate using dataset-specific evaluator
python run.py --type evaluate --cfg_file configs/city_rcnn_snake.yaml test.dataset CityscapesVal
```

### Visualization
```bash
# Visualize on test set
python run.py --type visualize --cfg_file configs/city_rcnn_snake.yaml test.dataset CityscapesTest ct_score 0.3

# Visualize on validation set
python run.py --type visualize --cfg_file configs/city_rcnn_snake.yaml test.dataset CityscapesVal ct_score 0.3
```

### Demo
```bash
# Run demo on image folder
python run.py --type demo --cfg_file configs/sbd_snake.yaml demo_path demo_images ct_score 0.3

# Run demo on single image
python run.py --type demo --cfg_file configs/sbd_snake.yaml demo_path demo_images/2009_000871.jpg ct_score 0.3
```

### Performance Benchmarking
```bash
python run.py --type network --cfg_file configs/city_rcnn_snake.yaml
```

### TensorBoard
```bash
tensorboard --logdir data/record/rcnn_snake  # for rcnn_snake task
tensorboard --logdir data/record/snake       # for snake task
```

## Configuration Pattern

Configs are YAML files with the following key fields:
- `model`: model name (determines save directory)
- `network`: backbone architecture (e.g., `rcnn_34`, `dla_34`)
- `task`: algorithm type (e.g., `rcnn_snake`, `snake`)
- `train.dataset`: training set name (registered in `lib/datasets/dataset_catalog.py`)
- `test.dataset`: validation/test set name
- `heads`: output heads for the network

## Adding New Components

1. **Dataset**: Create `lib/datasets/$dataset_id/$task.py` with a `Dataset` class, register in `lib/datasets/dataset_catalog.py`

2. **Network**: Create `lib/networks/$task/__init__.py` with `get_network(cfg)` function

3. **Trainer**: Create `lib/train/trainers/$task.py` with `train()` and `val()` methods

4. **Evaluator**: Create `lib/evaluators/$dataset_id/$task.py` with an `Evaluator` class

5. **Visualizer** (optional): Create `lib/visualizers/$task.py`

## Directory Structure

- `configs/`: Configuration YAML files for different datasets
- `lib/csrc/`: CUDA extensions (dcn_v2, extreme_utils, roi_align_layer)
- `lib/datasets/`: Dataset implementations by data source (coco, cityscapes, kins, sbd, voc)
- `lib/networks/`: Network architectures by task (snake, rcnn_snake, ct_rcnn)
- `lib/train/`: Training utilities (trainers, optimizer, scheduler, recorder)
- `lib/evaluators/`: Evaluators by dataset
- `lib/visualizers/`: Visualization utilities
- `lib/utils/snake/`: Snake-specific utilities (config, poly utilities, evaluation)
- `data/`: Data storage (models, records, results - create symlinks to datasets here)