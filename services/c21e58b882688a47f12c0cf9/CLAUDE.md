# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Swin Transformer is a hierarchical vision transformer that uses shifted windows for efficient attention computation. This repository contains implementations for ImageNet classification with multiple model variants:
- **Swin Transformer** (swin) - Original Swin Transformer
- **Swin Transformer V2** (swinv2) - Improved version with better scaling
- **Swin-MoE** (swin_moe) - Mixture-of-Experts variant using Tutel
- **SwinMLP** (swin_mlp) - MLP-based variant replacing attention with MLPs
- **SimMIM** - Masked Image Modeling for self-supervised pre-training

## Common Commands

### Setup
```bash
# Install dependencies
pip install opencv-python==4.4.0.46 termcolor==1.1.0 yacs==0.1.8 pyyaml scipy timm==0.4.12

# Install fused window process for acceleration (optional)
cd kernels/window_process
python setup.py install
```

### Training (ImageNet-1K)
```bash
# Standard training with 8 GPUs
python -m torch.distributed.launch --nproc_per_node 8 --master_port 12345 main.py \
--cfg configs/swin/swin_tiny_patch4_window7_224.yaml --data-path <imagenet-path>

# With zipped dataset
python -m torch.distributed.launch --nproc_per_node 8 main.py --cfg <config> --data-path <path> --zip

# With gradient checkpointing (memory efficient)
python -m torch.distributed.launch --nproc_per_node 8 --use-checkpoint

# With gradient accumulation
python -m torch.distributed.launch --nproc_per_node 8 --accumulation-steps 4
```

### Evaluation
```bash
python -m torch.distributed.launch --nproc_per_node 1 --master_port 12345 main.py --eval \
--cfg configs/swin/swin_base_patch4_window7_224.yaml \
--resume swin_base_patch4_window7_224.pth --data-path <imagenet-path>
```

### Throughput Benchmark
```bash
python -m torch.distributed.launch --nproc_per_node 1 main.py \
--cfg <config> --data-path <imagenet-path> --batch-size 64 --throughput --disable_amp
```

### SimMIM Pre-training
```bash
# Pre-train Swin-B for 800 epochs
python -m torch.distributed.launch --nproc_per_node 16 main_simmim_pt.py \
--cfg configs/simmim/simmim_pretrain__swin_base__img192_window6__800ep.yaml \
--batch-size 128 --data-path <imagenet-path>/train
```

### SimMIM Fine-tuning
```bash
python -m torch.distributed.launch --nproc_per_node 16 main_simmim_ft.py \
--cfg configs/simmim/simmim_finetune__swin_base__img224_window7__800ep.yaml \
--batch-size 128 --data-path <imagenet-path> --pretrained <pretrained-ckpt>
```

### Swin-MoE Training
Requires [Tutel](https://github.com/microsoft/tutel):
```bash
python -m torch.distributed.launch --nproc_per_node 8 --nnode=4 \
--node_rank=<node-rank> --master_addr=<master-ip> main_moe.py \
--cfg configs/swinmoe/swin_moe_small_patch4_window12_192_32expert_32gpu_22k.yaml \
--data-path <imagenet22k-path> --batch-size 128
```

## Architecture Overview

### Entry Points
- **main.py** - Main training script for standard Swin models
- **main_moe.py** - Training script for Swin-MoE models
- **main_simmim_pt.py** - Pre-training script for SimMIM
- **main_simmim_ft.py** - Fine-tuning script for SimMIM models

### Configuration System
- Uses **YACS** (YAML-based configuration)
- Configs located in `configs/` directory organized by model type
- Each config file inherits BASE defaults and overrides specific parameters
- Common settings: `DATA`, `MODEL`, `TRAIN`, `AUG`, `TEST`, `OUTPUT`

### Key Configuration Options
```yaml
DATA:
  BATCH_SIZE: 128      # Per-GPU batch size
  IMG_SIZE: 224        # Input image resolution
  DATA_PATH: ''        # Dataset path
  ZIP_MODE: False      # Use zipped ImageNet
  CACHE_MODE: 'part'   # Cache strategy (no, full, part)

MODEL:
  TYPE: 'swin'         # Model variant type
  SWIN:                # Model-specific params
    EMBED_DIM: 96
    DEPTHS: [2, 2, 6, 2]
    NUM_HEADS: [3, 6, 12, 24]
    WINDOW_SIZE: 7

TRAIN:
  EPOCHS: 300
  BASE_LR: 5e-4
  USE_CHECKPOINT: False  # Memory optimization
  ACCUMULATION_STEPS: 1  # Gradient accumulation
```

### Model Factory (`models/build.py`)
- `build_model(config, is_pretrain=False)` - Factory function creating models
- Each model type (swin, swinv2, swin_moe, swin_mlp) has its own class
- Model-specific parameters passed directly from config

### Data Loading (`data/build.py`)
- Supports ImageNet-1K and ImageNet-22K datasets
- Optional zip mode for faster I/O with cached sharding
- Mixup/Cutmix augmentation via `timm.data.Mixup`
- Distributed training with `DistributedSampler`

### Utility Modules
- **lr_scheduler.py** - Cosine and step-based learning rate schedules
- **optimizer.py** - AdamW, SGD with optional fused implementations
- **utils.py** - Checkpoint loading/saving, distributed utilities, gradient scaling
- **utils_moe.py** - MoE-specific utilities for load balancing and expert routing

### CUDA Kernels (`kernels/window_process/`)
- Custom fused window shift/partition kernels for acceleration
- Installed separately via `setup.py`
- Activated with `--fused_window_process` flag

## Distributed Training Notes

- Uses `torch.distributed.launch` with NCCL backend
- Global batch size = `BATCH_SIZE * WORLD_SIZE`
- Learning rate is automatically scaled: `BASE_LR * WORLD_SIZE * BATCH_SIZE / 512`
- Only rank 0 saves checkpoints by default (set `TRAIN.MOE.SAVE_MASTER` for MoE)