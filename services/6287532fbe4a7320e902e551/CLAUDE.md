# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DISC-MedLLM is a medical domain-specific large language model designed for conversational healthcare scenarios. It is fine-tuned from [Baichuan-13B-Base](https://github.com/baichuan-inc/Baichuan-13B) by Fudan-DISC lab to bridge general LLMs and real-world medical consultations.

## Commands

### Installation
```shell
pip install -r requirements.txt
```

### Running Demos
```shell
# Command-line demo
python cli_demo.py

# Web demo (Streamlit)
streamlit run web_demo.py --server.port 8888
```

### Training
Full-parameter fine-tuning using DeepSpeed ZeRO:
```shell
deepspeed --num_gpus={num_gpus} ./train/train.py --train_args_file ./train/train_args/sft.json
```

**Note:** Update `sft.json` configuration before training, particularly:
- `output_dir` - Where checkpoints will be saved
- `model_name_or_path` - Base model path (default: Flmc/DISC-MedLLM)
- `train_file` - Path to training data JSONL file

## Architecture

### Training Pipeline
The training system is built on HuggingFace Transformers with custom components:

- **Main entry point**: `train/train.py` - Initializes model, tokenizer, datasets, and custom Trainer
- **Data format**: JSONL files with `{"_id": "...", "source": "...", "conversation": [{"role": "user"|"assistant", "content": "..."}]}` structure
- **Custom tokens**: `user_token_id=195`, `assistant_token_id=196` (same as Baichuan-13B-Chat)
- **Loss computation**: Only assistant response tokens contribute to loss via `TargetLMLoss` (see `train/component/loss.py`)
- **Trainer**: Custom `Trainer` class in `train/component/trainer.py` that extends HuggingFace Trainer with custom loss handling

### Key Training Components (`train/component/`)
| File | Purpose |
|------|---------|
| `dataset.py` | `SFTDataset` - Loads multi-turn conversations, tokenizes with special tokens |
| `collator.py` | `SFTDataCollator` - Pads batches dynamically, maintains `target_mask` |
| `trainer.py` | Custom Trainer with `compute_loss` override for target-only loss |
| `loss.py` | `TargetLMLoss` - CrossEntropyLoss ignoring non-target tokens |
| `argument.py` | `CustomizedArguments` dataclass for training config |

### DeepSpeed Configuration
Uses ZeRO stage 3 for distributed training (see `train/train_args/ds_z3_config.json`):
- Optimizer: Adam with auto-tuned parameters
- Mixed precision: BF16 enabled (auto-configured)
- Gradient checkpointing: Controlled via `sft.json`

### Dialogue Format for Custom Training
If using external training code, format multi-turn conversations as:
```
<|195|>user_content<|196|>assistant_content<|195|>...
```

## Model Usage

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Flmc/DISC-MedLLM", use_fast=False, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("Flmc/DISC-MedLLM", device_map="auto", torch_dtype=torch.float16, trust_remote_code=True)

messages = [{"role": "user", "content": "我感觉自己颈椎非常不舒服"}]
response = model.chat(tokenizer, messages)
```

## Evaluation (`eval/`)

| Directory | Contents |
|-----------|----------|
| `dialogues/` | Multi-turn conversation samples from various models (DISC-MedLLM, Baichuan-Chat, GPT-3.5/4, etc.) |
| `samples/` | Test case specifications (CMB-cases.json, cmd_samples.json, cmid_samples.json) |
| `gpt4_scores/` | GPT-4 evaluation scores by criterion (proactivity, accuracy, helpfulness, linguistic quality) |

### Evaluation Datasets
- **Single-turn**: MLEC-QA (NMLEC exam categories), NEEP 306 (medical board questions)
- **Multi-turn**: CMB-Clin (consultation simulation), CMD (department-specialized), CMID (intent-focused)

## Important Implementation Details

1. **Padding**: Uses tokenizer's `pad_token_id` (set to `unk_token_id` if None)
2. **Sequence truncation**: Conversations truncated at `max_seq_length` to fit context window
3. **Target masking**: Only assistant tokens (between `assistant_token_id` and `eos_token_id`) are optimized
4. **Device mapping**: Supports auto device placement (`device_map="auto"`)
5. **Quantization**: Supports int8/int4 inference (see Baichuan-13B repo) but with potential performance degradation