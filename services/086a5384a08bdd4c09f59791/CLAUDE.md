# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WeTTS is a production-first, end-to-end Text-to-Speech toolkit. It consists of two main components:

1. **Frontend** (`wetts/frontend/`): Converts raw text to phoneme sequences with prosody labels. Uses BERT for polyphone disambiguation and prosody prediction.
2. **Backend (VITS)** (`wetts/vits/`): Generative vocoder that converts phonemes to audio waveforms.

Both components are exported to ONNX format for production deployment.

## Development Setup

```bash
# Create environment
conda create -n wetts python=3.8 -y
conda activate wetts
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

## Common Commands

### CLI Usage
```bash
# Synthesize speech from text
wetts --text "今天天气怎么样" --wav output.wav
```

### Running Tests
```bash
# Test frontend polyphone prediction accuracy
python wetts/frontend/test_polyphone.py --polyphone_dict <dict> --prosody_dict <dict> --test_data <test_file> --checkpoint <model.pt> --bert_name_or_path bert-chinese-base

# Test frontend prosody prediction F1 score
python wetts/frontend/test_prosody.py --polyphone_dict <dict> --prosody_dict <dict> --test_data <test_file> --checkpoint <model.pt> --bert_name_or_path bert-chinese-base
```

### Training

**Frontend (BERT-based classification)**:
```bash
python wetts/frontend/train.py \
  --polyphone_dict <dict> \
  --prosody_dict <dict> \
  --train_polyphone_data <data> \
  --cv_polyphone_data <data> \
  --train_prosody_data <data> \
  --cv_prosody_data <data> \
  --batch_size 32 \
  --num_epochs 4 \
  --model_dir <output_dir>
```

**VITS (Distributed training)**:
```bash
# Single GPU
cd examples/baker
python ../../wetts/vits/train.py --config v1.json --model_dir <exp_dir>

# Multi-GPU (uses WORLD_SIZE, LOCAL_RANK, RANK env vars)
torchrun --nproc_per_node=4 ../../wetts/vits/train.py --config v1.json --model_dir <exp_dir>
```

### Exporting Models to ONNX

**Frontend**:
```bash
python wetts/frontend/export_onnx.py \
  --polyphone_dict <dict> \
  --prosody_dict <dict> \
  --checkpoint <model.pt> \
  --onnx_model <output.onnx>
```

**VITS**:
```bash
python wetts/vits/export_onnx.py \
  --checkpoint <model.pth> \
  --cfg <config.json> \
  --onnx_model <output.onnx> \
  --phone_table <phone.txt> \
  --speaker_table <speaker.txt>
```

### Code Quality

```bash
# Run pre-commit hooks
pre-commit run --all-files

# Run manually
flake8 --config=.flake8 wetts/
cpplint --recursive runtime/
```

## Architecture

### Inference Pipeline

```
Text → Frontend (ONNX) → Phonemes + Prosody → VITS (ONNX) → Audio WAV
       |                              |
    BERT-based                    Polyphone
    prosody/polyphone           disambiguation
    classification
```

### Key Entry Points

- **`wetts/cli/tts.py`**: Main CLI for TTS synthesis (`wetts` command)
- **`wetts/cli/model.py`**: Model loading orchestration via `Hub.get_model()`
- **`wetts/cli/frontend.py`**: ONNX frontend runtime wrapper
- **`wetts/cli/hub.py`**: Model downloading from ModelScope

### Model Components

**Frontend** (`wetts/frontend/`):
- `model.py`: BERT-based classifier (polyphone + prosody heads)
- `g2p_prosody.py`: Grapheme-to-phoneme with prosody prediction
- `export_onnx.py`: Exports trained model to ONNX

**VITS** (`wetts/vits/`):
- `model/models.py`: `SynthesizerTrn` - main VITS model
- `model/encoders.py`: Text encoder and duration predictor
- `model/decoders.py`: Waveform decoder (HiFi-GAN compatible)
- `model/discriminators.py`: Multi-period discriminator, WavLM discriminator
- `inference.py`: PyTorch inference script
- `train.py`: Distributed training script with DDP

### Configuration Format

Training configs are JSON files in `examples/{dataset}/configs/`:
- `train`: Training hyperparameters (epochs, batch_size, learning_rate, fp16_run)
- `data`: Audio parameters (sampling_rate, hop_length, n_mel_channels)
- `model`: Model architecture (use_mel_posterior_encoder, n_layers, gin_channels)

### Data Formats

**Frontend Training Data**:
- Polyphone: `宋代出现了▁le5▁燕乐音阶的记载` (polyphones marked with `▁`)
- Prosody: `蔡少芬 #2 拍拖 #2 也不认啦 #4` (`#n` indicates prosody break level)

**VITS Training Files**: Path format `audio_path|speaker|text`

## Pre-trained Models

Models are downloaded automatically via `Hub.get_model()` to `~/.wetts/`:
- `frontend`: Baker BERT frontend (baker_bert_onnx.tar.gz)
- `multilingual`: Multilingual VITS model (multilingual_vits_v3_onnx.tar.gz)

## Style Guidelines

- Max line length: 80 characters (flake8 B950)
- Python: Follow flake8 configuration in `.flake8`
- C++: Google style with clang-format (`.clang-format`)
- Pre-commit hooks enforce formatting (trailing whitespace, isort, flake8, cpplint)