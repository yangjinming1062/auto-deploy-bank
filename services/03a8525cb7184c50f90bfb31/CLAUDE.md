# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Aether is a "Geometric-Aware Unified World Modeling" framework that unifies three capabilities:
1. **4D Dynamic Reconstruction**: Reconstruct dynamic point clouds from videos by estimating depths and camera poses
2. **Action-Conditioned Video Prediction**: Predict future frames based on initial observations with camera trajectory actions
3. **Goal-Conditioned Visual Planning**: Generate planning paths from observation/goal image pairs

Built on CogVideoX (diffusers), using diffusion transformers for video generation with multi-task outputs (RGB video, disparity/depth, raymap for camera poses).

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# 4D reconstruction from video
python scripts/demo.py --task reconstruction --video ./assets/example_videos/moviegen.mp4

# Action-conditioned prediction
python scripts/demo.py --task prediction --image ./assets/example_obs/car.png --raymap_action assets/example_raymaps/raymap_forward_right.npy

# Goal-conditioned planning
python scripts/demo.py --task planning --image ./assets/example_obs_goal/01_obs.png --goal ./assets/example_obs_goal/01_goal.png

# Gradio web interface
python scripts/demo_gradio.py

# Video depth evaluation (requires data/ with sintel, kitti, bonn folders)
bash evaluation/video_depth/run_aether.sh

# Relative camera pose evaluation (requires data/ with tum, sintel, scannetv2 folders)
bash evaluation/rel_pose/run_aether.sh

# Run pre-commit hooks
pre-commit run --all-files
```

## Code Architecture

### Core Pipeline (`aether/pipelines/aetherv1_pipeline_cogvideox.py`)
- `AetherV1PipelineCogVideoX` - Main inference class extending `CogVideoXImageToVideoPipeline`
- Supports three tasks: "reconstruction", "prediction", "planning"
- Default inference: 4 steps for reconstruction, 50 steps for prediction/planning
- Output: `AetherV1PipelineOutput(rgb, disparity, raymap)`

### Utilities (`aether/utils/`)
- `postprocess_utils.py`: Camera pose handling (`raymap_to_poses`, `camera_pose_to_raymap`), depth processing, point cloud generation (`postprocess_pointmap`, `project`)
- `preprocess_utils.py`: Input preprocessing
- `visualize_utils.py`: 3D visualization, GLB export with `predictions_to_glb`

### Key Data Flow
1. Input (video/image/goal) + optional raymap action → Pipeline
2. Diffusion inference → latents (RGB channels, disparity channels, camera channels)
3. Decode → RGB video, disparity video, raymap
4. Postprocess → Camera poses, point clouds, depth visualization

### Raymap Format
Raymaps encode camera poses as (num_frames, 6, h, w) tensors where:
- 6 channels: 3 for ray origin (camera position), 3 for ray direction
- h = image_height // 8, w = image_width // 8
- Convert camera poses using `camera_pose_to_raymap()` in `postprocess_utils.py`

### Sliding Window Processing
Long videos use sliding windows with overlap blending:
- Window size: `num_frames` (default 41)
- Stride: `sliding_window_stride` (default 24)
- Blending in `blend_and_merge_window_results()` handles temporal overlap

## Development Notes

- **Linting**: Ruff configured in `pyproject.toml` (line-length: 88, ignores C901, E501, E741, F402, F823)
- **Pre-commit**: `.pre-commit-config.yaml` runs ruff and ruff-format
- **Device**: CUDA required for inference; code checks `torch.cuda.is_available()`
- **Project root**: Identified by `.project-root` file; used by `rootutils.setup_root()`
- **Output directory**: Results saved to `./outputs/` by default
- **Frame constraints**: Height/width must be divisible by 8; num_frames in [17, 25, 33, 41]; fps in [8, 10, 12, 15, 24]