# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

YOLOv11-RGBT is a multispectral object detection framework built on Ultralytics YOLO. It enables training and inference with various image modalities (RGB, thermal/infrared, grayscale, multispectral) using dual-channel or multi-channel input strategies. The project supports multiple fusion strategies: early fusion, mid-fusion, late fusion, score fusion, and weight-sharing modes.

## Common Commands

### Installation
```bash
pip install -e .  # Install in editable mode for development
pip install -r requirements.txt  # Install base dependencies
```

### Training
```bash
python train.py --data <dataset.yaml>  # Basic RGB training
python train_RGBT.py  # RGBT (4-channel) training
python train_RGBRGB.py  # RGB+IR 6-channel training
python train_Gray.py  # Grayscale single-channel training
python train_multispectral.py  # Arbitrary channel multispectral training
```

Key training parameters:
- `use_simotm`: Image mode (RGB, RGBT, Gray, Gray16bit, Multispectral, etc.)
- `channels`: Number of input channels (1, 3, 4, 6, or n for multispectral)
- `pairs_rgb_ir`: Directory name mapping (default: ['visible', 'infrared'])

### Validation
```bash
python val.py  # Runs validation with current model
```

### Detection/Inference
```bash
python detect.py  # Basic detection
python detect-4C.py  # 4-channel detection
python detect-6C.py  # 6-channel detection
python heatmap_RGBT.py  # Grad-CAM heatmap visualization
```

### Testing
```bash
pytest tests/  # Run all tests
pytest tests/test_python.py -v  # Run Python API tests
pytest --durations=30  # Run with timing info
pytest --slow tests/  # Run slow tests
pytest --cov=ultralytics/ tests/  # Run with coverage
```

## Linting & Formatting
```bash
ruff check ultralytics/  # Lint with ruff
yapf -r ultralytics/ --style=pyproject.toml  # Format with yapf
isort ultralytics/  # Sort imports
codespell ultralytics/  # Check spelling
```

## Architecture

### Core Directory Structure

- **`ultralytics/nn/modules/`** - Neural network building blocks
  - `conv.py` - Convolution modules (Conv, Conv2, Focus, etc.)
  - `block.py` - Residual/block components (Bottleneck, C2f, C3k2, etc.)
  - `attention.py` - Attention mechanisms (PSA, CBAM, etc.)
  - `head.py` - Detection/segmentation heads
  - `rep_block.py` - Reparameterization blocks (DiverseBranchBlock, etc.)

- **`ultralytics/nn/tasks.py`** - Model construction and task routing
  - `BaseModel` - Base class for all models
  - Model factory functions that parse YAML configs and build network architectures
  - Handles detection, segmentation, pose, and OBB tasks

- **`ultralytics/data/`** - Dataset handling
  - `base.py` - `BaseDataset` class with multispectral image loading
  - `dataset.py` - YOLODataset implementation
  - `loaders.py` - Data loading utilities
  - Key: `load_and_preprocess_image()` handles multi-modal image fusion

- **`ultralytics/engine/`** - Training/inference pipeline
  - `trainer.py` - Core training loop
  - `model.py` - YOLO model wrapper class
  - `validator.py` - Validation logic
  - `predictor.py` - Inference logic

- **`ultralytics/cfg/`** - Configuration files
  - `models/` - Model architecture YAML files (v3-v13, including RGBT variants)
  - `datasets/` - Dataset configuration YAML files
  - `default.yaml` - Default training hyperparameters

### Data Loading (ultralytics/data/base.py)

The `BaseDataset` class handles multispectral image loading through `load_and_preprocess_image()`. For RGBT mode:
1. Reads visible image (BGR)
2. Replaces path component to read infrared image (using `pairs_rgb_ir` mapping)
3. Merges channels via `_merge_channels()` or `_merge_channels_rgb()`

### Image Modes (use_simotm)

| Mode | Channels | Description |
|------|----------|-------------|
| Gray | 1 | Single-channel 8-bit grayscale |
| Gray16bit | 1 | Single-channel 16-bit grayscale |
| SimOTM/SimOTMBBS | 3 | Gray converted to 3-channel |
| BGR | 3 | Standard 3-channel color |
| RGBT | 4 | RGB + infrared merged |
| RGBRGB6C | 6 | RGB + 3-channel IR |
| Multispectral | n | Arbitrary n-channel images |

### Model Configuration (YAML)

RGBT models use `ch: <n>` to specify input channels and include dual backbone branches:
- Visible light branch with `SilenceChannel` to select first 3 channels
- Infrared branch with `SilenceChannel` to select additional channels

Example RGBT mid-fusion model structure:
```
backbone:
  - [0, 1, SilenceChannel, [0, 3]]  # visible: channels 0-2
  - [0, 1, SilenceChannel, [3, 4]]  # infrared: channels 3
  - ... visible backbone ...
  - ... infrared backbone ...
  - [[6, 16], 1, Concat, [1]]  # fuse P3 features
head:
  - ... detection head ...
```

### Fusion Strategies
The framework supports multiple RGBT fusion strategies:
- **Early Fusion**: Combine RGB and IR at input level before backbone
- **Mid-Fusion**: Fuse features at intermediate backbone stages
- **Late Fusion**: Fuse features at detection head level
- **Score Fusion**: Combine detection scores from separate heads
- **Weight Sharing**: Share backbone weights between modalities

Key fusion blocks available: CAS, CMA, CFT, CTF, DetachDeepBB, EFM, MCF, NiNfusion, PGI, RDBB, TransformerFusionBlock

### Model Scale Variants
YAML configs support multiple scale variants:
- **n**: Nano (smallest, fastest)
- **s**: Small
- **m**: Medium
- **l**: Large
- **x**: Extra large (largest, most accurate)

Model configs are located in `ultralytics/cfg/models/` with version-specific subdirectories (v3-RGBT through v13-RGBT).

## Dataset Configuration

Supports 4 dataset layout methods. The key principle: visible and infrared directories must be at the same level, and paths in TXT files must contain `visible` for automatic path replacement to `infrared`.

Recommended structure (Method 1):
```
dataset/
├── visible/
│   ├── train/
│   └── test/
└── infrared/
    ├── train/
    └── test/
```

## Key Classes and Patterns

- **Detection heads**: `Detect`, `DetectV8`, `DetectDeepDBB`, `DetectWDBB` (in `ultralytics/nn/modules/head.py`)
- **Fusion blocks**: `CBFuse`, `CrossAttentionShared`, `Concat` (in `ultralytics/nn/modules/`)
- **Reparameterization**: `DeepDiverseBranchBlock`, `WideDiverseBranchBlock` (in `ultralytics/nn/modules/rep_block.py`)

## CI/CD & Docker

### GitHub Actions Workflows (`.github/workflows/`)
- **ci.yml**: Main CI pipeline (tests, benchmarks, GPU tests, multi-platform validation)
- **format.yml**: Auto-formatting on PRs
- **docker.yml**: Docker image building
- **docs.yml**: MkDocs documentation generation

### Docker Images (`docker/`)
Multiple variants available for different platforms:
- `Dockerfile` - CPU version
- `Dockerfile-arm64` - ARM64 architecture
- `Dockerfile-cuda` - CUDA-enabled
- `Dockerfile-jetson` - NVIDIA Jetson

Build with: `docker build -f docker/Dockerfile -t ultralytics:latest .`

## Documentation

- Built with **MkDocs** + Material theme
- API documentation auto-generated via mkdocstrings
- Configuration: `mkdocs.yml`
- Edit docs in `docs/` directory, build with `mkdocs build`