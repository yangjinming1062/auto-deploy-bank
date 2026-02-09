# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an LLM fine-tuning repository containing scripts to fine-tune Qwen2, GLM4, and Qwen2-VL models using LoRA (Low-Rank Adaptation). The project supports text classification, named entity recognition (NER), and multimodal tasks.

## Common Commands

**Install dependencies:**
```bash
pip install -r requirements.txt
# For Qwen2-VL, also install:
cd qwen2_vl && pip install -r requirements.txt
```

**Dataset preparation:**
- Text classification: Download from [huangjintao/zh_cls_fudan-news](https://modelscope.cn/datasets/swift/zh_cls_fudan-news/files) → save as `train.jsonl` and `test.jsonl` in root
- NER: Download from [qgyd2021/chinese_ner_sft](https://huggingface.co/datasets/qgyd2021/chinese_ner_sft/tree/main/data) → save as `ccfbdci.jsonl` in root
- Qwen2-VL: Run `python data2csv.py` then `python csv2json.py` in `qwen2_vl/` directory

**Training (from root directory):**
| Model | Task | Command |
|-------|------|---------|
| Qwen2-1.5B | Text Classification | `python train_qwen2.py` |
| Qwen2-1.5B | NER | `python train_qwen2_ner.py` |
| Qwen2-VL-2B | Multimodal | `cd qwen2_vl && python train_qwen2_vl.py` |
| GLM4-9B | Text Classification | `python train_glm4.py` |
| GLM4-9B | NER | `python train_glm4_ner.py` |

**Inference:**
```bash
python predict_qwen2.py        # Qwen2 series
python predict_glm4.py         # GLM4 series
cd qwen2_vl && python predict_qwen2_vl.py  # Qwen2-VL series
```

## Architecture & Patterns

All training scripts follow a consistent structure:
1. Download base model via `modelscope.snapshot_download()`
2. Load tokenizer and model using `transformers` (AutoTokenizer, AutoModelForCausalLM)
3. Transform dataset with `dataset_jsonl_transfer()` function (converts raw data to chat format)
4. Tokenize with `process_func()` - applies chat template, creates input_ids/attention_mask/labels
5. Configure LoRA with `peft.LoraConfig` (different target_modules per model)
6. Train with `Trainer` using `SwanLabCallback` for experiment tracking
7. Run inference on test set and log results with `swanlab.log()`

**Model-specific LoRA target modules:**
- Qwen2: `["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]`
- GLM4: `["query_key_value", "dense", "dense_h_to_4h", "activation_func", "dense_4h_to_h"]`

**Chat templates:**
- Qwen2 uses `<|im_start|>/<|im_end|>` format
- GLM4 uses `<|system|>/<|endoftext|>/<|user|>/<|assistant|>` format

**Output directories:**
- Trained models saved to `./output/{model-name}/` with checkpoint folders

## Key Dependencies

Core: `torch`, `transformers`, `datasets`, `peft`, `accelerate`, `modelscope`
Tracking: `swanlab`
Utilities: `pandas`, `tiktoken`
Multimodal (qwen2_vl): `torchvision`, `qwen-vl-utils`

## Development Notes

- Models are downloaded from ModelScope/HuggingFace to `./` cache directory on first run
- Training uses bfloat16 precision with `device_map="auto"`
- MAX_LENGTH is 384 for text models, 8192 for multimodal
- Gradient checkpointing is enabled for memory efficiency
- Always call `swanlab.finish()` after training/inference in Jupyter contexts