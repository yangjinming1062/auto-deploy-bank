# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**FastRTC** is a Python library for real-time audio and video streaming over WebRTC and WebSockets. It provides automatic voice detection, turn-taking, and built-in UI support via Gradio. The library enables developers to create audio/video streaming applications with minimal code.

## Architecture

### Core Components

**Backend (`backend/fastrtc/`)**
- **stream.py** - Main `Stream` class that encapsulates WebRTC functionality, UI generation, and FastAPI integration. This is the primary entry point for users.
- **webrtc_connection_mixin.py** - Mixin handling low-level WebRTC connection logic, peer connections, track management, and signaling.
- **webrtc.py** - Gradio WebRTC component wrapper providing the frontend integration.
- **websocket.py** - Alternative WebSocket-based handler for non-WebRTC streaming.
- **tracks.py** - Defines handler interfaces (`StreamHandler`, `AudioStreamHandler`, `VideoStreamHandler`) and track management utilities.

**Frontend (`frontend/`)**
- **Index.svelte**, **Example.svelte** - Svelte components for the WebRTC UI embedded in Gradio
- Built with Gradio custom component framework

**Sub-packages**
- **pause_detection/** - Voice activity detection using Silero VAD model
- **speech_to_text/** - Speech-to-text integration (Moonshine)
- **text_to_speech/** - Text-to-speech integration (Kokoro, Cartesia)
- **reply_on_pause.py** - Handler that processes audio when user pauses speaking
- **reply_on_stopwords.py** - Handler triggered by stop words (e.g., "Hey Computer")
- **credentials.py** - TURN/STUN server configuration (Cloudflare, Twilio, HuggingFace)

**Utils**
- **utils.py** - Audio conversion utilities, context management, and helper functions

### Key Design Patterns

1. **Stream Handler Interface** - User-defined handlers implement `StreamHandler` (sync) or `AsyncStreamHandler` (async) interface with `receive()`/`emit()` methods
2. **Mixin-based Architecture** - `WebRTCConnectionMixin` provides connection logic that `Stream` composes
3. **Multiple Transport Modes** - WebRTC (primary), WebSocket (alternative), Telephone integration
4. **Modality Support** - Audio-only, video-only, or audio-video combined streams

## Common Commands

### Development
```bash
# Install in development mode
pip install -e .[dev]

# Format code
just format
# Or manually:
ruff format .
ruff check --fix .
ruff check --select I --fix .
cd frontend && npx prettier --write . && cd ..

# Type checking
pyright

# Run tests
pytest
# Run specific test
pytest test/test_stream.py

# Build the package
just build
```

### Running Demos
```bash
# List available demos
just

# Run demo with uvicorn
just run <demo_name>
# Example:
just run llm_voice_chat

# Run demo with Gradio UI
just gradio <demo_name>
# Example:
just gradio llm_voice_chat

# Run demo in phone mode
just phone <demo_name>
# Example:
just phone llama_code_editor
```

### Publishing
```bash
# Upload all demo spaces to Hugging Face
just upload-all

# Upload specific demo
just upload <demo_path>

# Publish to PyPI
just publish

# Publish dev wheel to Hugging Face datasets
just publish-dev
```

### Documentation
```bash
# Serve docs locally at localhost:8081
just docs
```

## Testing

- Tests are in `test/` directory
- Uses `pytest` with `pytest-asyncio` for async tests
- CI runs on Python 3.10 and 3.13
- Dependencies: `pip install '.[dev, tts]'`

## Configuration

### Dependencies (pyproject.toml)
- Core: `gradio>=4.0,<6.0`, `aiortc`, `aioice`, `librosa`, `numpy`, `numba>=0.60.0`
- Optional extras:
  - `dev`: `build`, `twine`, `httpx`, `pytest`, `pytest-asyncio`
  - `vad`: `onnxruntime>=1.20.1` (voice activity detection)
  - `tts`: `kokoro-onnx` (text-to-speech)
  - `stopword`: `fastrtc-moonshine-onnx`, `onnxruntime>=1.20.1`
  - `stt`: `fastrtc-moonshine-onnx`, `onnxruntime>=1.20.1`

### Linting & Formatting
- **Ruff** for linting and formatting (configured in pyproject.toml)
- Target Python 3.10+
- Prettier for frontend code

### Key Installation
```bash
# Basic installation
pip install fastrtc

# With voice activity detection and text-to-speech
pip install "fastrtc[vad, tts]"
```

## Usage Patterns

### Basic Audio Stream
```python
from fastrtc import Stream, ReplyOnPause

def echo(audio: tuple[int, np.ndarray]):
    yield audio

stream = Stream(
    handler=ReplyOnPause(echo),
    modality="audio",
    mode="send-receive",
)

# Launch UI
stream.ui.launch()

# Or mount on FastAPI
app = FastAPI()
stream.mount(app)
```

### LLM Voice Chat Pattern
1. User speaks → `ReplyOnPause` detects pause
2. Audio sent to handler function
3. Convert to bytes and send to STT (e.g., Whisper, Moonshine)
4. Send text to LLM (e.g., Claude, OpenAI, Groq)
5. Convert LLM response to audio via TTS (e.g., Kokoro, ElevenLabs)
6. Stream audio back to user

See `demo/llm_voice_chat/` for complete example.

## Demos

Located in `demo/` directory with examples for:
- LLM voice chat (various providers)
- Whisper transcription
- Object detection (YOLOv10)
- Telephone integration
- Video streaming

## Deployment Notes

- Frontend is a Gradio custom component (Svelte-based)
- Backend uses FastAPI for API endpoints
- WebRTC requires TURN/STUN servers for production (handled by credentials.py)
- Supports telephone integration via FastPhone API (requires Hugging Face token)