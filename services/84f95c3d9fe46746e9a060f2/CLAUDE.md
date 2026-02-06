# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

USO (Unified Style and Subject-Driven Generation) is a unified style-subject customization model that can combine any subjects with any styles in any scenarios. Built on top of the FLUX.1-dev diffusion transformer architecture.

## Commands

### Setup
```bash
# Create virtual environment with Python 3.10-3.12
python -m venv uso_env
source uso_env/bin/activate

# Install PyTorch (required separately - not in requirements.txt)
pip install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu124

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp example.env .env
# Edit .env with your HF_TOKEN and local weight paths

# Download model weights
python ./weights/downloader.py
```

### Inference
```bash
# Subject-driven generation (identity preservation)
python inference.py --prompt "A man in flower shops carefully match bouquets." --image_paths "assets/gradio_examples/identity1.jpg" --width 1024 --height 1024

# Style-driven generation
python inference.py --prompt "A cat sleeping on a chair." --image_paths "" "assets/gradio_examples/style1.webp" --width 1024 --height 1024

# Style-subject driven generation
python inference.py --prompt "The woman gave an impassioned speech on the podium." --image_paths "assets/gradio_examples/identity2.webp" "assets/gradio_examples/style2.webp" --width 1024 --height 1024

# Multi-style generation
python inference.py --prompt "A handsome man." --image_paths "" "assets/gradio_examples/style3.webp" "assets/gradio_examples/style4.webp" --width 1024 --height 1024

# Low VRAM mode (~16GB peak)
python inference.py --prompt "your prompt" --image_paths "your_image.jpg" --width 1024 --height 1024 --offload --model_type flux-dev-fp8
```

### Gradio Web Demo
```bash
# Standard mode
python app.py

# Low VRAM mode
python app.py --offload --name flux-dev-fp8
```

## Architecture

### Core Pipeline (`uso/flux/pipeline.py`)
- `USOPipeline`: Main entry point for generation
- `forward()`: Core inference method handling denoising loop
- `gradio_generate()`: Gradio-friendly wrapper with image preprocessing
- Supports model offloading for memory-constrained environments

### Model Architecture (`uso/flux/model.py`)
- `Flux`: Transformer model for flow matching on sequences
- Dual-stream blocks process image and text tokens separately before cross-attention
- Single-stream blocks for final processing
- `feature_embedder`: `SigLIPMultiFeatProjModel` projects style features into hidden space
- `vision_encoder`: Pluggable SigLIP model for encoding style reference images

### Key Processing Blocks (`uso/flux/modules/layers.py`)
- `DoubleStreamBlock`: Separate image/text processing with cross-attention
- `SingleStreamBlock`: Unified processing after dual-stream
- `DoubleStreamBlockLoraProcessor`: LoRA-enhanced processor for style injection
- `SigLIPMultiFeatProjModel`: Projects multi-layer SigLIP features (layers -2, -11, -20) into unified space

### Sampling (`uso/flux/sampling.py`)
- `denoise()`: Main diffusion sampling loop
- `prepare_multi_ip()`: Prepares concatenated conditioning (text + style refs)
- `get_schedule()`: Generates timestep schedule with optional shift for high-res images

### Model Loading (`uso/flux/util.py`)
- `load_flow_model_only_lora()`: Loads base FLUX with USO LoRA weights and projection model
- Weights configured via `.env` file paths
- Supports fp8 quantization via model type selection

### Data Flow
1. Prompt → T5-XXL + CLIP for text encoding
2. Reference images → SigLIP vision encoder → `feature_embedder` (style tokens)
3. Content reference image → AE encoder → latents
4. All conditioning → concatenated in sequence
5. Denoising loop over timesteps
6. Final latents → AE decoder → output image

## Model Types
- `flux-dev`: Full precision FLUX.1-dev (24GB+ VRAM)
- `flux-dev-fp8`: FP8 quantized variant (~16GB VRAM with offload)
- `flux-schnell`: Faster distilled variant
- `flux-krea-dev`: Alternative FLUX variant

## Key Files
- `app.py`: Gradio web interface
- `inference.py`: CLI inference tool
- `weights/downloader.py`: Download required model weights from HuggingFace
- `uso/flux/pipeline.py`: Main pipeline
- `uso/flux/model.py`: Flux transformer
- `uso/flux/sampling.py`: Sampling utilities
- `uso/flux/util.py`: Model loading utilities