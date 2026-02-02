# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Multi-Code GAN Prior** repository for image processing using GAN inversion. The core idea is to invert images into multiple latent codes that can be used for various downstream tasks: colorization, super-resolution, inpainting, and semantic face editing.

## Dependencies

```bash
python -m pip install -r requirements.txt
```

**Note:** Requires CUDA 10.1 with PyTorch 1.1.0 and TensorFlow-GPU < 2.

## Pre-trained Models

GAN models (PGGAN, StyleGAN, StyleGAN2) must be downloaded and placed in `models/pretrain/`. PyTorch checkpoints go in `models/pretrain/pytorch/` and TensorFlow checkpoints in `models/pretrain/tensorflow/`. Available models are registered in `models/model_settings.py` under `MODEL_POOL`.

## Common Commands

### Image Inversion
```bash
python multi_code_inversion.py \
    --gan_model pggan_bedroom \
    --target_images ./examples/gan_inversion/bedroom \
    --outputs ./gan_inversion_bedroom \
    --composing_layer 8 \
    --z_number 20
```

### Colorization
```bash
python colorization.py \
    --gan_model pggan_bedroom \
    --target_images ./examples/colorization/bedroom \
    --outputs ./colorization \
    --composing_layer 6 \
    --z_number 20
```

### Inpainting
```bash
python inpainting.py \
    --gan_model pggan_churchoutdoor \
    --target_images ./examples/inpainting/church \
    --outputs ./inpainting \
    --mask ./examples/masks/mask-1.png \
    --composing_layer 4 \
    --z_number 30
```

### Super-Resolution
```bash
python super_resolution.py \
    --gan_model pggan_celebahq \
    --target_images ./examples/superresolution \
    --outputs ./SR_face \
    --factor 16 \
    --composing_layer 6 \
    --z_number 20
```

### Semantic Face Editing
```bash
python face_semantic_editing.py \
    --gan_model pggan_celebahq \
    --target_images ./examples/face \
    --outputs ./face_manipulation \
    --attribute_name gender \
    --composing_layer 6 \
    --z_number 30
```

## Architecture

### Core Pipeline

All applications follow this flow:
1. **Generator selection** via `get_derivable_generator()` from `derivable_models/derivable_generator.py`
2. **Loss function selection** via `get_loss()` from `inversion/losses.py`
3. **Optimization setup** via `get_inversion()` from `inversion/inversion_methods.py`
4. **Run inversion** to find latent codes that minimize the loss against target image
5. **Generate results** using the inverted latent codes

### Key Modules

| Directory | Purpose |
|-----------|---------|
| `derivable_models/` | Generator wrappers that support different latent space types (z, w, w+, Multi-Z) |
| `inversion/` | Optimization-based inversion methods (GD, Adam) and loss functions (L1, L2, VGG, Combine) |
| `models/` | GAN model implementations (PGGAN, StyleGAN, StyleGAN2) and `MODEL_POOL` configuration |
| `utils/` | Image I/O, preprocessing, and manipulation utilities |

### Latent Space Types

- **PGGAN-z / StyleGAN-z**: Single 512-dim latent vector
- **StyleGAN-w**: Single 512-dim w-space vector
- **StyleGAN-w+**: Per-layer w vectors `(18, 512)` for StyleGAN
- **PGGAN-Multi-Z**: Multiple latent codes (default 20-30) blended at a composing layer

### Multi-Code GAN Inversion

The key innovation is using multiple latent codes (`z_number`) that are blended at a specified `composing_layer`. Each code generates a feature map that is weighted by an alpha coefficient and summed before passing through the remaining generator layers. This allows more flexible reconstruction of complex images.

### Loss Functions

- **VGG**: Perceptual loss using pre-trained VGG-16 (layer 16 by default)
- **L1/L2**: Pixel-wise losses
- **Combine**: Weighted sum of L1, L2, and VGG losses

### Key Arguments

| Argument | Description |
|----------|-------------|
| `--gan_model` | Which GAN to use (e.g., `pggan_celebahq`, `pggan_churchoutdoor`) |
| `--inversion_type` | Latent space type (`PGGAN-Multi-Z`, `StyleGAN-w+`, etc.) |
| `--composing_layer` | Layer where multiple latent codes are blended |
| `--z_number` | Number of latent codes in multi-code inversion |
| `--iterations` | Optimization iterations (1000-3000 typical) |
| `--lr` | Learning rate for optimization |

## Semantic Boundaries

Face editing uses pre-trained semantic boundaries in `boundaries/` (gender, age, expression, pose). These are NumPy `.npy` files used with `get_boundary()` and `get_interpolated_wp()` in `utils/manipulate.py`.