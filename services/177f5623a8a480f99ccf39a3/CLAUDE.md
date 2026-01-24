# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Drive Like A Human is a research project exploring autonomous driving with Large Language Models. It uses GPT-3.5/Azure OpenAI to make real-time driving decisions in a highway simulation environment (highway-env).

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the main demo (requires configuring config.yaml with API keys)
python HELLM.py

# Configure LLM (edit config.yaml):
# - Set OPENAI_API_TYPE to 'azure' or 'openai'
# - Add your API key (OPENAI_KEY for OpenAI, AZURE_API_* for Azure)
```

## Architecture

The system uses a LangChain agent-based architecture for driving decision-making:

```
HELLM.py (entry point)
    ├── gymnasium highway-v0 environment
    ├── Scenario (scenario state management + SQLite DB)
    ├── DriverAgent (LLM + tool-based reasoning)
    │   └── Uses 8 safety/decision tools from customTools.py
    └── OutputParser (parses LLM output to action IDs)
```

**Key Flow:**
1. `HELLM.py` sets up the highway-env simulation and runs the control loop
2. Each frame: `Scenario.upateVehicles()` updates vehicle states from environment observations
3. `DriverAgent` queries the LLM with the current scenario and available tools
4. Tools in `customTools.py` (e.g., `getAvailableActions`, `isChangeLaneConflictWithCar`) provide safety checks
5. `OutputParser` extracts structured decisions (action_id, action_name, explanation)
6. Decisions are executed in the environment and logged to SQLite

**Core Components:**
- `LLMDriver/driverAgent.py`: Main LangChain ReAct agent using `CHAT_ZERO_SHOT_REACT_DESCRIPTION`
- `LLMDriver/customTools.py`: 8 tool classes for driving safety checks (lane availability, conflict detection)
- `scenario/scenario.py`: Manages roadgraph (4 lanes) and vehicle states; persists to SQLite
- `scenario/baseClass.py`: `Lane` and `Vehicle` dataclasses

**LLM Interaction:**
- Uses conversation memory (`ConversationTokenBufferMemory`) for context
- System prompts defined in `agent_propmts.py` with traffic rules and safety guidelines
- Decision process: available actions → available lanes → involved cars → safety checks → final decision

## Configuration

- `config.yaml`: LLM API credentials (OpenAI or Azure)
- `HELLM.py` lines 46-66: Environment configuration (vehicle count, action space, simulation duration)