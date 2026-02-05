# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TAICHI-flet is a Windows desktop application built with the Flet framework. It provides a multi-functional entertainment interface with features including image browsing, music listening, novel reading, resource searching, and AI chat capabilities.

## Commands

### Running the Application
```bash
python ui.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

The app uses `flet.app(target=main, assets_dir="assets")` as its entry point.

## Architecture

### Core Entry Point (`ui.py`)
- `main()` function is the Flet app entry point
- `NavigationBar` class manages tab-based navigation using `flet.Tabs`
- Views are dynamically loaded using `import_module` based on entries in `navigation_tabs` (defined in `settings.py`)

### View Pattern (`views/`)
Each tab view follows a consistent pattern:
- Module exports a `ViewPage` class that extends `flet.Stack`
- Constructor accepts `page: Page` parameter
- Optional `init_event()` method is called when the tab is activated (hooked in `NavigationBar.tab_init_event`)
- Dynamic loading: `import_module("views." + module_name)` instantiates `ViewPage(page)`

**Key views:**
- `main.py` - Home page with theme switching and animated backgrounds
- `mountain.py` - Image browsing (观山)
- `rain.py` - Music player (听雨)
- `immortality.py` - Novel reading (修仙)
- `lyra.py` - Resource searching (抚琴)
- `buddhist.py` - Media/resources (藏经阁)
- `treasure.py` - Tools dialogs launcher (百宝囊)
- `treasure_dialogs/` - Subpackage containing tool dialog modules (pdf2word, checkcovareas, etc.)

### Data Fetching Layer (`methods/`)
Contains scrapers and API clients for fetching content from various websites. Uses `requests_html` with xpath selectors.

**Pattern:** Classes inherit from `_Base` and implement `image_url_generator()` as an infinite yield-based generator using class-level state (`page_num`, `page_list`):
```python
class SomeAPI(_Base):
    base_url = "..."
    max_page = N
    page_list = []  # Class variable for caching

    @classmethod
    def _get_image_url(cls, detail_url):
        # Yield individual image URLs

    @classmethod
    def _get_page_list(cls, page_num: int):
        # Return list of detail page URLs
```

### Utilities (`utils.py`)
- `CORSImage` - Image class that wraps URLs through a CORS proxy (`https://pc-cors.elitb.com/proxy?url=`)
- `HTMLSession` - Custom `requests_html.HTMLSession` subclass with xpath support
- `one_shot_thread()` / `cycle_thread()` - Threading helpers for async operations
- `snack_bar()` - Show toast notifications via `page.snack_bar`
- `download_named_image()` - Downloads images to `~/Pictures/taichi`

### Configuration Files
- `settings.py` - `navigation_tabs` list of `[icon, name, module_name]` tuples defining available tabs
- `statics.py` - Shared static Image components (TAICHI, BIG_TAICHI, CLOUD, GONGZHONGHAO)

## Key Implementation Notes

- Views use `flet.Stack` as the base container for layering controls
- The app uses Chinese UI text throughout
- Theme switching via `page.theme_mode` stored in `page.client_storage`
- Navigation icons are from `flet.icons`
- Assets are in the `assets/` directory