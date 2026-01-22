# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Ruyi-Models contains the Ruyi-Mini-7B image-to-video generation model and a ComfyUI wrapper. The model generates 120-frame, 24fps videos (5 seconds) at 512x512 or 768x768 resolution.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run standalone inference (uses assets/ folder for input images)
python predict_i2v.py

# Run inference optimized for >80G GPU memory
python predict_i2v_80g.py
```

## Architecture

- **`ruyi/`**: Core library
  - **`pipeline/`**: Inference pipeline definitions
  - **`models/`**: Core model components (Transformer3D, Motion Module, VAE, Attention)
  - **`utils/`**: Diffusion scheduling, LoRA utilities, Gaussian diffusion
  - **`vae/`**: Custom Autoencoder (MagViT) implementation
- **`comfyui/`**: ComfyUI custom node implementation
  - `comfyui_nodes.py`: Defines `Load Model`, `Load LoRA`, and `Sampler` nodes
  - `workflows/`: JSON workflow definitions for the UI

## Key Configuration

- **Model Path**: Default is `Ruyi-Models/models/` or `ComfyUI/models/Ruyi/`
- **Auto-download**: Models are auto-downloaded from HuggingFace (`IamCreateAI/Ruyi-Mini-7B`) if missing
- **GPU Memory Modes**:
  - `normal_mode`: Faster generation, higher VRAM usage
  - `low_memory_mode`: Slower generation, significantly reduced VRAM usage
  - `GPU_offload_steps`: 0-10, trades off speed for VRAM

## Important Parameters

- `video_length`: Must be multiple of 8, max 120 frames
- `base_resolution`: 512 or 768
- `steps`: Generation iterations (25 is typical)
- `cfg`: Guidance scale (7-10 recommended)
- `motion`: 1 (static) to 4 (max motion)
- `camera_direction`: Controls camera movement (Static/Left/Right/Up/Down/Auto)