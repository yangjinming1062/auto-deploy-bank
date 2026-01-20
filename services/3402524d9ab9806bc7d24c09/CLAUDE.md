# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

3DTopia-XL is a high-quality 3D PBR asset generation project using Primitive Diffusion (CVPR 2025). It converts 3D meshes into a "PrimX" token representation for diffusion training.

## Build & Install

```bash
bash install.sh
```
This compiles custom CUDA extensions (simple-knn, cubvh) and installs dependencies.

## Development Commands

### Run Web Demo
```bash
python app.py
```
Automatically downloads weights from HuggingFace (`frozenburning/3DTopia-XL`). Access at http://localhost:7860.

### Run CLI Inference
```bash
python inference.py ./configs/inference_dit.yml
```
Key config parameters:
- `ddim`: Steps (25-100)
- `cfg`: Classifier-free Guidance scale (4-7)
- `export_glb`: Export textured mesh

### Run Tests
Tests are not configured in this repository; validate changes using the CLI inference.

## Architecture

- **Model Definitions (`models/`):** Contains `dit_crossattn.py` (DiT generator), `vae3d_dib.py` (3D VAE), `primsdf.py` (Primitive SDF), and custom `diffusion/` and `conditioner/` modules.
- **Differentiable Rendering (`dva/`):** Core differentiable rendering engine (`mvp/`), ray marching, and neural layers.
- **Configuration (`configs/`):** OmegaConf YAML configs for training and inference. Stage configs (fitting, VAE, DiT) are separate.
- **Data Pipeline (`datasets/`):** PrimX volume handling and GLB processing.

## Training Pipeline

1. **Mesh Fitting:** Convert meshes to PrimX format (`train_fitting.py`).
2. **VAE Training:** Compress PrimX to latent space (`train_vae.py`, torchrun).
3. **Feature Caching:** Cache VAE and condition features before DiT training:
   ```bash
   python scripts/cache_vae.py configs/train_dit.yml
   python scripts/cache_conditioner.py configs/train_dit.yml
   ```
4. **DiT Training:** Train diffusion transformer (`train_dit.py`, torchrun).

## Key Configs

- `models/dit_crossattn.py:25`: DiT architecture (28 layers, 1152 hidden size).
- `models/primsdf.py:8`: PrimSDF config (2048 primitives, 6-dim features).