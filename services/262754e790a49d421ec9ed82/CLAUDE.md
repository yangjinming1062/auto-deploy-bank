# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Multi-project research repository from Alibaba Research/DAMO-ConvAI containing ~30+ independent NLP/ML research projects focused on LLMs and conversational agents. Most projects are self-contained with independent dependencies.

**Primary research areas:**
- Strategic reasoning and RL for LLMs (EPO)
- Tool-augmented LLMs (API-Bank)
- Workflow-guided planning (FlowBench)
- Multimodal LLMs and instruction tuning
- Dialogue systems and conversation agents

## Main Project: EPO (Explicit Policy Optimization)

The `EPO/` directory is the primary integrated project for strategic reasoning in LLMs via reinforcement learning. It contains:

- **LLaMA-Factory/**: Training and fine-tuning framework (based on hiyouga/LLaMA-Factory)
- **Sotopia/**: Social intelligence simulation environment
- **Alfshop/**: Combined environment for WebShop and ALFWorld tasks

### EPO Setup
```bash
conda create -n epo python=3.10
conda activate epo
cd EPO
# Install LLaMA-Factory
cd LLaMA-Factory && pip install -e .
# Install Sotopia dependencies
cd ../Sotopia && pip install -r requirements.txt && cd sotopia && pip install -e .
```

### EPO Training
```bash
cd EPO/LLaMA-Factory

# Train on SOTOPIA-PI
llamafactory-cli train examples/train_epo/llama3_sotopia_pi_rl.yaml

# Train on WebShop and ALFWorld
llamafactory-cli train examples/train_epo/llama3_alfshop_rl.yaml
```

### EPO Evaluation
```bash
# SOTOPIA benchmark
cd EPO/Sotopia
sotopia benchmark --models <TEST_MODEL_NAME> --partner-model <PARTNER_MODEL> \
  --evaluator-model gpt-4o --strategy-model <REASON_MODEL> \
  --strategy-model-partner <REASON_MODEL> --batch-size <BATCH_SIZE> --task all

# WebShop/ALFWorld evaluation
cd EPO/Alfshop
python -m fastchat.serve.controller
python -m fastchat.serve.model_worker --model-path <YOUR_MODEL_PATH> --port 21002
python -m eval_agent.main --thought_agent_config fastchat \
  --thought_model_name <REASON_MODEL> --action_agent_config openai \
  --action_model_name <ACTION_MODEL> --exp_config <TASK_NAME> --split test
```

### EPO Data
Download RL training data from HuggingFace: `Tongyi-ConvAI/EPO-RL-data`

## LLaMA-Factory Commands (used by EPO, SDPO)

Located in `EPO/LLaMA-Factory/` and `SDPO/LLaMA-Factory/`

```bash
cd EPO/LLaMA-Factory

# Linting and formatting (ruff)
make quality          # Check code quality
make style            # Auto-fix issues

# Run tests
pytest tests/

# Model inference via API
API_PORT=8000 llamafactory-cli api examples/inference/llama3_vllm.yaml
```

**Code style**: 119 line length, 4-space indent, Ruff linter configured in `pyproject.toml`

## Project Structure Pattern

Most projects follow this structure:
```
<project_name>/
├── README.md              # Setup and usage instructions
├── requirements.txt       # Dependencies
├── scripts/ or *.sh       # Training/evaluation scripts
├── data/                  # (not included - download separately)
└── pyproject.toml         # (some projects)
```

## Common Dependencies

- `torch`, `transformers`, `tokenizers`, `sentencepiece`
- `accelerate`, `peft`, `bitsandbytes` (efficient training)
- `deepspeed` (distributed training)
- `wandb` (logging)
- `gradio` (demo interfaces)

## Key Individual Projects

- **API-Bank** (`api-bank/`): Benchmark for tool-augmented LLMs with 73 APIs, 314 dialogues
- **FlowBench** (`FlowBench/`): Workflow-guided planning benchmark (6 domains, 22 roles, 51 scenarios)
- **MMLatentAction**: Multimodal conversational agents with latent action learning
- **OmniCharacter**: Speech-language personality interaction for role-playing
- **MMEvol**: Multimodal LLM evolution with Evol-Instruct

## Important Notes

1. **Models and datasets not included**: Download from HuggingFace or links in project READMEs
2. **GPU required**: Deep learning projects requiring CUDA/GPU access
3. **Python 3.10**: Recommended version for most projects
4. **Redis required**: For Sotopia environment (used in EPO)