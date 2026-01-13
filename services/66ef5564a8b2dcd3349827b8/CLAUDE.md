# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**VV** - A Chinese subtitle extraction and search project for 张维为 (Zhang Weiwei) from the TV show "这就是中国" (This is China). The project identifies video segments featuring the subject's face and extracts corresponding subtitles, enabling keyword and semantic search across the content.

**Live Demo**: [https://vv.cicada000.work](https://vv.cicada000.work)

## Architecture

### Video Processing Pipeline
```
Videos Input → Frame Extraction → Face Recognition → Subtitle OCR → JSON Database
```

1. **Frame Extraction** (`main.py:82-88`): Extracts frames from video at 1 FPS
2. **Face Recognition** (`FaceRec_insightface.py`): Uses InsightFace to identify target face, calculates similarity scores
3. **Subtitle Extraction** (`CutSubtitle_paddleocr.py`): Uses PaddleOCR to extract Chinese text from subtitle region (bottom 90px of video)
4. **Output**: Saves to `subtitle/` folder as JSON files with face similarity, timestamp, and extracted text

### System Components

**Core Modules:**
- `main.py` - Main orchestration, processes all videos in `Videos/` folder
- `params.py` - Global configuration (GPU settings, paths, OCR model directory)
- `FaceRec_insightface.py` - Face recognition using InsightFace (primary) or `FaceRec.py` using dlib (alternative)
- `CutSubtitle_paddleocr.py` - Subtitle extraction using PaddleOCR (primary) or `CutSubtitle.py` using ddddocr (alternative)
- `generate_features_insightface.py` - Generate face feature vectors from training images in `target/` folder

**API Backend** (`api/`):
- `index.py` - Flask API endpoint `/search` that calls Rust subtitle search binary (`subtitle_search_api`)
- `bot.py` - Telegram bot webhook handler with inline query support

**Frontend** (`Web/`):
- `index.html` - Main search interface with advanced options (text match ratio, face similarity threshold, watermark toggle)
- `script.js` - Frontend search logic with streaming results
- `subtitle_db` - Binary database file for fast local search

**Semantic Search** (`search/local/`):
- `search.py` - Vector-based semantic search using SentenceTransformers and FAISS
- `mapping.py` - Maps episode numbers to file paths
- Requires downloading index database from Releases: [index.zip](https://github.com/wen999di/VV/releases/download/index/index.zip)

**Data Processing** (`DataProcess/`):
- Scripts to convert subtitle JSON files into search database
- `create_db.py`, `import_subtitles.py`, `compress_subtitle.py`

### Deployment Configuration
- `vercel.json` - Vercel deployment config for Python API (Python 3.9) and static frontend
- Routes: `/api/*` → Python handlers, everything else → static files

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# For GPU acceleration (recommended)
pip install paddlepaddle-gpu  # Use appropriate CUDA version
pip install onnxruntime-gpu

# Or install CPU versions (slower)
pip install paddlepaddle
pip install onnxruntime
```

### Video Processing
```bash
# Place videos in Videos/ folder (mp4, avi, mkv, mov supported)
# Run main processing pipeline
python main.py

# This will:
# 1. Process each video (extract frames, recognize face, extract subtitles)
# 2. Resume from last checkpoint if interrupted
# 3. Save results to subtitle/ folder as JSON
# 4. Clean output_frames/ folder after each video
```

### Face Recognition Model Training
```bash
# Create target/ folder with face images
mkdir target

# Add face images (named consistently)
# Generate feature vectors for FaceRec_insightface.py
python generate_features_insightface.py

# Or generate for dlib version
python generate_features.py
```

### Web Interface (Development)
```bash
# Start Flask API locally
cd api
python index.py
# API runs on http://localhost:8000

# Serve frontend
cd Web
# Use any static file server (python -m http.server, etc.)
```

### Semantic Search
```bash
# Download pre-built vector index database
wget https://github.com/wen999di/VV/releases/download/index/index.zip
unzip index.zip -d search/

# Run semantic search
python search/search.py
```

### API Usage
```bash
# Subtitle search
GET /search?query=关键词&min_ratio=50&min_similarity=0.5&max_results=10

# Web search (DuckDuckGo)
GET /search?query=关键词&ai_search=true

# Health check
GET /health
```

## Configuration (params.py)

**GPU Settings:**
- `USE_GPU_FACE = False` - Enable CUDA for face recognition
- `USE_GPU_OCR = False` - Enable CUDA for OCR
- `GPU_MEMORY_OCR = 500` - GPU memory limit in MB for OCR

**Paths:**
- `VIDEOS_FOLDER = "Videos"` - Input video directory
- `FEATURES_FILE = "face_features_insightface.npz"` - Precomputed face features
- `FRAMES_OUTPUT = "output_frames"` - Temporary frame extraction directory
- `SUBTITLE_OUTPUT = "subtitle"` - JSON output directory
- `OCR_MODEL_DIR = "ch_PP-OCRv4_rec_infer"` - PaddleOCR model directory

**Face Similarity Threshold:**
- Default: 0.5 (values above considered valid match)
- Adjust in web interface: 0.0-1.0 range

**Text Match Ratio:**
- Default: 50 (keyword matching threshold)
- Adjust in web interface: 0-100 range

## Key Technical Details

**OCR Region:**
- Fixed subtitle area: `(235, 900, 1435, 990)` in 1920x1080 video
- Height: 90px from bottom

**Face Recognition:**
- InsightFace buffalo_l model with 640x640 detection size
- Cosine similarity for matching
- Features stored in NPZ format with 'encodings' array

**Rust Search Binary:**
- Located at `api/subtitle_search_api`
- Provides high-performance subtitle search
- Streams JSON results line-by-line

**Telegram Bot:**
- Inline query support for searching quotes
- Returns images from video previews at specific timestamps
- Preview extraction from remote image server

## Data Flow

1. **Video Processing**: Video → Frames (1 FPS) → Face Recognition + OCR → JSON subtitles
2. **Search Flow**: Query → API → Rust binary → Streaming results → Web interface
3. **Database Creation**: JSON subtitles → DataProcess scripts → Binary DB → Frontend search

## Dependencies (requirements.txt)

**Core ML/AI:**
- insightface, paddleocr, paddlepaddle
- torch, torchvision (PyTorch)
- onnxruntime
- scikit-learn, transformers, sentence-transformers

**Image/Video:**
- opencv-python, pillow

**Web/API:**
- flask, aiohttp, requests

**NLP/Chinese:**
- jieba, pypinyin, pycorrector

**Database/Search:**
- faiss, numpy, pandas

## Important Notes

- **GPU Recommended**: CPU processing is very slow; GPU acceleration highly recommended
- **Video Resolution**: Currently expects 1920x1080 videos (hardcoded OCR region)
- **CUDA Version**: When using GPU, ensure CUDA/cuDNN versions match paddlepaddle-gpu requirements
- **Resume Processing**: `main.py` tracks progress and resumes from last timestamp
- **Rust Binary Required**: The `subtitle_search_api` binary must be present for API to function
- **Database Format**: Search uses both JSON files (api) and binary DB (frontend)
- **Chinese Content**: All text, comments, and UI are in Chinese

## File Structure

```
/
├── main.py                    # Main entry point
├── params.py                  # Configuration
├── FaceRec_insightface.py     # Face recognition (primary)
├── CutSubtitle_paddleocr.py   # Subtitle extraction (primary)
├── generate_features_*.py     # Feature generation scripts
├── api/
│   ├── index.py              # Flask API endpoint
│   ├── bot.py                # Telegram bot
│   ├── subtitle_search_api   # Rust binary (compiled)
│   └── search/               # Search utilities
├── Web/
│   ├── index.html            # Frontend UI
│   ├── script.js             # Frontend logic
│   ├── subtitle_db           # Binary search DB
│   └── *.js, *.css           # Static assets
├── search/
│   ├── local/                # Local semantic search
│   └── cloud/                # Cloud search (if exists)
├── DataProcess/               # DB creation scripts
├── subtitle/                  # Generated JSON subtitles
├── output_frames/             # Temporary frames (auto-cleaned)
├── Videos/                    # Input videos (manual creation)
└── target/                    # Training images (manual creation)
```

## Performance Optimization

- **GPU Memory**: Adjust `GPU_MEMORY_OCR` in `params.py` based on GPU capacity
- **Batch Processing**: Process multiple videos sequentially in `main.py`
- **Incremental**: Resume from checkpoints instead of reprocessing
- **Model Selection**: InsightFace more accurate than dlib; PaddleOCR more accurate than ddddocr
- **Frame Rate**: Currently 1 FPS (configurable in `main.py:86`)

## Troubleshooting

**Import Errors**: Ensure all GPU/CPU versions of packages match (paddlepaddle/paddlepaddle-gpu, onnxruntime/onnxruntime-gpu)

**OCR Fails**: Check video resolution is 1920x1080, verify OCR model directory exists

**Face Recognition Fails**: Verify `face_features_insightface.npz` exists, check CUDA availability

**API Search Returns Nothing**: Ensure `subtitle_search_api` binary is present and executable

**Slow Processing**: Enable GPU in `params.py`, reduce video resolution, or increase FPS interval