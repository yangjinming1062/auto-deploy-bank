# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Depth Anything V2 is a depth estimation model that outperforms the original V1 in fine-grained details and robustness. It uses a DINOv2 vision transformer encoder paired with a DPT (Dense Prediction Transformer) decoder head to generate depth maps from images.

## Commands

### Setup
```bash
pip install -r requirements.txt
```

Download pre-trained checkpoints from Hugging Face and place them under `checkpoints/`:
- `depth_anything_v2_vits.pth` (Small, 24.8M params)
- `depth_anything_v2_vitb.pth` (Base, 97.5M params)
- `depth_anything_v2_vitl.pth` (Large, 335.3M params)

### Run on Images
```bash
python run.py --encoder vitl --img-path <path> --outdir <outdir> [--input-size 518] [--pred-only] [--grayscale]
```
- `--img-path`: Can be a single image, image directory, or text file with image paths
- `--input-size`: Default 518; increase for more fine-grained results (must be multiple of 14)

### Run on Videos
```bash
python run_video.py --encoder vitl --video-path <path> --outdir <outdir> [--input-size 518] [--pred-only] [--grayscale]
```

### Launch Gradio Demo
```bash
python app.py
```

### Metric Depth Estimation (Fine-tuned Models)
See `metric_depth/` directory for models that output depth in meters rather than relative depth:
- Indoor scenes: Use `--max-depth 20` with Hypersim fine-tuned models
- Outdoor scenes: Use `--max-depth 80` with VKITTI fine-tuned models

## Architecture

### Core Model (`depth_anything_v2/dpt.py`)
- **DepthAnythingV2**: Main model class that combines encoder and decoder
- **DPTHead**: Decoder that fuses multi-scale features and outputs depth
- **infer_image()**: High-level inference method handling preprocessing and postprocessing

### Encoder (`depth_anything_v2/dinov2.py`)
DINOv2 vision transformer with configurable sizes:
- `vits`: ViT-Small (384 embed_dim, 12 layers, 6 heads)
- `vitb`: ViT-Base (768 embed_dim, 12 layers, 12 heads)
- `vitl`: ViT-Large (1024 embed_dim, 24 layers, 16 heads)
- `vitg`: ViT-Giant (1536 embed_dim, 40 layers, 24 heads, SwiGLU FFN)

Intermediate layer indices for feature extraction (used in `intermediate_layer_idx`):
```python
'vits': [2, 5, 8, 11]
'vitb': [2, 5, 8, 11]
'vitl': [4, 11, 17, 23]
'vitg': [9, 19, 29, 39]
```

### Feature Fusion (`depth_anything_v2/util/blocks.py`)
- **FeatureFusionBlock**: RefineNet-style fusion with residual conv units
- **_make_scratch**: Creates reduction layers for each feature scale
- Four RefineNet blocks progressively fuse features from largest to smallest scale

### Preprocessing (`depth_anything_v2/util/transform.py`)
- Images resized to input size (default 518) maintaining aspect ratio
- Dimensions padded to multiples of 14 (patch size)
- ImageNet normalization applied (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

## Key Implementation Details

1. **Patch Alignment**: Input dimensions must be multiples of 14 (patch_size). The `infer_image` method handles aspect-ratio-preserving resize with padding.

2. **Device Selection**: Automatic detection in order: CUDA > MPS > CPU.

3. **Output Normalization**: Depth maps are min-max normalized to 0-255 range before visualization.

4. **DPT Decoder Structure**: Projects and resizes 4 intermediate features, then fuses through RefineNet blocks with bilinear upsampling.

5. **Intermediate Features**: Uses `get_intermediate_layers()` to extract features from specific transformer blocks with `return_class_token=True`.

## Directory Structure

- `depth_anything_v2/` - Core model code
  - `dpt.py` - Main model and DPT head
  - `dinov2.py` - DINOv2 encoder wrapper
  - `dinov2_layers/` - Transformer block components
  - `util/` - Utility blocks and transforms
- `metric_depth/` - Fine-tuned metric depth estimation models
- `run.py` - Image inference script
- `run_video.py` - Video inference script
- `app.py` - Gradio web interface