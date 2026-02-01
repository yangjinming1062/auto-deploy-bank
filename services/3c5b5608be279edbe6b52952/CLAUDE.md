# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Seed1.5-VL Cookbook - A collection of examples and demos for ByteDance's Seed1.5-VL vision-language foundation model. The model is deployed on Volcano Engine (Model ID: `doubao-1-5-thinking-vision-pro-250428`) and accessed via REST API.

## Commands

### Run Gradio Demo (Main Entry Point)
```bash
# Install dependencies
pip install gradio decord torchvision httpx==0.23.3

# Launch with API key
API_KEY="..." python GradioDemo/app.py
```

The demo supports two modes:
- **Offline**: Upload images/videos and chat with the model
- **Online**: Real-time webcam streaming with chat

### Run Jupyter Notebooks
```bash
# Install notebook dependencies (same as above + jupyter)
pip install jupyter

# Launch notebook
jupyter notebook path/to/notebook.ipynb
```

Available notebooks:
- `GradioDemo/` - Interactive chat interface
- `GUI/gui.ipynb` - GUI agent task examples
- `Grounding/grounding.ipynb` - 2D visual grounding
- `3D-Understanding/3D Understanding.ipynb` - 3D spatial understanding
- `LongCoT/LongCoT.ipynb` - Chain-of-thought reasoning
- `Video/video_understanding.ipynb` - Video comprehension

## Architecture

### Core API Client (`GradioDemo/infer.py`)
The `SeedVLInfer` class handles all communication with the Seed1.5-VL API:
- **Video Processing**: `preprocess_video()` - Samples frames from video, resizes using `get_resized_hw_for_Navit()` (factor=28), and encodes to base64 JPEG
- **Image Processing**: `preprocess_streaming_frame()` - Handles webcam frames with same resize logic
- **Message Construction**: `construct_messages()` - Builds API payload with images/videos as base64 data URIs (`data:image/jpeg;base64,...`)
- **Streaming API**: `request()` - Handles SSE streaming responses, parses `delta.content` and `delta.reasoning_content`

### Key Configuration
- **Pixel Factor**: 28 (Navit tokenization requirement)
- **Default Resolution**: `min_pixels=4*28*28`, `max_pixels=5120*28*28`
- **Video Sampling**: 1 FPS by default, 16-81920 frames based on constraints
- **Model ID**: `doubao-1-5-thinking-vision-pro-250428`
- **API Endpoint**: `https://ark.cn-beijing.volces.com/api/v3/chat/completions`
- **Supported Image Formats**: JPG, JPEG, PNG, WebP
- **Aspect Ratio Limit**: Must be < 200

### Response Modes
- **General Mode** (`ConversationModeI18N.G`): Direct response without reasoning
- **Deep Thinking Mode** (`ConversationModeI18N.D`): Returns `<reasoning></think><response>` format for complex tasks

### GUI Agent (`GUI/`)
- **System Prompts** (`prompt.py`): Defines action spaces for computer use, mobile use, and grounding tasks
- **Action Parser** (`action_parser.py`): Parses model outputs into executable actions like `click()`, `type()`, `scroll()`, `hotkey()`, `drag()`
- Supports both absolute coordinates (Qwen format) and relative coordinate conversion

## Key Dependencies
```
gradio         # Web UI framework
decord         # Video reading
torchvision    # Image transformations (resize, encode_jpeg)
requests/httpx # HTTP client for API calls
PIL/numpy      # Image handling
```

## Environment Variables
- `API_KEY` - Required for all API calls (Volcano Engine credentials)

## Model Capabilities Demonstrated
1. **Visual understanding**: OCR, diagram interpretation, imageQA
2. **Visual grounding**: Point/box coordinate output with `<point>x y</point>` format
3. **Video understanding**: Frame extraction with timestamps `[{timestamp} second]`
4. **GUI agents**: Computer/mobile task automation
5. **3D spatial reasoning**: Depth/location understanding
6. **Chain-of-thought reasoning**: Configurable thinking mode

## Basic API Usage Example

```python
import base64
import requests

api_key = "your-api-key"
api_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
model = "doubao-1-5-thinking-vision-pro-250428"

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

# With image
data = {
    "model": model,
    "messages": [{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this image"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image('img.jpg')}"}}
        ]
    }],
    "thinking": {"type": "enabled"}  # Use "disabled" for direct answers
}

response = requests.post(api_url, headers={"Authorization": f"Bearer {api_key}"}, json=data)
result = response.json()["choices"][0]["message"]["content"]
```

## GUI Action Format

Actions from the model use coordinate format:
```
click(point='<point>x y</point>')
type(content='text\n')  # \n at end submits input
drag(start_point='<point>x1 y1</point>', end_point='<point>x2 y2</point>')
scroll(point='<point>x y</point>', direction='down')
hotkey(key='ctrl c')
```

Use `GUI/action_parser.py` to convert model outputs to executable pyautogui code.