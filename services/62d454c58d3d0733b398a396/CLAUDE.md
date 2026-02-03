# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FineGrainedRLHF is a research repository implementing Fine-Grained Reinforcement Learning from Human Feedback, from the paper "Fine-Grained Human Feedback Gives Better Rewards for Language Model Training" (arXiv:2306.01693). It provides data, code, and models for training language models with fine-grained human feedback.

## Setup

```bash
# Create conda environment
conda create --name py39 python=3.9
conda activate py39

# Install package and dependencies
pip install -e .
python -m spacy download en_core_web_sm
```

## Training Commands

All experiments were run on 80G A100 GPUs. Training scripts are located in `tasks/{task_name}/training/`.

### SFT Training (QA Feedback)
```bash
bash tasks/qa_feedback/training/train_sft.sh
```
Uses `t5-large` as the base model, trained on 1K examples. Model saved to `./tasks/qa_feedback/model_outputs/t5-large-1k-train`.

### Reward Model Training

First prepare RM training data:
```bash
bash tasks/qa_feedback/reward_modeling/create_rm_train_files.sh
```

Then train individual reward models:
```bash
# Relevance/Verbosity RM (R1)
bash tasks/qa_feedback/reward_modeling/train_rel_rm.sh

# Factuality RM (R2)
bash tasks/qa_feedback/reward_modeling/train_fact_rm.sh

# Completeness RM (R3)
bash tasks/qa_feedback/reward_modeling/train_comp_rm.sh

# Baseline preference-based RM
bash tasks/qa_feedback/reward_modeling/train_baseline_rm.sh
```

### RLHF Training

**Holistic RLHF** (uses preference-based reward model):
```bash
bash tasks/qa_feedback/training/train_baseline.sh
```

**Fine-Grained RLHF** (uses three fine-grained RMs):
```bash
bash tasks/qa_feedback/training/train_finegrained.sh
```

Configuration files for RLHF are YAML files with sections for model, reward, PPO hyperparameters, training settings, and logging. Update `wandb_entity` in the config before running.

## Architecture

### Core Library (`fgrlhf/`)

- **ppo.py**: `PPOTrainer` class - handles PPO training loop with advantage computation, policy/value loss, KL penalty, and evaluation with wandb logging
- **policy.py**: `T5Policy` class - wraps T5ForConditionalGeneration for text generation and forward passes, handles logprob/value extraction
- **value.py**: `T5Value` class - separate value function using MLP head on decoder hidden states; optionally shares encoder with policy
- **reward.py**: `BasicReward` abstract class - base for reward models with token-level reward computation and KL penalization
- **utils.py**: Utility functions for masking, reduction operations, whitening, and training utilities
- **evaluators.py**: ROUGE evaluation using rouge-score
- **reward_utils.py**: Text splitting utilities using spaCy for sentence/subsentence segmentation

### Task-Specific Code (`tasks/qa_feedback/`)

- **training/reward.py**: Task-specific reward implementations:
  - `PreferenceReward`: Baseline preference-based reward (Longformer sequence classification)
  - `FineGrainedReward`: Three-component reward combining verbosity, factuality, and completeness RMs
  - `SubSentenceVerbosityReward`: Token-level reward for relevance/verbosity errors
  - `FactualityReward`: Token-level reward for factual accuracy

- **training/train_baseline.py**: Holistic RLHF training script using `BaselineReward`
- **training/train_finegrained.py**: Fine-grained RLHF training script using `FineGrainedReward`
- **training/train_sft.sh**: Shell script that calls `sft/run_sft.py`
- **reward_modeling/**: Scripts for training reward models using Longformer-based classifiers

### Training Pipeline

1. **SFT** (`sft/run_sft.py`): Supervised fine-tuning using Seq2SeqTrainer with ROUGE evaluation
2. **Reward Modeling** (`reward_modeling/run_fg_rm.py`): Token classification for fine-grained RMs
3. **RLHF** (`fgrlhf/ppo.py`): PPO training with ref policy KL constraint and advantage computation via GAE

### Data Format

QA feedback data in `tasks/qa_feedback/data/`:
- `train.json`: Training instances with `text`, `question`, `answer`, `passages` fields
- `dev.json`: Validation set
- `test.json`: Test set

## Key Configuration

Update these values in config YAML before training:
- `wandb_entity`: Your wandb username
- `mean`/`std`: Reward model statistics from `mean_std.txt` in model outputs

## Feedback Collection Interfaces

HTML interfaces for human feedback collection are in `tasks/qa_feedback/interface_html/templates/`:
- `annotation.html`: Fine-grained feedback collection
- `comparison.html`: Preference feedback collection