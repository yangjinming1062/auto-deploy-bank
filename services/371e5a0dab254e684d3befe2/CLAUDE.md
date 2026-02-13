# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Cascadia Code is Microsoft's coding font with support for ligatures, arrows, and stylistic sets. The repository contains the font source files and a Python build system to compile them.

## Build Commands

Install dependencies:
```bash
pip install -r requirements.txt
```

Build variable fonts (default, includes ligatures):
```bash
python build.py
```

Build with all variants:
```bash
python build.py -S -W -I  # Static + web fonts + italic
```

Build options:
- `-P/--no-powerline`: Skip PowerLine variants
- `-NF/--no-nerdfonts`: Skip Nerd Font variants
- `-M/--no-mono`: Skip Mono (no-ligature) variants
- `-S/--static-fonts`: Build static TTF/OTF fonts
- `-I/--no-italic`: Skip italic variants
- `-V/--no-vtt-compile`: Skip VTT hinting compilation
- `-W/--web-fonts`: Generate WOFF2 web fonts

Output goes to `build/{ttf,otf,woff2}/` directories.

## Architecture

**Source Files** (`sources/`):
- `.ufo/` folders: UFO (Unified Font Object) master sources for each weight (ExtraLight, Regular, Bold)
- `CascadiaCode_variable.designspace`: Variable font definition with weight axis
- `CascadiaCode_variable_italic.designspace`: Italic variable font definition
- `features/*.fea`: OpenType feature files (ligatures, stylistic sets, etc.)
- `vtt_data/*.ttf`: VTT (TrueType hinting) source files
- `nerdfonts/`: Nerd Font symbol glyphs for NF variants
- `stat.yaml`: STAT table configuration

**Build Pipeline** (`build.py`):
1. Load designspace files and prepare fonts (merge features, set metadata)
2. Compile variable TTF fonts using ufo2ft
3. Merge VTT hinting data from source TTF files
4. Generate static font instances if `-S` flag
5. Add STAT tables using gftools
6. Autohint OTF (psautohint/cffsubr) and TTF (ttfautohint)
7. Compress to WOFF2 if `-W` flag

**Font Variants**:
- `Cascadia Code`: Standard with ligatures
- `Cascadia Mono`: Without ligatures
- `Cascadia Code PL`: With PowerLine symbols
- `Cascadia Code NF`: With Nerd Font symbols