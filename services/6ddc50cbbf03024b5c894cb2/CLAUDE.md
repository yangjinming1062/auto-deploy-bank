# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **Machine Learning Refined** (2nd edition) educational repository - a comprehensive machine learning textbook with interactive Jupyter notebooks. The pedagogical approach emphasizes intuition, visualization, and implementing ML algorithms from scratch rather than using high-level libraries.

## Architecture

### Directory Structure
- **`notes/`** - Interactive Jupyter notebooks organized by chapter (2-13), covering optimization methods, linear learning, and nonlinear learning
- **`exercises/`** - Exercise wrapper notebooks and datasets for hands-on practice
- **`chapter_pdfs/`** - PDF versions of each textbook chapter (downloadable from Dropbox links in README)
- **`presentations/`** - PowerPoint slides for each chapter (downloadable from Dropbox links in README)

### Technology Stack
- **Python 3.10+** (Anaconda/pip method) or Python 3.8 (Docker)
- **Jupyter Notebooks** - Primary learning interface
- **Core Libraries**: numpy, pandas, matplotlib, scipy, autograd, jax[cpu], notebook
- **Linting**: ruff
- **Docker**: Pre-configured container with all dependencies

### Code Patterns
- All code exists in Jupyter notebooks (no standalone Python modules)
- Algorithms implemented from scratch using fundamental libraries only
- Uses `autograd` for automatic differentiation (see `notes/3_First_order_methods/B_10_Automatic.ipynb`)
- Heavy emphasis on visualization and geometric intuition
- Interactive widgets demonstrate key concepts

## Development Commands

### Running the Notebooks

**Option 1: Docker (Recommended)**
```bash
docker-compose up -d
# Access at http://localhost:8888
```

**Option 2: Anaconda**
```bash
conda create python=3.10 --name mlr2 --file requirements.txt
conda activate mlr2
jupyter notebook --port=8888 --ip=0.0.0.0 --allow-root --NotebookApp.token=''
# Access at http://localhost:8888
```

**Option 3: pip/uv**
```bash
uv venv --python 3.10.0 && source .venv/bin/activate
uv pip install -r requirements.txt
jupyter notebook --port=8888 --ip=0.0.0.0 --allow-root --NotebookApp.token=''
# Access at http://localhost:8888
```

### Linting
The repository uses `ruff` for linting Python code in notebooks:
```bash
ruff check .
ruff format .
```

### Working with Exercises
Exercise datasets are available via Dropbox download link provided in `exercises/README.md`. Download and extract to access exercise data.

## Key Learning Resources

### Core Textbook Content
The repository covers three main parts:
1. **Mathematical Optimization** (Chapters 2-4) - Zero, first, and second-order methods
2. **Linear Learning** (Chapters 5-9) - Regression, classification, unsupervised learning, feature engineering
3. **Nonlinear Learning** (Chapters 10-14) - Feature engineering, neural networks, tree-based methods

### Interactive Notebooks
Each chapter has dedicated notebooks with:
- Geometric visualizations
- Step-by-step algorithm implementations
- Interactive widgets demonstrating concepts
- Exercise sections for practice

### Google Colab Integration
Most notebooks have Colab badges in the main README, allowing direct browser-based execution without local setup.

## Important Notes

- **Python Version**: Use Python 3.10+ for local development. The Docker image uses Python 3.8.
- **No Traditional Tests**: This is an educational repository with notebooks, not a production codebase with unit tests
- **Libraries**: Avoid high-level ML libraries (scikit-learn, TensorFlow, PyTorch) when implementing algorithms from scratch
- **Pedagogy**: Focus on intuition (simple picture) → mathematical derivation → implementation for each concept
- **Data**: Exercise datasets are external (Dropbox links), not included in the repository
- **External Resources**: Chapter PDFs and presentation slides are hosted externally via Dropbox

## Common Tasks

### Adding New Content
1. Create notebooks in the appropriate `notes/` subdirectory following naming convention (e.g., `3_5_Descent.ipynb`)
2. Use existing notebook structure as a template
3. Include geometric visualizations and interactive elements
4. Implement algorithms from first principles using numpy/autograd

### Modifying Dependencies
Update `requirements.txt` for library changes. Note that Docker builds from `requirements.txt`, so changes affect containerized development.

### Running Individual Notebooks
```bash
jupyter notebook --port=8888 --ip=0.0.0.0 --allow-root --NotebookApp.token=''
# Then select notebook from browser interface
```

Or use Docker's Jupyter interface at http://localhost:8888 after running `docker-compose up -d`.