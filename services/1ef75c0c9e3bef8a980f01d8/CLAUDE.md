# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Absolute Zero Reasoner (AZR)** - A reinforcement learning framework for training language models to generate and solve reasoning tasks through self-play, without using external training data. The approach uses a PROPOSE-SOLVE loop where models generate reasoning tasks (deduction, abduction, induction) and then solve them.

## Environment Setup

```bash
# Create conda environment
conda env create -f azr_env.yml
conda activate azr

# Install FlashAttention
pip install -r flashattn_requirements.txt

# Install dependencies
pip install -r requirements.txt

# Important: Remove Qwen3 think tokens (if using Qwen3 models)
python absolute_zero_reasoner/utils/remove_think_qwen3_tokenizer.py --model_name <Qwen3ModelName>
```

## Data Processing

```bash
# Process evaluation data for CruxEval/LiveCodeBench during training
python -m absolute_zero_reasoner.data_construction.process_code_reasoning_data
```

## Training Commands

### Seeding (Generate Initial Training Data)

Seeding generates initial datasets by prompting models to create reasoning problems. Scripts are located in `scripts/seeding/`:

```bash
# Set output paths
export OUTPUT_SEED_PATH=data/<new_ded_abd_seed_data_name>.jsonl
export OUTPUT_CODE_F_SEED_PATH=data/<new_ind_seed_data_name>.jsonl

# Generate seeds for different model sizes
bash scripts/seeding/7b.sh              # For 7B models
bash scripts/seeding/14b.sh             # For 14B models
bash scripts/seeding/coder3b.sh         # For 3B Coder models
bash scripts/seeding/coder7b.sh         # For 7B Coder models
bash scripts/seeding/coder14b.sh        # For 14B Coder models
bash scripts/seeding/llama.sh           # For Llama models
bash scripts/seeding/qwen3_4b.sh        # For Qwen3 4B models
```

**GPU Requirements:**
- 3B models: 2 × 80GB GPUs
- 7B/8B models: 4 × 80GB GPUs
- 14B models: 8 × 80GB GPUs

### Self-Play Training

Self-play is the core training loop where the model generates and solves problems iteratively. Scripts are in `scripts/selfplay/`:

```bash
# Basic self-play (uses default seed paths from environment or defaults to data/*.jsonl)
bash scripts/selfplay/7b.sh

# With custom seed datasets
export OUTPUT_SEED_PATH=data/<your_ded_abd_seed_data>.jsonl
export OUTPUT_CODE_F_SEED_PATH=data/<your_ind_seed_data>.jsonl
bash scripts/selfplay/7b.sh

# Resume training (add to any script)
trainer.wandb_run_id=<original_run_id> bash scripts/selfplay/7b.sh

# For Sandbox-Fusion executor (more secure, Docker-based)
# Add to config: azr.executor=sandboxfusion
bash scripts/selfplay/7b.sh azr.executor=sandboxfusion
```

### Checkpoint Conversion

```bash
# Convert veRL checkpoints to HuggingFace format
python -m absolute_zero_reasoner.utils.convert2hf \
  <veRL_ckpt_path>/actor \
  <veRL_ckpt_path>/actor/huggingface/ \
  <hf_ckpt_path>
```

## Evaluation

### LiveCodeBench (Code Generation)

```bash
# Download evaluation data first
git clone https://hf-mirror.com/datasets/livecodebench/code_generation_lite evaluation/code_eval/coding/LiveCodeBench/code_generation_lite

# Run evaluation
bash evaluation/code_eval/scripts/run_lcb_gen.sh --model <model_name>
# Example: --model andrewzh/Absolute_Zero_Reasoner-Coder-3b

# With custom parameters
bash evaluation/code_eval/scripts/run_lcb_gen.sh \
  --model <model> \
  --temperature 0.0 \
  --batch_size 128 \
  --n 1
```

### Evalplus (HumanEval/MBPP)

```bash
# Requires separate conda environment
conda create -n evalplus python=3.11
pip install --upgrade "evalplus[vllm] @ git+https://github.com/evalplus/evalplus@d362e933265c3e7e3df8101c930a89c3c470cd9f"
conda activate evalplus

# Run evaluation
bash evaluation/code_eval/scripts/run_evalplus.sh <dataset> <model> [greedy] [temperature] [top_p] [n_samples]
# Examples:
bash evaluation/code_eval/scripts/run_evalplus.sh humaneval andrewzh/Absolute_Zero_Reasoner-Coder-3b
bash evaluation/code_eval/scripts/run_evalplus.sh mbpp andrewzh/Absolute_Zero_Reasoner-Coder-7b 0 0.8 0.9 5
```

### Math Evaluation

See `evaluation/math_eval/README.md` for detailed math evaluation instructions.

## Code Architecture

### Core Components

**Training Infrastructure (`absolute_zero_reasoner/trainer/ppo/`)**
- `azr_ray_trainer.py` - Main PPO trainer implementing the PROPOSE-SOLVE loop with Ray for distributed training
- Handles self-play data generation, reward computation, and policy updates

**Reward System (`absolute_zero_reasoner/rewards/`)**
- `reward_managers.py` - Central reward manager (`CodeIORewardManager`) that:
  - Extracts code from model outputs
  - Executes code in sandbox (Python or Sandbox-Fusion)
  - Computes rewards for generation (diversity, complexity) and accuracy
- `code_reward.py` - Code-specific reward functions (AST checks, complexity metrics, edit distance)
- `math_utils.py` - Math problem evaluation utilities
- `custom_evaluate.py` - Reward extraction from model responses

**Self-Play Data Generation (`absolute_zero_reasoner/data_construction/`)**
- `constructor.py` - Generates training data through PROPOSE phase (task creation)
- `process_data.py` - Data preprocessing and formatting
- `process_code_reasoning_data.py` - Processes code reasoning datasets
- `prompts.py` - Prompt templates for different task types

**Execution Environment (`absolute_zero_reasoner/utils/code_utils/`)**
- `python_executor.py` - Raw Python execution sandbox (research use only, not secure)
- `sandboxfusion_executor.py` - Sandbox-Fusion executor (production-ready, Docker-based)
- `python_executor.py` - Validates and executes code with test cases
- `checks.py` - AST validation and code quality checks
- `parsers.py` - Parses code from model outputs

**Configuration (`absolute_zero_reasoner/configs/`)**
- `azr_ppo_trainer.yaml` - Main configuration with three key sections:
  - `actor_rollout_ref` - Actor model configuration (PPO policy)
  - `critic` - Critic model configuration (value function)
  - `azr` - AZR-specific settings (problem types, rewards, data selection)

### Problem Types

Three task types used in training:
1. **code_i** - Code completion (input → output)
2. **code_o** - Code generation (description → input/output)
3. **code_f** - Function generation (description → function)

### Configuration Key Points

**Reward Configuration (`azr.reward.generation_reward_config`)**
- `format_reward` - Reward for correct code format (default: true)
- `complexity_reward` - Encourages complex code (disabled by default)
- `mean_edit_distance_reward` - Encourages code diversity (disabled by default)
- `answer_diversity_reward` - Encourages diverse solutions (disabled by default)
- `intrinsic_combine_method` - How to combine intrinsic rewards (sum/multiply)

**Data Selection (`azr.data_selection_strategy`)**
- `valid_program_filter` - Filter for programs to keep:
  - `all` - Keep all valid programs
  - `non_one` - Exclude 100% accuracy programs
  - `non_extremes` - Exclude 0% and 100% accuracy programs
- `update_iteration` - How often to update training data
- `max_programs` - Maximum programs to keep in dataset

**Execution Settings (`azr`)**
- `executor` - Execution backend:
  - `qwq` - Raw Python (fast, not secure)
  - `sandboxfusion` - Docker sandbox (secure, production-ready)
- `execute_max_timeout` - Code execution timeout (seconds)
- `ast_check` - Validate code with AST before execution

### Training Flow

1. **Initialization**
   - Load base model (actor) and value model (critic)
   - Initialize Ray workers for distributed training
   - Load or generate seed datasets

2. **PROPOSE Phase**
   - Generate new reasoning problems (code_i, code_o, code_f)
   - Validate with AST checks and execution
   - Assign **learnability rewards** based on problem quality

3. **SOLVE Phase**
   - Attempt to solve generated problems
   - Execute solutions and verify against tests
   - Assign **accuracy rewards** based on correctness

4. **Training Update**
   - Use TRR++ (Trust Region Policy Optimization++) for stable updates
   - Combine generation and accuracy rewards
   - Update both actor (policy) and critic (value function)

5. **Data Selection**
   - Filter problems by learnability and difficulty
   - Update training dataset with new problems
   - Remove low-quality or saturated problems

### Important Scripts

**Training Scripts** (`scripts/`)
- `seeding/*.sh` - Generate initial training datasets
- `selfplay/*.sh` - Main training loop with different model configurations

**Evaluation Scripts** (`evaluation/code_eval/scripts/`)
- `run_lcb_gen.sh` - LiveCodeBench evaluation
- `run_evalplus.sh` - HumanEval/MBPP evaluation

### Development Tips

**Custom Reward Functions**
Add custom rewards in `azr.reward.generation_reward_config` (see config file for examples like `complexity_reward`, `diversity_reward`).

**Debug Mode**
Enable debug mode with `trainer.debug=True` in scripts. This:
- Starts a debugpy server on port 5678
- Disables auto-resume
- Increases logging verbosity

**W&B Integration**
Training logs to Weights & Biases. Set `trainer.wandb_run_id` to resume a specific run.

**Common Issues**
1. **Qwen3 Models**: Must run tokenizer cleanup script before use
2. **CUDA OOM**: Reduce batch sizes or use gradient checkpointing
3. **Executor Security**: Default Python executor is not production-safe; use Sandbox-Fusion for production
4. **Seed Data**: Ensure seed datasets exist before self-play training

## Dependencies

Built on top of:
- **veRL** - Reinforcement learning framework
- **vLLM** - High-throughput inference engine
- **Ray** - Distributed computing
- **Hydra** - Configuration management
- **FlashAttention** - Efficient attention implementation

## Citation

If using this codebase, cite:
```bibtex
@misc{zhao2025absolutezeroreinforcedselfplay,
      title={Absolute Zero: Reinforced Self-play Reasoning with Zero Data},
      author={Andrew Zhao and Yiran Wu and Yang Yue and Tong Wu and Quentin Xu and Yang Yue and Matthieu Lin and Shenzhi Wang and Qingyun Wu and Zilong Zheng and Gao Huang},
      year={2025},
      eprint={2505.03335},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
}
```