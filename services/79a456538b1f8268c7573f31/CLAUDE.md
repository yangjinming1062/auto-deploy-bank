# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a ComfyUI custom node that provides an adaptation of [IDM-VTON](https://github.com/yisol/IDM-VTON) for virtual try-on functionality. It allows users to virtually try garments on human images using Stable Diffusion XL with custom modifications.

**Requirements:** GPU with at least 16GB of VRAM

## Installation

Dependencies are automatically installed when running the install script:

```bash
python install.py
```

This will:
- Install Python dependencies from `requirements.txt`
- Download model weights from HuggingFace (`yisol/IDM-VTON`) to the `models/` directory

Dependencies can also be installed manually:

```bash
pip install -r requirements.txt
```

## Architecture

### Node Structure

The project exposes **2 main ComfyUI nodes**:

1. **`PipelineLoader`** (`src/nodes/pipeline_loader.py:19`)
   - Input node that loads the IDM-VTON model pipeline
   - Loads all model components: UNet, VAE, text encoders, image encoder, etc.
   - Supports weight dtypes: float32, float16, bfloat16
   - Returns a `PIPELINE` object used by the inference node

2. **`IDM_VTON`** (`src/nodes/idm_vton.py:14`)
   - Main inference node for virtual try-on
   - Takes: human image, pose image, mask image, garment image, and text prompts
   - Returns: generated image and mask

### Core Components

**Pipeline Loading** (`src/idm_vton/tryon_pipeline.py:309`):
- Heavily modified `StableDiffusionXLInpaintPipeline` from Diffusers
- Custom `__call__` method (line 1251) that adds garment-specific parameters
- Integrates pose estimation, garment features, and IP-Adapter

**Hacked Modules** (modified from original IDM-VTON):
- `src/idm_vton/unet_hacked_tryon.py` - Modified UNet for try-on process
- `src/idm_vton/unet_hacked_garmnet.py` - Modified UNet for garment encoding
- `src/idm_vton/attentionhacked_*.py` - Modified attention mechanisms
- `src/idm_vton/transformerhacked_*.py` - Modified transformer blocks
- `src/idm_vton/unet_block_hacked_*.py` - Modified UNet blocks

**IP-Adapter** (`src/ip_adapter/`):
- Provides image prompt adapter functionality
- `src/ip_adapter/ip_adapter.py` - Main IP-Adapter implementation
- `src/ip_adapter/resampler.py` - Feature resampling
- `src/ip_adapter/attention_processor.py` - Custom attention processors

### Node Mappings

All nodes are registered in `src/nodes_mappings.py:5`:
```python
NODE_CLASS_MAPPINGS = {
    "PipelineLoader": PipelineLoader,
    "IDM-VTON": IDM_VTON,
}
```

### Key Processing Flow

1. **Pipeline Loading**:
   - Models loaded from `models/IDM-VTON/` directory
   - Components: VAE, UNet (try-on + encoder), text encoders (2), image encoder, tokenizers (2)
   - All models moved to GPU and set to eval mode

2. **Inference** (`src/nodes/idm_vton.py:57`):
   - Preprocess images (resize, convert to tensors)
   - Encode prompts (both human and garment descriptions)
   - Run diffusion pipeline with:
     - Human image as base
     - Garment image for clothing appearance
     - Pose image for body guidance
     - Mask for inpainting region
   - Return generated image

## Dependencies

Key dependencies from `requirements.txt`:
- `torch`, `torchvision`, `torchaudio` - PyTorch
- `diffusers==0.27.2` - Diffusion models library
- `transformers==4.40.2` - Transformers (CLIP)
- `accelerate==0.30.0` - Model loading/acceleration
- `einops==0.8.0` - Tensor operations
- `bitsandbytes==0.42` - Quantization
- `opencv-python` - Image processing

## Development

**No test suite** - The project contains no automated tests.

**Model Weights**:
- Downloaded automatically by `install.py` from HuggingFace
- Stored in `models/IDM-VTON/` directory
- Includes: unet, unet_encoder, vae, text_encoder, text_encoder_2, image_encoder, tokenizers, scheduler

**Workflow**:
- Run `python install.py` to set up environment and download models
- Load in ComfyUI and use the provided workflow (see `workflow.png`)
- The workflow requires [ComfyUI Segment Anything](https://github.com/storyicon/comfyui_segment_anything) for mask generation
- DensePose estimation uses [ComfyUI's ControlNet Auxiliary Preprocessors](https://github.com/Fannovel16/comfyui_controlnet_aux)

## Publishing

The project uses GitHub Actions for publishing to Comfy Registry (`.github/workflows/publish.yml:1`):
- Triggered on push to `main` branch when `pyproject.toml` changes
- Requires `REGISTRY_ACCESS_TOKEN` secret
- Uses `Comfy-Org/publish-node-action@main`

## Important Notes

- **GPU Memory**: Requires 16GB+ VRAM minimum
- **Weight Downloads**: Large model files (~10GB) downloaded during installation
- **Modified Pipeline**: The `tryon_pipeline.py` is a substantial modification of StableDiffusionXLInpaintPipeline with garment-specific features
- **No Version Pinning**: Dependencies are not tightly versioned (except where specified in pyproject.toml)