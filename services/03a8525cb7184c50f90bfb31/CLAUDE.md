# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Aether is a geometric-aware unified world model that unifies 4D dynamic reconstruction, action-conditioned video prediction, and goal-conditioned planning. It is built on CogVideoX diffusion models and outputs RGB video, disparity (depth), and raymaps for camera pose estimation.

## Common Commands

### Running the Model

**CLI Demo:**
```bash
python scripts/demo.py --task <reconstruction|prediction|planning> --video <path> --image <path> --goal <path>
```

**Gradio Web Interface:**
```bash
python scripts/entrypoint.py
```

### Evaluation

```bash
# Video depth evaluation (requires sintel, kitti, bonn datasets in data/)
bash evaluation/video_depth/run_aether.sh

# Relative camera pose evaluation (requires tum, sintel, scannetv2 in data/)
pip install evo
bash evaluation/rel_pose/run_aether.sh
```

## Architecture

### Core Pipeline (`aether/pipelines/aetherv1_pipeline_cogvideox.py`)

The main `AetherV1PipelineCogVideoX` class inherits from `CogVideoXImageToVideoPipeline` and handles three tasks:

| Task | Input | Output | Default Steps | Guidance |
|------|-------|--------|---------------|----------|
| reconstruction | Video (N frames) | RGB, disparity, raymap | 4 | 1.0 |
| prediction | Image + optional raymap action | Future RGB, disparity, raymap | 50 | 3.0 |
| planning | Image + goal image | Path from obs to goal | 50 | 3.0 |

**Key methods:**
- `prepare_latents()`: Creates latent representations for image/video conditioning, concatenates camera_conditions from raymap
- `_preprocess_image()`: Centers crop images to target resolution (height/width must be divisible by 8)
- `check_inputs()`: Validates task-specific input requirements

### Data Flow

```
Input (Image/Video/Goal)
    ↓
Preprocess (crop_center, normalize, tokenize)
    ↓
Prepare Latents (encode with VAE, concatenate raymap as camera_conditions)
    ↓
Denoising Loop (transformer predicts noise in concatenated latents)
    ↓
Decode RGB/disparity/raymap from separated latent channels
    ↓
Postprocess (raymap_to_poses → project to pointcloud → save GLB)
```

### Key Output Structures

**`AetherV1PipelineOutput`:**
- `rgb`: np.ndarray (T, H, W, 3) - generated RGB frames in [0,1]
- `disparity`: np.ndarray (T, H, W) - inverse depth, lower values = further
- `raymap`: np.ndarray (T, 6, H/8, W/8) - encoded camera ray origins (3) + directions (3)

**Postprocessing (`postprocess_utils.py`):**
- `raymap_to_poses()`: Extracts camera extrinsics (4x4 matrices) from raymap
- `postprocess_pointmap()`: Projects disparity to 3D pointcloud using camera rays
- `smooth_poses()` / `smooth_trajectory()`: Kalman filter or Gaussian smoothing for camera trajectory

**Visualization (`visualize_utils.py`):**
- `predictions_to_glb()`: Converts pointclouds + camera poses to trimesh Scene (GLB export)
- Applies depth edge filtering (rtol parameter) to remove unreliable points

### Sliding Window Processing

For long videos in reconstruction mode, the pipeline uses overlapping windows:
- `num_frames`: Window size (must be 17, 25, 33, or 41)
- `sliding_window_stride`: Step between windows (default 24)
- `blend_and_merge_window_results()`: Aligns and blends overlapping windows using disparity scale + pose interpolation

### Raymap Actions (Prediction Task)

Raymaps encode camera motion as 6-channel features (ray origins + directions). Pre-computed actions available in `assets/example_raymaps/`:
- `backward`, `forward_right`, `left_forward`, `right`

## Model Configuration

- **Base CogVideoX model**: `THUDM/CogVideoX-5b-I2V`
- **Aether transformer**: `AetherWorldModel/AetherV1` (subfolder: `transformer`)
- **Precision**: torch.bfloat16
- **VAE**: AutoencoderKLCogVideoX with 8x spatial downsampling
- **Default resolution**: 480x720 (height x width)

## Important Conventions

- Height/width must be divisible by 8 (VAE downsampling factor)
- num_frames must be in [17, 25, 33, 41]
- fps must be in [8, 10, 12, 15, 24]
- Raymap shape: (T, 6, H/8, W/8) when provided
- Camera poses use OPENCV convention (X right, Y down, Z forward)
- Pointcloud axes are flipped (Y and X) when saving to GLB for correct visualization