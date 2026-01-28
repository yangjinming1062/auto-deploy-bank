# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FakeShield is a multi-modal framework for explainable image forgery detection and localization (IFDL). It uses multi-modal large language models (MLLMs) to analyze manipulated images, generate tampered region masks, and provide human-understandable explanations. The system consists of two core modules that process images sequentially:

1. **DTE-FDM** (Domain Tag-guided Explainable Forgery Detection Module): Built on LLaVA architecture, classifies forgery type and provides textual explanations of artifacts/inconsistencies
2. **MFLM** (Multimodal Forgery Localization Module): Built on GLaMM architecture, uses SAM (Segment Anything Model) to generate pixel-level tampered region masks

**Pipeline Flow**: Image → DTE-FDM (detection + explanation + domain tag) → MFLM (mask generation guided by DTE-FDM output)

## Common Commands

### Installation

```bash
# Install core dependencies
pip install -r requirements.txt

# Install MMCV (required)
git clone https://github.com/open-mmlab/mmcv
cd mmcv
git checkout v1.4.7
MMCV_WITH_OPS=1 pip install -e .

# Install DTE-FDM
cd DTE-FDM
pip install -e .
pip install -e ".[train]"
pip install flash-attn --no-build-isolation
```

### Model Weight Setup

```bash
# Download FakeShield weights
huggingface-cli download --resume-download zhipeixu/fakeshield-v1-22b --local-dir weight/

# Download SAM pretrained weight for MFLM
wget https://huggingface.co/ybelkada/segment-anything/resolve/main/checkpoints/sam_vit_h_4b8939.pth -P weight/
```

Expected weight structure:
```
weight/
├── fakeshield-v1-22b/
│   ├── DTE-FDM/
│   ├── MFLM/
│   └── DTG.pth
└── sam_vit_h_4b8939.pth
```

### Running the Demo

```bash
# CLI demo (single image)
bash scripts/cli_demo.sh

# Environment variables that can be customized:
# WEIGHT_PATH      - Path to FakeShield weights (default: ./weight/fakeshield-v1-22b)
# IMAGE_PATH       - Input image path
# DTE_FDM_OUTPUT   - DTE-FDM output JSONL path
# MFLM_OUTPUT      - MFLM output directory path
```

### Training

**DTE-FDM LoRA Fine-tuning:**
```bash
bash ./scripts/DTE-FDM/finetune_lora.sh
```
Uses DeepSpeed ZeRO-3 for distributed training. Requires `transformers==4.37.2`.

**MFLM LoRA Fine-tuning:**
```bash
bash ./scripts/MFLM/finetune_lora.sh
```
Uses DeepSpeed for training. Uses SAM mask decoder with LoRA. Requires `transformers==4.28.0`.

### Testing

```bash
bash ./scripts/test.sh
```

## Architecture Details

### DTE-FDM Module (`DTE-FDM/`)
- Based on LLaVA (LLaMA + CLIP vision encoder)
- Key files:
  - `llava/model/llava_arch.py`: Core LLaVA architecture with multimodal projector
  - `llava/train/train_mem.py`: Training script with LoRA support
  - `llava/serve/cli.py`: CLI inference interface
  - `llava/model/multimodal_encoder/`: Vision encoder (CLIP ViT-L/336)
  - `llava/model/multimodal_projector/`: MLP projector connecting vision to LLM
- DTG (Domain Tag Generator) provides forgery type guidance

### MFLM Module (`MFLM/`)
- Based on GLaMM (Ground LLaMA with SAM)
- Key files:
  - `model/GLaMM.py`: Core GLaMM model combining LLaMA with SAM
  - `model/SAM/`: SAM (Segment Anything Model) implementation
  - `cli_demo.py`: CLI interface for MFLM
  - `test.py`: Test script
  - `dataset/Tamper_PS_Segm_ds.py`: PhotoShop tampering segmentation dataset
- Uses special tokens: `<bbox>`, `[SEG]`, `<p>`, `</p>` for segmentation output format

### Key Configuration Files
- `scripts/DTE-FDM/zero3.json`: DeepSpeed ZeRO-3 configuration
- `scripts/DTE-FDM/zero2.json`: DeepSpeed ZeRO-2 configuration
- `scripts/DTE-FDM/zero3_offload.json`: ZeRO-3 with CPU offload

## Dependency Notes

- **Python**: 3.9
- **PyTorch**: 1.13.0
- **CUDA**: 11.6
- **Transformers version matters**: DTE-FDM requires `transformers==4.37.2`, MFLM requires `transformers==4.28.0`
- **MMCV**: Required for MFLM's mmdetection codebase
- **Flash Attention**: Required for efficient attention computation

## Dataset Organization for Training

```
dataset/
├── photoshop/           # CASIAv2, Fantastic Reality, CASIA1+, IMD2020, Columbia, coverage, NIST16, DSO, Korus
├── deepfake/            # FaceAPP, FFHQ
├── aigc/                # SD_inpaint, COCO2017
└── MMTD_Set/           # Multi-Modal Tamper Description (MMTD-Set-34k.json)
```

## Important Notes

- DTE-FDM and MFLM have conflicting `transformers` version requirements; scripts handle this by reinstalling before each operation
- Both modules use DeepSpeed for training; ensure GPUs are properly configured
- MFLM uses bfloat16 precision; ensure GPU supports it
- SAM pretrained weights (`sam_vit_h_4b8939.pth`) are required for MFLM even when using FakeShield weights