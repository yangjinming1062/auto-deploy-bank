# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LLM Finetune is a Chinese-language large language model fine-tuning project supporting multiple models (GLM4-9B, Qwen2-1.5B, Qwen2-VL-2B) for instruction tuning and specialized tasks.

## Commands

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Text classification training:**
```bash
python train_qwen2.py       # Qwen2-1.5B model
python train_glm4.py        # GLM4-9B model
```

**Named entity recognition (NER) training:**
```bash
python train_qwen2_ner.py   # Qwen2-1.5B NER
python train_glm4_ner.py    # GLM4-9B NER
```

**Multimodal (Qwen2-VL) training:**
```bash
cd qwen2_vl
python train_qwen2_vl.py
```

**Inference:**
```bash
python predict_qwen2.py     # Qwen2 series
python predict_glm4.py      # GLM4 series
cd qwen2_vl && python predict_qwen2_vl.py  # Qwen2-VL series
```

## Architecture

**Three model families with consistent training patterns:**

1. **GLM4 (ZhipuAI)**: Uses `<|system|>`, `<|user|>`, `<|assistant|>` chat template. LoRA target modules: `["query_key_value", "dense", "dense_h_to_4h", "activation_func", "dense_4h_to_h"]`

2. **Qwen2 (Alibaba)**: Uses `<|im_start|>system`, `<|im_start|>user`, `<|im_start|>assistant` chat template. LoRA target modules: `["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]`

3. **Qwen2-VL (Alibaba)**: Multimodal variant with vision capabilities in `qwen2_vl/` subdirectory

**Training pipeline pattern (all scripts follow this):**
1. Download model via `modelscope.snapshot_download()`
2. Load tokenizer and model with `AutoTokenizer`/`AutoModelForCausalLM`
3. Transform dataset format with `dataset_jsonl_transfer()`
4. Tokenize with model-specific `process_func()`
5. Configure LoRA with `peft.LoraConfig`
6. Train with `transformers.Trainer` and `SwanLabCallback`
7. Run inference on test set and log to SwanLab

**Key components:**
- `dataset_jsonl_transfer()`: Converts raw datasets to model-specific message format
- `process_func()`: Tokenizes with chat templates and handles truncation (MAX_LENGTH=384)
- `predict()`: Generates responses using `tokenizer.apply_chat_template()`
- LoRA configuration: `r=8`, `lora_alpha=32`, `lora_dropout=0.1`

## Datasets Required

**Text classification:**
- Download `train.jsonl` and `test.jsonl` from `huangjintao/zh_cls_fudan-news` to root directory

**NER:**
- Download `ccfbdci.jsonl` from `qgyd2021/chinese_ner_sft` to root directory

**Qwen2-VL:**
- Run `python data2csv.py && python csv2json.py` in `qwen2_vl/` directory

## Tech Stack

- **Framework**: Hugging Face Transformers + PEFT (LoRA)
- **Experiment tracking**: SwanLab
- **Model hub**: ModelScope
- **Compute**: CUDA with bfloat16 precision

## Output Locations

- Trained checkpoints: `./output/{MODEL_NAME}/checkpoint-*`
- Downloaded models: `./ZhipuAI/glm-4-9b-chat/` or `./qwen/`