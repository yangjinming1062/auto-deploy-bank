# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is GPT4Free (g4f), a Python 3.10+ library providing unified access to 108+ AI providers for text generation, image generation, audio processing, and video generation. The project includes:
- Python client library with sync/async support
- FastAPI-based OpenAI-compatible REST API (Interference API)
- Web GUI for interactive use
- CLI tools
- MCP (Model Context Protocol) server
- Docker support

## Development Commands

### Installation
```bash
# Clone repository
git clone https://github.com/xtekky/gpt4free.git && cd g4f

# Install minimal dependencies (30-60 seconds, NEVER cancel)
pip install -r requirements-min.txt

# Install full dependencies (2-5 minutes, NEVER cancel)
pip install -r requirements.txt

# Remove nodriver (CI requirement)
pip uninstall -y nodriver

# Install in editable mode (30 seconds, NEVER cancel)
pip install -e .
```

**Critical**: Always use long timeouts for package installations. Minimal: 120s+, Full: 600s+

### Testing
```bash
# Run unit tests (3-5 seconds, NEVER cancel)
python -m etc.unittest

# Time the tests for performance tracking
time python -m etc.unittest

# Run individual integration tests (may have outdated references)
python etc/testing/test_chat_completion.py
python etc/testing/test_async.py
python etc/testing/test_api.py
```

Expected: ~41 tests, 1-2 failures expected (network isolation), 5-8 skipped tests

### Running the Application
```bash
# CLI help
g4f --help

# Interactive client
g4f client "Hello world"

# Start API server with web GUI
python -m g4f --port 8080
# Access: http://localhost:8080/chat/

# API server only (no GUI)
python -m g4f.cli api --port 8080

# MCP server (stdio mode)
g4f mcp
# or
python -m g4f.mcp

# MCP server (HTTP mode)
g4f mcp --http --port 8765
```

### Python Client Usage
```python
# Basic usage
from g4f.client import Client
client = Client()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)

# Async usage
from g4f.client import AsyncClient
import asyncio
async def main():
    client = AsyncClient()
    response = await client.chat.completions.create(...)
    print(response.choices[0].message.content)
asyncio.run(main())

# Image generation
response = client.images.generate(
    model="flux",
    prompt="a white siamese cat",
    response_format="url"
)
```

## Project Architecture

### Core Components

#### 1. Provider System (`g4f/Provider/`)
- 128+ provider implementations across 5 categories
- **No Auth Required**: Cloudflare, Copilot, Perplexity, PollinationsAI, etc.
- **Needs Auth**: OpenAI, Gemini, Anthropic, Azure, etc.
- **Audio**: Audio generation providers
- **Local**: Local inference backends
- Each provider implements a standard interface with `create()` and `create_async()` methods

#### 2. Client Layer (`g4f/client/`)
- OpenAI-compatible client interface
- Sync and async implementations
- Streaming support
- Tool calling capability
- Media handling (images, audio, video)
- Response standardization across providers

#### 3. API Server (`g4f/api/`)
- FastAPI-based REST API
- OpenAI-compatible endpoints (`/v1/chat/completions`, etc.)
- WebSocket support for streaming
- CORS enabled for browser usage
- Swagger UI at `/docs`

#### 4. GUI (`g4f/gui/`)
- Flask-based web interface
- Chat UI at `/chat/`
- Real-time streaming responses
- Model selection interface
- WebSocket backend API

#### 5. CLI (`g4f/cli/`)
- Main entry point: `g4f` command
- Interactive client mode
- Provider testing
- Server management

### Key Directories

```
g4f/
├── Provider/          # 128+ provider implementations
├── api/              # FastAPI server
├── client/           # Python client library
├── gui/              # Web GUI (Flask)
├── cli/              # Command-line interface
├── mcp/              # MCP server implementation
├── tools/            # Utility tools
├── models.py         # Model registry and definitions
├── typing.py         # Type definitions
├── errors.py         # Exception classes
└── cookies.py        # Cookie management

etc/
├── unittest/         # Unit tests (run via python -m etc.unittest)
├── testing/          # Integration tests
└── examples/         # Usage examples

scripts/
├── build-deb.sh      # Build Debian package
├── build-nuitka.sh   # Build with Nuitka
└── validate-nuitka.sh # Validate builds
```

## Important Implementation Details

### Model Provider Resolution
- Models are mapped to providers in `g4f/models.py:100+`
- Each model has a `best_provider` field specifying which provider(s) to use
- Automatic provider fallback via `AnyProvider` and `IterListProvider`
- Model aliases supported via `ModelRegistry`

### Provider Categories
1. **Base Providers** (`g4f/Provider/base_provider.py`): Abstract base class
2. **Retry Providers** (`g4f/providers/retry_provider.py`): Automatic retry logic
3. **Any Provider** (`g4f/providers/any_provider.py`): Tries multiple providers until one succeeds
4. **Iter List Provider** (`g4f/providers/IterListProvider`): Cycles through provider list

### Response Standardization
- All provider responses converted to standard format
- `g4f/providers/response.py`: Response type definitions
- Supports: text, streaming chunks, media (images/audio/video), tool calls, reasoning

### Testing Strategy
- **Unit Tests** (`etc/unittest/`): Core functionality, provider basics
- **Integration Tests** (`etc/testing/`): Full workflows, may be outdated
- Network-dependent tests expected to fail in CI/isolated environments
- Always run `python -m etc.unittest` after changes

### Dependencies
Core (`requirements-min.txt`): requests, aiohttp, pycryptodome, nest_asyncio, brotli

Extra groups (`requirements.txt` or `setup.py` extras):
- `all`: Full installation with all features
- `slim`: Reduced size, auto-updates on startup
- `gui`: Flask components
- `api`: FastAPI server
- `image`: Pillow, cairosvg for image processing
- `search`: Web search capabilities
- `local`: Local inference (gpt4all)
- `files`: File processing utilities

## Critical Development Guidelines

### Before Making Changes
1. Run unit tests: `python -m etc.unittest`
2. Test import: `python -c "import g4f; print('OK')"`
3. Verify CLI works: `g4f --help`
4. For provider changes, test client creation and basic completions

### Timeouts (CRITICAL)
- `pip install -r requirements-min.txt`: 120+ seconds
- `pip install -r requirements.txt`: 600+ seconds
- `pip install -e .`: 120+ seconds
- `python -m etc.unittest`: 30+ seconds
- **NEVER CANCEL** long-running operations

### Known Issues
- `pydub` shows ffmpeg warning - harmless, expected
- Network timeouts expected for providers in isolated environments
- Some providers may fail - this is normal
- `nodriver` must be removed for CI: `pip uninstall -y nodriver`

## Entry Points
- **CLI Binary**: `g4f` (setuptools entry point)
- **Module**: `python -m g4f`
- **API Server**: `python -m g4f --port 8080`
- **Python Import**: `from g4f.client import Client`

## Docker Usage

### Full Image
```bash
docker run -p 8080:8080 -p 7900:7900 \
  --shm-size="2g" \
  -v ${PWD}/har_and_cookies:/app/har_and_cookies \
  -v ${PWD}/generated_media:/app/generated_media \
  hlohaus789/g4f:latest
```

### Slim Image
```bash
docker run -p 1337:8080 -p 8080:8080 \
  -v ${PWD}/har_and_cookies:/app/har_and_cookies \
  -v ${PWD}/generated_media:/app/generated_media \
  hlohaus789/g4f:latest-slim
```

## Validation Checklist

After changes, verify:
- [ ] `python -m etc.unittest` passes (or expected failures only)
- [ ] `python -c "from g4f.client import Client; print('OK')"` works
- [ ] `g4f --help` works without errors
- [ ] API server starts: `python -m g4f --port 8080` → `curl -I http://localhost:8080` returns 200
- [ ] No import errors or dependency conflicts
- [ ] Backwards compatible with Python 3.10+

## Additional Resources
- Documentation: https://g4f.dev/docs
- Client API: https://g4f.dev/docs/client
- Provider docs: https://g4f.dev/docs/providers-and-models
- GitHub: https://github.com/xtekky/gpt4free