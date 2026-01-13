# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django MarkdownX is a comprehensive Markdown editor plugin for Django with live preview, drag & drop image uploads, and real-time rendering. It provides a rich text editing experience with customizable image handling, SVG protection, and multiple editor instances per page.

## High-Level Architecture

The project follows a standard Django app structure with both backend and frontend components:

### Backend (Python/Django)
- **Core Module** (`markdownx/`):
  - `widgets.py` - MarkdownxWidget (extends forms.Textarea) and AdminMarkdownxWidget for Django admin integration
  - `views.py` - ImageUploadView (handles AJAX image uploads) and MarkdownifyView (converts Markdown to HTML)
  - `forms.py` - ImageForm processes uploads with PIL/Pillow for image manipulation, compression, and SVG security
  - `settings.py` - All configuration constants prefixed with `MARKDOWNX_`
  - `utils.py` - Markdownify function and image processing utilities (scale_and_crop, xml_has_javascript)
  - `models.py` - Database models
  - `exceptions.py` - MarkdownxImageUploadError

### Frontend (TypeScript/JavaScript)
- **Source** (`static-src/markdownx/js/`):
  - `markdownx.ts` - Main TypeScript source (28KB)
  - `utils.ts` - Utility functions
  - Compiled to `markdownx/static/markdownx/js/markdownx.js` and minified `markdownx.min.js`

### Testing
- **Test Suite** (`markdownx/tests/`):
  - `tests.py` - Contains SimpleTest with image upload testing
  - Tests require Django's test client and verify AJAX image upload functionality

### Documentation
- **Docs** (`docs-src/`):
  - Markdown files for MkDocs documentation
  - Built with `mkdocs build`

## Common Development Commands

### Initial Setup
```bash
# Install development environment (no container)
python dev.py -no-container

# Install with documentation tools
python dev.py -no-container --with-docs

# Install with TypeScript/npm tools
python dev.py -no-container --with-npm-settings
```

### Container-Based Development (Linux/macOS only)
```bash
# Vagrant setup
python dev.py --vagrant
python dev.py -run-vagrant  # Starts dev server on localhost:8000

# Docker setup
python dev.py --docker
python dev.py -run-docker  # Starts dev server on localhost:8000
```

### Running Tests
```bash
python runtests.py
```

### Building Documentation
```bash
mkdocs build
```

### Installing Package
```bash
python setup.py install
```

### Cleaning Up
```bash
python dev.py -c  # Removes auto-generated files
```

## Testing Matrix

The project tests across multiple Python and Django versions:
- **Python**: 3.8, 3.9, 3.10
- **Django**: 2.2, 3.0, 3.1, 3.2, 4.0, 4.1

Tests run via GitHub Actions (`.github/workflows/run-tests.yml`) and Travis CI (`.travis.yml`).

## Key Settings (markdownx/settings.py)

All settings are prefixed with `MARKDOWNX_`:
- `MARKDOWNX_MARKDOWNIFY_FUNCTION` - Markdown to HTML converter function
- `MARKDOWNX_URLS_PATH` - Endpoint for markdownify (default: `/markdownx/markdownify/`)
- `MARKDOWNX_UPLOAD_URLS_PATH` - Endpoint for image uploads (default: `/markdownx/upload/`)
- `MARKDOWNX_MEDIA_PATH` - Upload directory (default: `markdownx/`)
- `MARKDOWNX_UPLOAD_MAX_SIZE` - Max file size (default: 50MB)
- `MARKDOWNX_UPLOAD_CONTENT_TYPES` - Allowed formats (JPEG, PNG, SVG)
- `MARKDOWNX_IMAGE_MAX_SIZE` - Image dimensions and quality
- `MARKDOWNX_SVG_JAVASCRIPT_PROTECTION` - Security feature for SVG files
- `MARKDOWNX_EDITOR_RESIZABLE` - Editor resize option
- `MARKDOWNX_MARKDOWN_EXTENSIONS` - Markdown extensions list
- `MARKDOWNX_SERVER_CALL_LATENCY` - AJAX request delay in ms

## Development Workflow Notes

1. **Container Support**: Vagrant and Docker environments are Unix-only (Linux/macOS). Windows development not supported through `dev.py`.
2. **Auto-refresh**: Changes in containers auto-reload without restart.
3. **Cleanup Required**: Always run `python dev.py -c` before committing changes to save/clean auto-generated files.
4. **TypeScript Compilation**: Frontend source in `static-src/` compiles to `static/` for production.
5. **Test Images**: Tests use `markdownx/tests/static/django-markdownx-preview.png`.
6. **Security**: SVG files are scanned for JavaScript and rejected if malicious code detected.
7. **Image Processing**: Non-SVG images are processed with PIL (Pillow) for compression and resizing.

## Dependencies

Runtime dependencies (`requirements.txt`):
- Django
- Pillow
- Markdown

Documentation dependencies:
- mkdocs
- pymdown-extensions

See `setup.py` for complete package metadata and classifiers.