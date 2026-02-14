# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Cascadia Code is a coding font from Microsoft. The project uses UFO (Unified Font Object) format for source fonts and Python (build.py) for font compilation. Font sources are in `sources/` and compiled outputs go to `build/`.

## Build Commands

```bash
# Install dependencies
pip install -r requirements.txt ufolint
brew install ttfautohint  # macOS required for hinting

# Lint source fonts
ufolint sources/*.ufo

# Build variable fonts only (default)
python ./build.py

# Build with all options (static + web fonts)
python ./build.py -S -W

# Build variable fonts with web fonts
python ./build.py -W

# Build minimal variant (skip powerline, nerdfonts, mono, italic)
python ./build.py -P -NF -M -I

# Skip VTT compilation (leave VTT sources in output)
python ./build.py --no-vtt-compile
```

## Font Variants

The build script produces multiple variants based on designspace files:
- **Cascadia Code** / **Cascadia Code Italic** - Standard with ligatures
- **Cascadia Mono** / **Cascadia Mono Italic** - No ligatures
- **Cascadia Code PL** / **Cascadia Code PL Italic** - PowerLine symbols
- **Cascadia Mono PL** / **Cascadia Mono PL Italic** - PowerLine without ligatures
- **Cascadia Code NF** / **Cascadia Code NF Italic** - Nerd Font symbols
- **Cascadia Mono NF** / **Cascadia Mono NF Italic** - Nerd Font without ligatures

Static instances are generated from the variable font masters for each weight (200-700).

## Architecture

### Source Structure
- `sources/CascadiaCode-*.ufo/` - UFO master fonts organized by weight/style
- `sources/CascadiaCode_variable.designspace` - Variable font definition (weight axis 200-700)
- `sources/CascadiaCode_variable_italic.designspace` - Italic variable font definition
- `sources/features/*.fea` - OpenType feature files merged during build
- `sources/nerdfonts/` - Nerd Font glyphs merged into PL/NF variants
- `sources/vtt_data/` - TrueType hinting data merged during compilation
- `sources/stat.yaml` - STAT table configuration for variable font

### Build Pipeline (build.py)
1. **prepare_fonts()** - Loads designspace, merges feature files and Nerd Font glyphs, sets metadata
2. **compile_variable_and_save()** - Generates variable TTF, merges VTT hinting data
3. **compile_static_and_save()** - Generates static TTF/OTF instances
4. **autohint() / ttfautohint()** - Applies PostScript and TrueType hinting to static fonts
5. **to_woff2()** - Compresses TTF to WOFF2 for web use

### Output Structure
```
build/
├── ttf/           # Variable fonts
│   ├── CascadiaCode.ttf
│   ├── CascadiaCodeItalic.ttf
│   └── ...
├── ttf/static/    # Static TTF instances
├── otf/static/    # Static OTF instances
└── woff2/         # Web fonts
```

## Key Design Decisions

- **Weight mapping**: The variable font uses non-linear weight axis mapping (400→500, 700→750) for better visual progression
- **VTT hinting**: TrueType hinting data is merged from separate VTT source files and compiled
- **Feature assembly**: OpenType features are concatenated from multiple `.fea` files based on font variant
- **Overlap removal**: Static fonts use pathops backend for faster overlap removal during compilation