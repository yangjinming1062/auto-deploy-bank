# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Aether is a geometric-aware unified world modeling system that unifies three capabilities: 4D dynamic reconstruction, action-conditioned video prediction, and goal-conditioned visual planning. Built on CogVideoX, it accepts video/image inputs with optional camera raymap actions or goal images.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# 4D reconstruction from video
python scripts/demo.py --task reconstruction --video ./assets/example_videos/moviegen.mp4

# Action-conditioned video prediction
python scripts/demo.py --task prediction --image ./assets/example_obs/car.png --raymap_action assets/example_raymaps/raymap_forward_right.npy

# Goal-conditioned visual planning
python scripts/demo.py --task planning --image ./assets/example_obs_goal/01_obs.png --goal ./assets/example_obs_goal/01_goal.png

# Interactive Gradio demo
python scripts/demo_gradio.py

# Run evaluation
bash evaluation/video_depth/run_aether.sh   # Video depth evaluation
bash evaluation/rel_pose/run_aether.sh      # Relative camera pose evaluation

# Linting and formatting
pre-commit run --all-files  # Runs ruff (format + lint) and other hooks
```

## Architecture

- **Pipeline Core**: `aether/pipelines/aetherv1_pipeline_cogvideox.py` implements `AetherV1PipelineCogVideoX`, extending `CogVideoXImageToVideoPipeline`. Handles three tasks via the `__call__` method with configurable inference steps and guidance scales.
- **Utility Modules**: `aether/utils/` contains preprocessing (`preprocess_utils.py`: center cropping), postprocessing (`postprocess_utils.py`: depth/pose transforms, camera raymap conversions), and visualization (`visualize_utils.py`: predictions to GLB/trimesh scenes).
- **Model Components**: Uses `diffusers` library components - `CogVideoXTransformer3DModel`, `AutoencoderKLCogVideoX`, `CogVideoXDPMScheduler`, T5 encoder for text/prompt processing.
- **Evaluation**: `evaluation/` contains sliding-window inference scripts that handle 480x720 input dimensions, blending outputs across spatial and temporal windows.

## Input Conventions

- **Reconstruction**: Video file (processed with center-crop to 480x720 if needed)
- **Prediction**: Single image + raymap action numpy array (N, 6, H/8, W/8) representing camera trajectory
- **Planning**: Observation image + goal image pair

Camera poses must be in the coordinate system of the first frame. Use `camera_pose_to_raymap()` in `aether/utils/postprocess_utils.py` to convert camera trajectories to raymap actions.

## Key Configuration

- Linting: Ruff configured in `pyproject.toml` with 88-char line length
- Pre-commit: `ruff` (fix + format) and basic checks in `.pre-commit-config.yaml`
- Model weights: Download from Hugging Face (`AetherWorldModel/AetherV1`)