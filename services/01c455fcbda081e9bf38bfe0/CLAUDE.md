# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SE(3)-DiffusionFields: A PyTorch library for learning and sampling from diffusion models on SE(3), applied to 6D grasp distribution learning for robotic manipulation. Implements score-based diffusion on Lie groups (SO(3) + R³) combined with Signed Distance Fields (SDF).

## Installation

```bash
# Create conda environment
conda env create -f environment.yml
conda activate se3dif_env

# Install library
pip install -e .

# Install mesh_to_sdf dependency (separate repo)
git clone https://github.com/TheCamusean/mesh_to_sdf
pip install -e .
```

Note: `theseus-ai` pip package may have issues; install from source if needed: https://github.com/AI-App/Theseus

## Common Commands

### Training

Train pointcloud-conditioned SE(3) diffusion model:
```bash
python scripts/train/train_pointcloud_6d_grasp_diffusion.py --spec_file multiobject_p_graspdif
```

Train partial pointcloud-conditioned model:
```bash
python scripts/train/train_partial_pointcloud_6d_grasp_diffusion.py --spec_file multiobject_partialp_graspdif
```

Config files are in `scripts/train/params/` (e.g., `multiobject_p_graspdif/params.json`).

### Sampling / Inference

Sample grasps from full object pointcloud:
```bash
python scripts/sample/generate_pointcloud_6d_grasp_poses.py --n_grasps 10 --obj_id 0 --obj_class 'Mug'
```

Sample using class-specific model:
```bash
python scripts/sample/generate_pointcloud_6d_grasp_poses.py --n_grasps 10 --obj_id 10 --obj_class 'Mug' --model 'grasp_dif_mugs'
```

Sample from partial pointcloud:
```bash
python scripts/sample/generate_partial_pointcloud_6d_grasp_poses.py --n_grasps 10 --obj_id 12 --obj_class 'Mug'
```

### Data Preparation

Processed data based on Acronym and ShapeNet datasets should be downloaded and placed in the `data/` directory (sibling to the repository). See `scripts/create_data/README.md` for dataset preparation details.

### Evaluation

Isaac Gym simulation evaluation (requires Isaac Gym preview3 installed in conda environment):
```bash
python scripts/evaluate/evaluate_pointcloud_6d_grasp_poses.py --n_grasps 100 --obj_id 0 --obj_class 'Mug' --model 'grasp_dif_mugs' --device "cuda:0"
```

## Architecture

### Core Model Components (`se3dif/models/`)

- **grasp_dif.py**: `GraspDiffusionFields` - Main model combining:
  - `vision_encoder`: Encodes pointcloud/observation to latent code (VNNPointnet or LatentCodes)
  - `geometry_encoder`: Maps SE(3) poses to query points
  - `feature_encoder`: Time-conditioned MLP (`TimeLatentFeatureEncoder`)
  - `decoder`: Energy network predicting grasp quality

- **loader.py**: Model loading with `load_model(args)` - handles pretrained models and network architecture selection

### Datasets (`se3dif/datasets/`)

- **acronym_dataset.py**: Three dataset variants:
  - `AcronymAndSDFDataset`: Index-conditioned on object class
  - `PointcloudAcronymAndSDFDataset`: Multi-class with VNNPointnet encoder
  - `PartialPointcloudAcronymAndSDFDataset`: Partial view pointcloud conditioning

### Diffusion & Sampling (`se3dif/samplers/`)

- **grasp_samplers.py**: `Grasp_AnnealedLD` and `ApproximatedGrasp_AnnealedLD`
  - Annealed Langevin Dynamics sampling on SE(3)
  - Progressively reduces noise variance over T steps, then refines with T_fit steps

### Losses (`se3dif/losses/`)

- **denoising_loss.py**: Score matching losses
  - `SE3DenoisingLoss`: Full SE(3) denoising on Lie groups
  - `ProjectedSE3DenoisingLoss`: Projected version for efficiency

- **sdf_loss.py**: SDF reconstruction loss for implicit shape representation

### Utilities (`se3dif/utils/`)

- **directory_utils.py**: Data path configuration (`get_data_src()`, `get_pretrained_models_src()`)
- **geometry_utils.py**: SO(3) and SE(3) operations with Lie group math
- **torch_utils.py**: PyTorch convenience functions

### Training (`se3dif/trainer/`)

- **trainer.py**: Standard training loop with:
  - TensorBoard logging
  - Checkpointing (every N iterations and epochs)
  - Validation loop support
  - Gradient clipping option

## Data Directory Structure

```
data/
├── grasps/           # Acronym grasp datasets (.h5 files)
├── meshes/           # Object mesh files
├── sdf/              # Precomputed SDF data (.json via pickle)
├── models/           # Trained model checkpoints
└── train_data/       # Generated training data
```

## Key Dependencies

- PyTorch + torchvision
- pytorch3d
- theseus (Lie group operations)
- trimesh (mesh loading)
- h5py (grasp data format)
- configargparse (config files)
- tensorboard (logging)