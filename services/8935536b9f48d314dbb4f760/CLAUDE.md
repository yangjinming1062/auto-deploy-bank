# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UI-TARS is a Python package for parsing VLM (Vision-Language Model) generated GUI action instructions into executable pyautogui automation scripts. It supports multiple model output formats and handles coordinate scaling for GUI agents.

**Primary location**: `/home/ubuntu/deploy-projects/8935536b9f48d314dbb4f760/codes/` - All Python code is in the `codes/` subdirectory.

## Common Commands

```bash
# Run tests
cd /home/ubuntu/deploy-projects/8935536b9f48d314dbb4f760/codes && make test

# Run tests directly with unittest
cd /home/ubuntu/deploy-projects/8935536b9f48d314dbb4f760/codes && uv run python3 -m unittest discover tests '*_test.py'

# Install dev dependencies
cd /home/ubuntu/deploy-projects/8935536b9f48d314dbb4f760/codes && uv sync

# Build and publish to PyPI
cd /home/ubuntu/deploy-projects/8935536b9f48d314dbb4f760/codes && uv build && uv publish
```

## Architecture

### Core Modules (`codes/ui_tars/`)

- **action_parser.py**: Main parsing module containing:
  - `parse_action_to_structure_output()` - Parses model response text to structured action dicts with coordinate scaling
  - `parsing_response_to_pyautogui_code()` - Converts structured actions to executable pyautogui scripts
  - `add_box_token()` - Adds `<|box_start|>/<|box_end|>` tokens for Qwen-VL format compatibility
  - Image resizing utilities: `smart_resize()`, `linear_resize()` for handling VLM image preprocessing

- **prompt.py**: Three prompt templates for different use cases:
  - `COMPUTER_USE_DOUBAO` - Desktop GUI tasks (click, type, hotkey, scroll, drag, wait)
  - `MOBILE_USE_DOUBAO` - Mobile/Android emulator tasks (includes long_press, open_app, press_home, press_back)
  - `GROUNDING_DOUBAO` - Lightweight action-only output for training/evaluation

### Model Output Format Support

- **qwen25vl**: Uses absolute coordinates; requires coordinate scaling via `smart_resize()`
- **doubao/Seed-VL**: Uses point format `<point>x y</point>`; coordinate handling varies

### Coordinate System

When `model_type="qwen25vl"`, coordinates from the model are absolute values (e.g., `(197,525)`) that must be scaled back to original image dimensions using `smart_resize()`. This is critical for grounding actions correctly on the original screenshot.

### Supported Actions

- Mouse: `click`, `left_double`, `right_single`, `hover`, `drag`/`select`
- Keyboard: `type`, `hotkey`, `press`, `keydown`, `keyup`
- Scroll: `scroll` (with optional point and direction)
- Mobile: `long_press`, `open_app`, `press_home`, `press_back`
- Control: `wait`, `finished`

## Testing

Tests are in `codes/tests/`:
- **action_parser_test.py**: Tests for parsing functions
- **inference_test.py**: Coordinate visualization example using matplotlib/PIL

Tests use Python's built-in `unittest` framework. Add `sys.path` manipulation to import from `ui_tars` package.

## Package Configuration

- **Package name**: `ui-tars` on PyPI
- **Current version**: 0.1.4
- **Python requirement**: >=3.10, <4.0
- **Build backend**: hatchling
- **Package structure**: Only includes files matching `ui_tars/**/*.py`, excludes test files