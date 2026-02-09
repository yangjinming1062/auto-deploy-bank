# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DISC-MedLLM is a medical domain large language model designed for healthcare conversational scenarios, built on [Baichuan-13B-Base](https://github.com/baichuan-inc/Baichuan-13B). It provides medical consultation and treatment advice through high-quality health support services.

## Commands

### Installation
```bash
pip install -r requirements.txt
```

### Running Demos
```bash
# Command-line demo
python cli_demo.py

# Web-based demo
streamlit run web_demo.py --server.port 8888
```

### Model Fine-tuning
Training uses DeepSpeed for distributed training:
```bash
deepspeed --num_gpus={num_gpus} ./train/train.py --train_args_file ./train/train_args/sft.json
```

Before training, configure `train/train_args/sft.json` with appropriate settings (output_dir, model_name_or_path, train_file, etc.).

## Architecture

### Training Pipeline (`train/`)
Built on [Firefly](https://github.com/yangjianxin1/Firefly) with modifications for medical conversation fine-tuning:

- **`train.py`**: Entry point for training; initializes model, tokenizer, dataset, and custom trainer
- **`train/component/`**: Modular training components:
  - **`dataset.py`**: `SFTDataset` class for loading conversation data
  - **`collator.py`**: Data collation for batch processing
  - **`trainer.py`**: Custom `Trainer` class extending transformers.Trainer with `TargetLMLoss`
  - **`loss.py`**: `TargetLMLoss` computes cross-entropy loss only on assistant response tokens
  - **`argument.py`**: Custom argument definitions

### Conversation Data Format
Training data uses JSONL format where each line contains:
```json
{"conversation": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

Multi-turn conversations are formatted with special tokens:
- `<b><$user_token>`: User utterance marker (token ID: 195)
- `<$assistant_token>`: Assistant utterance marker (token ID: 196)
- Format: `<s><$user_token>content<$assistant_token>response<eos_token>...`

### Inference (`cli_demo.py`, `web_demo.py`)
Both demos load the model from Hugging Face (`Flmc/DISC-MedLLM`) using:
- `AutoModelForCausalLM` with `torch.float16` and `device_map="auto"`
- `AutoTokenizer` with `use_fast=False` and `trust_remote_code=True`
- `GenerationConfig` loaded from pretrained model

### Evaluation (`eval/`)
Contains evaluation datasets and results:
- `dialogues/`: Multi-turn dialogue samples
- `samples/`: Model-generated responses
- `gpt4_scores/`: GPT-4 evaluation scores

## Key Implementation Details

- Uses DeepSpeed ZeRO-3 optimization (config: `train/train_args/ds_z3_config.json`)
- Supports BF16 training (`bf16: true` in config)
- Custom loss masking: only assistant tokens contribute to loss calculation via `target_mask`
- Multi-turn conversation handling with sequence length truncation (`max_seq_length: 1200`)