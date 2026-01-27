# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Panoptic Lifting is a CVPR 2023 paper implementation for 3D scene understanding using neural radiance fields. It lifts noisy 2D panoptic segmentation masks into a consistent 3D panoptic radiance field that can be queried for color, depth, semantics, and instances at any point in space.

## Dependencies

```bash
pip install -r requirements.txt
```

## Common Commands

### Training
```bash
python trainer/train_panopli_tensorf.py experiment=<NAME> dataset_root=<PATH> wandb_main=True <HYPERPARAMS>
```

Example training configurations:
```bash
# ScanNet
python trainer/train_panopli_tensorf.py experiment=scannet042302 wandb_main=True batch_size=4096 dataset_root="data/scannet/scene0423_02/"

# Replica
python trainer/train_panopli_tensorf.py experiment=replicaroom0 wandb_main=True batch_size=4096 dataset_root="data/replica/room_0/" lambda_segment=0.75

# HyperSim
python trainer/train_panopli_tensorf.py experiment=hypersim001008 wandb_main=True dataset_root="data/hypersim/ai_001_008/" lambda_dist_reg=0 val_check_interval=1 instance_optimization_epoch=4 batch_size=2048 max_epoch=34

# Self-captured (in-the-wild)
python trainer/train_panopli_tensorf.py experiment=itw_office0213 wandb_main=True batch_size=8192
```

### Rendering/Inference
```bash
python inference/render_panopli.py <PATH_TO_CHECKPOINT> <IF_TEST_MODE>
```
- `<PATH_TO_CHECKPOINT>`: Path to `.ckpt` checkpoint file
- `<IF_TEST_MODE>`: `True` to render test set, `False` to render custom trajectory

Output is saved to `runs/<experiment>/`.

### Evaluation
```bash
python inference/evaluate.py --root_path <DATA_PATH> --exp_path <RENDER_OUTPUT_PATH>
```

## Architecture

### Core Pipeline
- **`trainer/train_panopli_tensorf.py`**: Main training entry point with `TensoRFTrainer` (PyTorch Lightning module)
  - Handles multi-task loss: RGB reconstruction, semantic segmentation, instance clustering
  - Manages grid upsampling during training
  - Uses 3 dataloaders: main rays, instance features, segment features

### Model Components
- **`model/radiance_field/tensoRF.py`**: `TensorVMSplit` - TensoRF-based radiance field representation
  - Separates density, appearance (RGB), semantics, and instance features into plane/line coefficients
  - Uses MLPs to decode features to final outputs
  - Supports grid upsampling and bounding box shrinkage

- **`model/renderer/panopli_tensoRF_renderer.py`**: Ray marching renderer
  - Samples points along rays through the volumetric representation
  - Accumulates color, density, semantics, and instance features

### Dataset System
- **`dataset/panopli.py`**: `PanopliDataset` - Main dataset class for all scene types
  - Supports ScanNet, Replica, HyperSim, and in-the-wild captures
  - Loads posed RGB images, 2D panoptic segmentation, instance labels, and semantic probabilities
  - Uses test-time augmented (TTA) mask2former outputs with confidence scores

- **`dataset/base.py`**: Base dataset class handling ray generation and camera transforms

### Configuration
- **`config/panopli.yaml`**: Hydra configuration for all training hyperparameters
  - Key parameters: `lambda_segment`, `lambda_semantics`, `lambda_instances`, `lambda_rgb`
  - Grid parameters: `min_grid_dim`, `max_grid_dim`, `grid_upscale_epochs`
  - Dataset parameters: `dataset_root`, `image_dim`, `max_depth`

## Key Conventions

- **Multi-task training**: Optimizes RGB + semantics + instance clustering simultaneously
- **Confidence-weighted losses**: Uses 2D segmentation confidences to weight loss contributions
- **Segment grouping**: Groups semantically similar rays for consistency optimization
- **Instance optimization**: Uses linear assignment to match predicted instances with 2D labels
- **Grid upsampling**: Volume grid grows progressively during training via `grid_upscale_epochs`

## Data Structure (after preprocessing)

```
data/<dataset>/<scene>/
├── color/              # RGB images
├── pose/               # Camera poses (txt)
├── intrinsic/          # Camera intrinsics
├── depth/              # Depth maps (optional)
├── filtered_semantics/ # Semantic segmentation masks (PNG)
├── filtered_instance/  # Instance ID masks (PNG)
├── <dataset>_probabilities/  # Semantic probabilities (NPZ)
├── segmentation_data.pkl      # Class and instance mappings
└── splits.json         # Train/val/test splits
```

## Implementation Details

- Uses `hydra-core` for configuration management (config path: `config/panopli.yaml`)
- Logging via Weights & Biases (set `wandb_main=True` for main project)
- Checkpoints saved to `runs/<experiment>/checkpoints/`
- Custom `SCELoss` for symmetric cross-entropy in `model/loss/loss.py`
- Total variation regularizers for density, semantics, and appearance fields