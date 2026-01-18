# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository combines [MMOCR](https://github.com/open-mmlab/mmocr) with [Segment Anything Model (SAM)](https://github.com/facebookresearch/segment-anything) to build OCR-related applications including **SAM for Text**, **Text Erasure**, and **Text Inpainting**. All applications can be run via command-line scripts or interactive Gradio web interfaces.

## Project Structure

- **app.py** - Main Gradio web interface combining all features (detection, erasure, inpainting)
- **mmocr_sam.py** - Basic SAM for text (detection + segmentation)
- **mmocr_sam_erase.py** - Text erasure using diffusion models
- **mmocr_sam_inpainting.py** - Text inpainting with Stable Diffusion
- **mmocr_sam_erase_app.py** - Gradio interface for erasure
- **mmocr_sam_inpainting_app.py** - Gradio interface for inpainting
- **latent_diffusion/** - Latent diffusion model implementation (LDM)
- **mmocr_dev/** - MMOCR configuration files (configs/, dicts/)
- **docs/** - Documentation (currently minimal)
- **imgs/** - Example images for testing

## Common Commands

### Installation
```bash
# Create conda environment
conda create -n ocr-sam python=3.8 -y
conda activate ocr-sam

# Install PyTorch (CUDA 11.3)
pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 --extra-index-url https://download.pytorch.org/whl/cu113

# Install MMOCR
pip install -U openmim
mim install mmengine
mim install mmocr
mim install 'mmcv==2.0.0rc4'
mim install 'mmdet==3.0.0rc5'
mim install 'mmcls==1.0.0rc5'

# Install SAM
pip install git+https://github.com/facebookresearch/segment-anything.git

# Install dependencies
pip install -r requirements.txt

# Install diffusion and web interface
pip install gradio diffusers pytorch-lightning==2.0.1.post0
```

### Model Checkpoints
```bash
# Create directories
mkdir checkpoints checkpoints/mmocr checkpoints/sam checkpoints/ldm

# Download models (or use app.py to auto-download)
wget -O checkpoints/mmocr/db_swin_mix_pretrain.pth https://github.com/yeungchenwa/OCR-SAM/releases/download/ckpt/db_swin_mix_pretrain.pth
wget -O checkpoints/mmocr/abinet_20e_st-an_mj_20221005_012617-ead8c139.pth https://download.openmmlab.com/mmocr/textrecog/abinet/abinet_20e_st-an_mj/abinet_20e_st-an_mj_20221005_012617-ead8c139.pth
wget -O checkpoints/sam/sam_vit_h_4b8939.pth https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth
wget -O checkpoints/ldm/last.ckpt https://heibox.uni-heidelberg.de/f/4d9ac7ea40c64582b7c9/?dl=1
```

### Running Applications

**SAM for Text (CLI)**:
```bash
python mmocr_sam.py --inputs /path/to/image --outdir results/ --device cuda
```

**Erasure (CLI)**:
```bash
python mmocr_sam_erase.py \
    --inputs /path/to/image \
    --outdir results/ \
    --device cuda \
    --use_sam True \
    --dilate_iteration 2 \
    --diffusion_model stable-diffusion  # or latent-diffusion
```

**Inpainting (CLI)**:
```bash
python mmocr_sam_inpainting.py \
    --img_path /path/to/image \
    --outdir results/ \
    --device cuda \
    --prompt "Your text prompt" \
    --select_index 0
```

**Web UI**:
```bash
# All-in-one interface
python app.py

# Erasure only
python mmocr_sam_erase_app.py

# Inpainting only
python mmocr_sam_inpainting_app.py
```

## Architecture

### Core Pipeline
1. **Text Detection**: DBNet++ (with SwinV2 backbone) detects text regions and generates polygons
2. **Text Recognition**: ABINet recognizes text content from detected regions
3. **Segmentation**: SAM generates precise masks for detected text regions
4. **Processing**: Either erasure (using latent/stable diffusion) or inpainting (using Stable Diffusion)

### Key Integration Points
- **MMOCR → SAM**: MMOCR's polygon outputs are converted to bounding boxes and fed to SAM's `predict_torch` with `apply_boxes_torch`
- **SAM → Diffusion**: SAM masks are processed (optionally dilated) and passed to diffusion models for inpainting/erasure
- **latent_diffusion/ldm_erase_text.py:82**: Contains `erase_text_from_image()` function used by erasure pipeline

### Model Configuration
- Detection: `mmocr_dev/configs/textdet/dbnetpp/dbnetpp_swinv2_base_w16_in21k.py`
- Recognition: `mmocr_dev/configs/textrecog/abinet/abinet_20e_st-an_mj.py`
- SAM: vit_h (highest accuracy)
- Diffusion: Stable Diffusion 2 Inpainting or Latent Diffusion

## Important Notes

- All scripts expect CUDA device; change `--device cpu` for CPU-only inference
- First run downloads model checkpoints automatically (see `app.py:1-6`)
- Checkpoints should be placed in `checkpoints/` directory structure
- No formal test suite exists; use images in `imgs/` directory for manual testing
- Web interfaces include example images for quick testing
- Mask dilation (--dilate_iteration) improves erasure quality by expanding detected regions