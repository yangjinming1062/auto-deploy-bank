# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

tensorflow-ocr is an OCR (Optical Character Recognition) system using TensorFlow/Keras with attention mechanisms. It includes synthetic text image generation from fonts and two main neural network approaches.

## Installation

```bash
pip install -r requirements.txt
```

## Training Commands

- **Simple letter recognition** (MNIST-like, auto-generates fonts): `./train_letters.py`
- **Full OCR model** (Conv + RNN + CTC loss): `./train.py`
- **Other specialized training scripts**: `train_attention.py`, `train_generator.py`, `train_letters.py`, `train_ocr_layer.py`, `train_text_localizer.py`

## Running Tests/Predictions

- **Recognize text in an image**: `python text_recognizer.py [image_file]` (defaults to `test_image.png`)
- **Real-time mouse pointer text detection**: `python mouse_prediction.py` (takes ~10 seconds to load, then outputs predictions)
- **Predict image**: `python predict_image.py`

## Architecture

### Approach 1: Custom TensorFlow Network (net.py)

Used by `train_letters.py`, `train_ocr_layer.py`, and `train_text_localizer.py`:

- **net.py**: Core neural network class with layers (`conv`, `dense`, `rnn`, `batchnorm`, `dropout`)
- Uses custom `layer` submodule for abstraction over raw TF operations
- Supports DenseNet-style blocks (`buildDenseConv`), pyramidal dense layers (`fullDenseNet`)
- Training via `net.train()` with checkpoint saving to `checkpoints/`

### Approach 2: Keras Conv+RNN+CTC (train.py)

Full OCR pipeline with on-the-fly image generation:

- **TextImageGenerator**: Keras Callback that generates synthetic text images with random fonts, sizes, rotations, speckle noise
- **Model architecture**: Conv2D → MaxPool → Dense → 2-layer Bidirectional GRU → Dense → Softmax
- **CTC Loss**: Connectionist Temporal Classification handles variable-length sequence alignment
- **Training phases**: Starts with 4-letter words (epochs 1-12), increases complexity, expands to longer sequences at epoch 20
- **Weights saved**: `weights/{run_name}/weights###.h5`
- **Visualization**: `VizCallback` shows predictions with edit distance metrics

### Data Generation

- **letter.py**: Generates synthetic letter images from system fonts for classification tasks
- **text.py**: Text rendering utilities with cairo for synthetic image generation
- Uses cairocffi for rendering text to images with various fonts, sizes, rotations

## Key Files

| File | Purpose |
|------|---------|
| `net.py` | Custom TF network class with conv/dense/RNN/batchnorm layers |
| `train.py` | Keras Conv+RNN+CTC OCR training with synthetic data generation |
| `letter.py` | Font-based letter image generator (classification) |
| `text.py` | Cairo-based text rendering utilities |
| `text_recognizer.py` | Inference using trained Keras model |
| `mouse_prediction.py` | Real-time OCR under mouse cursor |
| `predict_image.py` | Simple image prediction utility |
| `extensions.py` | Utility functions |
| `baselines.py` | Baseline model architectures |
| `deep_prior.py` | Deep prior approaches |

## Character Set

The models recognize: `a-zA-ZäöüÄÖÜß0-9!@#$%^&*()[]{}-_=+\|"\'`;:/.,?><~ ` (88 characters + CTC blank)

## Submodules

- `layer/`: Custom neural network wrapper (currently empty - requires `git submodule update --init`)
- `EAST/`: Text localization (fork of quasiris/EAST, requires submodule init)