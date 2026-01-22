# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DOVER is a Disentangled Objective Video Quality Evaluator (VQA) for User Generated Contents (UGC) from aesthetic and technical perspectives. It features a dual-branch architecture:
- **Technical branch**: Uses Swin Transformer 3D (`swin_tiny_grpb`) for spatial-temporal fragment-based quality assessment
- **Aesthetic branch**: Uses ConvNeXt 3D (`conv_tiny`) for frame-level quality assessment

## Installation

```bash
pip install -e .
mkdir pretrained_weights
cd pretrained_weights
wget https://github.com/QualityAssessment/DOVER/releases/download/v0.1.0/DOVER.pth
wget https://github.com/QualityAssessment/DOVER/releases/download/v0.5.0/DOVER-Mobile.pth
cd ..
```

## Key Commands

### Evaluation (Pre-trained Models)
```bash
# Single video with fused quality score
python evaluate_one_video.py -v ./demo/17734.mp4 -f

# With relative ranks in UGC-VQA databases
python evaluate_one_video.py -v ./demo/17734.mp4

# Evaluate a directory of videos
python evaluate_a_set_of_videos.py -in $INPUT_DIR -out $OUTPUT_CSV_PATH

# Default inference on all benchmark datasets
python default_infer.py

# ONNX conversion (for deployment)
python convert_to_onnx.py
python onnx_inference.py -v ./demo/17734.mp4
```

### Training
```bash
# Head-only transfer learning (recommended, low memory)
python transfer_learning.py -t val-kv1k   # KoNViD-1k
python transfer_learning.py -t val-ytugc  # YouTube-UGC
python transfer_learning.py -t val-livevqc  # LIVE-VQC
python transfer_learning.py -t val-cvd2014  # CVD2014

# End-to-end fine-tuning: set num_epochs: 0 -> 15 in dover.yml

# Full training with DIVIDE framework
python training_with_divide.py
```

### DOVER vs DOVER-Mobile
Add `-o dover-mobile.yml` to switch to the lighter model (9.86M params, 52.3 GFLOPs, 1.4s per video on CPU).

## Architecture

### Core Package: `dover/`
- **`models/`** - Neural network components
  - `evaluator.py`: Main `DOVER` class with dual-backbone architecture
  - `swin_backbone.py`: SwinTransformer3D for video feature extraction
  - `conv_backbone.py`: ConvNeXt3D for aesthetic quality assessment
  - `head.py`: VQA regression heads (VQAHead, IQAHead, VARHead)
- **`datasets/`** - Data loading
  - `dover_datasets.py`: `ViewDecompositionDataset` for aesthetic/technical view decomposition
  - `basic_datasets.py`: Base dataset classes and frame samplers

### Configuration Files
- `dover.yml`: Main config (DOVER, num_epochs=0 for head-only transfer)
- `dover-mobile.yml`: Lightweight DOVER config
- `divide.yml`: DIVIDE framework training config

### Key Configuration Structure
```yaml
model:
  type: DOVER
  args:
    backbone:
      technical: {type: swin_tiny_grpb}  # Fragments branch
      aesthetic: {type: conv_tiny}       # Resize branch
    divide_head: true  # Separate heads for each branch
    vqa_head: {in_channels: 768, hidden_channels: 64}
```

## View Decomposition (Key Concept)

DOVER processes videos through two pathways:
- **Technical view** (`fragments`): 7x7 grid of 32x32 patches sampled across time for compression/encoding artifacts
- **Aesthetic view** (`resize`): Full frames at 224x224 for content composition/aesthetics

Both views are processed independently, then fused via weighted combination.

## Dataset Labels

Label files are in `examplar_data_labels/`:
- LIVE_VQC, KoNViD, LSVQ (test/1080p), CVD2014, YouTubeUGC

Expected data structure:
```
datasets/
  LIVE_VQC/
  KoNViD/
  LSVQ/
  YouTubeUGC/
  CVD2014/
```

## Dependencies

Key packages: `torch~=1.13`, `torchvision`, `opencv-python`, `decord`, `timm`, `einops`, `wandb`, `thop==0.0.31-2005241907`, `onnx`

## Paper Citation

```bibtex
@inproceedings{wu2023dover,
  title={Exploring Video Quality Assessment on User Generated Contents from Aesthetic and Technical Perspectives},
  author={Wu, Haoning and Zhang, Erli and Liao, Liang and Chen, Chaofeng and Hou, Jingwen and Wang, Annan and Sun, Wenxiu and Yan, Qiong and Lin, Weisi},
  year={2023},
  booktitle={ICCV},
}
```