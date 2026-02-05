# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SkyAR is a PyTorch-based video sky replacement and harmonization system. It performs real-time sky segmentation and replacement with controllable styles, using a vision-based approach without requirements on capturing devices.

## Common Commands

### Running Inference (Sky Replacement)

```bash
# Run with a specific config
python skymagic.py --path ./config/config-canyon-district9ship.json

# Available configs in ./config/:
# - config-annarbor-castle.json
# - config-annarbor-supermoon.json
# - config-annarbor-thunderstorm.json
# - config-canyon-district9ship.json
# - config-canyon-galaxy.json
# - config-canyon-jupiter.json
# - config-canyon-rain.json

# Outputs:
# - demo.mp4: Final sky-replaced video
# - demo-cat.mp4: Side-by-side comparison (input | output)
```

### Training Sky Matting Model

```bash
python train.py \
    --dataset cvprw2020-ade20K-defg \
    --checkpoint_dir ./checkpoints \
    --vis_dir ./val_out \
    --in_size 384 \
    --max_num_epochs 200 \
    --lr 1e-4 \
    --batch_size 8 \
    --net_G coord_resnet50
```

**Note:** Training requires the full [CVPRW20-SkyOpt dataset](https://github.com/google/sky-optimization). The mini dataset in `datasets.zip` is only for demonstrating directory structure.

### Dependencies

```
matplotlib, scikit-image, scikit-learn, scipy, numpy,
torch, torchvision, opencv-python, opencv-contrib-python
```

### Pretrained Model

Download from [Google Drive](https://drive.google.com/file/d/1COMROzwR4R_7mym6DL9LXhHQlJmJaV0J/view?usp=sharing) and unzip to get `checkpoints_G_coord_resnet50/`.

## Architecture

### Pipeline Flow (skymagic.py → SkyFilter)

1. **Sky Matting** (`networks.py`): `ResNet50FCN` takes input frame → outputs coarse sky mask
   - Supports `resnet50` or `coord_resnet50` (with CoordConv layers for spatial awareness)
   - FPN-like decoder upscales features back to input resolution

2. **Mask Refinement** (`skyboxengine.py`): `SkyBox.skymask_refinement()` uses guided filtering to refine the coarse mask

3. **Motion Estimation** (`skybox_utils.py`): Optical flow tracking on sky regions estimates camera motion:
   - ShiTomasi corner detection on sky pixels
   - `cv2.calcOpticalFlowPyrLK` tracks features between frames
   - Kernel density filtering removes outliers
   - Affine transformation matrix fitted to motion

4. **Sky Rendering** (`skyboxengine.py`): `SkyBox.get_skybg_from_box()` warps skybox image using motion matrix

5. **Blending & Harmonization** (`skyboxengine.py`): `SkyBox.skyblend()` combines:
   - Alpha blending based on refined sky mask
   - `relighting()` for color matching between foreground and skybox
   - Optional `halo()` effect for realistic atmospheric scattering
   - Rain overlay if `rainy` in skybox filename

### Key Classes

| File | Class | Purpose |
|------|-------|---------|
| `skymagic.py` | `SkyFilter` | Main orchestrator; handles video/image loading, runs pipeline, writes output |
| `matting.py` | `SkyDetector` | Training loop for sky matting network |
| `networks.py` | `ResNet50FCN` | U-Net style encoder-decoder with optional CoordConv |
| `skyboxengine.py` | `SkyBox` | Sky rendering, blending, and harmonization |
| `skybox_utils.py` | - | Motion estimation utilities (`estimate_partial_transform`, `removeOutliers`) |
| `utils.py` | `CVPR2020_ADE20K_DEGF_Dataset` | Data loading with augmentations |

### Configuration Schema (JSON)

```json
{
  "net_G": "coord_resnet50",
  "ckptdir": "./checkpoints_G_coord_resnet50",
  "input_mode": "video|seq",
  "datadir": "./test_videos/annarbor.mp4",
  "skybox": "floatingcastle.jpg",
  "in_size_w": 384, "in_size_h": 384,
  "out_size_w": 845, "out_size_h": 480,
  "skybox_center_crop": 0.5,
  "auto_light_matching": false,
  "relighting_factor": 0.8,
  "recoloring_factor": 0.5,
  "halo_effect": true,
  "output_dir": "./eval_output",
  "save_jpgs": false
}
```

### Important Implementation Details

- **Device selection**: Automatic CUDA if available, else CPU (`torch.device("cuda:0" if torch.cuda.is_available() else "cpu")`)
- **Frame format**: OpenCV uses BGR, but internally converted to RGB for processing
- **Output range**: Images are normalized to [0, 1] float32 throughout the pipeline
- **CoordConv** (`networks.py:115-146`): Adds coordinate channels before convolution for spatial-aware features
- **Guided filtering** (`skyboxengine.py:70-78`): Uses blue channel as guidance for refined alpha matte