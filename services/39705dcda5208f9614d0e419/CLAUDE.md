# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Manga Image Translator - A tool for translating text in images (primarily manga/comics). Supports 20+ languages with both online API translators and offline translation models. Handles the full pipeline: text detection → OCR → translation → inpainting → rendering.

## Commands

### Python Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Run local batch translation
python -m manga_translator local -v -i <path> -o <dest>

# Run web server (UI at http://127.0.0.1:8000, API at http://127.0.0.1:8001)
cd server && python main.py --use-gpu

# Run WebSocket server
python -m manga_translator ws --host 0.0.0.0 --port 5003

# Run API server
python -m manga_translator shared --host 0.0.0.0 --port 5003

# Print config schema
python -m manga_translator config-help
```

### Frontend (React + TypeScript)

```bash
cd front
npm install
npm run dev        # Development with HMR (http://localhost:5173)
npm run build      # Production build
npm run start      # Run production build
npm run typecheck  # TypeScript checks
```

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest test/test_translation.py

# Run with verbose output
pytest -v
```

## Architecture

### Backend Pipeline (manga_translator/manga_translator.py)

The `MangaTranslator` class orchestrates this processing pipeline:

1. **Upscaling** (`upscaling/`) - Optional image upscaling before detection
2. **Detection** (`detection/`) - Text region detection using models (ctd, dbconvnext, craft, paddle)
3. **OCR** (`ocr/`) - Text extraction from detected regions (48px, 32px, mocr)
4. **Textline Merge** (`textline_merge/`) - Merge adjacent textlines
5. **Mask Refinement** (`mask_refinement/`) - Refine text masks
6. **Translation** (`translators/`) - Translate text via online APIs or offline models
7. **Inpainting** (`inpainting/`) - Remove original text from image (lama_large, sd, original)
8. **Rendering** (`rendering/`) - Render translated text onto image (default, manga2eng)
9. **Colorization** (`colorization/`) - Optional color restoration (mc2)

### Mode Handlers (manga_translator/mode/)

- `local.py` - Batch file/folder translation
- `ws.py` - WebSocket real-time translation service
- `share.py` - Shared API server mode
- `web.py` - Old Flask-based web UI (legacy)

### Server (server/)

FastAPI-based web server providing:
- Web UI (index.html) - Legacy interface
- API endpoints (`/translate`, `/translateStream`)
- WebSocket endpoint for real-time updates
- Instance management (instance.py)

### Key Configuration Classes

- **Config** (config.py) - Main configuration schema
- **Detector** - Text detection models and options
- **OCR** - Optical character recognition models
- **Translator** - Translation services (online APIs + offline models)
- **Inpainter** - Image inpainting models
- **Renderer** - Text rendering engines
- **Upscaler** - Image upscaling models

## Environment Variables

Create `.env` file for API keys:
```
OPENAI_API_KEY=sk-xxx
DEEPL_AUTH_KEY=xxx
SAKURA_API_BASE=http://127.0.0.1:8080/v1
```

See README.md for full environment variable reference.

## Model Management

- Models auto-download to `./models` at runtime
- Override with `--model-dir` or `MODEL_DIR` env var
- GPU support via `--use-gpu` (auto-switches between CUDA/MPS)

## Language Support

20+ languages with ISO 639-1 codes (CHS, CHT, JPN, ENG, KOR, etc.). Target language specified via config: `translator.target_lang`.

## Critical Implementation Notes

- Python 3.10-3.11 required (check pyproject.toml)
- GPU memory optimization enabled by default; disable with `--disable-memory-optimization`
- Concurrent batch mode available via `--batch-concurrent` to prevent truncation
- Pre/post-translation dictionaries use regex patterns (see README for format)
- Glossary support for OpenAI translator via `OPENAI_GLOSSARY_PATH`