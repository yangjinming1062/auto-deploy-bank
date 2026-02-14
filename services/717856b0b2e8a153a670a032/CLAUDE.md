# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OmniParser is a screen parsing tool that converts GUI screenshots into structured elements. It uses two models:
- **Icon Detection Model** (YOLO-based): Detects interactable UI elements
- **Icon Caption Model** (Florence-2 or BLIP2): Generates descriptions of detected icons

## Setup Commands

```bash
# Create and activate environment
conda create -n "omni" python=3.12
conda activate omni

# Install dependencies
pip install -r requirements.txt

# Download model weights
cd OmniParser/weights
huggingface-cli download microsoft/OmniParser-v2.0 --include "icon_detect/*" "icon_caption/*"
mv icon_caption icon_caption_florence

# Run Gradio demo
python gradio_demo.py

# Run OmniParser server (for OmniTool)
cd omnitool/omniparserserver
python -m omniparserserver --som_model_path ../../weights/icon_detect/model.pt \
  --caption_model_name florence2 --caption_model_path ../../weights/icon_caption_florence \
  --device cuda --BOX_TRESHOLD 0.05

# Run OmniTool Gradio UI (separate terminal)
cd omnitool/gradio
python app.py --windows_host_url localhost:8006 --omniparser_server_url localhost:8000
```

## Key Components

### Core Parsing (`util/utils.py`)
- `get_som_labeled_img()`: Main entry point for parsing screenshots
- `check_ocr_box()`: OCR text detection using EasyOCR or PaddleOCR
- `predict_yolo()`: YOLO model inference for icon detection
- `get_parsed_content_icon()`: Batch caption generation for detected icons
- `remove_overlap_new()`: NMS-like filtering of overlapping boxes

### Model Loaders (`util/utils.py`)
- `get_yolo_model()`: Loads YOLO model from ultralytics
- `get_caption_model_processor()`: Loads Florence-2 or BLIP2 for icon captioning

### Gradio Demos
- `gradio_demo.py`: Simple standalone demo for OmniParser
- `omnitool/gradio/app.py`: Full OmniTool UI with multi-model support

### Server (`omnitool/omniparserserver/omniparserserver.py`)
- FastAPI server exposing `/parse/` endpoint for screen parsing
- Takes base64-encoded images, returns annotated images and parsed content

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Image     │────▶│  OCR (Easy   │────▶│    YOLO     │
│  Input      │     │   OCR/Paddle │     │  Detection  │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
┌─────────────┐     ┌──────────────┐     ┌──────▼──────┐
│ Annotated   │◀────│   Caption    │◀────│  Crop &     │
│   Image     │     │   Model      │     │  Resize     │
└─────────────┘     └──────────────┘     └─────────────┘
```

## Supported Models & Providers

- **Caption models**: `florence2` (default), `blip2`, `phi3_v`
- **LLM providers for OmniTool**: OpenAI (4o/o1/o3-mini), Anthropic, DeepSeek (R1), Qwen (2.5VL), Groq, Azure, Vertex
- **Detection**: YOLOv8 via ultralytics

## Common Development Tasks

### Adding a new LLM provider
1. Add the provider to `APIProvider` enum in `loop.py`
2. Create a new client in `agent/llm_utils/`
3. Update model selection dropdown in `app.py`

### Modifying parsing behavior
- Adjust `BOX_TRESHOLD` to filter more/less detected boxes
- Modify `iou_threshold` in `get_som_labeled_img()` for overlap handling
- Change caption batch size for memory optimization

## Model Weights

Weights must be downloaded to `weights/` directory:
- `weights/icon_detect/model.pt` - Detection model
- `weights/icon_caption_florence` - Caption model (Florence-2)
- `weights/icon_caption_blip2` - Optional alternative caption model

## Dependencies

Key packages: torch, ultralytics, transformers, gradio, openai, paddleocr, easyocr, supervision, pytest
