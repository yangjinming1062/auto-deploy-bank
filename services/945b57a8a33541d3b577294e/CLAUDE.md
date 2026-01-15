# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Linguflex is a modular voice AI assistant framework with real-time speech-to-text, text-to-speech, and LLM integration. The system uses an event-driven architecture where modules communicate via a central event system.

## Common Commands

**Run the application:**
```bash
python -m lingu.core.run
# or
run.bat
```

**Run tests:**
```bash
python -m lingu.core.run --test
# or any flag: --runtests, --tests, --test
```

**Windows installation:**
```bash
_install_win.bat
```

**Linux/macOS installation:**
```bash
pip install -r requirements.txt
pip install torch==2.1.2+cu118 torchaudio==2.1.2+cu118 --index-url https://download.pytorch.org/whl/cu118
pip install deepspeed llama-cpp-python
python download_models.py
```

## Architecture

### Directory Structure
- `lingu/core/` - Framework base classes and core functionality
- `lingu/modules/` - Loadable modules (each subfolder is a module)
- `lingu/ui/` - UI components and widgets
- `lingu/config/` - Configuration management
- `lingu/rvc/` - Realtime Voice Conversion processing
- `lingu/settings.yaml` - Main configuration file

### Core Base Classes

| Class | Purpose |
|-------|---------|
| `Logic` | Business logic for modules; provides `inference()`, `trigger()`, event system access |
| `State` | Persistable module state (JSON serialization); stores UI symbols, active state |
| `Populatable` | Pydantic BaseModel for AI-populated data; fields populated by LLM before `on_populated()` |
| `Invokable` | Wraps functions to generate OpenAI function schemas for LLM tool calling |
| `UI` | PyQt6-based module settings interface |
| `Test` | Base class for module tests with helper methods (`user()`, `trigger()`) |

### Module Structure

Each module is a folder in `lingu/modules/` containing:

```
module_name/
├── inference.py       # Populatable classes (LLM-called functions)
├── inference.{lang}.json  # Keywords, prompts per language (en, de, etc.)
├── logic.py           # Logic class (module business logic)
├── state.py           # State class (module state)
├── ui.py              # UI class (PyQt6 settings dialog)
├── handlers/          # Business logic independent of Linguflex
└── test.py            # Optional Test class for module testing
```

**Module loading order (defined in `modules.py`):**
1. `state.py`, `logic.py`, `test.py` (start modules)
2. `inference.py`, `ui.py` (delayed modules)

### Configuration

Settings are loaded from `lingu/settings.yaml` using `cfg(key1, key2, default=...)`. Environment variables can override settings via `env_key` parameter.

Example:
```python
from lingu import cfg
model = cfg("local_llm", "model_name", default="llama3.1:8b")
```

### Event System

Modules communicate via `events.trigger(event_name, module_name, data)` and `events.add_listener(event_name, module_name, callback)`.

Key events:
- `user_text`, `user_text_complete` - Speech input
- `assistant_text`, `assistant_text_complete` - AI responses
- `module_state_active`, `module_state_inactive` - Module state changes
- `escape_key_pressed`, `volume_interrupt` - User interruptions

### Creating a New Module

1. Create folder in `lingu/modules/`
2. Create `state.py` - extend `State` class
3. Create `logic.py` - extend `Logic` class, create singleton `logic = ClassName()`
4. Create `inference.py` - extend `Populatable` for AI-called functions
5. Create `inference.{lang}.json` - define keywords that trigger each function
6. Create `ui.py` - extend `UI` for settings dialog (optional)
7. Add module name to `modules:` list in `settings.yaml`

### Key Imports

```python
from lingu import cfg, log, notify, events
from lingu import Logic, State, Populatable, Invokable, UI, Test
from lingu import repeat, import_repeat_functions
```