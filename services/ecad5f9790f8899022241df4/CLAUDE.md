# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MarkItDown is a Python utility for converting various document formats (PDF, Word, Excel, PowerPoint, images, audio, HTML, etc.) to Markdown. The primary package is in `packages/markitdown/`, with related packages in `packages/markitdown-mcp/` (MCP server) and `packages/markitdown-sample-plugin/` (example plugin).

The project uses a plugin-based architecture where each file format is handled by a separate `DocumentConverter` class registered with the `MarkItDown` orchestrator.

## Build and Test Commands

```bash
# Install the package with all optional dependencies
cd packages/markitdown
pip install -e '.[all]'

# Enter hatch environment (installs dependencies from pyproject.toml)
cd packages/markitdown && hatch shell

# Run all tests
hatch test

# Run a single test file
hatch test tests/test_module_vectors.py

# Run a specific test function
hatch test -k "test_excel_vectors"

# Run tests with coverage
hatch test --cov

# Type checking
hatch run types:check

# Pre-commit checks (Black formatting)
pre-commit run --all-files
```

## Architecture

### Core Components (`packages/markitdown/src/markitdown/`)

**MarkItDown class** (`_markitdown.py`):
- Main entry point for conversions
- Manages converter registration and prioritization
- Handles multiple input sources: local paths, URLs, file streams, HTTP responses, data URIs
- Uses `StreamInfo` to track file metadata (mimetype, extension, charset, filename, url)
- Utilizes `magika` library for file type detection
- Supports plugins via entry points (`markitdown.plugin` group)

**DocumentConverter** (`_base_converter.py`):
- Abstract base class for all converters
- Interface: `accepts(file_stream, stream_info, **kwargs) -> bool` and `convert(...) -> DocumentConverterResult`
- `DocumentConverterResult` contains `markdown` (required) and `title` (optional)

**Converters** (`converters/` directory):
- Each file format has its own converter class inheriting from `DocumentConverter`
- Converter priorities: lower values are tried first
  - `PRIORITY_SPECIFIC_FILE_FORMAT = 0.0` - specific format converters
  - `PRIORITY_GENERIC_FILE_FORMAT = 10.0` - generic converters (text, HTML, ZIP)

| Converter | Priority | Formats |
|-----------|----------|---------|
| PlainTextConverter | 10.0 | text/* |
| ZipConverter | 10.0 | application/zip (recursive) |
| HtmlConverter | 10.0 | text/html |
| Others (Pdf, Docx, etc.) | 0.0 | Format-specific |

**Plugin System**:
- Plugins are discovered via Python entry points: `project.entry-points."markitdown.plugin"`
- Plugins implement a `register_converters(markitdown_instance, **kwargs)` function
- See `packages/markitdown-sample-plugin` for reference implementation

### Conversion Flow

1. `MarkItDown.convert(source)` accepts: file path, URL, `requests.Response`, or binary stream
2. `StreamInfo` is built from source metadata (extension, mimetype, URL, etc.)
3. `_get_stream_info_guesses()` uses `magika` to detect file type from content, producing multiple guesses
4. For each guess, `_convert()` iterates registered converters in priority order (sorted stable)
5. Converter's `accepts(file_stream, stream_info)` returns True if it can handle the format
6. First converter that accepts and successfully converts wins
7. If all converters fail, `FileConversionException` is raised with details

### Key Conventions

- **Stream preservation**: Converters must not change stream position during `accepts()`; `_convert()` resets position after each check
- **Binary streams only**: `convert_stream()` requires binary file-like objects (not `io.StringIO`)
- **Lazy imports**: Dependencies are imported at module level to support optional dependency groups
- Use `MissingDependencyException` when optional dependencies are missing
- Results are normalized (trailing whitespace stripped, multiple newlines collapsed)
- **Nested conversions**: Converters can use `_parent_converters` kwarg to recursively process embedded files (e.g., images in PDFs, files in ZIPs)

### CLI Usage

```bash
# Basic conversion
markitdown document.pdf -o output.md

# Pipe content
cat document.pdf | markitdown

# List available plugins
markitdown --list-plugins

# Enable plugins for conversion
markitdown --use-plugins document.rtf -o output.md
```

### Optional Dependency Groups

- `[pdf]` - PDF processing
- `[docx]` - Word documents
- `[pptx]` - PowerPoint
- `[xlsx]`/`[xls]` - Excel files
- `[audio-transcription]` - Speech recognition
- `[youtube-transcription]` - YouTube transcripts
- `[az-doc-intel]` - Azure Document Intelligence
- `[all]` - All optional dependencies