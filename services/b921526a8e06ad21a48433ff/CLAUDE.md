# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Deep Snake is a real-time instance segmentation algorithm (CVPR 2020). The codebase uses a modular plugin architecture with factory functions to dynamically load task-specific components.

## Commands

### Installation
```bash
# Create conda environment
conda create -n snake python=3.7
conda activate snake

# Install PyTorch and dependencies
pip install torch==1.1.0 -f https://download.pytorch.org/whl/cu90/stable
pip install -r requirements.txt

# Install NVIDIA Apex
cd external/apex && python setup.py install --cuda_ext --cpp_ext

# Compile CUDA extensions
cd lib/csrc/dcn_v2 && python setup.py build_ext --inplace
cd ../extreme_utils && python setup.py build_ext --inplace
cd ../roi_align_layer && python setup.py build_ext --inplace
```

### Training
```bash
# Single task training
python train_net.py --cfg_file configs/sbd_snake.yaml model sbd_snake

# Two-stage training (Cityscapes with R-CNN)
python train_net.py --cfg_file configs/city_ct_rcnn.yaml model rcnn_det
python train_net.py --cfg_file configs/city_rcnn_snake.yaml model rcnn_snake det_model rcnn_det

# Key training parameters (override via command line):
# train.lr, train.milestones, train.gamma, train.batch_size, train.epoch
```

### Testing
```bash
# Evaluate model
python run.py --type evaluate --cfg_file configs/city_rcnn_snake.yaml

# Speed test
python run.py --type network --cfg_file configs/city_rcnn_snake.yaml
```

### Visualization & Demo
```bash
# Visualize on test set
python run.py --type visualize --cfg_file configs/city_rcnn_snake.yaml test.dataset CityscapesTest ct_score 0.3

# Demo on images
python run.py --type demo --cfg_file configs/sbd_snake.yaml demo_path demo_images ct_score 0.3
```

### Monitoring
```bash
tensorboard --logdir data/record/rcnn_snake
```

## Architecture

The project follows a task-based plugin pattern where components are dynamically loaded based on `cfg.task` and dataset configuration.

### Core Directory Structure
```
lib/
├── config/           # YACS configuration system (cfg.py, yacs.py)
├── networks/         # Factory: make_network() loads from lib/networks/{task}/__init__.py
├── datasets/         # Factory: make_data_loader() loads from lib/datasets/{data_source}/{task}.py
├── evaluators/       # Factory: make_evaluator() loads from lib/evaluators/{data_source}/{task}.py
├── train/            # Trainer, optimizer, scheduler, recorder
│   └── trainers/     # Task-specific trainers in lib/train/trainers/{task}.py
├── visualizers/      # Factory: make_visualizer() loads from lib/visualizers/{task}.py
└── utils/            # Utility functions including snake-specific geometry utils
```

### Key Factory Patterns
- **Networks**: `lib.networks.{task}.get_network(cfg)` - returns `nn.Module`
- **Datasets**: `lib.datasets.{data_source}.{task}.Dataset` - extends `torch.utils.data.Dataset`
- **Evaluators**: `lib.evaluators.{data_source}.{task}.Evaluator` - implements `evaluate()` and `summarize()`
- **Trainers**: `lib.train.trainers.{task}.Trainer` - implements `train()` and `val()`
- **Visualizers**: `lib.visualizers.{task}.{task}.Visualizer` - implements `visualize()`

### Configuration System
- YAML config files in `configs/` define model, task, network, datasets
- `cfg.task` determines which plugin components are loaded
- `cfg.test.dataset` determines evaluator via `DatasetCatalog.get()` → `data_source`
- Override configs via CLI: `python train_net.py --cfg_file x.yaml train.lr 0.001`

### Adding New Components
1. **New task variant**: Create `lib/networks/{task}/__init__.py` with `get_network()`
2. **New dataset**: Register in `lib/datasets/dataset_catalog.py`, create `lib/datasets/{data_source}/{task}.py`
3. **New evaluator**: Create `lib/evaluators/{data_source}/{task}.py` with `Evaluator` class
4. **New trainer**: Create `lib/train/trainers/{task}.py` with `Trainer` class

### CUDA Extensions
Located in `lib/csrc/`: `dcn_v2`, `extreme_utils`, `roi_align_layer` - must be compiled before running.

### Data Paths
- Models: `data/model/{task}/{model_name}/`
- Records: `data/record/{task}/{model_name}/`
- Results: `data/result/{task}/{model_name}/`