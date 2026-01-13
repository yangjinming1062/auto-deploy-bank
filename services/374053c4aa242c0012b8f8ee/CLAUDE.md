# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **Datawhale's Statistical Learning Method Solutions Manual** - an educational Chinese-language repository containing solutions to machine learning exercises from Hang Li's textbook "机器学习方法" (Machine Learning Methods). The repository is maintained by **Datawhale**, an AI learning community, and implements classical machine learning algorithms across three domains:

**Live Documentation**: https://datawhalechina.github.io/statistical-learning-method-solutions-manual
**License**: CC BY-NC-SA 4.0 (Creative Commons Attribution-NonCommercial-ShareAlike 4.0)

- **Supervised Learning**: Perceptron, k-NN, Naive Bayes, Decision Trees, Logistic Regression, SVM, AdaBoost, EM Algorithm, HMM, CRF
- **Unsupervised Learning**: Clustering, SVD, PCA, LSA, PLSA, MCMC, LDA, PageRank
- **Deep Learning**: Feedforward Neural Networks, CNN, RNN, Seq2Seq, Pretrained Language Models, GANs

## High-Level Architecture

This repository follows a **three-layer documentation structure**:

```
codes/              # Exercise implementations (Python scripts)
    ↓               (Written from scratch + using libraries)
notebook/           # Jupyter notebook format solutions
    ↓               (Export to markdown)
docs/               # Markdown documentation (served via Docsify)
```

**Content Flow**: Jupyter Notebooks → Markdown export → docs/ directory → merge_docs.py → compiled documentation

Each chapter has:
- **Python implementations** in `codes/chXX/` - standalone scripts with Chinese comments
- **Notebook versions** in `notebook/notes/` - detailed explanations and examples
- **Markdown docs** in `docs/chapterXX/` - generated from notebooks for web viewing

**Coverage**: 25 of 28 chapters complete (missing ch12-13, ch22). Each exercise includes both "scratch-built" and "library-based" (sklearn, PyTorch) implementations.

## Chapter Coverage

### Complete Chapters

**Part 1: Supervised Learning (ch01-11)**
- ch02: Perceptron | ch03: k-Nearest Neighbor | ch04: Naive Bayes
- ch05: Decision Trees | ch06: Logistic Regression | ch07: SVM
- ch08: AdaBoost | ch09: EM Algorithm | ch10: HMM | ch11: CRF

**Part 2: Unsupervised Learning (ch14-21)**
- ch14: Clustering | ch15: SVD | ch16: PCA | ch17: LSA
- ch18: PLSA | ch19: MCMC | ch20: LDA | ch21: PageRank

**Part 3: Deep Learning (ch23-28)**
- ch23: Feedforward NN | ch24: CNN | ch26: Seq2Seq
- ch27: Pretrained LM | ch28: GAN

**Missing**: ch12-13, ch22

## Environment Setup

**Required Python Version**: Python 3.10.X (other versions may have dependency compatibility issues)

**Install Dependencies**:
```bash
pip install -r requirements.txt
```

**Install Graphviz** (required for decision tree visualization):
```bash
# Refer to: https://blog.csdn.net/HNUCSEE_LJK/article/details/86772806
```

**Install PyTorch** (required for deep learning chapters):
```bash
pip3 install torch==1.12.1+cu116 torchvision==0.13.1+cu116 torchaudio==0.12.1+cu116 -f https://download.pytorch.org/whl/torch_stable.html
```

**Run Documentation Server** (for docsify):
```bash
docsify serve ./docs
```

## Repository Structure

```
├── codes/                    # Exercise implementations (Python files)
│   ├── ch02/                 # Perceptron
│   ├── ch03/                 # k-Nearest Neighbors & KD-Tree
│   ├── ch05/                 # Decision Trees
│   ├── ch06/                 # Logistic Regression & Max Entropy
│   ├── ch07/                 # Support Vector Machine
│   ├── ch08/                 # AdaBoost
│   ├── ch09/                 # EM Algorithm
│   ├── ch10/                 # Hidden Markov Model
│   ├── ch11/                 # Conditional Random Field
│   ├── ch14/                 # Clustering
│   ├── ch15/                 # Singular Value Decomposition
│   ├── ch16/                 # Principal Component Analysis
│   ├── ch17/                 # Latent Semantic Analysis
│   ├── ch18/                 # Probabilistic Latent Semantic Analysis
│   ├── ch19/                 # Markov Chain Monte Carlo
│   ├── ch20/                 # Latent Dirichlet Allocation
│   ├── ch21/                 # PageRank
│   ├── ch23/                 # Feedforward Neural Networks
│   ├── ch24/                 # Convolutional Neural Networks
│   ├── ch26/                 # Sequence-to-Sequence Models
│   ├── ch27/                 # Pretrained Language Models
│   └── ch28/                 # Generative Adversarial Networks
├── docs/                     # Documentation (generated from notebooks)
│   └── chapterXX/            # Chapter documentation
├── notebook/                 # Jupyter notebooks (source for docs)
│   ├── part01/               # Supervised Learning (Part 1)
│   ├── part02/               # Supervised Learning (Part 2)
│   ├── part03/               # Unsupervised Learning (Part 1)
│   ├── part04/               # Unsupervised Learning (Part 2)
│   └── part05/               # Deep Learning
├── images/                   # Images for documentation
└── requirements.txt          # Python dependencies
```

## Code Architecture

All code implementations follow a consistent pattern:

- **Self-contained Python files**: Each file is a standalone script with `if __name__ == '__main__'` entry point
- **Class-based implementations**: Algorithms are implemented as classes (e.g., `Perceptron`, `MyDecisionTree`, `NeuralNetwork`)
- **Chinese comments and variable names**: Code contains Chinese comments and docstrings
- **Built-in test data**: Each file includes example data in the `if __name__ == '__main__'` section
- **No external test framework**: Uses simple assertions or direct execution for testing

### Common Implementation Patterns

1. **Supervised Learning** (e.g., perceptron.py):
   - Model class with `fit()` method for training
   - Visualization hooks (matplotlib integration)
   - Example usage in `__main__` with book exercise data

2. **Unsupervised Learning** (e.g., pca_svd.py):
   - Matrix-based implementations using numpy
   - Mathematical operations aligned with textbook formulas
   - Direct execution for demonstration

3. **Deep Learning** (e.g., feedforward_nn_backpropagation.py):
   - Neural network classes with layer definitions
   - Forward propagation and backpropagation methods
   - Integration with real datasets (MNIST for neural networks)

## Common Development Tasks

### Running Code Examples

Execute any algorithm implementation directly:
```bash
python codes/ch02/perceptron.py
python codes/ch05/my_decision_tree.py
python codes/ch23/feedforward_nn_backpropagation.py
```

### Running All Code in a Chapter

Execute all files in a chapter directory:
```bash
for file in codes/ch05/*.py; do python "$file"; done
```

### Working with Jupyter Notebooks

Launch Jupyter:
```bash
jupyter notebook
```

The notebooks in `notebook/partXX/notes/` contain detailed explanations and are the source for generating the markdown docs. After editing notebooks, export them to markdown to update the docs directory.

### Generating Documentation

This project uses [docsify](https://docsify.js.org/) for documentation. To serve the docs locally:
```bash
docsify serve ./docs
```

The documentation is auto-generated from Jupyter notebooks in the `notebook/` directory.

## Key Dependencies

- **numpy**: Core numerical computations
- **scikit-learn**: Machine learning utilities and datasets
- **matplotlib**: Plotting and visualization
- **torch/torchvision**: Deep learning frameworks
- **pandas**: Data manipulation
- **scipy**: Scientific computing
- **tqdm**: Progress bars
- **graphviz**: Decision tree visualization
- **jupyter**: Notebook environment

See `requirements.txt` for the complete dependency list.

## Collaboration Workflow

This is a **community-driven project** by Datawhale with 12 core contributors from various Chinese universities. The standard workflow is:

1. Write solutions in Jupyter notebooks (`notebook/partXX/notes/`)
2. Export notebooks to markdown format
3. Update corresponding chapter files in `docs/chapterXX/`
4. Code implementations go in `codes/chXX/`
5. Use `codes/summary/merge_docs.py` to compile comprehensive documentation

### Project Statistics
- **174 total files** in the repository
- **182 Python packages** in requirements.txt
- **Self-study timeline**: 82-day structured learning path
- **Progress tracking**: Completion status table in documentation

### Documentation Compilation
The `codes/summary/merge_docs.py` script merges individual chapter documentation into comprehensive guides. This automation ensures consistent formatting across all documentation.

## Important Notes

- **Python 3.10 Required**: Use exactly Python 3.10.X for dependency compatibility
- **Self-contained scripts**: Each Python file can be executed independently
- **Chinese language**: Code, comments, and documentation are in Chinese
- **Educational focus**: These are learning implementations, not production code
- **No formal tests**: No pytest/unittest files; test by running the scripts
- **PyTorch version specific**: Uses PyTorch 1.12.1+cu116 for CUDA 11.6 compatibility
- **Reference project**: This is documentation/reference material, not a deployable application
- **No build systems**: No Makefile, setup.py, or pyproject.toml (uses standard Python package management)
- **Library versions**: All 182 dependencies are pinned in requirements.txt

## Quick Reference

**Most commonly run algorithms**:
- Perceptron: `codes/ch02/perceptron.py`
- Decision Tree: `codes/ch05/my_decision_tree.py`
- Neural Network: `codes/ch23/feedforward_nn_backpropagation.py`
- SVM: `codes/ch07/svm_demo.py`
- k-Means: `codes/ch14/divisive_clustering.py`

**Environment commands**:
- Install deps: `pip install -r requirements.txt`
- Start docs: `docsify serve ./docs`
- Start notebook: `jupyter notebook`
- Compile docs: `python codes/summary/merge_docs.py`

**Project type**: Educational reference/documentation (not a deployable application)
**Community**: Datawhale AI learning community
**Contributors**: 12 core members from Chinese universities