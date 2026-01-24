# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MuSc is a zero-shot industrial anomaly detection and segmentation method (ICLR 2024). It uses a Mutual Scoring mechanism to assign anomaly scores to unlabeled test images without training or prompts.

## Dependencies

- Python 3.8
- CUDA 11.7
- PyTorch 2.0.1
- See `requirements.txt` for other dependencies.

## Setup

1. Clone the repository.
2. Create a virtual environment: `conda create --name musc python=3.8 && conda activate musc`.
3. Install dependencies: `pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 && pip install -r requirements.txt`.

## Datasets

- MVTec AD: Place in `./data/mvtec_anomaly_detection/`.
- VisA: Place in `./data/visa/`. Preprocess with `python ./datasets/visa_preprocess.py`.
- BTAD: Place in `./data/btad/`.

## Running the Code

The main entry point is `examples/musc_main.py`. Arguments passed via command line override the defaults in `configs/musc.yaml`.

### Examples

Run on MVTec AD (all classes):
```bash
python examples/musc_main.py --device 0 \
--data_path ./data/mvtec_anomaly_detection/ --dataset_name mvtec_ad --class_name ALL \
--backbone_name ViT-L-14-336 --pretrained openai --feature_layers 5 11 17 23 \
--img_resize 518 --divide_num 1 --r_list 1 3 5 --batch_size 4 \
--output_dir ./output --vis True --save_excel True
```

### Key Configuration Options

- `backbone_name`: Feature extractor. Options include `ViT-L-14-336` (CLIP), `dinov2_vitb14`, etc.
- `pretrained`: Pretrained weights source (e.g., `openai` for CLIP).
- `r_list`: Aggregation degrees for the LNAMD module (e.g., `1 3 5`).
- `divide_num`: Number of subsets to split the test set into (for memory management).

## Architecture

- **Backbones**: Located in `models/backbone/`. Supports CLIP, DINO, and DINO_v2.
- **Core Modules**: `models/modules/` contains `_LNAMD.py` (Local Neighborhood Aggregation) and `_MSM.py` (Mutual Scoring Mechanism).
- **Main Model**: `models/musc.py` orchestrates the pipeline.