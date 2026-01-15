# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TextClassification-Keras is a repository implementing various deep learning models for text classification using Keras/TensorFlow 2.0. Each model type has its own directory under `/model/` containing the model architecture and a demo application.

## Environment

```
Python 3.7
numpy==1.17.2
tensorflow==2.0.1
```

Install dependencies: `pip install -r requirements.txt`

## Running Models

Each model directory contains a `main.py` file that demonstrates training on the IMDB dataset. To run any model:

```bash
cd model/{ModelName}
python main.py
```

Available models: FastText, TextCNN, TextRNN, TextBiRNN, TextAttBiRNN, HAN, RCNN, RCNNVariant

## Architecture Patterns

Each model follows a consistent structure:
- **`model_name.py`**: Keras `Model` class implementation
  - Constructor params: `maxlen`, `max_features`, `embedding_dims`, `class_num`, `last_activation`
  - Validates input shape in `call()` method before processing
- **`main.py`**: Training/inference demo using IMDB dataset
  - Loads data with `imdb.load_data()`
  - Pads sequences with `sequence.pad_sequences()`
  - Uses `EarlyStopping` callback monitoring `val_accuracy`
  - Compiles with `adam` optimizer and `binary_crossentropy` loss

### Shared Utilities

- **`attention.py`**: Custom Keras `Layer` implementing feed-forward attention (used by HAN and TextAttBiRNN)
- **Common layers**: `Embedding`, `Dense`, `Bidirectional(CuDNNLSTM/GRU)`, `Conv1D`, `GlobalMaxPooling1D`

### Model-Specific Notes

- **HAN**: Takes 3D input `(samples, sentences, words)` - reshapes IMDB data to `(batch, maxlen_sentence, maxlen_word)`
- **RCNN**: Takes 3 inputs (current, left context, right context) - implementation detail differs from paper
- **FastText**: Simplest model - embedding + GlobalAveragePooling1D + Dense classifier
- **TextCNN**: Multiple parallel Conv1D layers with different kernel sizes, results concatenated
- **RNN variants**: Use `CuDNNLSTM` (GPU-accelerated) - cannot use generic LSTM/GRU layers