# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MagicAnimate is a temporally consistent human image animation system using diffusion models. It animates a reference image according to a motion sequence (DensePose poses) while preserving the reference appearance. Built on Stable Diffusion V1.5 with 3D UNet extensions for video generation.

## Build Commands

**Install dependencies:**
```bash
# Using conda (recommended)
conda env create -f environment.yaml
conda activate manimate

# Using pip
pip3 install -r requirements.txt
```

**Run inference:**
```bash
# Single GPU
bash scripts/animate.sh

# Multi-GPU distributed
bash scripts/animate_dist.sh
```

**Launch Gradio demo:**
```bash
# Single GPU
python3 -m demo.gradio_animate

# Multi-GPU
python3 -m demo.gradio_animate_dist
```

## Architecture

### Pipeline Structure

The project extends HuggingFace Diffusers with a modular design:

```
magicanimate/pipelines/
├── pipeline_animation.py    # Main DiffusionPipeline subclass with 5D video tensor handling
├── animation.py             # Entry point, loads models and runs denoising loop
└── context.py               # Context scheduling for video chunking
```

### Core Model Components

**AnimationPipeline** (`magicanimate/pipelines/pipeline_animation.py`):
- Extends `DiffusionPipeline` from HuggingFace
- Handles 5D video tensors: `(batch, channels, frames, height, width)`
- Implements DDIM inversion for img2img workflows
- Distributed inference with `torch.distributed` and context queueing

**UNet3DConditionModel** (`magicanimate/models/unet_controlnet.py`):
- Extends 2D UNet to 3D for video denoising
- Accepts `down_block_additional_residuals` and `mid_block_additional_residual` from ControlNet
- Motion modules with temporal self-attention at multiple resolutions

**Transformer3DModel** (`magicanimate/models/attention.py`):
- 3D transformer blocks for video attention
- `SparseCausalAttention2D` for cross-frame attention (self.attn1)
- Temporal self-attention (self.attn_temp) along frame dimension
- Tensor reshape: `(b f) c h w -> (b d) f c -> (b f) d c`

**ControlNetModel** (`magicanimate/models/controlnet.py`):
- DensePose ControlNet conditions on pose estimation maps
- Outputs skip connections and mid-block residuals injected into UNet

**ReferenceAttentionControl** (`magicanimate/models/mutual_self_attention.py`):
- Mutual self-attention for appearance transfer
- Writer mode stores appearance features from AppearanceEncoder
- Reader mode injects features into UNet attention blocks
- Controlled by `fusion_blocks` config ("midup", "up", "all")

### Key Files

- `magicanimate/models/unet_3d_blocks.py`: 3D ResNet/Attention blocks (DownBlock3D, CrossAttnDownBlock3D, etc.)
- `magicanimate/utils/videoreader.py`: Video loading via decord (falls back to OpenCV)
- `magicanimate/models/motion_module.py`: Temporal attention motion module

### Inference Data Flow

1. Load source image → encode to VAE latents
2. Load driving video (DensePose) → ControlNet conditions
3. Initialize random noise latents for video frames
4. Denoising loop (per timestep):
   - AppearanceEncoder processes source (write attention banks)
   - ControlNet processes video frames → cache residuals per frame
   - UNet3D denoises with temporal attention + ControlNet residuals + appearance injection
5. VAE decode latents to video frames
6. Save as MP4 with source/control/output grid

### Configuration

**Main config** (`configs/prompts/animation.yaml`):
- `source_image`: Paths to reference images
- `video_path`: Paths to driving videos (DensePose)
- `steps`: DDIM steps (default 25)
- `guidance_scale`: CFG scale (default 7.5)
- `L`: Context frame length
- `fusion_blocks`: Attention injection points

**Inference config** (`configs/inference/inference.yaml`):
- `unet_additional_kwargs`:
  - `unet_use_cross_frame_attention`: Enable cross-frame attention
  - `unet_use_temporal_attention`: Enable temporal self-attention
  - `motion_module_type`: "Vanilla" for standard temporal attention
  - `temporal_position_encoding_max_len`: Max frames (24)

## Dependencies

- Python 3.8+, CUDA 11.3+, ffmpeg
- PyTorch 2.0.1, diffusers 0.21.4, transformers 4.32.0
- xformers 0.0.22 for memory-efficient attention
- gradio 3.41.2 for web demo
- einops for tensor reshaping, omegaconf for YAML

## Pretrained Models

Download from HuggingFace to `pretrained_models/`:
- StableDiffusion v1.5 (base model)
- SD VAE FT MSE
- MagicAnimate checkpoints (appearance encoder, densepose controlnet, temporal attention)