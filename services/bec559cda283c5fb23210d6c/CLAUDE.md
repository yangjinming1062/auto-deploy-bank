# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commonly Used Commands

### Running Tests
To run the test suite, execute the following command:

```bash
python runtests.py
```

### Installing Dependencies
The project has different dependencies for the core library, the tests, and the example projects.

**Core library:**
The core library has no external dependencies.

**Tests:**
To install the dependencies for running the tests, use the following command:
```bash
pip install -r requirements_test.txt
```

**Example project:**
To install the dependencies for the example project, use the following command:
```bash
pip install -r example/requirements.txt
```

**Minimal example project:**
To install the dependencies for the minimal example project, use the following command:
```bash
pip install -r example_minimal/requirements.txt
```

## High-level Code Architecture and Structure
This project is a Django app that provides advanced integration with the jQuery DataTables.net library, allowing for server-side processing of tables.

The core of the project is the `ajax_datatable.views.AjaxDatatableView` class. This class is intended to be subclassed to create views that render and respond to Ajax requests from DataTables.net.

The project includes two example projects:
- `example`: A more realistic example that uses Bootstrap 4.
- `example_minimal`: A minimal working example.

The main application logic is contained within the `ajax_datatable` directory. This includes the `views.py`, `columns.py`, and `filters.py` files, which handle the server-side logic for the DataTables.

The `ajax_datatable/templates` directory contains the Django templates used to render the tables and their components.

The `ajax_datatable/static` directory contains the necessary static assets (CSS, JavaScript, images) for the DataTables integration.
