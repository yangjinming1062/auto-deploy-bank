# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Microsoft's "AI for Beginners" - a 12-week, 24-lesson educational curriculum covering Artificial Intelligence fundamentals. The repository contains Jupyter Notebooks with TensorFlow/PyTorch code, a Vue.js quiz application, and 40+ language translations.

## Commands

### Python/Jupyter Curriculum
```bash
# Create conda environment
conda env create --name ai4beg --file environment.yml
conda activate ai4beg

# Start Jupyter
jupyter notebook
# or
jupyter lab

# Run a specific notebook
jupyter notebook lessons/3-NeuralNetworks/03-Perceptron/Perceptron.ipynb

# Run Python scripts directly
python lessons/4-ComputerVision/07-ConvNets/pytorchcv.py
```

### Quiz Application (Vue.js)
```bash
cd etc/quiz-app
npm install
npm run serve     # Development server at localhost:8080
npm run build     # Production build to dist/
npm run lint      # Lint and auto-fix
```

## Architecture

```
lessons/
  ├── 0-course-setup/       # Environment setup instructions
  ├── 1-Intro/              # AI introduction
  ├── 2-Symbolic/           # Knowledge representation, expert systems
  ├── 3-NeuralNetworks/     # Perceptron, MLP, frameworks (PyTorch/TensorFlow)
  ├── 4-ComputerVision/     # OpenCV, CNNs, transfer learning, GANs, segmentation
  ├── 5-NLP/                # Text embeddings, RNNs, transformers, BERT, LLMs
  ├── 6-Other/              # Genetic algorithms, RL, multi-agent systems
  ├── 7-Ethics/             # Responsible AI
  └── X-Extras/             # Multi-modal networks, CLIP

etc/
  ├── quiz-app/             # Vue 2.x quiz application
  ├── quiz-src/             # Quiz source files
  └── pdf/                  # PDF versions of lessons

examples/                   # Beginner-friendly standalone examples
translations/               # 40+ language localizations
```

Each lesson typically contains: README.md (theory), .ipynb notebooks (PyTorch & TensorFlow versions), and optional lab exercises.

## Key Dependencies

- Python 3, Jupyter
- TensorFlow 2.17, PyTorch (via conda), Keras 3.x
- scikit-learn, OpenCV, pandas, numpy, matplotlib
- Vue 2.x for quiz app

## Development Notes

- This is educational content, not production software - notebooks prioritize learning over optimization
- Most notebooks are framework-duplicated (PyTorch and TensorFlow versions)
- Translations are automated via GitHub Actions (co-op-translator)
- No traditional test suite exists; validate notebooks by running cells sequentially
- Later CV/NLP lessons benefit significantly from GPU acceleration