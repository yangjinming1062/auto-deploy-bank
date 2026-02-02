# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DEPS (Describe, Explain, Plan and Select) is an interactive LLM-based planning system for open-world Minecraft agents. It uses Large Language Models to generate plans for multi-task completion in Minecraft, combined with a neural network policy (trained with MineCLIP goal embeddings) for action execution.

## Running the Agent

```bash
python main.py model.load_ckpt_path=<path/to/ckpt>
```

Configuration is managed via Hydra. Override config values via command line, e.g.:
```bash
python main.py model.load_ckpt_path=/path/to/ckpt eval.task_name=obtain_diamond
```

Key config options:
- `model.load_ckpt_path`: Path to the policy checkpoint
- `eval.task_name`: Task to evaluate (e.g., `obtain_planks`, `obtain_diamond`)
- `eval.env_name`: Minecraft biome (default: `Plains`)
- `pretrains.clip_path`: Path to MineCLIP checkpoint

## Environment Setup

```bash
conda create -n planner python=3.9
conda activate planner
python -m pip install numpy torch==2.0.0.dev20230208+cu117 --index-url https://download.pytorch.org/whl/nightly/cu117
pip install -r requirements.txt
pip install git+https://github.com/MineDojo/MineCLIP
# Install MC-Simulator (modified MineDojo) and MC-Controller from CraftJarvis
```

OpenAI API keys should be placed in `data/openai_keys.txt` (one key per line).

## Architecture

### Main Loop (`main.py`)
The `Evaluator` class orchestrates the entire agent:
1. Resets environment and initializes Planner, MineAgent, CraftAgent, Selector
2. `initial_planning()`: Planner generates goal list from task question
3. `eval_step()`: Main evaluation loop running for `max_ep_len` timesteps
4. On each step: checks goal completion, executes actions via MineAgent/CraftAgent
5. `replan_task()`: If goal fails, replans using LLM with updated inventory context

### Planning Module (`planner.py`)
`Planner` class handles LLM-based planning:
- `initial_planning()`: Generates initial plan from task question using OpenAI Codex/GPT-3
- `generate_goal_list()`: Parses LLM output into structured goals (name, type, object, prerequisites, ranking)
- `replan()`: Generates new plan when goals fail, incorporating failure descriptions and inventory
- `query_gpt3()` / `query_codex()`: OpenAI API calls with key rotation

Goal types: `mine`, `craft`, `smelt`

### Action Execution (`controller.py`)
Three agent types handle different goal types:

**MineAgent**: Neural network policy (`SimpleNetwork`) trained with imitation learning
- Uses MineCLIP text encoder to embed goal descriptions
- Backbone: IMPALA CNN or ResNet for visual features
- Fusion strategies for goal-image conditioning: `concat`, `bilinear`, `film`, `rgb`
- Optional recurrent module: GRU or Transformer (GPT-2 backbone)
- Horizon prediction for goal timing

**MineAgentWrapper**: Executes MineAgent actions with goal ranking
- For simple goals (cobblestone, stone, coal, iron_ore, diamond): uses scripted behaviors
- For complex goals: samples from neural policy action distribution

**CraftAgent**: Hand-crafted action sequences for crafting/smelting
- `craft_w_table()` / `craft_wo_table()`: Craft with/without crafting table
- `smelt_w_furnace()` / `smelt_wo_furnace()`: Smelt with/without furnace
- Uses generators for multi-step action sequences

### Selector (`selector.py`)
`Selector` class for goal selection - currently raises `NotImplementedError`.

## Key Data Files

- `data/task_info.json`: Task definitions with question, group, alias, episode length, target object
- `data/goal_mapping.json`: Mappings for goal types (mineclip, clip, horizon)
- `data/goal_lib.json`: Goal library with type, output objects, prerequisites, and tools
- `data/openai_keys.txt`: OpenAI API keys (one per line)

Task groups (alias):
- `basic`: Basic crafting (planks, sticks, slabs, etc.)
- `simple_tool`: Wood/stone tools, crafting table, furnace
- `dig_down`: Mining stone, coal, torches
- `hunt_and_food`: Food, beds, paintings
- `complex_tool`: Iron/gold tools, buckets, shears
- `equipment`: Armor, shields
- `iron_stage`: Iron-based items (minecart, hopper, etc.)
- `challenge`: Diamond mining

## Code Structure

```
src/
├── models/simple.py          # SimpleNetwork: main policy architecture
├── mineclip_lib/             # MineCLIP integration (CLIP model, pooling, etc.)
├── utils/
│   ├── foundation.py         # Embedding modules (ExtraObs, PrevAction, FiLM, etc.)
│   ├── impala_lib/           # IMPALA CNN, attention, action heads
│   ├── vpt_lib/              # Video Pretraining (VPT) utilities from Minecraft
│   ├── vision.py             # Backbone creation, image resizing
│   ├── loss.py               # Loss functions (action_loss, horizon_loss)
│   └── mlp.py                # MLP building blocks
```

## Neural Network Details

`SimpleNetwork` forward pass:
1. Embed goal via `self.embed_goal` (linear from MineCLIP embedding dim)
2. Extract image features via backbone with goal-conditioned processing
3. Fuse RGB and goal embeddings (concat/bilinear/FiLM)
4. Append extra obs (biome, compass, GPS, voxels) and previous actions
5. Process through recurrent (GRU/Transformer) for temporal modeling
6. Fuse horizon embedding (predicted or ground truth)
7. Predict action logits via MLP head

Action space: `[3, 3, 4, 11, 11, 8, 1, 1]` (discrete multi-categorical)