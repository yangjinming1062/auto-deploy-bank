# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **VQAScore**, a Python package for evaluating text-to-visual (image/video/3D) generation models. It implements alignment scoring using vision-language models via a VQA-style question-answering approach.

## Build and Test Commands

```bash
# Install in editable mode
pip install -e .

# Run paper evaluations (Winoground, TIFA160, etc.)
python eval.py --model clip-flant5-xxl
python eval.py --model openai:ViT-L-14

# GenAI-Bench evaluations
python genai_image_eval.py --model clip-flant5-xxl
python genai_video_eval.py --model clip-flant5-xxl

# Generate images for a model
python -m genai_bench.generate --output_dir ./outputs --gen_model runwayml/stable-diffusion-v1-5

# Evaluate generated images
python -m genai_bench.evaluate --model clip-flant5-xxl --output_dir ./outputs --gen_model runwayml/stable-diffusion-v1-5
```

## Architecture

### Three Scoring Paradigms

The package implements three scoring approaches, each with multiple model implementations:

1. **VQAScore** (`t2v_metrics/vqascore.py`) - VQA-based scoring using question-answer probability
2. **CLIPScore** (`t2v_metrics/clipscore.py`) - CLIP-based similarity scoring
3. **ITMScore** (`t2v_metrics/itmscore.py`) - Image-Text Matching scoring

### Model Registration Pattern

Each scoring paradigm uses a registration pattern in its `models/[type]_models/__init__.py`:

```python
# Model lists are exported from each model implementation
from .clip_t5_model import CLIP_T5_MODELS, CLIPT5Model
from .llava_model import LLAVA_MODELS, LLaVAModel

# Combined in ALL_VQA_MODELS list
ALL_VQA_MODELS = [CLIP_T5_MODELS, LLAVA_MODELS, ...]

# Factory function selects the right model class
def get_vqascore_model(model_name, device='cuda', cache_dir=..., **kwargs):
    if model_name in CLIP_T5_MODELS:
        return CLIPT5Model(model_name, device=device, cache_dir=cache_dir, **kwargs)
    elif model_name in LLAVA_MODELS:
        return LLaVAModel(...)
```

### Score Base Class (`t2v_metrics/score.py`)

- `Score` is the abstract base class for all scoring models
- Handles video input for image-only models by frame concatenation (video_mode="concat")
- Native video models (Qwen2-VL, LLaVA-OneVision) handle videos directly (video_mode="direct")
- `forward()` method: accepts images/videos and texts, returns M×N score tensor
- `batch_forward()` method: processes batches with DataLoader for large datasets

### Model Base Class (`t2v_metrics/models/model.py`)

- `ScoreModel` is the abstract base class for all model implementations
- Subclasses must implement: `load_model()`, `load_images()`, `forward()`
- Common utilities in `vqascore_models/mm_utils.py` for vision-language models

### Model Implementations Location

| Scoring Type | Directory |
|--------------|-----------|
| VQAScore models | `t2v_metrics/models/vqascore_models/` |
| CLIPScore models | `t2v_metrics/models/clipscore_models/` |
| ITMScore models | `t2v_metrics/models/itmscore_models/` |

## Common Usage Patterns

### Basic Scoring

```python
import t2v_metrics

# Get a scoring function (auto-selects VQAScore, CLIPScore, or ITMScore)
score_func = t2v_metrics.get_score_model(model='clip-flant5-xxl')

# Single image-text pair
score = score_func(images=['path/to/image.png'], texts=['a cat sitting on a couch'])

# Pairwise M×N scoring
scores = score_func(images=['img1.png', 'img2.png'], texts=['text1', 'text2'])
# Returns 2×2 tensor

# Batch processing
scores = score_func.batch_forward(dataset=[{'images': [...], 'texts': [...]}], batch_size=16)
```

### Video Scoring

```python
# For native video models (Qwen2.5-VL, LLaVA-OneVision, etc.)
score = t2v_metrics.VQAScore(model='qwen2.5-vl-7b')
score(images=['video.mp4'], texts=['a baby crying'], fps=8.0)

# For image-only models, frames are auto-concatenated
score = t2v_metrics.VQAScore(model='clip-flant5-xxl')
score(images=['video.mp4'], texts=['a baby crying'], num_frames=8)
```

### Custom Templates

```python
score = t2v_metrics.VQAScore(model='clip-flant5-xxl')
scores = score(
    images=['img.png'],
    texts=['caption'],
    question_template='Does this figure show "{}"?',
    answer_template='Yes'
)
```

## Key File Locations

- `t2v_metrics/__init__.py` - Main exports and model factory
- `t2v_metrics/score.py` - Base Score class with video handling
- `t2v_metrics/models/model.py` - Base ScoreModel class
- `t2v_metrics/models/video_utils.py` - Video frame extraction utilities
- `t2v_metrics/constants.py` - HF cache dir, context length, system messages

## System Requirements

- **ffmpeg** is a required system dependency (checked on import)
- Python 3.10+
- GPU with 40GB+ memory recommended for large models (clip-flant5-xxl, llava-v1.5-13b)