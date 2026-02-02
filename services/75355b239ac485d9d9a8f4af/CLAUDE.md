# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

traiNNer is an image/video restoration (super-resolution, denoising, deblurring) and image-to-image translation toolbox based on PyTorch. The codebase is modular, organized around five main components: Config, Data, DataOps, Model, and Network.

## Common Commands

**Training:**
```bash
# Train a model using a YAML configuration file
python train.py -opt options/sr/train_sr.yml

# Train with debug mode (includes "debug" in model name)
python train.py -opt options/sr/train_sr.yml

# Resume training from a previous state
python train.py -opt options/sr/train_sr.yml  # set resume_state in config
```

**Testing:**
```bash
# Test SR models (ESRGAN, PPON, PAN, etc.)
python test.py -opt options/sr/test_sr.yml

# Test SRFlow models
python test_srflow.py -opt options/srflow/test_srflow.yml

# Test video super-resolution
python test_vsr.py -opt options/video/test_video.yml

# Test SFTGAN (requires segmentation maps)
python test_seg.py
python test_sftgan.py
```

**Utility Scripts:**
```bash
# Create LMDB database for faster IO
python codes/scripts/create_lmdb.py

# Interpolate between two models
python codes/scripts/net_interp.py

# Extract kernels for blind SR (requires DLIP repo)
```

## Architecture

### Component Flow
Training follows this pipeline:
1. **Config** (`codes/options/options.py`) - Reads YAML/JSON configuration files
2. **Data** (`codes/data/`) - Creates train/val dataloaders from folders or LMDB
3. **DataOps** (`codes/dataops/`) - Augmentations, image resizing, filters
4. **Model** (`codes/models/`) - Instantiates model, loss functions, optimizer
5. **Network** (`codes/models/modules/architectures/`) - Creates neural network architecture

### Configuration Structure
All training/test settings are in YAML files under `codes/options/`:
- `scale`: Upsampling factor (1-4 for SR, 1 for restoration)
- `model`: sr, ppon, srflow, sftgan, cyclegan, pix2pix, vsr, etc.
- `datasets/train`: HR/LR paths, batch_size, crop_size, augmentations
- `path`: pretrained models, resume states, output directories
- `use_amp`: Enable automatic mixed precision (PyTorch 1.7+)
- `use_swa`: Enable stochastic weight averaging

### Supported Model Types
- **Super-Resolution**: ESRGAN, SRGAN, PAN, PPON, SFTGAN, SRFlow
- **Restoration**: Denoising, deblurring (1x scale SR networks)
- **Image-to-Image Translation**: pix2pix, CycleGAN, WBC (White-box Cartoonization)
- **Video**: SOFVSR, EDVR, DVD (video super-resolution and frame interpolation)

### Network Architectures
Located in `codes/models/modules/architectures/`:
- `RRDBNet_arch.py` - ESRGAN's Residual-in-Residual Dense Block network
- `PAN_arch.py` - Pixel Attention Network (lightweight)
- `discriminators.py` - Various GAN discriminators (PatchGAN, U-Net, etc.)
- `block.py` - Reusable network blocks (RRDB, Conv, Upsample)

### Augmentations
Three types of augmentations controlled via YAML presets:
1. **Image Augmentations** (`codes/dataops/augmentations.py`, `imresize.py`): noise, blur, downscaling kernels
2. **Batch Augmentations** (`codes/dataops/batchaug.py`): CutMix, MixUp, CutBlur, DiffAugment
3. **Differential Augmentations** (`codes/dataops/diffaug.py`): For discriminator regularization

Presets for blind SR (Real-SR, BSRGAN, Real-ESRGAN strategies) in `codes/options/presets/`.

## Data Requirements

**Folder Structure:**
```
datasets/
  train/
    hr1/, hr2/          # High-resolution images
    lr1/, lr2/          # Low-resolution images (optional, can generate on-the-fly)
  val/
    hr/, lr/            # Validation pairs
```

**LMDB Support:** Use `create_lmdb.py` for faster IO, especially on HDDs.

**Image Format:** NCHW tensor, [0,1] range, RGB. Use `znorm: true` for [-1,1] range.

## Key Files

- `codes/train.py` - Main training loop with logging, validation, LR scheduling
- `codes/test.py` - Inference with automatic metrics (PSNR, SSIM, LPIPS)
- `codes/models/base_model.py` - Base model class; `sr_model.py` for most SR models
- `codes/data/create_dataset.py` - Dataset factory; `data/__init__.py` for available datasets
- `codes/dataops/common.py` - Tensor/image conversion utilities

## Notable Conventions

- `crop_size` in SR refers to HR crop size; LR size is `crop_size / scale`
- Model name containing "debug" triggers debug mode (disables tb_logger, etc.)
- Presets can be combined with `augs_strategy: combo` for multiple augmentation types
- Use `preprocess: resize_and_crop` (default) or other options in `data/augmentations.py`
- Pretrained models go in `experiments/pretrained_models/` by default

## Dependencies

Core: PyTorch, PyYAML, numpy, opencv-python, tensorboardX

Optional: lmdb (LMDB support), scipy (CEM module), Pillow (alternative image backend), joblib (WBC models)