# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Glasses - An intelligent navigation and assistance system for visually impaired users, integrating blind path navigation, crosswalk assistance, object detection, and real-time voice interaction. Built with Python 3.9-3.11, FastAPI, YOLO models, and Aliyun DashScope API.

## Build & Run Commands

```bash
# Setup (Linux/macOS)
source setup.sh

# Manual setup
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Run
python app_main.py

# Docker
docker-compose up --build

# Model files required in model/:
# - yolo-seg.pt (blind path segmentation)
# - yoloe-11l-seg.pt (open-vocabulary detection)
# - shoppingbest5.pt (object recognition)
# - trafficlight.pt (traffic light detection)
# - hand_landmarker.task (MediaPipe hand detection)
```

## Architecture

### Core Layers

```
┌─────────────────────────────────────────────────────────────┐
│ FastAPI Server (app_main.py)                               │
│ - WebSocket routing (/ws/camera, /ws/viewer, /ws_audio)    │
│ - Global state management                                  │
│ - Model loading                                            │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│ NavigationMaster (navigation_master.py)                     │
│ State machine: IDLE → CHAT → BLINDPATH_NAV → CROSSING →   │
│               ITEM_SEARCH → TRAFFIC_LIGHT_DETECTION        │
│ - Coordinates all workflows                                │
│ - Manages mode transitions                                 │
│ - Voice command routing                                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
┌───▼───┐      ┌──────▼──────┐   ┌─────▼─────┐
│Blind  │      │ Crossstreet │   │ Item      │
│Path   │      │ Navigator   │   │ Search    │
│Nav    │      │             │   │ (yolo-    │
│       │      │             │   │  media)   │
└───────┘      └─────────────┘   └───────────┘
    │                 │                 │
    └─────────────────┼─────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│ Model Inference Layer                                       │
│ - YOLO segmentation/detection (ultralytics)                │
│ - MediaPipe hand detection                                 │
│ - HSV color-based traffic light detection (fallback)       │
│ - Lucas-Kanade optical flow stabilization                  │
└─────────────────────────────────────────────────────────────┘
```

### Key Modules

| Module | Purpose |
|--------|---------|
| `app_main.py` | Entry point, FastAPI app, WebSocket routing |
| `navigation_master.py` | Central state machine orchestrator |
| `workflow_blindpath.py` | Blind path detection, obstacle avoidance, turn handling |
| `workflow_crossstreet.py` | Crosswalk detection, alignment guidance |
| `yolomedia.py` | Object search with YOLO-E + MediaPipe hand tracking |
| `bridge_io.py` | Thread-safe frame buffer, producer-consumer pattern |
| `asr_core.py` | Aliyun DashScope Paraformer ASR for voice recognition |
| `omni_client.py` | Qwen-Omni-Turbo multimodal conversation client |
| `audio_player.py` | Multi-channel audio playback, TTS |

### Data Flows

**Video**: ESP32-CAM → `/ws/camera` (WebSocket) → `bridge_io` → NavigationMaster → `/ws/viewer` → Browser
**Voice Input**: ESP32-MIC → `/ws_audio` → DashScope ASR → Command parsing
**IMU**: ESP32-IMU → UDP 12345 → `/ws` → Three.js visualizer

### Key Design Patterns

1. **State Machine** - `navigation_master.py` manages mode transitions
2. **Producer-Consumer** - `bridge_io.py` decouples video capture from processing
3. **Strategy Pattern** - Each workflow implements `process_frame()` interface
4. **Observer** - WebSocket clients subscribe to video streams via `camera_viewers` set

## Development Notes

### Adding New Navigation Modes

1. Add state constant in `navigation_master.py`:
```python
NEW_MODE = "NEW_MODE"
```

2. Create workflow in `workflow_newmode.py` with `process_frame()` method

3. In `navigation_master.py`, handle state transition in the main loop

### Voice Commands

Commands are processed in `app_main.py` → `start_ai_with_text_custom()`. Add new command handlers there. Keywords like "帮我找" (find object), "开始导航" (start navigation) trigger specific modes.

### Performance Tuning

- `workflow_blindpath.py`: Adjust `FEATURE_PARAMS` for optical flow (fewer features = faster)
- `yolomedia.py`: Modify `HAND_DOWNSCALE` (smaller = faster) and `HAND_FPS_DIV` (larger = faster)

## Dependencies

- **FastAPI** for WebSocket/HTTP server
- **ultralytics (YOLO)** for segmentation and detection
- **MediaPipe** for hand landmark detection
- **dashscope** for Aliyun ASR and Qwen-Omni API
- **opencv-python** for video processing
- **PyTorch** 2.0.1+ for model inference

## API Keys Required

- `DASHSCOPE_API_KEY` - Aliyun DashScope (required for ASR and multimodal chat)

## Ports

- `8081` - HTTP/WebSocket server
- `12345/udp` - IMU data from ESP32