# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AutoDL is the NeurIPS 2019 AutoDL Challenge winning solution - an automated deep learning framework for multi-label classification across multiple modalities (image, video, speech, text, tabular data). The system automatically infers the data domain and applies appropriate domain-specific models.

## Common Commands

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Local Tests
```bash
# Default test with miniciao dataset and sample code submission
python run_local_test.py

# Custom dataset and code directory
python run_local_test.py -dataset_dir='AutoDL_sample_data/miniciao' -code_dir='AutoDL_sample_code_submission'
```

Results appear in `AutoDL_scoring_output/detailed_results.html` with real-time learning curves.

### Download Public Datasets
```bash
python download_public_datasets.py
```

## Architecture

### Directory Structure
- `AutoDL_ingestion_program/` - Challenge ingestion runtime that executes participant code
- `AutoDL_scoring_program/` - Scoring evaluator that computes metrics and generates HTML reports
- `AutoDL_sample_code_submission/` - Reference implementations for all domain models
- `AutoDL_sample_data/` - Sample datasets (miniciao, Monkeys)

### Domain Detection (in model.py)
The `infer_domain()` function determines data type from tensor shape:
- `sequence_size == 1, row_count/col_count > 1` → image
- `sequence_size == 1, row_count/col_count == 1` → tabular
- `sequence_size > 1, row_count/col_count == 1, has channels` → text
- `sequence_size > 1, row_count/col_count == 1, no channels` → speech
- `sequence_size > 1, row_count/col_count > 1` → video

### Data Format
Datasets use TFRecords with `metadata.textproto` files:
```
dataset.data/
├── test/
│   ├── metadata.textproto
│   └── sample-*.tfrecord
└── train/
    ├── metadata.textproto
    └── sample-*.tfrecord
```

### Model API
All participant models must implement:
```python
class Model:
    def __init__(self, metadata):  # metadata is AutoDLMetadata
        self.done_training = False

    def train(self, dataset, remaining_time_budget=None):
        # dataset is tf.data.Dataset yielding (example, labels)
        # example shape: (sequence_size, row_count, col_count, num_channels)
        # labels shape: (output_dim,)
        pass

    def test(self, dataset, remaining_time_budget=None) -> np.ndarray:
        # returns predictions shape: (sample_count, output_dim)
        # values in [0,1] or binary
        # returning None stops training loop
        pass
```

### Ingestion Loop (ingestion.py)
The `train/test` cycle repeats until:
- `model.done_training == True`
- Time budget exhausted
- `model.test()` returns `None`

### Domain-Specific Models
- `Auto_Image/` - ResNet-based image classification with PyTorch
- `Auto_Video/` - 3D CNN video classification (MC3 architecture)
- `Auto_Tabular/` - LightGBM/CatBoost/XGBoost ensemble with AutoML
- `at_speech/` - Audio/speech classification with pretrained models
- `Auto_NLP/`/`at_nlp/` - Text classification with embeddings

## Dependency Notes
- Python 3.5+ required
- TensorFlow 1.x (not 2.x) for dataset parsing
- CUDA 10, cuDNN 7.5 recommended for GPU
- Some models pip install dependencies on import (hyperopt, catboost, xgboost)