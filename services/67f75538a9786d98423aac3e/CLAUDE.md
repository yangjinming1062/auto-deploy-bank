# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CrossWOZ is the first large-scale Chinese Cross-Domain Wizard-of-Oz task-oriented dialogue dataset. It contains 6K dialogue sessions and 102K utterances across 5 domains: hotel, restaurant, attraction, metro, and taxi. The project provides a toolkit for building and evaluating task-oriented dialogue systems using the ConvLab-2 architecture.

## Commands

### Installation
```bash
pip install -e .                    # Basic install
pip install -e .[develop]           # Install with dev dependencies
```

**Python requirement**: >= 3.5

### Testing
```bash
pytest tests/ --cov=ConvLab-2 --cov-report term-missing
```

### Training Individual Models
```bash
# NLU (BERT-based)
python convlab2/nlu/jointBERT/train.py

# DST (TRADE)
python convlab2/dst/trade/crosswoz/train.py

# Policy (MLE)
python convlab2/policy/mle/crosswoz/train.py

# NLG (SCLSTM)
python convlab2/nlg/sclstm/crosswoz/train.py
```

### Evaluating Models
```bash
# Policy evaluation with simulation
python convlab2/policy/mle/crosswoz/evaluate.py
```

## Architecture

This codebase implements a **pipeline architecture** for task-oriented dialogue systems with modular components:

```
User Utterance → NLU → DST → Policy → NLG → System Utterance
                    ↑___________________|
                      (Dialog State)
```

### Core Components (convlab2/)

| Component | Purpose | Interface |
|-----------|---------|-----------|
| **NLU** | Converts text → dialog acts | `predict(utterance, context)` |
| **DST** | Tracks belief state | `update(action)`, `state` dict with 'history', 'belief_state' |
| **Policy** | Selects next action given state | `predict(state)` returns dialog acts |
| **NLG** | Converts dialog acts → text | `generate(action)` |

### Dialog Agents (convlab2/dialog_agent/)

- **Agent** (ABC): Base interface with `response()` and `init_session()`
- **PipelineAgent**: Combines NLU, DST, Policy, NLG modules flexibly
- **BiSession**: Manages two-agent conversations (user ↔ system)
- **Session**: Manages single-agent sessions

### Module Structure

Each component follows `convlab2/util/module.py` interface with:
- `train()`, `test()`: Model lifecycle
- `init_session()`: Reset for new dialog
- `from_cache()`, `to_cache()`: State persistence

### Data Format

Dialog acts use tuple format: `[intent, domain, slot, value]`
- Intent: General, Request, Inform, Select, Recommend, NoOffer, etc.
- Domains: 酒店 (hotel), 餐厅 (restaurant), 景点 (attraction), 出租 (taxi), 地铁 (metro)

## Key Modules

### NLU (convlab2/nlu/)
- **BERTNLU**: Joint BERT-based intent/slot classification with context

### DST (convlab2/dst/)
- **RuleDST**: Rule-based dialog state tracker for CrossWOZ
- **TRADE**: Transferable multi-domain state tracker (neural)

### Policy (convlab2/policy/)
- **MLE**: Maximum Likelihood Estimation policy
- **Simulator**: Rule-based user simulator for evaluation

### NLG (convlab2/nlg/)
- **SCLSTM**: SC-LSTM for response generation
- **TemplateNLG**: Template-based response generation

### Utilities (convlab2/util/)
- **crosswoz/state.py**: Default state schema
- **crosswoz/lexicalize.py**: Delexicalization utilities
- **crosswoz/goal_generator.py**: User goal generation
- **crosswoz/database/**: Knowledge bases for hotel, restaurant, attraction, metro, taxi

## Pre-trained Models

Models are automatically downloaded from HuggingFace when first instantiated:
- **BERTNLU**: `https://huggingface.co/ConvLab/ConvLab-2_models/resolve/main/bert_crosswoz_all_context.zip`
- **TRADE DST**: `https://huggingface.co/ConvLab/ConvLab-2_models/resolve/main/trade_crosswoz_model.zip`
- **MLE Policy**: `https://huggingface.co/ConvLab/ConvLab-2_models/resolve/main/mle_policy_crosswoz.zip`
- **SCLSTM NLG**: `https://huggingface.co/ConvLab/ConvLab-2_models/resolve/main/nlg_sclstm_crosswoz.zip`

## Data

CrossWOZ dataset in `data/crosswoz/` (zipped JSON):
- `train.json.zip`: 5,012 dialogues
- `val.json.zip`: 500 dialogues
- `test.json.zip`: 500 dialogues

Also includes database files and vocabulary files (sys_da_voc.json, usr_da_voc.json).

## Web Annotation Platform

The `web/` directory contains an annotation platform for dialogue data labeling. Run with:
```bash
cd web && sh setup.sh && python run.py
```

Supports two annotators conversing synchronously with online annotations.

## Common Evaluation Patterns

End-to-end evaluation typically uses:
```python
from convlab2.dialog_agent import PipelineAgent, BiSession

user_agent = PipelineAgent(nlu, None, user_policy, nlg_usr, name='user')
sys_agent = PipelineAgent(nlu, dst, sys_policy, nlg_sys, name='sys')
session = BiSession(sys_agent=sys_agent, user_agent=user_agent)

# Iterate turns
sys_response, user_response, session_over, reward = session.next_turn(sys_response)
```