# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Gradio is an open-source Python package that allows you to quickly build and share machine learning web apps, APIs, or any Python function. It consists of:

- **Python backend** (`/gradio`): Core library providing `Interface`, `Blocks`, `ChatInterface` classes and 40+ components
- **JavaScript/TypeScript frontend** (`/js`): Svelte-based UI components (78 packages in monorepo)
- **Client libraries** (`/client`): Python and JS clients for querying Gradio apps programmatically
- **Demo applications** (`/demo`): 200+ example applications showcasing various features

## Development Prerequisites

- **Python 3.10+** (tested up to 3.13)
- **Node.js 24.0+**
- **pnpm 10.x** (use exact version from package.json)

## Common Development Commands

### Backend (Python)

```bash
# Install Gradio in editable mode
pip install -e .

# Run tests (pytest)
bash scripts/run_backend_tests.sh

# Format code
bash scripts/format_backend.sh

# Run a specific test
pytest test/test_blocks.py::test_blocks_in_event_driven_interface -xvs

# Start app in reload mode (auto-reloads on file changes)
gradio app.py
python app.py  # without auto-reload

# Run specific demo
gradio demo/chatbot_simple/run.py
```

### Frontend (JavaScript/TypeScript)

```bash
# Install dependencies
pnpm i

# Development server
pnpm dev  # starts frontend on port 9876 (requires backend running on 7860)

# Build frontend
pnpm build

# Format code
pnpm format:write

# Type checking
pnpm ts:check

# Linting
pnpm lint

# Run unit tests
pnpm test

# Run unit tests (non-watch mode)
pnpm test:run

# Run browser tests
pnpm test:browser

# Run browser tests with UI mode
pnpm test:browser --ui

# Run browser tests (full build + test)
pnpm test:browser:full

# Storybook for component development
pnpm storybook  # http://localhost:6006
```

### Setup Scripts

```bash
# Full setup (installs Python deps, builds frontend, sets up test env)
bash scripts/install_gradio.sh

# Frontend only
bash scripts/run_frontend.sh

# Test requirements
bash scripts/install_test_requirements.sh
```

## Architecture Overview

### Python Backend (`/gradio/`)

**Core Classes:**
- `Interface` (`interface.py`): High-level API for ML demos (input → function → output)
- `Blocks` (`blocks.py`): Low-level layout system for custom UIs with event-driven programming
- `ChatInterface` (`chat_interface.py`): Specialized for chatbot UIs

**Key Modules:**
- `components/`: All 40+ Gradio components (Audio, Image, Textbox, etc.)
- `events.py`: Event system and decorators (`@on`, `api`)
- `routes.py`: FastAPI routes for the web server
- `cli/`: Command-line interface commands
- `data_classes.py`: Pydantic models for API communication

**Component Structure:**
Each component follows a Python ↔ JavaScript pairing:
- Python: `gradio/components/<component_name>.py`
- JavaScript: `js/<component_name>/` (Svelte components)

### Frontend (`/js/`)

**Monorepo Structure:**
- 78 npm packages under `@gradio/*` and `@self/*` scopes
- Main app: `@self/app` (Vite + Svelte + Tailwind)
- Component packages: `@gradio/button`, `@gradio/image`, etc.
- Build toolchain: Vite, Svelte, TypeScript, Tailwind CSS, Storybook

**Key Directories:**
- `atoms/`: Low-level UI primitives
- `app/`: Main Svelte application
- `_website/`: Documentation site (gradio.app)
- Component directories: Individual packages for each Gradio component

### Client Libraries (`/client/`)

- **Python client** (`client/python/`): Query Gradio apps programmatically
- **JavaScript client** (`client/js/`): Browser/client-side library for Gradio apps

## Key Files

- `pyproject.toml`: Python build config (Ruff linting, pytest, Hatch build)
- `package.json`: Node.js scripts and dependencies
- `CONTRIBUTING.md`: Detailed contribution guidelines
- `README.md`: Project overview and quickstart
- `gradio/__init__.py`: Main exports and API surface
- `test/`: Python test suite (472 test files)
- `demo/`: Example applications (200+ demos)

## Testing Strategy

**Python Tests (`/test/`:**
- Unit tests with pytest
- Integration tests with real Gradio apps
- Run: `bash scripts/run_backend_tests.sh` or `pytest test/`

**JavaScript Tests:**
- Unit tests: Vitest (`.test.ts` files)
- Browser tests: Playwright (`*spec.ts` files in `js/spa/test/`)
- Component tests: Storybook interactions

**Single Test Execution:**
```bash
# Python
pytest test/test_blocks.py::test_specific_function -xvs

# JavaScript unit
pnpm test -- ComponentName.test.ts

# JavaScript browser
pnpm test:browser -- test.spec.ts
```

## Build System

**Python:** Hatchling (PEP 517 build backend)
- Version from: `gradio/package.json`
- Artifacts: Frontend code, templates, Python stubs
- Linting: Ruff (see `tool.ruff` in pyproject.toml)

**JavaScript:** Vite + pnpm workspaces
- Monorepo with 78 packages
- CSS generation: `pnpm css` (Tailwind + custom theme)
- TypeScript: Strict checking, Svelte integration

## Important Patterns

### Adding a New Component

1. Create Python class in `gradio/components/<name>.py`
2. Create Svelte component in `js/<name>/`
3. Export in `gradio/__init__.py`
4. Add demo in `demo/<name>_component/`
5. Write tests in `/test/`
6. Add Storybook story in `js/<name>/*.stories.svelte`

### Event Handling

- Use `@on` decorator for component events: `@on.click`, `@on.upload`, etc.
- `api` decorator exposes functions as REST endpoints
- Event data classes in `events.py` (e.g., `SelectData`, `UploadData`)

### Component Props

- Python and JS props are synchronized via `ComponentMeta`
- Type validation on both client and server
- Use `gradio/component_meta.py` for property definitions

## Hot Reload Development

```bash
# Terminal 1: Backend in reload mode
gradio app.py  # watches /gradio for changes

# Terminal 2: Frontend development
pnpm dev  # watches /js for changes

# Access: http://localhost:7860 (auto-reloads on changes)
```

## CI/CD

**Python Tests:** GitHub Actions (`.github/workflows/test-python.yml`)
- Pytest on Python 3.10-3.13
- Type checking with ty

**JavaScript Tests:** GitHub Actions (`.github/workflows/tests-js.yml`)
- Unit tests (Vitest)
- Browser tests (Playwright)
- Type checking (tsc)
- Formatting (Prettier)

**Main Branch Protection:**
- Require PR reviews from maintainers
- All CI checks must pass
- No direct commits to main

## Version Management

- **Python:** Version synced from `gradio/package.json` via Hatch
- **Frontend:** Built and embedded in Python package
- **Releases:** Changeset workflow (`pnpm ci:version`, `pnpm ci:publish`)

## Troubleshooting

**Frontend Build Failures:**
```bash
rm -rf node_modules pnpm-lock.yaml
bash scripts/install_gradio.sh
bash scripts/build_frontend.sh
```

**Memory Errors:**
```bash
NODE_OPTIONS='--max-old-space-size=8192' pnpm build
```

**Import Errors:**
```bash
export PYTHONPATH="./"  # ensure local gradio is used
pip install -e .  # editable install
```

**Version Mismatches:**
```bash
pip uninstall gradio -y
pip install -e .
```

## Documentation

**API Docs:** Auto-generated from docstrings using mdsvex templates (`js/_website/src/lib/templates/gradio/`)

**Guides:** Markdown files in `/guides/` directory

**Component Docs:** Edit docstrings in `gradio/components/<name>.py` → reflected in website

**View Local Docs:**
```bash
pip install -e .  # editable install
cd js/_website
pnpm dev  # http://localhost:5173
```

## Key Maintainers

- @abidlabs, @aliabid94, @aliabd, @AK391, @dawoodkhan82, @pngwn, @freddyaboulton, @hannahblair, @hysts, @whitphx

## Getting Help

- **Issues:** GitHub Issues with "good first issue" label
- **Discord:** [gradio Discord](https://discord.com/invite/feTf9x3ZSB)
- **Website:** https://gradio.app
- **Docs:** https://gradio.app/docs