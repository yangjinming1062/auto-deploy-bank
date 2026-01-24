# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **ChatGLM-6B** large language model fine-tuning project with multi-GPU support. It uses **LoRA (Low-Rank Adaptation)** for parameter-efficient fine-tuning and supports multiple training/inference strategies via DeepSpeed and Accelerate.

## Commands

### Installation
```bash
pip install -r requirements.txt
```

### Fine-tuning

**Simple single-node multi-GPU (torchrun + DeepSpeed):**
```bash
torchrun --nproc_per_node=2 multi_gpu_fintune_belle.py \
    --dataset_path data/alpaca \
    --lora_rank 8 \
    --per_device_train_batch_size 1 \
    --learning_rate 2e-5 \
    --fp16 \
    --num_train_epochs 2 \
    --output_dir output \
    --deepspeed ds_config_zero3.json
```

**With Accelerate + DeepSpeed ZeRO-3:**
```bash
accelerate launch --config_file accelerate_ds_zero3_cpu_offload_config.yaml \
    multi_gpu_fintune_belle.py \
    --dataset_path data/alpaca \
    --lora_rank 8 \
    --per_device_train_batch_size 2 \
    --max_steps 10000 \
    --learning_rate 2e-5 \
    --fp16 \
    --output_dir output
```

**Simple script (no DeepSpeed):**
```bash
python finetune.py \
    --dataset_path data/alpaca \
    --lora_rank 8 \
    --per_device_train_batch_size 2 \
    --max_steps 2000 \
    --save_steps 1000 \
    --learning_rate 2e-5 \
    --fp16 \
    --output_dir output \
    --report_to wandb
```

### Inference

**Batch inference with DeepSpeed:**
```bash
deepspeed --num_gpus 2 chatglm_deepspeed_inference.py
```

**With CPU offload (for low VRAM):**
```bash
python chatglm_multi_gpu_inference.py
```

### Web UI
```bash
streamlit run webui/web_feadback.py --server.port 6006
```

## Architecture

### Core Model Files
- **modeling_chatglm.py** - Custom ChatGLMForConditionalGeneration model implementation (51KB)
- **configuration_chatglm.py** - ChatGLMConfig with 28 layers, 4096 hidden size, 32 attention heads
- **tokenization_chatglm.py** - Custom SPTokenizer using icetk.TextTokenizer

### Training Scripts
- **finetune.py** - Simple fine-tuning using HuggingFace Trainer with custom data_collator and ClearCacheCallback
- **multi_gpu_fintune_belle.py** - Multi-GPU training with manual optimizer/scheduler management, memory tracking via TorchTracemalloc
- **finetune.py** uses `ModifiedTrainer` extending HuggingFace Trainer
- **multi_gpu_fintune_belle.py** uses raw Accelerate + manual training loop

### LoRA Configuration
Uses PEFT library with:
- `task_type=TaskType.CAUSAL_LM`
- `r=8` (rank), `lora_alpha=32`, `lora_dropout=0.1`
- Only LoRA parameters saved to `chatglm-lora.pt`

### Data Processing
- **tokenize_dataset_rows_belle.py** - Tokenizes JSONL datasets with `max_seq_length` truncation
- Data format: HuggingFace `datasets.load_from_disk()` format (finetune.py) or custom AlpacaDataset (multi_gpu_fintune_belle.py)

### DeepSpeed Configs
- **ds_config_zero3.json** - ZeRO Stage 2 with CPU optimizer offload
- **accelerate_ds_zero3_cpu_offload_config.yaml** - ZeRO Stage 3 with bf16 mixed precision

### Position Encoding
ChatGLM uses 2D position encoding with `position_encoding_2d=True`. The model has special tokens:
- `[gMASK]` = 150001
- `[sMASK]` = 150002
- BOS = 150004
- EOS = 150005

### Key Implementation Details
1. Custom `data_collator` handles attention_mask and 2D position_ids generation
2. `CastOutputToFloat` wrapper converts LM head output to float32 for training stability
3. `ClearCacheCallback` clears GPU cache every 1000 steps to prevent OOM
4. Uses `gradient_checkpointing_enable()` for memory-efficient training

## Application Examples (APP_example/)
- **chat_langchain/** - RAG-based chat with knowledge base
- **chatglm_agent/** - Agent capabilities with tools
- **clip_retrieval/** - Image retrieval with CLIP embeddings
- **lora_sd/** - Stable Diffusion LoRA training
- **real_time_draw/** - Real-time drawing generation
- **retrieval_image_gen/** - Retrieval-augmented image generation
- **auto_poster/** - Intelligent poster generation with text/layout/image
- **digital_human/** - AI digital human (image gen, voice clone, motion, lip-sync)