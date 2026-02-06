# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ImagePy is an open-source, Python-based image processing framework with a wxPython GUI. It functions similarly to ImageJ, supporting plugin-based extensions and integration with scientific computing libraries (scipy.ndimage, scikit-image, OpenCV, SimpleITK, Mayavi, etc.).

## Installation

```bash
# Using pip
pip install -e .

# Using conda
conda env create -f environment.yml
conda activate imagepy

# Run the application
python -m imagepy
```

Note: On Linux/Mac, wxpython may require downloading a wheel from https://wxpython.org/pages/downloads/. On Linux, ImagePy may need sudo or `--user` flag due to config file permissions.

## Architecture

### Three Core Packages

1. **sciapp** - Backend framework defining data structures and the App container
   - `sciapp.app.App` - Base application class with managers for images, tables, meshes
   - `sciapp.manager.Manager` - Generic key-value-tag container for managing app resources
   - `sciapp.object` - Data structures: Image (numpy-based), Table (pandas-based), Shape, Surface, ROI

2. **sciwx** - GUI widget library (canvas, grid, mesh, plot, widgets)
   - Used by imagepy.app for the UI components

3. **imagepy** - The main application and plugins
   - `imagepy.app.startup` - Application initialization, plugin/tool/widget loading
   - `imagepy.app.imagepy.ImagePy` - Main frame class combining sciwx widgets
   - `imagepy.menus/` - Menu structure with plugin files (`*_plg.py`)
   - `imagepy.tools/` - Interactive tools (Draw, Measure, Transform, etc.)
   - `imagepy.ipyalg/` - Built-in algorithms (hydrology, transform, classify, graph)

### Plugin System

Plugins inherit from sciapp.action classes and are placed in `imagepy/menus/`:

- **Filter** - Image filtering with type checking, ROI support, stack handling, preview, undo
- **Simple** - General image operations (no in-place modification requirement)
- **Table** - Table operations using pandas DataFrame
- **Free** - Standalone actions (open/save/exit)
- **Tool** - Mouse-interactive tools (drawing, measurement)
- **Widget** - Panel widgets (macro recorder, navigator, histogram)

#### Plugin Structure Example

```python
from sciapp.action import Simple

class MyPlugin(Simple):
    title = 'My Plugin'
    note = ['all', 'preview']  # 'all' = all types, 'preview' = supports preview
    para = {'param1': value}
    view = [(type, 'param1', ...)]

    def run(self, ips, imgs, para=None):
        # ips: ImagePlus wrapper with img, lut, roi, etc.
        # imgs: list of images (stack or single)
        # modify ips.img directly or return new image
        pass
```

**Note keywords**: `all`, `8-bit`, `16-bit`, `rgb`, `float`, `int`, `not_slice`, `req_roi`, `auto_snap`, `auto_msk`, `preview`, `2int`, `2float`

### Key Classes

- `sciapp.object.Image` - Numpy array wrapper with lut, range, roi, title properties
- `sciapp.object.Table` - Pandas DataFrame wrapper with row/col masks
- `sciapp.object.Shape` - Vector data (points, lines, polygons) with coordinate system
- `sciapp.object.Surface` - 3D surface data

### Entry Point

The application starts via `imagepy:show` (console script) which calls `imagepy.app.startup.start()`, loading:
1. Plugins from `imagepy/menus/`
2. Tools from `imagepy/tools/`
3. Widgets from `imagepy/widgets/`
4. Documentation from `imagepy/doc/`
5. Language dictionaries from `imagepy/lang/`

Then creates either `ImagePy` (default) or `ImageJ` style frame based on config.

## Development Notes

- Plugins are auto-discovered by directory structure under `menus/`
- File naming: `*_plg.py` for plugins, `*.md` for documentation
- Menu hierarchy mirrors directory structure
- Plugin `title` attribute determines menu placement and macro recording