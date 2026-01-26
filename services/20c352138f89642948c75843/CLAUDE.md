# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

HuatuoGPT-Vision is a medical multimodal LLM project for injecting medical visual knowledge into LLMs at scale. The codebase supports two model architectures:
- **Legacy LLaVA-based models**: Uses `LlavaLlamaForCausalLM` or `LlavaQwen2ForCausalLM` from `llava/model/language_model/`
- **Qwen2.5-VL based models**: Uses `Qwen2_5_VLForConditionalGeneration` with `Qwen2_5_VLProcessor`

## Build & Test Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Model inference (CLI chat interface)
python cli.py --model_dir path-to-huatuogpt-vision-model

# Evaluate on medical VQA datasets
accelerate launch eval.py --data_path Medical_Multimodal_Evaluation_Data/medical_multimodel_evaluation_data.json --model_path HuatuoGPT-Vision-7B

# Convert Qwen2.5-LLM to Qwen2.5-VL (initialization step)
python convert_llm_to_vl.py --vl_model_path Qwen/Qwen2.5-VL-7B-Instruct --llm_model_path Qwen/Qwen2.5-7B-Instruct --save_path ./Qwen2.5-VL-7B-Base

# Vision alignment pretraining (DeepSpeed)
accelerate launch --config_file ./config/ds.yaml --num_processes 8 train_vl.py \
  --experiment_name huatuogpt_vision_alignment --model_path ./Qwen2.5-VL-7B-Base \
  --data_path Vision_Alignment_Data.json --output_dir ./huatuogpt_vision_alignment_checkpoint

# Vision instruction fine-tuning
accelerate launch --config_file ./config/ds.yaml --num_processes 8 train_vl.py \
  --experiment_name huatuogpt_vision_sft --model_path huatuogpt_vision_alignment_model \
  --data_path Vision_SFT_Data.json
```

## Key Files

| File | Purpose |
|------|---------|
| `cli.py` | `HuatuoChatbot` class for model inference; handles image preprocessing and conversation tokenization |
| `eval.py` | Evaluation on medical VQA datasets (VQA-RAD, SLAKE, PathVQA, PMC-VQA, OmniMedVQA, MMMU-Medical) |
| `train_vl.py` | Training script for Qwen2.5-VL models with support for gradient checkpointing and layer freezing |
| `scorer.py` | Scoring utilities for multiple-choice VQA evaluation (`score_mix_llava()`) |
| `llava/model/` | Legacy LLaVA model architecture (for older model checkpoints) |

## Architecture Notes

- **Training**: Uses `accelerate` with DeepSpeed ZeRO stage 1. Configure via `config/ds.yaml` (8 GPUs by default)
- **Evaluation**: Uses `HuatuoChatbot` for inference with distributed gathering via `torch.distributed`
- **Image Processing**: Legacy models use `image_processor` from vision tower; Qwen2.5-VL models use `Qwen2_5_VLProcessor` with `qwen_vl_utils.fetch_image`
- **Conversation Format**: Uses `<|user|>` and `<|assistant|>` tokens for Qwen2.5-VL; `<image>` placeholders for images
- **Freezing Options**: `--freeze_vision_tower`, `--freeze_multi_modal_projector`, `--freeze_language_model` flags in training