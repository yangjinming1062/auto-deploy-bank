# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Lackey is a Python implementation of Sikuli script - a GUI automation library that uses image recognition to control applications. It allows running automation scripts developed in the Sikuli editor with pure Python.

## Commands

### Development Setup
```bash
pip install -e ./   # Install in development mode with symlink
```

### Building
```bash
python setup.py bdist_wheel    # Build wheel package
python setup.py sdist          # Build source distribution
```

### Testing
```bash
python tests/appveyor_test_cases.py   # Unit tests (mouse, keyboard, screen, pattern methods)
python tests/test_cases.py            # Integration tests (requires Windows/notepad.exe)
python -m pytest tests/               # Alternative pytest runner
```

## Architecture

### Core Module Structure (lackey/)

- **RegionMatching.py**: Central module containing:
  - `Pattern`: Image template with similarity threshold and target offset
  - `Region`: Base class for screen regions with find(), click(), type() methods
  - `Screen`: Inherits Region; represents a display monitor
  - `Match`: Result of a successful find operation
  - `ObserveEvent`: Event for onAppear/onVanish observers
  - `PlatformManager`: Singleton handling OS-specific operations

- **PlatformManager{Windows,Darwin}.py**: OS-specific implementations of:
  - Screen capture
  - Mouse/keyboard emulation
  - Window management
  - Active window detection

- **InputEmulation.py**: Mouse and Keyboard classes for user input

- **Geometry.py**: Location class for coordinate handling

- **TemplateMatchers.py**: PyramidTemplateMatcher for efficient image search

- **Ocr.py**: TextOCR class wrapping pytesseract

- **SettingsDebug.py**: Settings and Debug configuration classes

- **App.py**: Application focus/open/close management

- **KeyCodes.py**: Key, Button, KeyModifier enums

- **Exceptions.py**: FindFailed, ImageMissing exceptions

- **SikuliGui.py**: Popup dialogs (popup, input, select, popFile)

### Image Search Resolution

When a Pattern is created with a filename string, it searches through:
1. `sys.path`
2. `Settings.BundlePath`
3. Current working directory
4. `Settings.ImagePaths` (custom paths added via `addImagePath()`)

### Sikuli Patching

`from lackey import *` exports Screen methods to global namespace, which **overrides Python builtins**:
- `type()` → Sikuli type function (use `type_()` for native Python)
- `input()` → Sikuli input dialog (use `input_()` for native Python)

Alt+Shift+C interrupts running scripts.

## Platform Support

- **Windows**: Full support via PlatformManagerWindows (ctypes-based)
- **macOS**: Full support via PlatformManagerDarwin (pyobjc-based)
- **Linux**: Not currently supported (would need PlatformManagerLinux implementation)