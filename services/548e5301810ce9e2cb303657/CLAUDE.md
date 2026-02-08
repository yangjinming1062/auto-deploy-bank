# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UI-Venus is a state-of-the-art UI agent that leverages Reinforcement Fine-Tuning (RFT) for GUI understanding and action prediction across mobile, desktop, and web interfaces. The project includes:

- **Grounding models** (UI-Venus-Ground-7B/72B): Locate UI elements based on natural language instructions
- **Navigation models** (UI-Venus-Navi-7B/72B): Execute multi-step UI actions to complete tasks

All models are based on Qwen2.5-VL architecture.

## Installation

```bash
pip install -r requirements.txt
```

Dependencies: transformers==4.49.0, vllm==0.8.3, qwen_agent, qwen_vl_utils, torch, torchvision, torchaudio

## Running Evaluation

### Grounding Tasks (UI Element Localization)

Run grounding evaluation on ScreenSpot benchmarks:
```bash
bash scripts/run_gd_7b.sh    # 7B model
bash scripts/run_gd_72b.sh   # 72B model
```

Key arguments for `eval_screenspot_pro.py`:
- `--model_type`: "ui_venus_ground_7b" or "ui_venus_ground_72b"
- `--screenspot_imgs`: Folder containing screenshots
- `--screenspot_test`: Folder containing annotation JSON files
- `--model_name_or_path`: HuggingFace model path or local checkpoint
- `--log_path`: Output JSON path
- `--task`: "all" or comma-separated task names
- `--gt_type`: "positive" or "negative" ground truth type
- `--inst_style`: "instruction", "action", or "description"

### Navigation Tasks (UI Action Prediction)

```bash
bash scripts/run_navi_7b.sh
bash scripts/run_navi_72b.sh
```

Key arguments for `runner.py`:
- `--model_path`: Model checkpoint path (HuggingFace or local)
- `--input_file`: JSON file with trace tasks (see examples/trace/trace.json)
- `--output_file`: Output path for execution history
- `--max_pixels`/`--min_pixels`: Image resolution constraints
- `--tensor_parallel_size`: GPU parallelization (default: 1 for 7B, 4 for 72B)

## Architecture

### Grounding Pipeline (`models/grounding/`)

1. `ui_venus_ground_7b.py` / `ui_venus_ground_72b.py`: Model wrapper classes
   - Load Qwen2.5-VL model with flash attention and bfloat16
   - `inference()`: Takes instruction + image path, returns bounding box coordinates

2. `eval_screenspot_pro.py`: Main evaluation script
   - Loads model and test annotations
   - Runs inference on all samples
   - Computes metrics: overall accuracy, text/icon accuracy, per-platform breakdown
   - Outputs detailed results with fine-grained, seeclick-style, and leaderboard-style metrics

### Navigation Pipeline (`models/navigation/`)

1. `ui_venus_navi_vllm.py`: vLLM-based inference wrapper
   - Uses vLLM for batch inference with tensor parallelism
   - Processes multi-modal inputs (image + text prompt)

2. `ui_venus_navi_agent.py`: Main agent class
   - `VenusNaviAgent`: Orchestrates multi-step UI navigation
   - `step()`: Executes one action given a task and screenshot
   - Maintains action history with configurable length
   - Parses model output into structured actions (Click, Drag, Scroll, Type, etc.)
   - Handles coordinate rescaling from model input to original image size

3. `utils.py`: Action parsing and prompt templates
   - `parse_answer()`: Converts model output like `Click(box=(0.5,0.3))` to structured JSON
   - `USER_PROMPT`: System prompt defining available actions and reasoning format
   - Supported actions: Click, Drag, Scroll, Type, Launch, Wait, Finished, CallUser, LongPress, PressBack, PressHome, PressEnter, PressRecent

4. `runner.py`: Entry point for navigation evaluation
   - Loads trace data (list of task/screenshot pairs)
   - Runs agent step-by-step and exports execution history

## Data Formats

### Grounding Input (`examples/grounding_meta_format.json`)
```json
{
  "img_filename": "pc_ede36f9b-1154-4f76-b7f8-c15d7d3f9b6e.png",
  "bbox": [910, 78, 954, 112],
  "instruction": "close this window",
  "application": "windows",
  "ui_type": "icon",
  "platform": "desktop",
  "img_size": [960, 540]
}
```

### Grounding Output (`examples/grounding_result_format.json`)
```json
{
  "details": [{
    "img_path": "osworld/0FOB4CLBT2.png",
    "prompt_to_evaluate": "Open the filter function for search settings.",
    "pred": [1435.5, 339.5],
    "bbox": [1422, 326, 1449, 354],
    "correctness": "correct"
  }]
}
```

### Navigation Input (`examples/trace/trace.json`)
Array of traces, where each trace is a list of steps:
```json
[
  [
    {"image_path": "path/to/screenshot.png", "task": "任务描述"},
    ...
  ]
]
```

## Key Conventions

- Coordinates are normalized (0-1 range) in model input, rescaled to pixel values for execution
- Model outputs use structured tags: `</think>` for reasoning, `<action>` for action, `<conclusion>` for summary
- Input images are resized using `smart_resize` from qwen_vl_utils with min_pixels/max_pixels constraints
- Evaluation follows ScreenSpot protocol with filterable results by platform, UI type, instruction style