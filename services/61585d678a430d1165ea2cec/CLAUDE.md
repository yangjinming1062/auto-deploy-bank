# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RayDiffusion is a camera pose estimation research codebase implementing "Cameras as Rays: Pose Estimation via Ray Diffusion" (ICLR 2024). The method uses diffusion models to predict camera poses from input images by first converting cameras to ray representations (plucker coordinates) on the image plane.

## Development Commands

```bash
# Install dependencies
conda create -n raydiffusion python=3.10
conda activate raydiffusion
conda install pytorch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 pytorch-cuda=11.8 -c pytorch -c nvidia
conda install xformers -c xformers
pip install -r requirements.txt
pip install --no-index --no-cache-dir pytorch3d -f https://dl.fbaipublicfiles.com/pytorch3d/packaging/wheels/py310_cu118_pyt211/download.html

# Linting
ruff check .
black .

# Training (multi-GPU)
accelerate launch --multi_gpu --gpu_ids 0,1,2,3,4,5,6,7 --num_processes 8 train.py \
    training.batch_size=8 training.max_iterations=450000

# Training regression model
accelerate launch --multi_gpu --gpu_ids 0,1,2,3,4,5,6,7 --num_processes 8 train.py \
    training.batch_size=8 training.max_iterations=300000 training.regression=True

# Debug training (single GPU, single category)
accelerate launch train.py training.batch_size=4 dataset.category=apple debug.wandb=False \
    hydra.run.dir=output_debug

# Resume training from checkpoint
accelerate launch train.py training.resume=True hydra.run.dir=/path/to/output_dir

# Run demo (with bboxes from JSON)
python demo.py --model_dir models/co3d_diffusion --image_dir examples/robot/images \
    --bbox_path examples/robot/bboxes.json --output_path robot.html

# Run demo (with masks - bboxes extracted automatically)
python demo.py --model_dir models/co3d_diffusion --image_dir examples/robot/images \
    --mask_dir examples/robot/masks --output_path robot.html

# Run demo with regression model (single-step prediction)
python demo.py --model_dir models/co3d_regression --image_dir examples/robot/images \
    --bbox_path examples/robot/bboxes.json --output_path robot.html

# Evaluation
python -m ray_diffusion.eval.eval_jobs --eval_type diffusion --eval_path models/co3d_diffusion
python -m ray_diffusion.eval.eval_jobs --eval_type regression --eval_path models/co3d_regression

# CO3D preprocessing
python preprocess_co3d.py --category all --precompute_bbox --co3d_v2_dir /path/to/co3d_v2
python preprocess_co3d.py --category all --co3d_v2_dir /path/to/co3d_v2
```

## Architecture

```
ray_diffusion/
├── dataset/
│   ├── co3d_v2.py          # CO3Dv2 dataset loader with camera intrinsics and augmentation
│   └── custom.py           # Custom dataset for inference/demo
├── model/
│   ├── diffuser.py         # RayDiffuser wrapper: feature extraction + noise scheduling
│   ├── dit.py              # DiT (Diffusion Transformer) backbone adapted from DiT
│   ├── scheduler.py        # NoiseScheduler for DDPM forward process
│   └── feature_extractors.py  # DINO-based spatial feature extractor
├── inference/
│   ├── load_model.py       # Model checkpoint loading with config preservation
│   ├── ddpm.py             # DDPM sampling loop (denoising trajectory)
│   └── predict.py          # High-level prediction interface handling regression/diffusion
├── eval/
│   ├── eval_category.py    # Per-category evaluation metrics
│   ├── eval_jobs.py        # Batch evaluation orchestration
│   └── utils.py            # Evaluation utilities
├── utils/
│   ├── rays.py             # Ray classes, plucker/coordinate conversions, camera-ray transforms
│   ├── normalize.py        # Camera batch normalization and alignment
│   ├── bbox.py             # Bounding box utilities
│   └── visualization.py    # Plotly visualizations and training logging
└── conf/
    └── config.yaml         # Hydra configuration for all training/hyperparameters
```

### Key Data Flow

1. **Input**: Images (B, N, 3, H, W) with camera intrinsics (focal_length, principal_point) and extrinsics (R, T)
2. **Ray Conversion**: `cameras_to_rays()` converts cameras to plucker coordinates on image grid
3. **Features**: `SpatialDino` extracts per-image patch features (B, N, feature_dim, 16, 16)
4. **Model Forward**: Concatenate features + noisy rays + optional NDC coordinates
5. **DiT Processing**: Transformer with adaptive layer norm zero (adaLN-Zero) conditioning on timestep
6. **Output**: Predicted ray noise (epsilon) or direct ray prediction (x0)
7. **Post-processing**: `rays_to_cameras()` converts predicted rays back to camera extrinsics via optimal rotation alignment

### Key Classes

- **RayDiffuser**: Main model wrapper combining feature extractor, noise scheduler, and DiT backbone
- **DiT**: Diffusion Transformer with PatchEmbed, sinusoidal timestep embedding, configurable depth/width/heads
- **Co3dDataset**: PyTorch Dataset for CO3Dv2 with bbox cropping, augmentation, and camera normalization
- **NoiseScheduler**: Linear/cosine beta schedule for DDPM diffusion process

### Configuration

Uses Hydra for configuration management. Key config groups:
- `training`: batch_size, max_iterations, mixed_precision, learning rate
- `model`: model_type, depth, num_patches, feature_extractor
- `noise_scheduler`: type, max_timesteps, beta bounds
- `dataset`: category, augmentation, num_images

Override via command line: `train.py training.batch_size=4 dataset.category=apple`

### Important Patterns

- Ray representations use plucker coordinates (directions + moments) for 6D ray representation. Moments = origin × direction, making rays canonical for learning
- NDC (Normalized Device Coordinates) are appended as additional conditioning for crop-aware patch position predictions
- Multi-GPU training via `accelerate` with automatic mixed precision (AMP)
- Training visualizations logged to Weights & Biases
- Checkpoints saved at configurable intervals with metadata (iteration, wandb_id) for resumption
- `pred_x0` mode predicts clean rays directly instead of noise (useful for regression)
- `random_num_images` allows training with varying numbers of input images (2-8)