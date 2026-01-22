# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository implements **V3D: Video Diffusion Models are Effective 3D Generators**. It primarily consists of three distinct components:
1.  **sgm**: The core Video Diffusion model (based on Stable Video Diffusion).
2.  **recon**: 3D Gaussian Splatting training and rendering pipeline.
3.  **mesh_recon**: NeuS/Neuralangelo reconstruction pipeline.

## Common Commands

### Setup
```bash
# Install core dependencies
pip install -r requirements.txt

# Sync and install submodules for 3D Gaussian Splatting (recon)
cd recon
git config -f .gitmodules --get-regexp '^submodule\..*\.path$' | while read path_key path; do name=$(echo $path_key | sed 's/\submodule\.\(.*\)\.path/\1/'); url_key=$(echo $path_key | sed 's/\.path/.url/'); branch_key=$(echo $path_key | sed 's/\.path/.branch/'); url=$(git config -f .gitmodules --get "$url_key"); branch=$(git config -f .gitmodules --get "$branch_key" || echo "master"); git submodule add -b $branch --name $name $url $path || true; done
pip install submodules/diff-gaussian-rasterization
pip install submodules/simple-knn
cd ..
```

### Running Inference (Image to 3D)

1. **Generate Multi-view Video**:
   ```bash
   PYTHONPATH="." python scripts/pub/V3D_512.py --input_path <image> --save --border_ratio 0.3 --min_guidance_scale 4.5 --max_guidance_scale 4.5 --output-folder <output_dir>
   ```

2. **Reconstruct 3D (Gaussian Splatting)**:
   ```bash
   PYTHONPATH="." python recon/train_from_vid.py -w --sh_degree 0 --iterations 4000 --lambda_dssim 1.0 --lambda_lpips 2.0 --save_iterations 4000 --num_pts 100_000 --video <video_path>
   ```

3. **Reconstruct 3D (NeuS/Instant-NSR)**:
   ```bash
   cd mesh_recon
   PYTHONPATH="." python launch.py --config configs/videonvs.yaml --gpu <gpu_id> --train system.loss.lambda_normal=0.1 dataset.scene=<scene_name> dataset.root_dir=<output_dir> dataset.img_wh='[512, 512]'
   ```

4. **Refine Mesh** (requires Blender installed):
   ```bash
   python refine.py --mesh <mesh.obj> --scene <video> --num-opt 16 --lpips 1.0 --iters 500
   ```

## Code Architecture

- **`sgm/`**: Contains the video diffusion model, autoencoders, and sampling logic. heavily based on `Stability-AI/generative-models`.
- **`recon/`**: Contains the 3D Gaussian Splatting implementation (based on `3d-gaussian-splatting`). Note: This directory has its own `environment.yml` and submodule dependencies (`diff-gaussian-rasterization`, `simple-knn`) which must be built separately.
- **`mesh_recon/`**: Contains Neuralangelo/NeuS implementations. Uses `omegaconf` for config management. Runs via `launch.py`.
- **`scripts/`**: High-level scripts for running the pipeline (e.g., `scripts/pub/V3D_512.py`).

## Configuration

- **`configs/`**: Configuration files for various training and inference settings.
- **`mesh_recon/configs/`**: Hydra configurations for the NeuS pipeline.