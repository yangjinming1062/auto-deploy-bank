# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MetaMath is a mathematical reasoning project that bootstraps LLM capabilities through data augmentation. It includes:
- **MetaMathQA**: A 395K math reasoning dataset generated via multiple augmentation techniques
- **MetaMath models**: Fine-tuned LLaMA-2, Mistral, and Llemma models for math reasoning

## Setup

```bash
pip install -r requirements.txt
# If Ray installation fails:
pip install --upgrade ray pyarrow pandas
export APIKEY="your-openai-api-key"  # Required for data generation
```

## Training

MetaMath uses HuggingFace Transformers Trainer with FSDP for distributed training:

```bash
# LLaMA-2 training (8 GPUs)
bash run.sh

# Mistral training
bash run_mistral.sh

# Direct command example:
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python3 -m torch.distributed.launch \
    --nproc_per_node=8 --use_env train_math.py \
    --model_name_or_path "meta-llama/Llama-2-7b-hf" \
    --data_path "meta-math/MetaMathQA" \
    --bf16 True \
    --output_dir "./save" \
    --num_train_epochs 3 \
    --per_device_train_batch_size 4 \
    --learning_rate 2e-5 \
    --fsdp "full_shard auto_wrap" \
    --fsdp_transformer_layer_cls_to_wrap 'LlamaDecoderLayer'
```

Key hyperparameters:
- Max length: 512 tokens
- LR scheduler: cosine
- Warmup ratio: 0.03
- FSDP wraps decoder layer classes (LlamaDecoderLayer for LLaMA, MistralDecoderLayer for Mistral)

## Evaluation

Uses vLLM for fast batch inference:

```bash
# GSM8K benchmark
python eval_gsm8k.py --model "./save" --data_file ./data/test/GSM8K_test.jsonl

# MATH benchmark
python eval_math.py --model "./save" --data_file ./data/test/MATH_test.jsonl

# With custom batch size and tensor parallelism
python eval_gsm8k.py --model "./save" --data_file ./data/test/GSM8K_test.jsonl \
    --batch_size 400 --tensor_parallel_size 8
```

Inference prompt format:
```
"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{instruction}\n\n### Response: Let's think step by step."
```

## Data Generation Pipeline

The `code_for_generating_data/code/` directory contains scripts for generating MetaMathQA using OpenAI API:

| Technique | Command | Purpose |
|-----------|---------|---------|
| Create backward questions | `bash run_create_backward_questions.sh` | Reverses question-answer pairs |
| AnsAug (forward) | `bash run_forward.sh` | Answer augmentation |
| Rephrasing | `bash run_rephrase.sh` | Question rephrasing |
| Self-Verification | `bash run_sv.sh` | Self-check rewriting |
| FOBAR | `bash run_backward.sh` | Forward-backward reasoning |

Arguments for data generation:
- `--num_repeat`: Number of ChatGPT outputs per input (temperature sampling)
- `--part`: Partition index to avoid overwriting
- `--cont`: Continue from previous generation

## Data Format

Training data expects `query` (instruction+input) and `response` fields, or `instruction`, `input`, and `output` fields. Evaluation files are JSONL format with:
- GSM8K: `query`, `response` (answer after `####`)
- MATH: `instruction`, `output` (answer in `\boxed{}`)

## Architecture Notes

- **train_math.py**: SFT trainer using causal LM; handles tokenization with padding, ignores loss on prompt tokens via IGNORE_INDEX (-100)
- **eval_gsm8k.py**: Extracts answers from `The answer is: X` pattern
- **eval_math.py**: Uses `util.py` string normalization (`strip_string`, `is_equiv`) for comparing LaTeX answers
- **util.py**: Contains math-specific string normalization for fraction/sqrt/unit handling