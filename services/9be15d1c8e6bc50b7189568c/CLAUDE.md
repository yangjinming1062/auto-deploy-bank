# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Development Commands

```bash
# Install Pillow and run selftest
make install

# Run tests on installed Pillow
make test

# Run tests with parallel execution
make test-p

# Run lint checks (ruff, black, pre-commit hooks)
make lint

# Automatically fix lint issues
make lint-fix

# Run mypy type checking
make mypy

# Run coverage report
make coverage

# Build source distribution
make sdist

# Full pre-release test suite
make release-test
```

### Running Individual Tests

```bash
# Run a specific test file
python3 -m pytest Tests/test_image.py

# Run tests matching a pattern
pytest -k test_image.py

# Run selftest directly
python3 selftest.py
```

## Project Architecture

Pillow is a hybrid Python/C library providing image processing capabilities. The codebase is organized as follows:

### Core C Implementation (`src/`)

- **`_imaging.c`**: Main imaging module binding; exports the `Image.core` Python object
- **`libImaging/`**: Low-level image processing algorithms (Convert, Draw, Filter, Resample, etc.)
- **Extension modules** (built via pybind11):
  - `_imaging.c`: Core image operations
  - `_imagingft.c`: FreeType font rendering
  - `_imagingcms.c`: Little CMS color management
  - `_webp.c`: WebP format support
  - `_avif.c`: AVIF format support
  - `_imagingmath.c`: Image math operations
  - `_imagingmorph.c`: Morphological operations
  - `_imagingtk.c`: Tkinter integration

### Python Package (`src/PIL/`)

- **`Image.py`** (152KB): Central module; contains the `Image` class and lazy-loading plugin system via `_plugins`
- **Image plugins** (`*ImagePlugin.py`): Format-specific handlers (e.g., `JpegImagePlugin.py`, `PngImagePlugin.py`)
- **Supporting modules**:
  - `ImageDraw.py`, `ImageDraw2.py`: Drawing primitives
  - `ImageFont.py`: Font handling
  - `ImageFilter.py`, `ImageOps.py`, `ImageChops.py`: Image transformations
  - `ImageCms.py`: Color management
  - `ImageFile.py`: Base class for file-based image handlers
  - `ImagePalette.py`: Color palette handling

### Build System

- **`setup.py`**: Custom build using pybind11's `Pybind11SetupHelpers` with `pil_build_ext` custom builder
- **`_custom_build/`**: Custom build backend for dependency detection
- **`pyproject.toml`**: Project metadata and tool configurations (ruff, mypy, pytest, cibuildwheel)

### Key Patterns

- **Lazy plugin loading**: Image plugins are auto-discovered via `PIL._plugins` and registered through `Image.register_open()`
- **C/Python boundary**: Python code wraps C extensions via `Image.core` (private, subject to change)
- **Memory model**: Images use reference counting; call `load()` to ensure data is loaded before access
- **Format detection**: `Image.open()` identifies format by file content/extension; raises `UnidentifiedImageError` if unknown

## Testing

- 166+ test files in `Tests/`, named `test_*.py`
- Test helper utilities in `Tests/helper.py`
- Test images in `Tests/images/`
- Uses `pytest` with `pytest-xdist` for parallel execution

## Dependencies

Required: Python 3.10+, zlib, libjpeg
Optional: freetype, libimagequant, lcms2, libtiff, libwebp, libavif, raqm, harfbuzz, fribidi, xcb

Build-time dependencies are detected automatically via `pkg-config` or environment variables (`JPEG_ROOT`, `FREETYPE_ROOT`, etc.).