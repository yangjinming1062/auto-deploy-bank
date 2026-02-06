# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AutoDL is an automated deep learning framework for multi-modal classification (images, video, speech, text, tabular data). This is the winning solution from the NeurIPS 2019 AutoDL Challenge. The framework automatically selects and trains appropriate models based on the input data domain.

## Commands

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Local Test
```bash
python run_local_test.py
```

Test on a specific dataset:
```bash
python run_local_test.py -dataset_dir=./AutoDL_sample_data/miniciao -code_dir=./AutoDL_sample_code_submission
```

Results are saved to `AutoDL_scoring_output/detailed_results.html`.

### Download Public Datasets
```bash
python download_public_datasets.py
```

## Architecture

### Directory Structure
- **AutoDL_ingestion_program/**: Competition ingestion program that runs participant code
- **AutoDL_scoring_program/**: Scoring program that evaluates predictions
- **AutoDL_sample_code_submission/**: Sample participant submission code
- **AutoDL_sample_data/**: Sample datasets (miniciao, Monkeys)

### Domain-Specific Models
The framework dispatches to the appropriate model based on data shape via `AutoDL_sample_code_submission/model.py`:
- `Auto_Image/`: Image classification (ResNet, etc.)
- `Auto_Video/`: Video classification (MC3, etc.)
- `at_speech/`: Speech/audio classification
- `Auto_NLP/`: Text classification (BERT, etc.)
- `Auto_Tabular/`: Tabular data (LightGBM, XGBoost, neural networks)

### Domain Inference
Domain is inferred from tensor shape in `infer_domain()`:
- `sequence_size == 1, row_count > 1, col_count > 1` → image
- `sequence_size > 1, row_count > 1, col_count > 1` → video
- `sequence_size > 1, row_count == 1, col_count == 1, has channels` → text
- `sequence_size > 1, row_count == 1, col_count == 1, no channels` → speech
- `sequence_size == 1, (row_count == 1 or col_count == 1)` → tabular

### Data Format
Datasets use TFRecords with `metadata.textproto` (Protocol Buffer) files specifying:
- Matrix dimensions, channels, sequence size
- Output dimensions (number of classes)
- Sample count

### Model API
All models must implement:
```python
class Model:
    def __init__(self, metadata): ...
    def train(self, dataset, remaining_time_budget=None): ...
    def test(self, dataset, remaining_time_budget=None): ...
    done_training: bool  # Flag to stop training loop
```

The `train()` and `test()` methods are called repeatedly. Predictions should return numpy arrays of shape `(sample_count, output_dim)`.

## Environment Requirements
- Python 3.5+
- TensorFlow 1.15 (GPU recommended)
- PyTorch 1.3.1
- CUDA 10, cuDNN 7.5