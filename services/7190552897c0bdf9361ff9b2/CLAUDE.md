# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FaceNet implementation using PyTorch for face recognition. Supports training on custom datasets and evaluation on LFW (Labeled Faces in the Wild).

## Commands

### Installation
```bash
pip install -r requirements.txt
```

### Training
1. Prepare dataset in the specified format (`datasets/` folder).
2. Generate annotation file: `python txt_annotation.py`
3. Train the model: `python train.py`

### Evaluation
Evaluate on LFW dataset:
```bash
python eval_LFW.py
```
Note: Requires LFW dataset in the root directory and configured model weights.

### Prediction
Compare two face images:
```bash
python predict.py
img\1_001.jpg
img\1_002.jpg
```

## Architecture

- **nets/**: Neural network definitions.
  - `facenet.py`: Main model interface.
  - `facenet_training.py`: Training loop and loss functions.
  - `mobilenet.py`, `inception_resnetv1.py`: Backbone networks.
- **utils/**: Utilities.
  - `dataloader.py`: Data loading and augmentation.
  - `utils_fit.py`: Training helper.
  - `utils_metrics.py`: Evaluation metrics (e.g., accuracy, ROC).
- **model_data/**: Stores pre-trained weights and configuration files.
- **logs/**: Checkpoints and training logs.

## Key Configuration
- `facenet.py` contains the default model settings (input shape, backbone, CUDA).
- `train.py` contains training hyperparameters (batch size, epochs, learning rate).