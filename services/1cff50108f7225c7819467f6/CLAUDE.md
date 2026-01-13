# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Chinese project that implements **DouZero** (a deep reinforcement learning AI for DouDiZhu card game) to play Happy DouDiZhu in real-world gameplay scenarios. The application uses computer vision to recognize cards from the game screen and provides AI-powered move recommendations through a PyQt5 GUI.

**Key characteristic**: This project performs screen capture and pixel-level coordinate-based operations on the Happy DouDiZhu game window. It's designed for 1920x1080 resolution with the game window maximized in the bottom-right corner.

## Dependencies

- Python project with these key dependencies (see `requirements.txt`):
  - `torch==1.6.0` - Deep learning framework
  - `PyQt5==5.13.0` - GUI framework
  - `PyAutoGUI==0.9.50` - Screen capture and automation
  - `Pillow>=5.2.0` - Image processing
  - `opencv-python` - Computer vision
  - `rlcard` - Card game framework

## Common Development Commands

### Installation
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
python main.py
```

### Adjusting Screen Coordinates
If the card recognition coordinates don't match your screen setup:
```bash
python pos_debug.py
```

This will help you identify and adjust the screenshot region coordinates in `main.py:64-68`.

### Model Switching
The default model is **DouZero-WP** (Winning Percentage optimized). Models are loaded from:
- `main.py:75-79` - Model paths dictionary
- `baselines/douzero_WP/` directory contains:
  - `landlord.ckpt` - Landlord player model
  - `landlord_up.ckpt` - Upper farmer model
  - `landlord_down.ckpt` - Lower farmer model

To switch models, update the paths in the `card_play_model_path_dict` in `main.py`.

Available model types (from README):
- **SL** (`baselines/sl/`) - Supervised learning from human data
- **DouZero-ADP** (`baselines/douzero_ADP/`) - Trained with ADP (Average Difference Points) objective
- **DouZero-WP** (`baselines/douzero_WP/`) - Trained with WP (Winning Percentage) objective

## Repository Structure

### Core Application
- **`main.py`** - Main application entry point. Contains:
  - `MyPyQT_Form` class - Main PyQt5 GUI window
  - Screen capture coordinates (lines 64-68)
  - Confidence thresholds for card detection (lines 53-61)
  - Model path configuration (lines 75-79)
  - Card recognition and game logic

- **`MainWindowUI.py`** - Auto-generated PyQt5 UI code from `MainWindow.ui`

### DouZero Core Library (`douzero/` directory)
- **`env/`** - Game environment and card recognition
  - `game.py` - `GameEnv` class managing game state
  - `move_detector.py` - Card combination type detection
  - `move_generator.py` - Legal move generation
  - `move_selector.py` - Move selection logic
  - `env.py` - Environment observation functions

- **`evaluation/`** - AI agent implementations
  - `deep_agent.py` - `DeepAgent` class using trained models to predict moves
  - `random_agent.py` - Random move agent
  - `rlcard_agent.py` - RLCard-based agent
  - `simulation.py` - Game simulation utilities

- **`dmc/`** - Deep learning models
  - `models.py` - LSTM-based neural network models (`LandlordLstmModel`, `FarmerLstmModel`)
  - `dmc.py` - Deep Monte Carlo implementation

### Models and Assets
- **`baselines/`** - Pre-trained model checkpoints
  - `douzero_WP/` - Default WP-optimized models
  - `put_pretrained_models_here/` - Placeholder for additional models

- **`pics/`** - Template images for card recognition
  - Contains template images for all 54 cards in both red and black suits
  - Used for OpenCV template matching to recognize cards on screen
  - `bg.png` - Background image for GUI
  - `favicon.ico` - Application icon

### Utilities
- **`pos_debug.py`** - Tool for debugging and adjusting screenshot coordinates
- **`MainWindow.ui`** - Qt Designer UI file (source for MainWindowUI.py)

## High-Level Architecture

### 1. **GUI Layer** (PyQt5)
Located in `main.py:36+` - The `MyPyQT_Form` class provides the user interface that overlays on top of the game window. It displays:
- Current hand cards
- Opponent played cards
- AI-predicted moves
- Win rate percentage
- Control buttons (Start/End)

### 2. **Computer Vision Layer**
- Uses **PyAutoGUI** for screen capture
- Uses **OpenCV template matching** to recognize cards from screenshot regions
- Templates stored in `pics/` directory
- Recognition coordinates defined in `main.py:64-68`

### 3. **Game Environment Layer** (`douzero/env/`)
The `GameEnv` class (`douzero/env/game.py:23+`) manages:
- Game state (player hands, played cards, remaining cards)
- Turn management and player position tracking
- Bomb detection and scoring
- Move validation through `move_detector.py`

### 4. **AI Decision Layer** (`douzero/evaluation/`)
The `DeepAgent` class (`douzero/evaluation/deep_agent.py:22+`) uses trained neural networks to:
- Convert game state to observations via `get_obs()` (line 32)
- Feed observations through LSTM models (lines 33-38)
- Output move recommendations with confidence scores (lines 40-44)

### 5. **Deep Learning Models** (`douzero/dmc/`)
LSTM-based neural networks:
- `LandlordLstmModel` - For landlord player decisions
- `FarmerLstmModel` - For farmer player decisions
- Models use historical card play sequence (`z` input) and current state (`x` input)

### Data Flow
```
Screen Capture → Card Recognition → GameEnv State Update → DeepAgent Prediction → GUI Display
```

## Important Implementation Details

### Card Representation
Two card representation systems:
- **Environment cards** - Numeric representation (3-30) for AI
- **Real cards** - String representation ('3'-'T', 'J', 'Q', 'K', 'A', '2', 'X', 'D') for display

Mapping defined in `main.py:20-26` and `douzero/env/game.py:5-11`.

### Coordinate System
All screenshot coordinates are hardcoded for 1920x1080 resolution:
- `MyHandCardsPos` (line 64) - Player's hand cards region
- `LPlayedCardsPos` (line 65) - Left opponent played cards
- `RPlayedCardsPos` (line 66) - Right opponent played cards
- `LandlordFlagPos` (line 67) - Three landlord indicator regions
- `ThreeLandlordCardsPos` (line 68) - Bottom three cards region

**Critical**: If running on different resolution, coordinates MUST be adjusted using `pos_debug.py`.

### Confidence Thresholds
Configurable recognition thresholds in `main.py:53-61`:
- `MyConfidence` - Player's card detection confidence (default 0.95)
- `OtherConfidence` - Opponent's card detection confidence (default 0.9)
- `WhiteConfidence` - White space detection confidence (default 0.9)
- `LandlordFlagConfidence` - Landlord marker detection (default 0.9)
- `ThreeLandlordCardsConfidence` - Bottom cards detection (default 0.9)

## Usage Workflow (from README)

1. Start Happy DouDiZhu in windowed mode, maximize window
2. Position game window to bottom-right corner
3. Run `python main.py`
4. Wait for hand cards and landlord role to be confirmed
5. Click **Start** button - AI will identify cards (takes a few seconds)
6. AI will show win rate and suggested moves
7. Manually play the recommended cards in the game
8. Game result popup appears at end of round
9. Use **End** button to stop recording if errors occur

## Known Issues

- **王炸 bug** (line 26 in README): When playing "King Bomb" (joker pair), the card effect animation may cause recognition issues, potentially missing one of the jokers.

## Key Files to Understand

- `main.py` - Entry point, GUI, coordinate configuration
- `douzero/env/game.py` - Game state management
- `douzero/evaluation/deep_agent.py` - AI decision making
- `douzero/dmc/models.py` - Neural network architecture
- `douzero/env/move_detector.py` - Card combination validation