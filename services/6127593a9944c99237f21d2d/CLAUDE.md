# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

DiffIR is an efficient diffusion model for image restoration that achieves SOTA performance on multiple tasks while consuming less computational costs. The repository contains four distinct image restoration tasks:

1. **Inpainting** (`DiffIR-inpainting/`): Fill in missing regions of images
2. **GAN-based single-image super-resolution** (`DiffIR-SRGAN/`): Enhance image resolution using GAN training
3. **Real-world super-resolution** (`DiffIR-RealSR/`): Real-world SR without paired LQ/GT data
4. **Motion deblurring** (`DiffIR-demotionblur/`): Remove motion blur from images

Each task directory is self-contained with its own configuration files, training scripts, and evaluation code.

## Key Components and Architecture

### Two-Stage Training Process

DiffIR uses a novel two-stage training approach:

**Stage 1 (Pretraining)**: Train the **Compact IR Prior Extraction Network (CPEN)** using ground-truth images to learn a compact Image Prior Representation (IPR)

**Stage 2 (Training DM)**: Train the **diffusion model** to estimate the same IPR using only LQ images

This approach is more efficient than traditional diffusion models because the IPR is a compact vector, requiring fewer iterations for accurate estimation.

### Core Architecture

- **`DiffIR/`**: Main implementation directory containing:
  - **`models/`**: Core model implementations
    - `DiffIR_S1_model.py`: Stage 1 model (CPEN)
    - `DiffIR_S2_model.py`: Stage 2 model (diffusion transformer)
    - `DiffIR_GAN_S2_model.py`: Stage 2 with GAN training
  - **`archs/`**: Network architectures
    - `S1_arch.py`: CPEN architecture with transformer blocks
    - `S2_arch.py`: Diffusion transformer (DIRformer)
    - `attention.py`: Attention mechanisms
    - `common.py`: Common building blocks
    - `discriminator_arch.py`: Discriminator for GAN training
  - **`data/`**: Data loading and augmentation
  - **`losses/`**: Loss functions
  - **`utils/`**: Utility functions

- **`ldm/`**: Latent diffusion model components
  - `ddpm.py`, `ddim.py`: Diffusion scheduling algorithms
  - `classifier.py`: Classifier for guidance
  - `util.py`, `util2.py`: Utility functions

- **`options/`**: YAML configuration files
  - `train_DiffIRS1_x*.yml`: Stage 1 training configs (x1, x2, x4 scales)
  - `train_DiffIRS2_*.yml`: Stage 2 training configs
  - `train_DiffIRS2_GAN_*.yml`: Stage 2 with GAN configs
  - `test_DiffIRS2_*.yml`: Testing configs

### Configuration Structure

All training uses YAML configuration files with these key sections:
- `network_g`: Generator network architecture parameters
- `datasets`: Data loading configuration (paths, transforms, batch size)
- `train`: Training settings (optimizer, scheduler, losses)
- `path`: Model checkpoint paths
- `val`: Validation settings

## Common Commands

### Installation

Each task has its own installation script:

```bash
# Inpainting
cd DiffIR-inpainting && bash pip.sh

# SRGAN
cd DiffIR-SRGAN && bash pip.sh

# RealSR
cd DiffIR-RealSR && bash pip.sh

# Motion deblurring
cd DiffIR-demotionblur && bash pip.sh
```

### Training Commands

All tasks follow a similar training pattern with slight variations:

#### Inpainting (CelebA dataset example)
```bash
cd DiffIR-inpainting

# Stage 1: Pretrain CPEN
bash train_celebahqS1.sh

# Convert Stage 1 model
python3 S1forS2.py  # Edit path in script first

# Stage 2: Train diffusion model
bash train_celebahqS2.sh
```

#### SRGAN
```bash
cd DiffIR-SRGAN

# Stage 1: Pretrain
bash trainS1.sh

# Stage 2: Train diffusion
# Edit options/train_DiffIRS2_x4.yml to set pretrained paths
bash trainS2.sh

# Stage 2: Train with GAN
# Edit options/train_DiffIRS2_GAN_x4.yml to set pretrained paths
bash trainS2.sh
```

#### RealSR
```bash
cd DiffIR-RealSR

# Stage 1: Pretrain
bash train_DiffIRS1.sh

# Stage 2: Train diffusion
# Edit options/train_DiffIRS2_x4.yml to set pretrained paths
bash train_DiffIRS2.sh

# Stage 2: Train with GAN
# Edit options/train_DiffIRS2_GAN_x4.yml to set pretrained paths
bash train_DiffIRS2_GAN.sh
# Or V2 version for better perceptual quality
bash train_DiffIRS2_GANv2.sh
```

#### Motion Deblurring
```bash
cd DiffIR-demotionblur

# Download and prepare data
python download_data.py --data train-test
python generate_patches_gopro.py

# Stage 1: Pretrain
bash trainS1.sh

# Stage 2: Train diffusion
# Edit options/train_DiffIRS2.yml to set pretrained paths
bash trainS2.sh
```

**Note**: All training scripts use 8 GPUs by default. Modify the scripts or configs to change GPU count:
- Training: Uses `torch.distributed.launch --nproc_per_node=N`
- Testing: Single GPU by default

### Testing Commands

```bash
# Inpainting
cd DiffIR-inpainting
bash test_place2_512_thick.sh

# SRGAN
cd DiffIR-SRGAN
bash test.sh

# RealSR
cd DiffIR-RealSR
bash test.sh

# Motion deblurring
cd DiffIR-demotionblur
bash test.sh
```

Before testing, ensure you've:
1. Downloaded pre-trained models from the provided Google Drive links
2. Placed models in `./experiments/`
3. Updated dataset paths in the test YAML configs

### Metric Calculation

```bash
# For SR tasks (SRGAN, RealSR)
python3 Metric/PSNR.py --folder_gt /path/to/GT --folder_restored /path/to/results
python3 Metric/LPIPS.py --folder_gt /path/to/GT --folder_restored /path/to/results
python3 Metric/dists.py --folder_gt /path/to/GT --folder_restored /path/to/results

# For motion deblurring
# Run MATLAB script
matlab -nodisplay -r "run('evaluate_gopro_hide.m'); exit;"
```

### Inference (RealSR)

```bash
cd DiffIR-RealSR

# 4x super-resolution
python3 inference_diffir.py --im_path /path/to/LR --res_path ./outputs --model_path /path/to/4xModel --scale 4

# 2x super-resolution
python3 inference_diffir.py --im_path /path/to/LR --res_path ./outputs --model_path /path/to/2xModel --scale 2

# 1x super-resolution
python3 inference_diffir.py --im_path /path/to/LR --res_path ./outputs --model_path /path/to/1xModel --scale 1
```

### Single GPU Training

For debugging or limited resources, all tasks support single GPU training:

```bash
cd DiffIR-RealSR

# Stage 1
python3 DiffIR/train.py -opt options/train_DiffIRS1_x4.yml
```

## Configuration Files

All configs are YAML files with these naming conventions:
- `train_DiffIRS1_x*.yml`: Stage 1 training (x1, x2, x4 scales)
- `train_DiffIRS2_*.yml`: Stage 2 training
- `train_DiffIRS2_GAN_*.yml`: Stage 2 with GAN
- `train_DiffIRS2_GAN_*_V2.yml`: V2 models (better perceptual quality)
- `test_DiffIRS2_*.yml`: Testing configuration

Key parameters to modify when fine-tuning:
- `dataroot_gt`: Path to ground-truth training data
- `meta_info`: Path to dataset metadata file
- `pretrain_network_g`: Path to Stage 2 pretrained model
- `pretrain_network_S1`: Path to Stage 1 pretrained model
- `pretrain_network_d`: Path to discriminator (for GAN training)

## Dataset Preparation

### RealSR
```bash
# Download DF2K (DIV2K + Flickr2K) + OST datasets
# Generate multi-scale images
python scripts/generate_multiscale_DF2K.py --input datasets/DF2K/DF2K_HR --output datasets/DF2K/DF2K_multiscale

# Crop to sub-images
python scripts/extract_subimages.py --input datasets/DF2K/DF2K_multiscale --output datasets/DF2K/DF2K_multiscale_sub --crop_size 400 --step 200

# Generate metadata
python scripts/generate_meta_info.py --input datasets/DF2K/DF2K_HR datasets/DF2K/DF2K_multiscale --root datasets/DF2K datasets/DF2K --meta_info datasets/DF2K/meta_info/meta_info_DF2Kmultiscale.txt
```

### Inpainting
```bash
# Places dataset
bash fetch_data/places_standard_train_prepare.sh
bash fetch_data/places_standard_test_val_prepare.sh

# CelebA dataset
bash fetch_data/celebahq_dataset_prepare.sh
```

## Dependencies

Core dependencies (see each task's `requirements.txt`):
- `basicsr>=1.3.3.11`: Base SR framework
- `torch>=1.7`: PyTorch
- `torchvision`: Computer vision utilities
- `tqdm`: Progress bars
- `opencv-python`: Image processing
- `Pillow`: Image handling
- `numpy`: Numerical operations
- `einops`: Tensor reshaping
- `lpips`: Perceptual loss

## Notes

- **V1 vs V2 models**: V2 models trade off some fidelity for better perceptual quality and denoising ability
- **Multi-scale training**: Each task supports x1, x2, x4 scaling factors
- **Distributed training**: Scripts use PyTorch DDP by default with 8 GPUs
- **Model checkpoints**: Automatically saved during training with EMA weights
- **Validation**: Can be enabled in config files for periodic validation during training