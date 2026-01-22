# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BERT-BILSTM-CRF is a Chinese Named Entity Recognition (NER) system using a BERT encoder followed by BiLSTM and CRF layers. Supports multiple datasets (DGRE, DUIE) with distributed training and ONNX/Triton inference optimization.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Data preprocessing (process raw data to NER format)
python process.py

# Manual training (custom loop)
python main.py

# HuggingFace Trainer-based training (with distributed support)
bash train.sh

# Distributed training (2 GPUs example)
export NCCL_P2P_DISABLE=1
export NCCL_IB_DISABLE=1
CUDA_VISIBLE_DEVICES=0,1 torchrun --nnodes 1 --nproc_per_node=2 transformers_trainer.py

# Inference
python predict.py

# ONNX conversion and benchmarking
cd convert_onnx && python convert_onnx.py
```

## Architecture

### Model Structure
```
BERT Encoder → BiLSTM (hidden=128, bidirectional) → Linear → CRF
```

- **model.py**: `BertNer` class defines the forward pass and model architecture
- Uses differential learning rates: BERT (3e-5) vs BiLSTM/CRF (3e-3)

### Data Pipeline
```
process.py (raw data) → ner_data/{train.txt, dev.txt, labels.txt} → NerDataset → DataLoader
```

- **data_loader.py**: PyTorch `NerDataset` class for tokenization and label mapping
- Data format: JSON with `id`, `text` (character list), and `labels` (BIO tags)
- Labels stored in `labels.txt` are converted to BIO scheme (B-prefix, I-prefix, O)

### Training Approaches

1. **main.py**: Manual training loop with custom `Trainer` class
2. **transformers_trainer.py**: HuggingFace `Trainer` with distributed training support

### Configuration

- **config.py**: `NerConfig` class manages hyperparameters per dataset
- Key settings: `max_seq_len`, `train_batch_size`, `epochs`, `save_step`, learning rates
- Configs saved to `checkpoint/{dataset_name}/ner_args.json`

### Inference Optimization

- **convert_onnx/**: ONNX export and inference benchmarking (`model.onnx`, `model_fp16.onnx`)
- **convert_triton/**: Triton Inference Server deployment (see convert_triton/readme.md)

### Key Files

| File | Purpose |
|------|---------|
| `model.py` | BertNer model definition |
| `main.py` | Manual training loop |
| `transformers_trainer.py` | HuggingFace Trainer + distributed training |
| `process.py` | Raw data to NER format preprocessing |
| `predict.py` | Trained model inference |
| `config.py` | Configuration management |

### Common Issues

- **CRF batch_first error**: Use `pytorch-crf==0.7.2`
- **NCCL errors in distributed training**: Set `NCCL_P2P_DISABLE=1` and `NCCL_IB_DISABLE=1`