# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Manga Image Translator - A Python-based tool for translating text in manga/comic images with support for multiple languages, OCR, and rendering. The project supports both local CLI usage and web server modes via FastAPI.

## Development Commands

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running Tests
```bash
# Run all tests
pytest test

# Run with specific translator
pytest --translator=chatgpt --target-lang=ENG

# Run specific test file
pytest test/test_translation.py

# Run with verbose output
pytest -v test/
```

### Running the Application
```bash
# Local batch translation
python -m manga_translator local -v -i <path_to_image_or_folder>

# Web server mode (port 8000)
cd server && python main.py --use-gpu

# WebSocket mode
python -m manga_translator ws --host=127.0.0.1 --port=5003

# API mode (port 5003)
python -m manga_translator shared --host=127.0.0.1 --port=5003

# Show config help
python -m manga_translator config-help
```

### Docker
```bash
# Build image
make build-image

# Run web server with GPU
make run-web-server

# Or manually run container
docker run --gpus all -p 5003:5003 --ipc=host --rm manga-image-translator \
  server/main.py --verbose --start-instance --host=0.0.0.0 --port=5003 --use-gpu
```

### Frontend (React)
```bash
cd front
npm install
npm run dev      # Development with HMR
npm run build    # Production build
```

## Architecture

### Core Pipeline Flow

The translation process follows this pipeline in `manga_translator/manga_translator.py`:

1. **Detection** (`manga_translator/detection/`) - Finds text regions in images
   - Detectors: `default`, `dbconvnext`, `ctd`, `craft`, `paddle`, `none`

2. **OCR** (`manga_translator/ocr/`) - Extracts text from detected regions
   - Models: `32px`, `48px`, `48px_ctc`, `mocr`

3. **Translation** (`manga_translator/translators/`) - Translates extracted text
   - Online: `chatgpt`, `deepseek`, `deepl`, `youdao`, `baidu`, `sakura`, etc.
   - Offline: `sugoi`, `nllb`, `nllb_big`, `m2m100`, `qwen2`, etc.

4. **Inpainting** (`manga_translator/inpainting/`) - Removes original text
   - Models: `lama_large`, `lama_mpe`, `sd`, `original`, `none`

5. **Rendering** (`manga_translator/rendering/`) - Overlays translated text
   - Renderers: `default`, `manga2eng`, `none`

6. **Optional: Colorization** (`manga_translator/colorization/`) - Adds color back
   - Model: `mc2`

### Key Entry Points

| File | Purpose |
|------|---------|
| `manga_translator/__main__.py` | CLI entry point with mode dispatching |
| `manga_translator/manga_translator.py` | Main `MangaTranslator` class with full pipeline |
| `manga_translator/args.py` | Argument parsing for all modes |
| `server/main.py` | FastAPI web server endpoints |

### Mode Structure

- **local** (`manga_translator/mode/local.py`): Batch image translation
- **ws** (`manga_translator/mode/ws.py`): WebSocket real-time translation
- **shared** (`manga_translator/mode/share.py`): API server with task queue

### Configuration

Configuration uses a nested schema in `manga_translator/config.py`:
- `translator`: Translation service and target language
- `detector`: Text detection model and parameters
- `ocr`: Optical character recognition model
- `inpainter`: Text removal model
- `render`: Text rendering/overlay options
- `upscale`: Image upscaling (improves detection on small text)

### Important Modules

| Module | Description |
|--------|-------------|
| `manga_translator/utils/` | Shared utilities (logging, image I/O, model loading) |
| `manga_translator/translators/common.py` | Base `CommonTranslator` class for all translators |
| `manga_translator/textline_merge.py` | Merges split text lines for better translation |
| `manga_translator/mask_refinement/` | Refines text masks before inpainting |

### Model Management

Models are automatically downloaded to `./models` at runtime. To download manually:
```bash
python docker_prepare.py --models=detector.default,ocr.48px,inpaint.lama_large
```

### Translation Chain Support

Multiple translators can be chained:
```bash
--translator-chain "google:JPN;sugoi:ENG"  # Japanese→English via Google→Sugoi
```

## Environment Variables

API-based translators require keys in `.env`:
- `OPENAI_API_KEY`, `DEEPL_AUTH_KEY`, `YOUDAO_APP_KEY`, etc.
- `OPENAI_GLOSSARY_PATH` for custom glossaries
- `SAKURA_API_BASE` for local Sakura server

See `README.md` for full environment variable documentation.