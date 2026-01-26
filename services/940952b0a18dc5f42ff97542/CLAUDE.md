# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**dia-tts-server** is a FastAPI-based text-to-speech server that wraps the Nari Labs Dia TTS model. It provides both an OpenAI-compatible API and a custom API, plus a web UI for interactive use.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server (default port 8003)
python server.py

# Access Web UI: http://localhost:8003
# Access API Docs: http://localhost:8003/docs
```

## Architecture

### Core Components

- **server.py**: FastAPI application with endpoints for TTS generation and Web UI rendering. Handles request validation, routes to engine, and manages UI state.
- **engine.py**: Core TTS generation logic. Manages model loading (via `Dia` class from the `dia` package), handles voice cloning preparation, text chunking, and audio post-processing.
- **config.py**: YAML-based configuration manager (`YamlConfigManager` singleton). Handles config.yaml loading/saving with `.env` overrides only during initial seeding.
- **models.py**: Pydantic request/response models for API validation (`OpenAITTSRequest`, `CustomTTSRequest`).
- **utils.py**: Audio encoding/decoding, text chunking by sentences, silence trimming, and Whisper transcript generation.

### Voice Modes

1. **dialogue**: Multi-speaker mode using `[S1]`/`[S2]` tags in text
2. **single_s1** / **single_s2**: Single speaker modes
3. **clone**: Voice cloning using reference audio from `./reference_audio` (requires `.txt` transcript or Whisper fallback)
4. **predefined**: Curated voices from `./voices` directory (treated as clone mode internally)

### Text Chunking

Long text is automatically split by sentence boundaries when `split_text=True`. Chunking respects speaker tags - each chunk contains sentences from only one speaker unless `allow_multiple_tags=True`. This prevents voice inconsistency when generating long dialogues.

### Configuration

Primary config is `config.yaml`. Key sections:
- `server`: host, port
- `model`: HuggingFace repo_id, weights filename (defaults to `ttj/dia-1.6b-safetensors`)
- `paths`: model_cache, reference_audio, output, voices directories
- `generation_defaults`: default values for CFG scale, temperature, top_p, seed, etc.

Changes to `server`, `model`, or `paths` require server restart. `generation_defaults` and `ui_state` apply dynamically.

### Model Loading

Models download automatically from HuggingFace on first run into `./model_cache`. The server loads weights to CPU first to reduce VRAM spikes, then moves to GPU. BF16 SafeTensors are the default (reduced VRAM ~7GB).

## API Endpoints

- **`POST /v1/audio/speech`**: OpenAI-compatible TTS endpoint
- **`POST /tts`**: Custom endpoint with full parameter control (chunking, explicit transcript, etc.)
- **`GET /`**: Serves the web UI (Jinja2 template at `ui/index.html`)
- **`POST /web/generate`**: Handles web UI form submissions
- **`POST /save_settings`**: Saves config updates to `config.yaml`
- **`GET /health`**: Returns server status and model load state