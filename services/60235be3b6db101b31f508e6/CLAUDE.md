# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Agent0 is a self-evolving agent framework that eliminates dependency on external data or human annotations. The codebase contains two main components:

- **Agent0** (`/Agent0`): Self-evolving language agents with tool-integrated reasoning
- **Agent0-VL** (`/Agent0-VL`): Self-evolving vision-language agents (code release pending)

The framework uses a symbiotic competition between:
- **Curriculum Agent**: Proposes increasingly challenging frontier tasks
- **Executor Agent**: Learns to solve tasks using external tools (code interpreter)

## Environment Setup

```bash
# Install dependencies
cd Agent0/Agent0
pip install -r requirements.txt

# Install Verl in development mode for both training modules
cd curriculum_train && pip install -e verl
cd ../executor_train && pip install -e verl

# Install flash-attention separately (requires build isolation)
pip install "flash-attn==2.8.3" --no-build-isolation
```

## Required Environment Variables

```bash
export STORAGE_PATH=""      # Storage path for models, generated questions, and results
export HUGGINGFACENAME=""   # HuggingFace model name/path
export WANDB_API_KEY=""     # Weights & Biases API key for logging
export VLLM_DISABLE_COMPILE_CACHE=1  # Recommended for training
```

## Sandbox Service Setup

The code execution sandbox (SandboxFusion) is required for tool-integrated reasoning. See [SandboxFusion](https://github.com/bytedance/SandboxFusion) for deployment:

```bash
git clone https://github.com/bytedance/SandboxFusion.git
cd SandboxFusion
poetry install
make run-online
```

Configure sandbox URLs in `curriculum_train/vllm_service_init/start_vllm_server_tool.py` (lines 36-41).

## Training Workflow

### 1. Train Curriculum Agent

```bash
cd curriculum_train/
mkdir -p "$STORAGE_PATH/evaluation" "$STORAGE_PATH/models" "$STORAGE_PATH/generated_question" "$STORAGE_PATH/temp_results"

bash scripts/curriculum_train.sh Qwen/Qwen3-4B-Base Qwen/Qwen3-4B-Base qwen3_4b_curriculum_v1
```

The curriculum agent generates increasingly challenging tasks for the executor agent.

### 2. Data Curation

Generate and evaluate training questions using the trained curriculum agent:

```bash
executor_agent_path=Qwen/Qwen3-4B-Base
curriculum_agent_path=${STORAGE_PATH}/models/qwen3_4b_curriculum_v1/global_step_5/actor/huggingface
experiment_name=qwen3_4b_executor_v1

# Generate questions (parallelized across 8 GPUs)
bash question_generate/question_generate.bash $curriculum_agent_path 1000 $experiment_name

# Evaluate generated questions
bash question_evaluate/evaluate.sh $executor_agent_path $experiment_name

# Filter and prepare training data (self-consistency score 0.3-0.8)
LOCAL_DATA_PATH=$(python question_evaluate/upload.py --max_score 0.8 --min_score 0.3 --experiment_name ${experiment_name})
```

### 3. Train Executor Agent

```bash
cd ../executor_train/
bash examples/train/math_tir/train_qwen3_4b_adpo.sh
```

Uses ADPO algorithm with multi-turn RL. Checkpoints saved to `checkpoints/torl/`.

## Key Directories

- `curriculum_train/`: Curriculum agent training (VeRL-based, uses Ray)
- `executor_train/`: Executor agent training (ADPO via verl-tool)
- `curriculum_train/verl/`: VeRL reinforcement learning framework
- `executor_train/verl_tool/`: Tool-integrated RL training
- `curriculum_train/vllm_service_init/`: vLLM server initialization for tool use

## Key Frameworks

- **VeRL**: Reinforcement learning trainer (curriculum training)
- **VeRL-Tool**: Tool-integrated RL training (executor training)
- **vLLM**: Inference server for both agents
- **Ray**: Distributed training orchestration
- **W&B**: Experiment logging

## Code Architecture

### Curriculum Training (VeRL-based)
- `verl/trainer/main.py`: Main entry point
- `verl/workers/`: Actor, critic, rollout workers
- `examples/reward_function/curriculum_reward.py`: Reward computation
- `question_generate/question_generate.py`: Question generation with tool use
- `question_evaluate/evaluate.py`: Question evaluation

### Executor Training (ADPO)
- `verl_tool/trainer/main_ppo.py`: PPO training entry point
- `verl_tool/servers/serve.py`: Tool server for code execution
- Configuration via command-line arguments (Hydra-style)

## Model Checkpoints

- Curriculum checkpoints: `${STORAGE_PATH}/models/{experiment_name}/global_step_5/actor/huggingface`
- Executor checkpoints: `checkpoints/torl/`
- Merged models: Use `scripts/model_merger.py` to merge LoRA adapters