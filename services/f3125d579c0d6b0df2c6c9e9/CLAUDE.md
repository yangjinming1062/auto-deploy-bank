# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NeuRay is a neural rendering system for occlusion-aware image-based rendering. It supports two modes:
- **Generalization (gen)**: Renders novel views without scene-specific training
- **Finetuning (ft)**: Adapts the model to a specific scene for higher quality

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Train generalization model
python run_training.py --cfg configs/train/gen/neuray_gen_depth_train.yaml

# Render with pretrained model
python render.py --cfg configs/gen/neuray_gen_depth.yaml \
                 --database llff_colmap/fern/high \
                 --pose_type eval

# Evaluate rendering quality (PSNR/SSIM/LPIPS)
python eval.py --dir_gt data/render/<database_name>/gt \
               --dir_pr data/render/<database_name>/<renderer_name>-pretrain-eval

# Run COLMAP for custom scenes
python run_colmap.py --example_name desktop --colmap <path-to-colmap>

# Finetune on a specific scene
python run_training.py --cfg configs/train/ft/neuray_ft_depth_lego.yaml
```

## Architecture

### Core Components

- **network/renderer.py**: Main rendering network containing `NeuralRayGenRenderer` and `NeuralRayFtRenderer` classes
- **dataset/database.py**: `BaseDatabase` class manages all datasets; extend this for new datasets
- **train/trainer.py**: Training loop and validation logic
- **network/ibrnet.py**: Image-based rendering network components
- **network/init_net.py**: Depth and cost-volume initialization networks

### Data Flow

1. **Query ray sampling**: Sample rays from query views (`que_*` variables)
2. **Visibility feature projection**: Project query rays to reference views using camera poses (`prj_dict`)
3. **Radiance field construction**: Aggregate projected features via `agg_net`
4. **Volume rendering**: Integrate density and color along rays to get pixel colors

### Key Naming Conventions (see codes_explanations.md)

- `que`: Query/test view (novel view being rendered)
- `ref`: Reference/input view (source images)
- `prj`: Projected points on reference views
- `nr`: Network rendering (from constructed radiance fields)
- `dr`: Direction rendering (from NeuRay representation directly)
- `qn`: Query number (number of test views)
- `rfn`: Reference view number (working views)
- `rn`: Ray number
- `dn`: Depth sample number per ray

### Configuration System

- `configs/gen/*.yaml`: Rendering configs for generalization mode
- `configs/train/gen/*.yaml`: Training configs for generalization models
- `configs/train/ft/*.yaml`: Training configs for finetuning
- All settings controlled via YAML configs; no hardcoded parameters in core logic

### Renderer Architecture

```
NeuralRayBaseRenderer
├── vis_encoder: Encodes visibility features
├── dist_decoder: Predicts distance distribution (mixture logistics)
├── image_encoder: ResUNet for image features
├── agg_net: Aggregates reference view features
├── sph_fitter: Spherical harmonics for color prediction
└── (optional) fine_dist_decoder, fine_agg_net: Hierarchical sampling
```

## Database Format

Databases are named as `<dataset_name>/<scene_name>/<scene_setting>`:
- `llff_colmap/fern/high` - LLFF dataset, fern scene, high resolution
- `nerf_synthetic/lego/black_800` - NeRF Synthetic, lego scene, 800x800, black background
- `dtu_test/snowman/black_400` - DTU dataset, snowman scene, 400 resolution

Implement `BaseDatabase` subclass in `dataset/database.py` to add new datasets.