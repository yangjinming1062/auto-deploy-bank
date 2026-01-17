# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the official implementation of **"Cameras as Rays: Pose Estimation via Ray Diffusion"** (ICLR 2024), which introduces a diffusion-based approach for camera pose estimation. The method treats camera poses as rays and uses a DiT (Diffusion Transformer) architecture to generate camera poses.

**Key Resources:**
- [arXiv Paper](https://arxiv.org/abs/2402.14817)
- [Project Page](https://jasonyzhang.com/RayDiffusion/)
- [Colab Demo](https://colab.research.google.com/drive/1dqp9qnFyHA71y3motSoJpJFBHZVftXzb?usp=sharing)

## Development Environment

### Setup
```bash
# Create conda environment
conda create -n raydiffusion python=3.10
conda activate raydiffusion

# Install PyTorch (adjust CUDA version as needed)
conda install pytorch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 pytorch-cuda=11.8 -c pytorch -c nvidia

# Install dependencies
conda install xformers -c xformers
pip install -r requirements.txt

# Install PyTorch3D (use pre-built wheel for your CUDA version)
pip install --no-index --no-cache-dir pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py310_cu118_pyt211/download.html
```

### Code Quality
- **Linter**: `ruff` (configured in `ruff.toml`)
- **Run linter**: `ruff check .`
- **Apply fixes**: `ruff check --fix .`

## Project Structure

```
ray_diffusion/           # Main Python package
├── dataset/            # Data loading (CO3D v2, custom datasets)
├── eval/               # Evaluation scripts
├── inference/          # Model inference (DDPM, prediction)
├── model/              # Core models (DiT, diffuser, scheduler)
└── utils/              # Utilities (rays, normalization, visualization)

conf/
└── config.yaml         # Default Hydra configuration

train.py                # Training script
demo.py                 # Inference/demo script
preprocess_co3d.py      # CO3D dataset preprocessing

examples/               # Example datasets
├── robot/              # Example: robot images with bboxes
├── human-toy/          # Example: human-toy images
└── espresso/           # Example: espresso images

docs/
├── train.md            # Detailed training instructions
└── eval.md             # Evaluation instructions
```

## Common Commands

### Training

**Ray Diffusion Model** (main method):
```bash
accelerate launch --multi_gpu --gpu_ids 0,1,2,3,4,5,6,7 --num_processes 8 train.py \
    training.batch_size=8 training.max_iterations=450000
```

**Ray Regression Model** (baseline):
```bash
accelerate launch --multi_gpu --gpu_ids 0,1,2,3,4,5,6,7 --num_processes 8 train.py \
    training.batch_size=8 training.max_iterations=300000 training.regression=True
```

**Single GPU (for debugging)**:
```bash
accelerate launch train.py training.batch_size=4 dataset.category=apple debug.wandb=False hydra.run.dir=output_debug
```

**Resume training**:
```bash
accelerate launch train.py training.resume=True hydra.run.dir=/path/to/output_dir
```

### Dataset Preprocessing

**CO3D v2 Dataset** (before training):
```bash
# Pre-compute bounding boxes
python preprocess_co3d.py --category all --precompute_bbox --co3d_v2_dir /path/to/co3d_v2

# Preprocess annotations
python preprocess_co3d.py --category all --co3d_v2_dir /path/to/co3d_v2
```

### Running Demos

**With known bounding boxes**:
```bash
python demo.py --model_dir models/co3d_diffusion \
    --image_dir examples/robot/images \
    --bbox_path examples/robot/bboxes.json \
    --output_path robot.html
```

**With automatic mask-based bbox detection**:
```bash
python demo.py --model_dir models/co3d_diffusion \
    --image_dir examples/robot/images \
    --mask_dir examples/robot/masks \
    --output_path robot.html
```

**Ray regression model**:
```bash
python demo.py --model_dir models/co3d_regression \
    --image_dir examples/robot/images \
    --bbox_path examples/robot/bboxes.json \
    --output_path robot.html
```

### Evaluation

**Diffusion model**:
```bash
python -m ray_diffusion.eval.eval_jobs --eval_type diffusion --eval_path models/co3d_diffusion
```

**Regression model**:
```bash
python -m ray_diffusion.eval.eval_jobs --eval_type regression --eval_path models/co3d_regression
```

## Architecture

### Core Components

1. **Model Architecture** (`ray_diffusion/model/`):
   - **DiT (Diffusion Transformer)**: Adapted from facebookresearch/DiT, with adaptive layer norm zero conditioning
   - **RayDiffuser**: Main diffusion model that predicts camera poses
   - **NoiseScheduler**: Handles noise scheduling (linear, cosine)
   - **Feature Extractors**: DINO-based image feature extraction

2. **Training Pipeline** (`train.py`):
   - Uses **Hydra** for configuration management (see `conf/config.yaml`)
   - Uses **Accelerate** for distributed training across multiple GPUs
   - Supports both diffusion and regression training modes
   - Implements training visualizations, checkpointing, and W&B logging

3. **Inference Pipeline** (`demo.py`):
   - Loads pre-trained models
   - Processes images with optional bounding boxes or masks
   - Generates camera pose predictions
   - Outputs interactive HTML visualizations using Plotly

4. **Dataset Handling** (`ray_diffusion/dataset/`):
   - **Co3dDataset**: Loads and processes CO3D v2 dataset
   - **CustomDataset**: Handles custom image datasets for inference

5. **Evaluation** (`ray_diffusion/eval/`):
   - Evaluates rotation accuracy and camera center accuracy
   - Reports metrics for seen and unseen object categories
   - Can be parallelized using submitit

6. **Key Utilities** (`ray_diffusion/utils/`):
   - **rays.py**: Converts between camera parameters and ray representations
   - **normalize.py**: Normalization utilities for camera batches
   - **bbox.py**: Bounding box utilities
   - **visualization.py**: Creates Plotly visualizations

### Configuration System

The project uses **Hydra** for hierarchical configuration management:

- **Main config**: `conf/config.yaml`
- **Override parameters**: Passed via command line (e.g., `training.batch_size=8`)
- **Key config sections**:
  - `training`: batch size, iterations, learning rate, checkpointing
  - `model`: DiT architecture parameters (depth, num_patches, feature extractor)
  - `noise_scheduler`: DDPM noise scheduling parameters
  - `dataset`: Dataset name, category, augmentation settings
  - `debug`: W&B logging, anomaly detection

### Model Types

1. **Diffusion Model** (default):
   - Uses DDPM to iteratively refine camera pose predictions
   - Trained for 450K iterations
   - Supports variable number of input images (random_num_images=True)

2. **Regression Model** (baseline):
   - Direct pose regression from images
   - Trained for 300K iterations
   - Generally faster inference but lower accuracy

## Key Implementation Details

- **Input Representation**: Images are converted to ray representations via `cameras_to_rays()` in `ray_diffusion/utils/rays.py:1`
- **Conditioning**: Image features from DINO are used to condition the diffusion process
- **Attention**: Supports both standard attention and memory-efficient xformers attention
- **Patch Processing**: Images are processed as patches (default 16x16) in the DiT architecture
- **Multi-GPU Training**: Uses Accelerate with specific GPU ID configuration

## Common Development Tasks

### Modifying Model Architecture
- **DiT Block**: `ray_diffusion/model/dit.py:61` - Main transformer block with adaLN-Zero conditioning
- **Feature Extractor**: `ray_diffusion/model/feature_extractors.py` - Currently uses DINO
- **Model Parameters**: Modify in `conf/config.yaml` or via command line

### Adding New Datasets
- Implement new dataset class in `ray_diffusion/dataset/custom.py`
- Follow the pattern of `CustomDataset` or `Co3dDataset`
- Ensure proper bbox/mask handling for inference

### Debugging Training
- Use single GPU mode for debugging
- Set `debug.wandb=False` to disable logging
- Use `debug.anomaly_detection=True` for gradient checking
- Check `hydra.run.dir` output for detailed logs

### Evaluation Metrics
- See `ray_diffusion/eval/eval_category.py` for metric computation
- Rotation accuracy and camera center accuracy are the primary metrics
- Results are reported for both seen and unseen object categories

## Notes

- **Hardware**: Trained on 4 A6000 GPUs with total batch size of 64
- **Mixed Precision**: Supports AMP, but can be disabled if encountering NaNs
- **Memory Optimization**: Uses xformers for memory-efficient attention
- **W&B Integration**: Enabled by default, can be disabled for debugging
- **Checkpoint Management**: Automatic checkpointing with configurable intervals