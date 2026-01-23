# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DiffIR is an efficient diffusion model for image restoration (ICCV 2023). It consists of four task variants:
- **DiffIR-inpainting**: Image inpainting
- **DiffIR-SRGAN**: GAN-based single-image super-resolution
- **DiffIR-RealSR**: Real-world super-resolution
- **DiffIR-demotionblur**: Motion deblurring

## Installation

Each variant has its own `pip.sh` script. Common dependencies include:
- `basicsr>=1.3.3.11` - Core framework (install via pip.sh)
- `einops` - Tensor operations
- `lpips` - Perceptual similarity metrics
- `facexlib`, `gfpgan` - Face processing utilities

```bash
# Example for DiffIR-RealSR
cd DiffIR-RealSR
bash pip.sh
sudo python3 setup.py develop
```

## Common Commands

### Training (Two-Stage Process)

**Stage 1 - Pretrain DiffIR_S1:**
```bash
# Single GPU
python3 DiffIR/train.py -opt options/train_DiffIRS1_x4.yml

# Multi GPU (uses 8 GPUs by default)
sh trainS1.sh
```

**Stage 2 - Train DiffIR_S2 (Diffusion):**
```bash
# Set 'pretrain_network_g' and 'pretrain_network_S1' in options/train_DiffIRS2_x4.yml
sh trainS2.sh
```

**Stage 3 - Train DiffIR_S2_GAN (Optional, for perceptual quality):**
```bash
# Set pretrained paths in options/train_DiffIRS2_GAN_x4.yml
sh train_DiffIRS2_GAN.sh
```

### Testing
```bash
# Modify dataset path in options/test_DiffIRS2_GAN_x4.yml
sh test.sh

# Or run directly
python3 DiffIR/test.py -opt options/test_DiffIRS2_GAN_x4.yml
```

### Inference
```bash
python3 inference_diffir.py --im_path PathToLR --res_path ./outputs --model_path PathToModel --scale 4
```

### Metrics Calculation
```bash
python3 Metric/PSNR.py --folder_gt PathToGT --folder_restored PathToSR
python3 Metric/LPIPS.py --folder_gt PathToGT --folder_restored PathToSR
python3 Metric/dists.py --folder_gt PathToGT --folder_restored PathToSR
```

## Architecture

DiffIR consists of three core components:

1. **CPEN (Compact IR Prior Extraction Network)**: Extracts a compact IPR (IR Prior Representation) from ground-truth images (S1) or LQ images (S2)
2. **DIRformer (Dynamic IR Transformer)**: U-Net style transformer that takes LQ image and IPR to restore the image
3. **Denoising Network**: Predicts IPR in the diffusion process for S2

Key architecture files:
- `DiffIR/archs/S1_arch.py` - Stage 1 network (CPEN + DIRformer)
- `DiffIR/archs/S2_arch.py` - Stage 2 network (adds diffusion denoising)
- `DiffIR/archs/attention.py` - Attention mechanisms
- `DiffIR/models/DiffIRS*_model.py` - Training loops with degradation synthesis
- `ldm/ddpm.py` - Diffusion model implementation

## Training Pipeline

The training uses `basicsr` framework:
- Configs in `options/*.yml` define dataset paths, model architecture, losses, optimizers
- `DiffIR/train.py` calls `train_pipeline()` from `train_pipeline.py`
- `DiffIR/test.py` calls `test_pipeline()` from `basicsr`
- Synthetic degradations are applied on-the-fly during training (blur, noise, JPEG, resize)

## Data Preparation

Most tasks require preparing:
1. HR (ground-truth) images
2. Meta-info txt file with image paths
3. Optional: pre-cropped subimages and multi-scale versions

Each variant has specific README instructions for dataset setup.

## Key Configuration Options

Training options are YAML files with sections for:
- `datasets` - Training/validation data paths
- `model` - Network architecture settings (scale, dim, blocks, heads)
- `train` - Iterations, batch size, learning rate, schedulers
- `losses` - Pixel, perceptual, GAN losses
- `path` - Checkpoint and pretrain paths