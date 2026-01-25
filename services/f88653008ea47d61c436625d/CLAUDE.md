# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mini-o3 is a visual reasoning model that achieves deep multi-turn "thinking-with-images" capability for visual search tasks. It builds upon [verl](https://github.com/volcengine/verl.git) (Volcano Engine Reinforcement Learning) and uses Qwen2.5-VL-7B-Instruct as the base model. The training consists of two stages: cold-start SFT followed by RL with GRPO.

## Commands

### Installation
```bash
conda create -n minio3 python=3.11 -y
conda activate minio3
cd Mini-o3
pip3 install -r requirements.txt
pip3 install -e .
pip3 install httpx==0.23.3
```

### Environment Variables for Training/Inference
```bash
export API_KEY=[YOUR_API_KEY]
export API_VERSION=[YOUR_API_VERSION]
export END_POINT=[YOUR_END_POINT]
export BASE_IMAGE_DIR=[YOUR_IMAGES_DIR]
```

### Training Pipeline

**Stage 1: Cold-start SFT** (uses LLaMA-Factory)
```bash
# Preprocess cold-start dataset
python3 scripts/preprocess_coldstart.py --dataset_path Mini-o3/Mini-o3-Coldstart-Dataset --output_dir [YOUR_DATASET_FOLDER]

# Train with LLaMA-Factory
llamafactory-cli train sft_configs/qwen2.5-vl.yaml
```

**Stage 2: RL Training** (uses verl with GRPO)
```bash
python3 -m verl.trainer.main_ppo algorithm.adv_estimator=grpo [other config options...]
```

Key training arguments:
- `trainer.nnodes`, `trainer.n_gpus_per_node`: Distributed training configuration
- `data.train_files`, `data.val_files`: Dataset paths (JSON format)
- `actor_rollout_ref.model.path`: Model checkpoint path
- `actor_rollout_ref.rollout.n`: Number of rollouts per prompt
- `actor_rollout_ref.rollout.max_generation_round`: Max multi-turn generations (default: 6)
- `reward_model.reward_manager`: Reward manager type (e.g., `naive_multithreads_tool`)

### Evaluation
Run validation-only mode to evaluate a checkpoint:
```bash
trainer.val_only=True actor_rollout_ref.rollout.val_n=32 actor_rollout_ref.rollout.val_do_sample=True
```

### Tests
```bash
pytest tests/
```

## Architecture

### Training Framework (verl)
- **Main entry point**: `verl/trainer/main_ppo.py` - Ray-based PPO trainer using Hydra configuration
- **Core trainer**: `verl/trainer/ppo/ray_trainer.py` - Implements PPO loop, advantage estimation, metrics logging
- **Workers**: `verl/workers/` - Distributed worker classes:
  - `fsdp_workers.py` - FSDP-based ActorRolloutRefWorker with vLLM integration
  - `rollout/` - vLLM rollout workers including multi-turn tool calling
  - `reward_manager/` - Reward computation (naive, multi-threaded, tool-enabled)

### DataFlow
1. `MultiModalDataset` (`verl/utils/dataset/multimodal_dataset.py`) loads JSON data with images
2. `DataProto` (`verl/protocol.py`) is the core data structure passing between workers (batches, tensors, non-tensors)
3. RayRemote workers handle Actor (training), Rollout (generation), Critic (value estimation), RewardModel
4. GRPO advantage computation normalizes rewards within groups

### Multi-Turn Tool Calling
- Rollout name: `vllm_multi_turn_tool_call` (see `verl/workers/rollout/vllm_rollout/`)
- Supports crop tool with `<grounding>` XML tags for visual search
- Uses `multi_turn_response_mask` to track separate response segments
- Configured via `actor_rollout_ref.rollout.multi_turn_prompt_type="v2"`
- Max generations per sample: `actor_rollout_ref.rollout.max_generation_round`

### Reward System
- **Hybrid reward manager**: Combines rule-based scoring with GPT-4V evaluation
- **Rule-based**: `verl/utils/reward_score/general_qa_tool_mc.py` - Multiple choice verification
- **GPT-based**: `verl/utils/reward_score/general_qa_tool.py` - Free-form answer evaluation via Azure OpenAI
- **Tool call penalty**: Penalizes excessive/invalid tool calls
- **Format reward**: Enforces `<answer>` tags and proper response structure

### Key Configuration Patterns
- Uses Hydra for config management (`verl/trainer/config/*.yaml`)
- FSDP strategy: `actor_rollout_ref.actor.strategy=fsdp`
- vLLM async mode: `actor_rollout_ref.rollout.mode=async`
- Use relative coordinates: `actor_rollout_ref.rollout.use_relative_coordinates=True`

## Data Format

Training/validation data uses JSON with:
```json
{
    "images": ["path/to/image1.jpg", ...],
    "doc_id": "unique_id",
    "problem": "Question about the image",
    "solution": "Correct answer",
    "data_source": "visual_probe_train|deepeyes_train|visual_probe_easy|..."
}
```

## Model Variants
- `Mini-o3-7B-SFT`: Cold-start supervised fine-tuned model
- `Mini-o3-7B-v1`: RL-trained model (final checkpoint)