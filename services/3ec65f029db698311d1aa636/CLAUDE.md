# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **Google Research** repository containing 700+ independent machine learning and AI research projects. Each project is a self-contained subdirectory with its own code, documentation, and dependencies.

### Project Structure

Each project directory typically contains:
- `README.md` - Research description, paper citations, and usage instructions
- `requirements.txt` - Python dependencies (present in ~280 projects)
- `setup.py` or `pyproject.toml` - Installation configuration for Python packages
- `run.sh` - Test script (present in ~454 projects, used by CI)
- `examples/` - Jupyter notebooks demonstrating usage
- `data/` - Example datasets or data loaders

### Licensing

- **Source code**: Apache 2.0 License
- **Datasets**: CC BY 4.0 International License

## Common Commands

### Installing a Project

Each project is independent. To work on a specific project:

```bash
# Clone the repository
git clone git@github.com:google-research/google-research.git --depth 1

# Navigate to project
cd google-research/[PROJECT_NAME]

# Install dependencies (varies by project)
pip install -r requirements.txt

# Install in editable mode if project has setup.py
pip install -e .
```

### Running Tests

Projects with CI integration use `run.sh`:

```bash
./run.sh
```

This typically:
1. Creates a virtual environment
2. Installs dependencies from requirements.txt
3. Runs unit tests

To run tests manually:

```bash
python -m pytest [TEST_MODULE]
# or
python [PROJECT_NAME]/[MODULE]_test.py
```

### Installation Patterns

**For packages with setup.py:**
```bash
pip install -e google-research/[PROJECT_NAME]
```

**For JAX-based projects** (like jax_dft):
```bash
# Follow JAX installation guide for GPU support
# https://github.com/jax-ml/jax#pip-installation
pip install -e google-research/jax_dft
```

**For TensorFlow projects:**
```bash
pip install -r requirements.txt  # Use tensorflow-gpu for GPU support
```

## Architecture Patterns

### Project Types

1. **Python Packages** - Have `setup.py` and proper package structure
   - Example: `jax_dft/`, `drjax/`, `bigbench/`

2. **Research Code** - Scripts and notebooks without package structure
   - Example: `abps/`, `activation_clustering/`

3. **Hybrid** - Research code with some packaging
   - Example: `graph_embedding/` (subprojects)

### Framework Distribution

Projects use various frameworks:
- **JAX**: jax_dft, jax_mpc, jaxnerf, jaxsel
- **TensorFlow**: activation_clustering, state_of_sparsity
- **PyTorch**: Fewer projects, check individual READMEs
- **NumPy/SciPy**: Many projects with minimal dependencies

### Testing Strategy

- **454 projects** use CircleCI with `run.sh` scripts
- Tests are typically Python unit tests named `[module]_test.py`
- Some projects use `absl.testing` (Google's testing framework)
- CI tests install dependencies and run basic test suites

### Documentation

- Each project has a dedicated README.md
- README includes paper citations, installation, and usage
- Examples often in Jupyter notebooks
- No centralized documentation - check individual project READMEs

## Development Guidelines

### Working on Projects

1. **Read the README** - Each project's README.md contains specific instructions
2. **Check dependencies** - requirements.txt or setup.py for install requirements
3. **Review run.sh** - Understand the testing workflow
4. **Note framework version** - Some projects specify exact versions (e.g., TensorFlow 2.1.0)

### Adding New Work

Since this is a research repository:
- Each project directory is independent
- Follow the Apache 2.0 license header pattern
- Include a README.md with paper citations
- Add run.sh if implementing tests
- Include requirements.txt for Python dependencies

### Common Patterns

**Virtual environment setup in run.sh:**
```bash
virtualenv -p python3 env
source env/bin/activate
pip install -r [PROJECT_NAME]/requirements.txt
python -m [PROJECT_NAME].[MODULE]_test
```

**Package structure:**
```
[PROJECT_NAME]/
├── [PROJECT_NAME]/
│   ├── __init__.py
│   ├── [module].py
│   └── [module]_test.py
├── README.md
├── requirements.txt
└── setup.py
```

## Examples

### jax_dft (JAX-based package)
```bash
cd jax_dft
pip install -e .
# See examples/ for Jupyter notebooks
```

### state_of_sparsity (TensorFlow research)
```bash
./run.sh  # Automated test
# or
pip install -r requirements.txt
python -m state_of_sparsity.sparse_transformer.models.sparse_transformer_test
```

### activation_clustering (Standalone research)
```bash
pip install -e .
# Run example scripts or notebooks
```

## Key Differences from Standard Projects

1. **No monorepo build system** - Each project is independent
2. **Research code** - Not production-ready, experimental
3. **Varying quality** - Projects released as-is from research papers
4. **Version diversity** - Different projects use different framework versions
5. **Self-contained** - Minimal cross-project dependencies

## Finding Projects

Browse the repository by:
- Subdirectory names (descriptive of research area)
- README.md files in each directory
- requirements.txt for technology stack
- run.sh for test coverage

For example:
- `jax_*` - JAX-based projects
- `*_rl` - Reinforcement learning
- `graph_*` - Graph neural networks
- `transformer`, `bert`, `gpt` - Language models

## Notes

- This is not an official Google product
- Repository large (700+ directories) - use selective cloning
- Each project represents a published research paper
- Code quality varies - research-grade, not production-grade