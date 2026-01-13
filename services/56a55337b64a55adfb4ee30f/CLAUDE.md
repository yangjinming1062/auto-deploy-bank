# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **Real Python Materials** repository - a collection of bonus materials, exercises, and example projects for Real Python's [Python tutorials](https://realpython.com). The repository contains 200+ independent Python projects and code samples, each demonstrating different Python concepts, libraries, and frameworks.

Each top-level directory represents a different tutorial or example project with its own structure, dependencies, and README. This is **not** a single cohesive application but rather a educational code library.

## Code Style and Linting

This repository uses **Ruff** for code formatting and linting:

- **Ruff version**: `ruff==0.14.1` (specified in `requirements.txt`)
- **Python version**: Target Python 3.14 (specified in `pyproject.toml`)
- **Line length**: 79 characters
- **Configuration**: See `pyproject.toml` for full Ruff settings

### Common Commands

```bash
# Check code style without making changes
ruff format --check
ruff check

# Automatically fix linting issues and format code
ruff format
ruff check --fix

# Run both checks (as used in CI)
ruff format --check && ruff check
```

### CI/CD

GitHub Actions workflow `.github/workflows/linters.yml` runs:
- Code formatting checks with Ruff
- Directory layout validation with `.github/workflows/dircheck.py`
- Tests against Python 3.14 on Linux

## Working With Individual Projects

Most projects are self-contained with their own:

- `pyproject.toml` or `requirements.txt` for dependencies
- `README.md` with project-specific instructions
- Test files (usually using `pytest` or `unittest`)
- Source code in a package directory

### Typical Project Structure Patterns

**Pattern 1: Step-by-step projects**
```
project-name/
├── source_code_step_1/
├── source_code_step_2/
├── ...
├── source_code_final/
└── README.md
```

**Pattern 2: Advent of Code**
```
advent-of-code/
├── solutions/
│   └── YEAR/
│       └── DAY_description/
│           ├── aocYEARDAY.py
│           ├── test_aocYEARDAY.py
│           └── README.md
├── templates/
│   ├── aoc_template.py
│   ├── test_aoc_template.py
│   └── README.md
├── aoc_grid.py
└── aoc_state_machine.py
```

**Pattern 3: Single example**
```
example-name/
├── source_code/
│   └── package/
│       ├── __init__.py
│       └── module.py
├── tests/
│   └── test_module.py
├── pyproject.toml or requirements.txt
└── README.md
```

### Installing Dependencies

**For projects using Poetry** (have `pyproject.toml` with `[tool.poetry]`):
```bash
cd project-directory
poetry install
poetry run python script.py
# or
poetry shell
python script.py
```

**For projects using pip** (have `requirements.txt`):
```bash
cd project-directory
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python script.py
```

**For standard library only projects** (no dependencies):
```bash
cd project-directory
python script.py
```

### Running Tests

**Using pytest** (most common):
```bash
# Run all tests in a project
pytest

# Run specific test file
pytest tests/test_module.py

# Run with verbose output
pytest -v
```

**Using unittest**:
```bash
# Run all tests
python -m unittest discover

# Run specific test file
python -m unittest tests.test_module
```

## Key Project Categories

The repository contains projects covering:

- **Web Development**: Django, Flask, FastAPI applications
- **Game Development**: Pygame, Arcade library games
- **Data Science**: NumPy, Pandas, Polars examples
- **CLI Tools**: Typer, Click applications
- **Algorithms**: Data structures, coding interview problems
- **Async Programming**: asyncio examples
- **Testing**: Unit testing patterns and examples
- **Python Fundamentals**: Language feature demonstrations

## Important Notes

1. **No global build command**: Each project is independent - there is no single `make build` or root-level test command that applies to all projects.

2. **Project-specific READMEs**: Always check the `README.md` in each project directory for specific setup, installation, and running instructions.

3. **Version requirements**: Some projects may have specific Python version requirements (check `pyproject.toml` or `requirements.txt`).

4. **Dependencies**: External dependencies vary by project. Some use only the standard library, others require specific packages installed via pip/poetry.

5. **Test patterns**: Most testable projects follow the `tests/` directory structure with `test_*.py` files using pytest conventions.

6. **Educational context**: These projects are designed for learning - they demonstrate best practices and common patterns used in Python development.

## Development Workflow

When working on a specific project:

1. Navigate to the project directory
2. Check its `README.md` for setup instructions
3. Install dependencies using the project's preferred method (poetry or pip)
4. Run tests using the project's test framework
5. Apply Ruff formatting before committing changes
6. Follow the existing code patterns and structure in that project

## Support

For questions about Real Python materials:
- Join weekly [Office Hours calls](https://realpython.com/office-hours/)
- Ask in the [RP Community Chat](https://realpython.com/community/)
- Do **not** create GitHub issues for 1:1 support