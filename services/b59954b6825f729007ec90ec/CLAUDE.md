# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PromptDA is a metric depth estimation model that uses prompting to achieve 4K resolution depth estimation. It combines a DINOv2 ViT encoder with a DPT (Dense Prediction Transformer) decoder and prompt-guided fusion blocks.

## Commands

### Setup
```bash
pip install -r requirements.txt
pip install -e .
sudo apt install ffmpeg  # for video generation
```

### Running Inference on Example Images
```bash
python -m promptda.scripts.sanity_check
```

### Processing Stray Scanner Captures
```bash
python -m promptda.scripts.infer_stray_scan --input_path data/8b98276b0a.zip --output_path data/results
python -m promptda.scripts.generate_video process_stray_scan --input_path data/8b98276b0a --result_path data/results
ffmpeg -framerate 60 -i data/results/%06d_smooth.jpg -c:v libx264 -pix_fmt yuv420p data/results.mp4
```

## Architecture

**Encoder**: DINOv2 ViT (vits/vitb/vitl/vitg variants) loaded locally from `torchhub/facebookresearch_dinov2_main`

**Model Entry Point**: `promptda/promptda.py` - `PromptDA` class
- `from_pretrained()`: Loads model from HuggingFace Hub (`depth-anything/prompt-depth-anything-vitl`) or local checkpoint
- `predict()`: Main inference method requiring `image` and `prompt_depth` tensors

**DPT Decoder**: `promptda/model/dpt.py` - `DPTHead` class
- Takes encoder features and processes through 4 RefineNet fusion blocks
- `FeatureFusionDepthBlock` in `blocks.py` handles prompt depth fusion

**Key Dimensions**:
- Patch size: 14px
- Image dimensions must be multiples of 14 (enforced in `io_wrapper.py:ensure_multiple_of()`)
- Default max size: 1008px

## Data Format

**Input Images**: Loaded via `load_image()` - normalizes to [0,1], resizes to max 1008px maintaining aspect ratio

**Input Depth (prompt_depth)**: ARKit LiDAR depth in meters
- PNG format: depth / 1000 (uint16 to meters)
- NPZ format: direct float array

**Output Depth**: Float32 in meters (HxW tensor)

## Module Structure

```
promptda/
├── promptda.py           # Main PromptDA model class
├── model/
│   ├── dpt.py           # DPT decoder head
│   ├── blocks.py        # Fusion blocks (FeatureFusionDepthBlock, ResidualConvUnit)
│   └── config.py        # Model configs for vits/vitb/vitl/vitg
├── scripts/
│   ├── infer_stray_scan.py    # Process Stray Scanner zip files
│   ├── generate_video.py      # Generate visualization videos
│   └── sanity_check.py        # Quick test on example images
└── utils/
    ├── io_wrapper.py          # Image/depth loading/saving
    ├── depth_utils.py         # Depth visualization, smoothing, unprojection
    ├── parallel_utils.py      # ThreadPool parallel execution
    └── logger.py              # Logging utility with rate limiting
```

## Dependencies Notes

- Python 3.9-3.11 required
- PyTorch 2.0.1 with torchvision 0.15.2 and torchaudio 2.0.2
- xformers 0.0.22 for memory-efficient attention
- gradio for the demo UI (not required for core inference)