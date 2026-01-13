# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is **zero-to-nlp**, a comprehensive Chinese NLP training framework built on PyTorch and Transformers. It provides out-of-the-box training solutions for Chinese-language models including text classification, text generation, multimodal models (CLIP, LLaVA), and support for major LLMs (ChatGLM, LLaMA, Qwen, Baichuan, Bloom, InternLM, etc.).

The repository contains **30+ model implementations**, each in its own self-contained directory with training scripts, data processing notebooks, inference demos, and documentation.

## Core Dependencies

```
pandas
numpy
datasets
transformers
evaluate
sentencepiece
gradio
```

Additional requirements (commonly used):
- `deepspeed` - for distributed training
- `torch` - with CUDA support for GPU training
- `accelerate` - for multi-GPU training
- `peft` - for LoRA fine-tuning

## Repository Structure

### Model Implementations

Each model directory follows a consistent structure:

- **`readme.md`** - Model-specific documentation and usage instructions
- **`train.py`** - Main training script
- **`.sh` files** - Shell scripts for running training with specific configurations
- **`.ipynb` files** - Jupyter notebooks for data processing, training, and inference
- **`infer.ipynb`** - Inference/demo notebook (often with Gradio)
- **`ds_*.json`** - DeepSpeed configuration files (ZeRO-2/ZeRO-3)
- **`configs/`** - Additional configuration files

### Key Model Directories

| Directory | Purpose | Notes |
|-----------|---------|-------|
| `chinese_classifier` | Text classification | Uses transformers pipeline |
| `chinese_bloom` | Bloom model SFT | Supports ZeRO-2/3, multiple sizes (560M-13B) |
| `train_qwen` | Qwen2 SFT training | Includes fix for JSON serialization issue |
| `internlm-sft` | InternLM SFT with LoRA | Self-identity & refusal training |
| `train_llava` | LLaVA multimodal training | Vision + language understanding |
| `chinese_clip_ddp` | CLIP text-image embedding | Distributed training support |
| `baichuan2_dpo` | Baichuan2 DPO training | Direct preference optimization |
| `model_clm` | Causal language modeling | Pre-training infrastructure |
| `verl_base` | VERL reinforcement learning | Ray + FSDP for RLHF |

## Common Development Tasks

### Running Training

Each model uses shell scripts for training. The general pattern is:

```bash
# Single GPU or simple multi-GPU
bash train.sh

# DeepSpeed distributed training
deepspeed --include localhost:0,1,2,3 train.py \
    --deepspeed ds_zero2_no_offload.json \
    --model_name_or_path model/path \
    --use_lora true \
    --data_path data/custom_data \
    --output_dir output_dir \
    --num_train_epochs 3 \
    --per_device_train_batch_size 4 \
    --learning_rate 4e-4 \
    --model_max_length 2048

# Multi-node with torchrun
torchrun --nproc_per_node=4 --nnodes=1 \
    --master_addr="127.0.0.1" --master_port=1234 \
    train.py [arguments]
```

**Example locations:**
- `train_qwen/train_zero2.sh` - Qwen2 training
- `chinese_bloom/ds_all.sh` - Bloom model with DeepSpeed
- `internlm-sft/train_zero2.sh` - InternLM with LoRA
- `pytorch_base/multi_process/run_code05.sh` - Basic multi-GPU example

### Data Processing

Most models use Jupyter notebooks for data processing:

```bash
# Typical workflow
jupyter notebook code01_processdata.ipynb  # Data preprocessing
jupyter notebook code02_trainmodel.ipynb   # Training
jupyter notebook code03_predict.ipynb      # Inference
```

**Data format (SFT style):**
```json
{"instruction": "...", "input": "...", "output": "..."}
{"instruction": "What is X?", "input": "", "output": "X is..."}
```

**Classification data format:**
```csv
text,label
"example text",0
"example text",1
```

### Running Inference

Most models include Gradio-based inference demos:

```bash
jupyter notebook infer.ipynb
# or
python app.py  # if present
```

**Example:** `chinese_bloom/code05_infer.ipynb` provides a full Gradio interface

### Multi-GPU Training

The framework uses two approaches:

1. **DeepSpeed ZeRO** (most common):
   - `ds_zero2_no_offload.json` - ZeRO-2 without CPU offloading
   - `ds_zero3_no_offload.json` - ZeRO-3 for larger models
   - Use `--include localhost:0,1,2,3` to specify GPUs

2. **torchrun** (simpler cases):
   ```bash
   torchrun --nproc_per_node=N train.py
   ```

### Testing Individual Components

Check `pytorch_base/` for isolated examples:
- `multi_process/` - Multi-GPU training fundamentals
- `simple_thu_chatglm6b/` - Basic ChatGLM training
- `transformers_flow/` - Transformer internals

## Architecture Patterns

### Training Script Structure

Most training scripts follow this pattern:

```python
# 1. Parse arguments (dataclasses)
@dataclass
class ModelArguments:
    model_name_or_path: str
    use_lora: bool = False

# 2. Load dataset
raw_datasets = load_dataset_from_path(data_path)

# 3. Tokenize function
def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=model_max_length
    )

# 4. Setup Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=DataCollatorForSeq2Seq()
)

# 5. Train
trainer.train()
```

### LoRA Fine-tuning

To add LoRA to any model:

```bash
--use_lora true \
--lora_r 8 \
--lora_alpha 16 \
--lora_dropout 0.1 \
--target_modules ["query", "value"]  # Model-specific
```

### Gradient Checkpointing

For large models to save memory:

```bash
--gradient_checkpointing true
```

### Mixed Precision Training

```bash
# bf16 (recommended for A100)
--bf16 true --fp16 false

# fp16 (for older GPUs)
--bf16 false --fp16 true
```

## Model-Specific Notes

### Qwen2 (`train_qwen/`)
- **Issue:** Custom fix for JSON serialization error in transformers Trainer (line 258-263)
- **Solution:** Wraps tensor values with `.item()` before logging
- **Command:** See `train_zero2.sh` for LoRA + DeepSpeed setup

### InternLM (`internlm-sft/`)
- **Specialty:** Self-identity training and refusal capability
- **Data:** Uses `yuanzhoulvpi/rename_robot` dataset
- **LoRA:** Enabled by default
- **Output:** Personality-based responses (e.g., "我是良睦路程序员训练的机器人小埋")

### Bloom (`chinese_bloom/`)
- **Multi-size:** Supports 560M, 3B, 7B, 13B models
- **Multi-lingual:** Chinese, English, code, French, Spanish
- **Deployment:** Gradio demo available
- **Command:** `sh ds_all.sh` for full training

### CLIP (`chinese_clip_ddp/`)
- **Purpose:** Text-image embedding
- **Training:** Distributed (DDP) by default
- **Scripts:** `train_ddp_text_image.sh`, `train_ddp_ti_all.sh`
- **Data:** Requires image-text pairs

### Baichuan2 DPO (`baichuan2_dpo/`)
- **Method:** Direct Preference Optimization (not SFT)
- **Command:** `bash train_ds.sh`
- **Use case:** Preference-based fine-tuning

## Key Configuration Files

- **`ds_zero2_no_offload.json`** - DeepSpeed ZeRO-2 config
- **`ds_zero3_no_offload.json`** - DeepSpeed ZeRO-3 config
- **`.gitignore`** - Excludes model outputs, cache_data, datasets

## Performance Optimization Tips

1. **Memory efficiency:**
   - Use gradient checkpointing: `--gradient_checkpointing true`
   - Enable ZeRO: `--deepspeed ds_zero2_no_offload.json`
   - Use LoRA: `--use_lora true`
   - Reduce batch size with gradient accumulation: `--gradient_accumulation_steps 8`

2. **Speed optimization:**
   - Use bf16: `--bf16 true` (A100)
   - Enable tf32: `--tf32 true` (A100)
   - Use data preloading and caching

3. **Multi-GPU scaling:**
   - Monitor GPU utilization: `nvidia-smi`
   - Use NCCL backend (default in DeepSpeed)
   - Check for data loading bottlenecks

## Common Data Issues

1. **Encoding:** Chinese data often uses GB18030 encoding
2. **Missing values:** Remove rows with null values before training
3. **Data leakage:** Ensure train/test/valid sets don't overlap
4. **Length limits:** Respect `model_max_length` to avoid OOM

## Model Deployment

Most models include:
- **Gradio demo:** `infer.ipynb` with `gradio.Interface`
- **FastAPI:** Some models include `app.py` for API deployment
- **HuggingFace Spaces:** Several models deployed at `yuanzhoulvpi/*`

## Troubleshooting

### CUDA OOM (Out of Memory)
```bash
# Reduce batch size
--per_device_train_batch_size 2

# Enable gradient checkpointing
--gradient_checkpointing true

# Use ZeRO-2/3
--deepspeed ds_zero2_no_offload.json

# Enable CPU offloading (slower but less memory)
# Modify ds config: "cpu_offload": true
```

### Multi-GPU Issues
```bash
# Check GPU visibility
nvidia-smi

# Verify DeepSpeed sees all GPUs
deepspeed --list_gpus

# Set CUDA devices
export CUDA_VISIBLE_DEVICES=0,1,2,3
```

### Data Loading Problems
- Check file paths in `--data_path`
- Verify JSON format (one JSON per line)
- Ensure sufficient disk space for cache (`cache_data/`)

## Development Notes

- Each model directory is self-contained and independently usable
- `.ipynb_checkpoints/` are git-ignored
- Output directories: `output_*/`, `model_result/`, `cache_data/` are git-ignored
- Model weights (`.bin`, `.safetensors`) should not be committed
- Large datasets should be downloaded separately (see READMEs)

## Additional Resources

- **Videos:** Author shares training videos on Bilibili (良睦路程序员)
- **HuggingFace:** Model downloads and deployments at https://huggingface.co/yuanzhoulvpi
- **Datasets:** Custom datasets at https://huggingface.co/datasets/yuanzhoulvpi