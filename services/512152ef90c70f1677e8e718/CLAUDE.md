# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`imgutils` (dghs-imgutils) is an anime-style image processing library that integrates various advanced models for:
- **Metrics**: Visual similarity/difference calculation (lpips, ccip for character matching)
- **Tagging**: WD14, DeepDanbooru, and other image tagging models
- **Detection**: Face, head, person, eyes, hands, text, and censorship detection
- **Segment/Edge/Restore**: Background removal, lineart generation, and image super-resolution
- **Validation**: Monochrome detection, truncated file checking

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt

# Full installation with GPU support
pip install -r requirements-gpu.txt
pip install -r requirements-model.txt
pip install -r requirements-torchvision.txt
pip install -r requirements-transformers.txt

# Run tests (requires dataset)
make dataset
make unittest

# Run a single test file
pytest test/metrics/test_ccip.py -sv -m unittest

# Run a specific test
pytest test/metrics/test_ccip.py::test_ccip_extract_feature -sv -m unittest

# Build package
make package

# Build docs
make docs
```

Test configuration is in `pytest.ini`. Tests use the `-m unittest` marker. The Makefile `unittest` target includes coverage reporting and automatic retry for network-related failures (OSError, HTTP 429/502/504).

## Architecture

### Package Structure

The main package is in `imgutils/` with these key modules:

- **`data/`**: Image loading and preprocessing utilities (`load_image`, `load_images`)
- **`metrics/`**: Visual similarity metrics (lpips, ccip, psnr, aesthetic scoring)
- **`tagging/`**: Image tagging implementations (wd14, deepdanbooru, camie)
- **`detect/`**: Object detection wrappers (faces, heads, persons, hands, eyes)
- **`segment/`**: Character segmentation (isnetis, briaai)
- **`edge/`**: Line detection (lineart, canny, hed)
- **`restore/`**: Image restoration (waifu2x, realcugan)
- **`validate/`**: Image validation (monochrome, truncation check)
- **`utils/`**: Internal utilities including the `ts_lru_cache` decorator

### Model Loading Pattern

Models are loaded from HuggingFace using `hf_hub_download()` and cached with `@ts_lru_cache()`:

```python
from imgutils.utils import ts_lru_cache
from huggingface_hub import hf_hub_download

@ts_lru_cache()
def _load_model():
    return open_onnx_model(hf_hub_download(
        repo_id='deepghs/model_name',
        filename='model.onnx',
    ))
```

The `zoo/` directory contains model-specific files including ONNX weights, config files, and metadata for models hosted on HuggingFace.

### Key Utilities

- **`ts_lru_cache(level='global')`**: Thread-safe LRU cache decorator (defined in `imgutils/utils/cache.py`)
- **`open_onnx_model()`**: Load ONNX runtime sessions (defined in `imgutils/utils/onnxruntime.py`)
- **`load_image()` / `load_images()`**: Unified image loading with automatic format detection

## Testing

Tests are in `test/` mirroring the `imgutils/` structure. Test files use pytest with the `unittest` marker. Test data is downloaded from HuggingFace datasets via `make dataset`. Tests have automatic retry for network failures (8 retries with 2-second delays).

## Code Style

- Follows PEP 8 with flake8 validation
- Functions use type hints extensively
- Docstrings follow numpydoc format with `:param` and `:rtype` annotations
- Public APIs are exported via `__all__` in each module