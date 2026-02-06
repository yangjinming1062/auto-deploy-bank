# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sa2VA (SAM2 + LLaVA) is a unified multi-modal model for dense grounded understanding of images and videos. It combines SAM-2 (Segment Anything Model 2) with LLaVA-style vision-language models to support referring segmentation, VQA, and conversation tasks.

## Installation

Use `uv` for dependency management:
```bash
uv sync --extra=latest    # For InternVL3, Qwen2.5-VL, Qwen3-VL models
uv sync --extra=legacy    # For InternVL2.5 and earlier models
source .venv/bin/activate
```

## Commands

### Demo
```bash
# Script-based demo with image/video folder
python demo/demo.py PATH_TO_FOLDER --model_path ByteDance/Sa2VA-8B --work-dir OUTPUT_DIR --text "<image>Describe the video"

# Gradio web interface
PYTHONPATH=. python projects/sa2va/gradio/app.py ByteDance/Sa2VA-4B
```

### Training
Uses MMEngine + XTuner with distributed training:
```bash
# Multi-GPU training (requires 8+ GPUs, A100 recommended)
bash tools/dist.sh train projects/sa2va/configs/sa2va_in30_8b.py 8

# Fine-tuning
bash tools/dist.sh train projects/sa2va/configs/sa2va_finetune.py 8
```

### Model Conversion
```bash
# PTH (training) -> HuggingFace format
python tools/convert_to_hf.py projects/sa2va/configs/sa2va_in30_8b.py --pth-model PATH --save-path PATH

# HuggingFace -> PTH (for fine-tuning)
python tools/convert_to_pth.py hf_model_path --save-path PATH --arch-type internvl  # or qwen
```

### Evaluation

**Referring Segmentation:**
```bash
# Run all segmentation benchmarks
python projects/sa2va/evaluation/run_all_evals.py /path/to/HF_MODEL --gpus 8

# Single benchmark
./projects/sa2va/evaluation/dist_test.sh projects/sa2va/evaluation/sa2va_eval_ref_vos.py path-to-hf-model 8 --work-dir path-to-output
```

**VQA Benchmarks** (via sa2va_eval/VLMEvalKit):
```bash
# Single GPU
python sa2va_eval/run.py --data MMBench_DEV_EN MME SEEDBench_IMG --model Sa2VA-4B --verbose

# Multi-GPU
torchrun --nproc-per-node=8 sa2va_eval/run.py --data MMBench_DEV_EN SEEDBench_IMG MMStar --model Sa2VA-4B Sa2VA-8B --verbose
```

## Architecture

### Model Components (`projects/sa2va/models/`)

- `sa2va.py` - Main **Sa2VAModel** class combining:
  1. **MLLM Backbone** (`mllm`): InternVL, Qwen-VL providing text/image embeddings
  2. **SAM2 Grounding Encoder** (`grounding_encoder`): `SAM2TrainRunner` for mask generation
  3. **Projection Layer** (`text_hidden_fcs`): Maps MLLM hidden states to SAM2's hidden dim
  4. **Loss Functions**: CrossEntropyLoss and DiceLoss for mask supervision
- `mllm/` - MLLM wrapper classes (InternVLMLLM, etc.)
- `sam2_train.py` - SAM2 integration for training

### Training Configuration (`projects/sa2va/configs/`)

Configs use MMEngine's registry system with 5 parts:
1. **Settings**: Model path, tokenizer, max_length
2. **Model**: MLLM + SAM2 config, LoRA settings
3. **Dataset**: Task-specific configs (see below)
4. **Scheduler/Optimizer**: LinearLR + CosineAnnealing, AdamW
5. **Runtime**: Hooks for checkpoint, logger, distributed

**Dataset Types** (`projects/sa2va/datasets/`):
- `Sa2VA01RefSeg` - Image referring segmentation (RefCOCO, RefCOCO+, RefCOCOg)
- `LLaVADataset` - Image VQA (LLaVA-665k)
- `Sa2VA03RefVOS` - Video referring segmentation (ReVOS, MeVIS, RefYTVOS, Ref-SAV)
- `Sa2VA04VideoQA` - Video question answering (UniVI)
- `Sa2VA05GCGDataset` - Grounded conversation (GCG tasks)
- `Sa2VA06VPDataset` - Visual pointing (Osprey-724k)

### Key Integration Points

- Special tokens: `[SEG]`, `<p>`, `</p>`, `<vp>`, `</vp>` - the `[SEG]` token identifies segmentation requests
- Forward pass returns `prediction`, `prediction_masks` when `[SEG]` is in output
- Training uses `sa2va_collect_fn` for collation

### Evaluation Wrappers

- `sa2va_eval/vlmeval/vlm/sa2va_chat.py` - **Sa2VAChat** for VQA evaluation
- `projects/sa2va/hf/` - HuggingFace model wrappers

## Data Structure

**Training data** in `./data/`:
```
data/
├── video_datas/          # ReVOS, MeVIS, DAVIS, SA-V, etc.
├── ref_seg/              # RefCOCO/RefCOCO+/RefCOCOg
├── glamm_data/           # GCG annotations
├── osprey-724k/          # Conversation/description
├── llava_data/           # LLaVA VQA
└── sam_v_full/           # SA-V (download from Meta separately)
```

**Pretrained models** in `./pretrained/`:
```
pretrained/
├── sam2_hiera_large.pt
└── InternVL2_5-4B/  (or InternVL3-8B, etc.)
```

## Supported Model Families

| Family | Example Models | Extra |
|--------|---------------|-------|
| InternVL2.5 | Sa2VA-1B/4B/8B/26B | legacy |
| InternVL3 | Sa2VA-InternVL3-2B/8B/14B | latest |
| Qwen2.5-VL | Sa2VA-Qwen2_5-VL-3B/7B | latest |
| Qwen3-VL | Sa2VA-Qwen3-VL-2B/4B | latest |