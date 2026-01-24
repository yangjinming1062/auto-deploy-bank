# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **DouZero_For_Happy_DouDiZhu** - a PyQt5 GUI application that integrates the DouZero reinforcement learning AI with the "Happy DouDiZhu" (欢乐斗地主) game. It uses screen scraping and template matching to recognize cards, then provides AI-suggested moves.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Architecture

The application follows a layered architecture:

```
main.py (PyQt5 GUI + Recognition + Game Loop)
         │
         ├──► pics/ (Template images for card recognition)
         │    - m*.png: My card templates
         │    - o*.png: Other players' card templates
         │    - pass.png: "Don't play" button template
         │    - landlord_words.png: Landlord badge template
         │    - white.png: Empty area detection
         │
         ├──► douzero/ (RL environment from DouZero project)
         │    ├── env/game.py: Card game simulation and rules
         │    ├── env/move_*: Card combination generation/selection
         │    └── evaluation/deep_agent.py: Deep reinforcement learning agent
         │
         └──► baselines/douzero_WP/ (Pretrained PyTorch models)
              - landlord.ckpt, landlord_up.ckpt, landlord_down.ckpt
```

**Key entry point**: `main.py` contains `MyPyQT_Form` class which:
- Initializes screen capture coordinates in `__init__` (lines 64-68)
- Handles card recognition via template matching in `find_my_cards`, `find_other_cards`, `find_three_landlord_cards`
- Manages game flow through `init_cards` → `start` loop
- Uses `DeepAgent` from `douzero.evaluation.deep_agent` for AI suggestions

## Card Recognition System

The application uses PyAutoGUI template matching (`locateOnScreen`, `locateAll`) with confidence thresholds:
- `MyConfidence = 0.95` for player's own cards
- `OtherConfidence = 0.90` for other players' cards
- `cards_filter()` method filters duplicate detections by x-coordinate distance

**Important**: Screen coordinates are hardcoded for 1920x1080 resolution with the game window maximized in the bottom-right corner. See `pos_debug.py` for a debug tool to adjust these.

## Key Files

- `main.py`: Main application logic, UI event handling, recognition, and AI integration
- `MainWindow.ui` / `MainWindowUI.py`: Qt Designer UI definition (auto-generated)
- `pos_debug.py`: Debug tool for adjusting screenshot region coordinates
- `douzero/env/game.py`: Core DouDiZhu game rules and state management
- `douzero/evaluation/deep_agent.py`: Neural network inference for card decisions