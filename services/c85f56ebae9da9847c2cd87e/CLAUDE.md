# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **TextStarCraft II** project - an LLM-based StarCraft II bot that uses Chain of Summarization (CoS) approach. The system converts game observations to text, uses LLMs for strategic decision-making, and executes actions via the burnysc2 library. It can defeat built-in AI at Harder (Lv5) difficulty.

## Development Commands

```bash
# Install dependencies (run from project root)
pip install -r requirements.txt

# Note: chromadb must be installed before burnysc2 due to package conflicts
# burnysc2==6.2.0 is the core library for SC2 interaction

# Run single process LLM agent test
python sc2_bot/StarCraft2_ruleagent/protoss_agent/env_test/test_the_env.py

# Run multi-process parallel testing (recommended for faster evaluation)
python sc2_rl_agent/starcraftenv_test/multiprocess_test.py

# Run with specific agent type (random, chatgpt, gemini, claude2, qwen_7b, llama2_7b, prompt1)
python sc2_rl_agent/starcraftenv_test/multiprocess_test.py --agent_type gpt --num_processes 4

# Run ChromaDB vector database tests
python sc2_rl_agent/starcraftenv_test/vector_database/Chroma_vdb.py

# Run Protoss tech tree tests
python sc2_rl_agent/starcraftenv_test/techtree/ProtossTechTree.py
```

## Key Configuration Options

| Parameter | Description | Values |
|-----------|-------------|--------|
| `--player_race` | Bot's race | `Protoss` (fully supported), `Zerg`, `Terran` (under development) |
| `--opposite_race` | Opponent race | `Protoss`, `Zerg`, `Terran` |
| `--difficulty` | Built-in AI difficulty | `VeryEasy`, `Easy`, `Medium`, `Hard`, `Harder` (Lv5, best tested) |
| `--map_idx` | Map index from ladder pool | 0-6 (LADDER_MAP_2023 pool) |
| `--agent_type` | LLM backend | `gpt`, `gemini`, `claude2`, `qwen_7b`, `llama2_7b` |
| `--LLM_model_name` | Specific model | `gpt-3.5-turbo-16k`, `gemini-pro`, `glm-4`, etc. |

## Architecture

```
sc2_bot/
├── StarCraft2_ruleagent/
│   ├── protoss_agent/          # Primary implemented race
│   │   ├── for_test_env.py     # VsBuildIn gym environment
│   │   ├── test_for_finetune.py # WarpGateBot - main Protoss agent
│   │   ├── env_test/
│   │   │   ├── test_the_env.py # Single process runner
│   │   │   ├── llm_agent.py    # LLM agent wrapper
│   │   │   └── random_agent.py # Baseline random agent
│   │   └── ...
│   ├── zerg_agent/             # Partial implementation
│   └── terran_agent/           # Partial implementation

sc2_rl_agent/starcraftenv_test/
├── agent/                      # LLM agent implementations
│   ├── chatgpt_agent.py
│   ├── gemini_agent.py
│   ├── claude2_agent.py
│   ├── qwen_7b_agent.py
│   ├── llama2_agent.py
│   └── ...
├── prompt/
│   └── prompt.py               # Prompt templates (V1-V4, realtime variants)
├── techtree/
│   └── ProtossTechTree.py      # Race-specific tech trees
├── config/
│   └── config.py               # Maps, difficulties, build levels
├── vector_database/
│   └── Chroma_vdb.py           # ChromaDB memory/retrieval
├── LLM/                        # API integrations
└── worker.py                   # Multi-process worker functions
```

## Core Systems

### 1. Environment (`VsBuildIn` gym env)
- Located in `sc2_bot/StarCraft2_ruleagent/protoss_agent/for_test_env.py`
- Uses multiprocessing for communication between gym interface and SC2 bot
- Transaction dict shares state: `information`, `action_*`, `reward`, `done`, `result`
- Maps: `Altitude LE`, `Ancient Cistern LE`, `Babylon LE`, `Dragon Scales LE`, `Gresvan LE`, `Neohumanity LE`, `Royal Blood LE`

### 2. Chain of Summarization Pipeline
1. **L1 Summarization**: Raw SC2 observation → text description (`summarize/L1_summarize.py`)
2. **L2 Summarization**: Multi-frame analysis → strategic decisions (`summarize/L2_summarize.py`)
3. **Action Extraction**: Parse LLM decisions into executable actions
4. **Execution**: `WarpGateBot.on_step()` applies actions to SC2

### 3. Action Space
Actions are categorized into:
- `building_supply`: Pylon construction
- `expansion`: Nexus expansion
- `produce_worker`: Probe production
- `build_vespene`: Assimilator construction
- `train_*`: Unit training (zealot, stalker, ht, archon)
- `research_*`: Upgrade research (blink, warpgate, ground weapons, etc.)
- `CHRONOBOOST`: Nexus ability usage

### 4. Protoss Bot (`WarpGateBot`)
- Extends `BotAI` from burnysc2
- Implements `on_step()` loop with:
  - `procedure()`: Time-based build order (00:00-09:00+)
  - `distribute_workers()`: Resource gathering
  - `defend()`: Base defense
  - `attack()`: Army coordination
- Uses `get_information()` to generate text observation
- Auto-mode after 05:00 for LLM-controlled decisions

### 5. Prompt System
- `StarCraftIIPrompt_V4` (default) - Most refined version
- `StarCraftIIPrompt_realtime` - For fine-tuned models
- System prompts include race-specific guidance (Chrono Boost for Protoss, Larva injection for Zerg)

### 6. LLM API Configuration
Default API endpoints:
- OpenAI-compatible: `http://172.18.116.172:8000/v1` (for local models like Qwen)
- Claude: Uses `zhipuai` library for GLM models
- Set `LLM_api_key` and `LLM_api_base` for custom endpoints

## Important Notes

- **StarCraft II client required**: Game must be installed (Windows recommended per README)
- **Protoss only**: Zerg and Terran implementations are incomplete
- **OpenAI version constraint**: Use `openai==0.27.9` - later versions have API changes
- **Replay saving**: Configured in `multiprocess_test.py` to `sc2_rl_agent/starcraftenv_test/log/`
- **Transaction logging**: Enabled in `test_for_finetune.py` to `transaction_logs2.txt`