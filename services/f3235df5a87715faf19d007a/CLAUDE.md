# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DreamO is a unified image customization framework built on FLUX.1-dev that enables personalized image generation from reference images. It supports multiple task types: IP (image personalization), ID (facial identity), Try-On, Style, and Multi-Condition generation.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Gradio demo UI
python app.py

# Run with options (see README for details)
python app.py --quant nunchaku --offload  # For low VRAM GPUs
python app.py --version v1                # Use v1 instead of v1.1
python app.py --device mps                # Use Apple Silicon MPS

# Lint code (ruff, black, isort configured in pyproject.toml)
ruff check .
black .
isort .
```

## Architecture

### Entry Points
- **app.py**: Gradio web interface; parses CLI args and launches the generator
- **dreamo_generator.py**: `Generator` class orchestrates model loading and preprocessing

### Core Pipeline (`dreamo/`)
- **dreamo_pipeline.py**: Extends `FluxPipeline`; manages diffusion inference with reference conditioning
  - `load_dreamo_model()`: Loads LoRA weights, embeddings, and merges them
  - `load_dreamo_model_nunchaku()`: Same for Nunchaku quantized models
  - `__call__()`: Main denoising loop with reference latents concatenated to main latents
- **transformer.py**: Patches `FluxTransformer2DModel.forward` to accept `embeddings` parameter (task+idx embeddings added to hidden states)
- **utils.py**: Helper functions for image/tensor conversion, VAE encoding, and FLUX LoRA to Diffusers conversion

### Preprocessing
- **tools/BEN2.py**: Background removal model for IP task
- **facexlib**: Facial detection and alignment for ID task

### Conditioning Flow
1. Reference image → background removal (IP) or face crop (ID)
2. Preprocessed image → VAE encode to latents
3. Task embeddings (`task_embedding`) + index embeddings (`idx_embedding`) computed
4. Reference latents concatenated to main latents in denoising loop

### Model Components
- Base: `black-forest-labs/FLUX.1-dev`
- LoRAs: `dreamo.safetensors`, `dreamo_cfg_distill.safetensors`, FLUX-turbo, quality/SFT/DPO LoRAs
- Custom embeddings: `t5_embedding`, `task_embedding`, `idx_embedding` (10 tokens added to tokenizer)

## Key Implementation Details

- **Turbo LoRA**: Enabled by default (reduces steps from 25 to 12)
- **Quantization**: Three modes - `none` (bf16), `int8` (optimum-quanto), `nunchaku` (mit-han-lab/nunchaku)
- **Device offloading**: `enable_model_cpu_offload()` for memory-constrained inference
- **Reference image resolution**: Default 512x512; increase for fine details