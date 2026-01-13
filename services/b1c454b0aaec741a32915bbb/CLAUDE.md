# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **SUPIR** (Scaling Up to Excellence), a state-of-the-art deep learning-based image restoration system that performs photo-realistic image enhancement using a two-stage diffusion process. The system combines:
- A pre-denoising stage for quality enhancement
- LLaVA (Language and Vision Assistant) for automatic captioning
- A diffusion-based restoration stage for final output

## Common Commands

### Installation
```bash
conda create -n SUPIR python=3.8 -y
conda activate SUPIR
pip install -r requirements.txt
```

### Running Tests/Inference
```bash
# Basic inference on a directory of images
python test.py --img_dir /path/to/input --save_dir /path/to/output --SUPIR_sign Q

# Run with specific upscale factor and steps
python test.py --img_dir /path/to/input --save_dir /path/to/output --SUPIR_sign F --upscale 2 --edm_steps 50

# With LLaVA for automatic captioning (default)
python test.py --img_dir /path/to/input --save_dir /path/to/output --SUPIR_sign Q

# Without LLaVA (faster, manual prompts only)
python test.py --img_dir /path/to/input --save_dir /path/to/output --no_llava --SUPIR_sign Q
```

### Running Interactive Demos
```bash
# Basic Gradio demo
python gradio_demo.py --ip 0.0.0.0 --port 6688 --use_image_slider --log_history

# Fast demo with Lightning model
python gradio_demo.py --ip 0.0.0.0 --port 6688 --use_image_slider --log_history --opt options/SUPIR_v0_Juggernautv9_lightning.yaml

# Memory-efficient mode (12G VRAM for Diffusion, 16G for LLaVA)
python gradio_demo.py --ip 0.0.0.0 --port 6688 --use_image_slider --log_history --loading_half_params --use_tile_vae --load_8bit_llava

# Face-specific demo
python gradio_demo_face.py --ip 0.0.0.0 --port 6688 --use_image_slider --log_history

# Tiled demo for large images
python gradio_demo_tiled.py --ip 0.0.0.0 --port 6688 --use_image_slider --log_history
```

### Important Arguments
- `--SUPIR_sign`: Model variant (Q=Quality-oriented, F=Fidelity-oriented with light degradation)
- `--upscale`: Upsampling ratio (default: 1)
- `--edm_steps`: Number of EDM sampling steps (default: 50)
- `--s_cfg`: Classifier-free guidance scale (default: 4.0 for fidelity, 6.0-7.5 for quality)
- `--s_stage2`: Control strength of Stage 2 (1.0 for fidelity, 0.93 for quality)
- `--min_size`: Minimum output resolution (default: 1024)
- `--use_tile_vae`: Enable tile-based VAE for memory efficiency
- `--load_8bit_llava`: Load LLaVA in 8-bit mode for memory efficiency

## High-Level Architecture

### Core Components

**1. Main Package: `SUPIR/`**
- `SUPIR/models/SUPIR_model.py`: Main model orchestration class that combines all stages
- `SUPIR/modules/SUPIR_v0.py`: Core network architectures (GLVControl, LightGLVUNet)
- `SUPIR/util.py`: Utility functions for model loading, tensor/PIL conversion, and image processing

**2. Diffusion Framework: `sgm/`** (Stability Graphics Library)
Contains diffusion-related modules:
- Autoencoder components (first stage)
- Diffusion samplers and denoisers
- Conditioners and guidance mechanisms
- EDM (Elucidating Design of Image Generation Models) sampler implementation

**3. Language-Vision Integration: `llava/`**
- `llava_agent.py`: Wrapper for LLaVA model to generate image captions
- Used for automatic prompt generation in Stage 2 of the restoration process

**4. Entry Points**
- `test.py`: Command-line interface for batch processing images
- `gradio_demo*.py`: Web-based interactive demos with various configurations

### Model Configuration

Configuration files in `options/` directory define model architecture and hyperparameters:
- `SUPIR_v0.yaml`: Main configuration with Q/F model variants
- `SUPIR_v0_Juggernautv9_lightning.yaml`: Fast sampling variant
- `SUPIR_v0_tiled.yaml`: Tiled processing configuration

**Key configuration sections:**
- `model.control_stage_config`: GLVControl network parameters
- `model.network_config`: LightGLVUNet architecture
- `model.conditioner_config`: CLIP embeddings for text guidance
- `model.first_stage_config`: Autoencoder settings (VAE)
- `model.sampler_config`: EDM sampler parameters

### Checkpoint Management

**File: `CKPT_PTH.py`**
Centralized location for all model checkpoint paths:
- `LLAVA_CLIP_PATH`, `LLAVA_MODEL_PATH`: LLaVA captioning model
- `SDXL_CLIP1_PATH`, `SDXL_CLIP2_CKPT_PTH`: SDXL CLIP encoders
- `SDXL_CKPT`: Stable Diffusion XL base model
- `SUPIR_CKPT_Q`, `SUPIR_CKPT_F`: SUPIR model variants

### Processing Pipeline

The system operates in a **two-stage process**:

**Stage 1: Pre-denoising**
- Takes low-quality input image
- Applies denoising to create intermediate "clean" image
- Output used for LLaVA captioning

**Stage 2: Diffusion Restoration**
- Takes original input + LLaVA-generated captions
- Performs diffusion-based restoration
- Applies color correction and final refinement
- Outputs high-quality restored image

### Device Allocation

When multiple GPUs are available:
- `cuda:0`: SUPIR model (restoration)
- `cuda:1`: LLaVA model (captioning)
- Falls back to single GPU if only one available

Memory optimization options:
- `--loading_half_params`: Use FP16 for model weights
- `--use_tile_vae`: Tile-based VAE encoding/decoding
- `--load_8bit_llava`: 8-bit quantization for LLaVA

## Key Files to Know

- `README.md`: Complete documentation with papers, model links, and usage examples
- `requirements.txt`: Python dependencies
- `CKPT_PTH.py`: All checkpoint paths (edit this for your setup)
- `test.py`: Main inference script with all parameters
- `options/SUPIR_v0.yaml`: Model architecture and hyperparameters
- `gradio_demo.py`: Interactive web demo
- `gradio_demo_face.py`: Face-specific demo
- `gradio_demo_tiled.py`: Tiled processing for large images

## Development Notes

- **No explicit linting/formatting tools** configured (no pytest, flake8, black, etc.)
- Model supports both quality-oriented (Q) and fidelity-oriented (F) variants
- LLaVA integration is optional (can be disabled with `--no_llava`)
- All configuration is YAML-based using OmegaConf
- Gradients are computed in FP16/BF16, but model can run in FP32
- CUDA-only implementation (CPU inference not supported)

## Empirical Settings for Best Results

**Quality-oriented (higher visual quality):**
- `s_cfg = 6.0`, `spt_linear_CFG = 3.0`, `s_noise = 1.02`
- `s_stage2 = 0.93`

**Fidelity-oriented (closer to original):**
- `s_cfg = 4.0`, `spt_linear_CFG = 1.0`, `s_noise = 1.01`
- `s_stage2 = 1.0`

## Model Variants

- **SUPIR-v0Q**: Quality-oriented, general-purpose model with high generalization
- **SUPIR-v0F**: Fidelity-oriented, trained with light degradation, preserves more details

## Non-Commercial Use

This software is restricted to **non-commercial use only**. See LICENSE file for details.