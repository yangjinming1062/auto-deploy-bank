# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Image-Generation-CoT is a research repository exploring Chain-of-Thought (CoT) reasoning for autoregressive image generation. It implements verification (ORM, PARM) and preference alignment (DPO) techniques to improve image generation quality. The base model is [Show-o](https://github.com/showlab/Show-o), an autoregressive text-to-image model using discrete token generation with mask scheduling.

## Installation

```bash
conda create -n img_cot python=3.10
conda activate img_cot
pip install -r requirements.txt

# Install mmdetection for GenEval evaluation
git clone https://github.com/open-mmlab/mmdetection.git
cd mmdetection && git checkout 2.x && pip install -v -e .

# Install LLaVA-NeXT for reward models
git clone https://github.com/LLaVA-VL/LLaVA-NeXT && cd LLaVA-NeXT && pip install -e ".[train]"
```

## Common Commands

### Training

```bash
# Train ORM (Outcome Reward Model)
bash scripts/orm_ft.sh

# Train PARM (Potential Assessment Reward Model)
bash scripts/parm.sh

# Train Show-o with DPO (Direct Preference Optimization)
bash scripts/dpo.sh
```

### Evaluation / Image Generation

All evaluation runs use torchrun for distributed training across 8 GPUs:

```bash
# Baseline Show-o (no reward model)
torchrun --nnodes=1 --nproc_per_node=8 --node_rank=0 --master_port=12475 main.py \
  --prompts_file geneval/prompts/generation_prompts.txt \
  --metadata_file geneval/prompts/evaluation_metadata.jsonl \
  --config config.yaml

# Zero-shot ORM
torchrun --nnodes=1 --nproc_per_node=8 --node_rank=0 --master_port=12475 main.py \
  --prompts_file geneval/prompts/generation_prompts.txt \
  --metadata_file geneval/prompts/evaluation_metadata.jsonl \
  --config config.yaml \
  --reward_model orm_zs

# Fine-tuned ORM
--reward_model orm_ft

# PARM
--reward_model parm

# DPO models (combine with reward models)
--dpo_model dpo           # Initial DPO
--dpo_model dpo_iter      # Iterative DPO
--dpo_model dpo_iter_parm_guide  # Iterative DPO with PARM guidance

# Example: Iterative DPO + PARM
torchrun --nnodes=1 --nproc_per_node=8 --node_rank=0 --master_port=12475 main.py \
  --prompts_file geneval/prompts/generation_prompts.txt \
  --metadata_file geneval/prompts/evaluation_metadata.jsonl \
  --config config.yaml \
  --reward_model parm \
  --dpo_model dpo_iter_parm_guide
```

Or use the convenience script:
```bash
./run.sh  # Edit REWARD_MODEL and DPO_MODEL variables as needed
```

### Download Models

```bash
# GenEval evaluation models
mkdir geneval/evaluation/object
bash geneval/evaluation/download_models.sh geneval/evaluation/object

# Reward model and DPO checkpoints (from HuggingFace)
# Download from https://huggingface.co/ZiyuG/Image-Generation-CoT and place in ckpts/
```

## Architecture

### Entry Points
- `main.py` - Dispatcher that routes to different execution modes based on `--reward_model` and `--dpo_model` flags
- `orm.py` - ORM (Outcome Reward Model) evaluation; uses ImageSelector to score final images
- `parm.py` - PARM (Potential Assessment Reward Model) evaluation; scores intermediate generation steps with potential assessment
- `baseline.py` - Vanilla Show-o generation without reward model

### Key Components

**Showo Model** (`models/modeling_showo.py`):
- Autoregressive text-to-image model based on Phi-1.5 LLM
- Uses discrete token prediction with mask scheduling (MaskGit-style)
- `t2i_generate()` method handles iterative generation with classifier-free guidance

**MAGVITv2** (`models/modeling_magvitv2.py`):
- VQGAN for encoding/decoding images to/from discrete tokens
- `decode_code()` converts token IDs back to images

**ImageSelector** (`selector.py`):
- LLaVA-based reward model for evaluating generated images
- `orm()` - Final image quality assessment (yes/no + confidence)
- `parm()` - Intermediate step potential assessment with clarity judgment

**Training** (`training/`):
- `train.py` - Show-o fine-tuning
- `train_dpo.py` - DPO preference alignment training
- `train_w_clip_vit.py` - Training with CLIP vision encoder
- `prompting_utils.py` - UniversalPrompting handles tokenization with special tokens (`<|soi|>`, `<|eoi|>`, `<|t2i|>`, etc.)

### Configuration

Config files use OmegaConf YAML format (`config.yaml`, `scripts/*.yaml`):
- `model.showo` - Show-o architecture (vocab sizes, LLM path, token counts)
- `model.vq_model` - VQGAN configuration
- `training` - Batch size, guidance scale, timesteps, noise schedule
- `dataset.preprocessing` - Max sequence length, resolution

### Key Files
- `models/sampling.py` - `cosine_schedule()`, `mask_by_random_topk()` for mask generation
- `models/phi.py` - PhiForCausalLM wrapper
- `llava/` - LLaVA-NeXT dependencies for reward model
- `geneval/prompts/` - Test prompts and metadata for GenEval benchmark

## Model Checkpoints

Expected checkpoint locations:
- `ckpts/orm_ft` - Fine-tuned ORM
- `ckpts/parm` - Fine-tuned PARM
- `ckpts/dpo` - Initial DPO
- `ckpts/dpo_iter` - Iterative DPO
- `ckpts/dpo_iter_parm_guide` - Iterative DPO with PARM guidance

## Dependencies

Key libraries: PyTorch, Transformers, diffusers, pytorch-lightning, accelerate, deepspeed, omegaconf, einops, liger-kernel (optional)