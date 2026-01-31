# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Depth Anything 3 is a visual geometry foundation model that predicts spatially consistent depth, camera poses, and 3D Gaussian Splats from arbitrary visual inputs. Key capabilities:
- Monocular and multi-view depth estimation
- Camera pose estimation (with or without known poses)
- 3D Gaussian Splatting parameter prediction for novel view synthesis
- Ultra-long video processing via streaming inference (see `da3_streaming/`)

## Build Commands

```bash
# Basic installation
pip install -e .

# With Gradio web UI (Python 3.10+)
pip install -e ".[app]"

# With 3D Gaussian Splatting support
pip install -e ".[gs]"

# With all features
pip install -e ".[all]"

# Pre-commit hooks
pre-commit install
```

## Running Tests

This project uses pre-commit hooks for linting (black, isort, flake8, pyupgrade, autoflake). Run manually:

```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Or run individually:
black --config pyproject.toml .
isort --settings-file pyproject.toml --filter-files .
flake8 --config .flake8
pyupgrade --py38-plus --keep-runtime-typing
autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place
```

## CLI Commands

```bash
# Auto-detect input type (image, directory, video, or COLMAP)
da3 auto <input_path> --export-dir ./output --export-format glb

# Process single image
da3 image <image_path> --export-dir ./output

# Process directory of images
da3 images <images_dir> --export-dir ./output

# Process video (extract frames at specified FPS)
da3 video <video_path> --fps 15 --export-dir ./output

# Process COLMAP data with known poses
da3 colmap <colmap_dir> --export-dir ./output

# Start backend service (keeps model in GPU memory)
da3 backend --model-dir depth-anything/DA3NESTED-GIANT-LARGE --port 8008

# Launch Gradio web UI
da3 gradio --model-dir depth-anything/DA3NESTED-GIANT-LARGE

# Launch gallery server for viewing exports
da3 gallery --gallery-dir ./workspace/gallery
```

## Benchmark Evaluation

```bash
# Full evaluation on all datasets (downloads from HuggingFace)
python -m depth_anything_3.bench.evaluator model.path=depth-anything/DA3-GIANT

# Specific datasets and modes
python -m depth_anything_3.bench.evaluator \
    model.path=depth-anything/DA3-GIANT \
    eval.datasets=[hiroom] \
    eval.modes=[pose]

# Multi-GPU evaluation
CUDA_VISIBLE_DEVICES=0,1,2,3 python -m depth_anything_3.bench.evaluator model.path=depth-anything/DA3-GIANT
```

## Python API Usage

```python
from depth_anything_3.api import DepthAnything3

# Load model from Hugging Face
model = DepthAnything3.from_pretrained("depth-anything/DA3NESTED-GIANT-LARGE")
model = model.to("cuda")

# Run inference
prediction = model.inference(
    images=["path/to/image.png"],  # list of images, paths, or numpy arrays
    export_dir="./output",
    export_format="glb",
    infer_gs=True,  # enable 3DGS output
    use_ray_pose=False,  # use ray-based pose estimation (more accurate, slower)
    ref_view_strategy="saddle_balanced",  # reference view selection
)
# Returns: Prediction(depth, conf, extrinsics, intrinsics, processed_images, gaussians, ...)
# prediction.depth: [N, H, W] float32 depth map
# prediction.extrinsics: [N, 3, 4] float32 (OpenCV w2c format)
# prediction.intrinsics: [N, 3, 3] float32 camera intrinsics
```

## Architecture

### Configuration System

Models are defined via YAML configs in `src/depth_anything_3/configs/`. Configs use OmegaConf with:
- `__object__`: class path and args (`path: depth_anything_3.model.da3`, `name: DepthAnything3Net`)
- `__inherit__`: inherit from another config (e.g., `depth_anything_3.configs.da3-giant`)
- `__object__.args`: `as_params` for kwargs, `as_config` for DictConfig

Load configs with:
```python
from depth_anything_3.cfg import load_config, create_object
from depth_anything_3.registry import MODEL_REGISTRY

config = load_config(MODEL_REGISTRY["da3-large"])
model = create_object(config)
```

### Model Registry

`src/depth_anything_3/registry.py` auto-discovers all YAML configs and creates `MODEL_REGISTRY`. Available presets:
- `da3-giant`, `da3-large`, `da3-base`, `da3-small` (any-view models)
- `da3metric-large`, `da3mono-large` (specialized)
- `da3nested-giant-large` (nested: any-view + metric for real-world scale)

### Core Classes

- **DepthAnything3** (`api.py`): High-level API, handles preprocessing, inference, export
- **DepthAnything3Net** (`model/da3.py`): Main network with DinoV2 backbone + depth head + optional camera decoder + optional GS head
- **NestedDepthAnything3Net** (`model/da3.py`): Combines any-view model + metric model for metric depth
- **Prediction** (`specs.py`): Output dataclass with depth, conf, extrinsics, intrinsics, gaussians

### Network Components

- **Backbone**: DinoV2 vision transformer with RoPE (`dinov2/`)
- **Depth Head**: DPT or DualDPT (`dpt.py`, `dualdpt.py`)
- **Camera Encoder/Decoder**: `cam_enc.py`, `cam_dec.py` for pose estimation
- **3DGS**: GSDPT head + GaussianAdapter (`gsdpt.py`, `gs_adapter.py`)

### Services Layer (`src/depth_anything_3/services/`)

- **backend.py**: FastAPI service keeping model resident on GPU
- **inference_service.py**: Unified inference interface
- **input_handlers.py**: Dispatcher for different input types (image, video, COLMAP)

### Key Directories

- `src/depth_anything_3/utils/export/`: Export to GLB, PLY, NPZ, COLMAP, 3DGS video
- `src/depth_anything_3/utils/geometry.py`: Camera geometry transformations
- `src/depth_anything_3/bench/`: Benchmark evaluation pipeline
- `da3_streaming/`: Sliding-window streaming inference for ultra-long videos

## Key Conventions

- **Python version**: 3.9-3.13
- **Output format**: Models return `addict.Dict` for dict-like access
- **Pose format**: Extrinsics are OpenCV w2c (world-to-camera) matrices, shape `[N, 3, 4]`
- **Preprocessing**: Images normalized with ImageNet mean/std, resized to `process_res` (default 504)
- **Export formats**: `mini_npz`, `npz`, `glb`, `ply`, `gs`, `gs_video`, `colmap`, `feat_vis` (can be combined with hyphens)
- **HuggingFace integration**: Models extend `PyTorchModelHubMixin` for Hub compatibility