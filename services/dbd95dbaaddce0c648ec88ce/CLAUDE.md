# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Xwin-LM is a suite of Large Language Models (LLMs) focused on alignment technologies for coding and mathematical reasoning. Built on Llama 2 architecture, the project provides instruction-finetuned models and evaluation frameworks.

**Main Modules:**
- `Xwin-Coder/`: Coding capabilities evaluation (HumanEval, MBPP, APPS, DS1000, MT-Bench)
- `Xwin-Math/`: Mathematical reasoning evaluation (GSM8K, MATH)

## Commands

### Installation
```bash
# For Xwin-Coder
pip install -r Xwin-Coder/requirements.txt

# For Xwin-Math (note pinned versions)
pip install -r Xwin-Math/requirements.txt
```

**Recommended Docker Environment:**
```bash
sudo docker run -it -p 8022:22 -d --name=<docker name> --privileged --net=host --ipc=host --gpus=all -v /:/data superbench/dev:cuda11.8 bash
```

### Xwin-Coder Evaluation

```bash
# Interactive chat demo
python Xwin-Coder/online_chat.py --model <model_path>

# HumanEval evaluation
cd Xwin-Coder/HumanEval/ && bash eval_humaneval.sh

# MBPP evaluation (set model path in generate_MBPP.sh first)
cd Xwin-Coder/MBPP/ && bash generate_MBPP.sh

# APPS evaluation
cd Xwin-Coder/APPS/ && bash eval_apps.sh

# DS1000 evaluation
cd Xwin-Coder/DS1000/ && bash generate_ds1000.sh && bash eval_ds1000.sh

# MT-Bench evaluation
cd Xwin-Coder/MT_bench/ && bash eval.sh
```

### Xwin-Math Evaluation

```bash
# Generate responses on math dataset
cd Xwin-Math/eval/ && python generate.py --dataset_path dataset/gsm8k.json --model_path <model_path>

# Evaluate generated responses
cd Xwin-Math/eval/ && python eval.py <path_to_responses>
```

**Note:** For Xwin-Math, set `model` variable in `eval_humaneval.sh` and update `model_path` in generate/eval scripts.

## Architecture

### Xwin-Coder Structure
Each benchmark is a separate module with its own evaluation scripts:
- `humaneval_gen.py`: Generates model predictions on HumanEval
- `process_humaneval.py`: Processes predictions for evaluation
- `evaluate_functional_correctness`: Official HumanEval evaluator

Evaluations use vLLM for GPU-accelerated inference with parallel GPU processing (typically 4 GPUs).

### Xwin-Math Evaluation Pipeline
The evaluation uses a flexible multi-stage answer checking strategy:
1. **Literal check**: Character-by-character string matching
2. **Numerical check**: Convert and compare with tolerances
3. **Symbolic check**: Use SymPy for mathematical equivalence

The configuration in `eval_config.json` defines checking policies per problem type (MAWPS, etc.).

### Conversation Template
All models use Vicuna-style template for multi-turn conversations:
```
A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. USER: <prompt> ASSISTANT:
```

Math models require answers in format: `The answer is: <ANSWER>.`

## Key Dependencies

- **vLLM**: High-throughput inference (use vLLM=0.1.7 for H100 GPUs)
- **PyTorch 2.0+**: Deep learning framework
- **Transformers 4.31.0**: Model loading (Xwin-Math pinned to this version)
- **SymPy**: Symbolic mathematics for math answer verification
- **fire**: CLI argument parsing (Xwin-Math)
- **rich/tqdm/tabulate**: Progress display and formatting