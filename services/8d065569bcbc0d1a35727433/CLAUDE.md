# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MASR (Magical Automatic Speech Recognition) is a PyTorch-based ASR framework supporting both streaming and non-streaming recognition. Implements DeepSpeech2 architecture variants with CTC decoding.

**Python:** 3.8+ | **PyTorch:** 1.12.1+ | **License:** Apache 2.0

## Build & Development Commands

```bash
# Install from source
python setup.py install

# Or via pip
pip install -r requirements.txt

# Train model (Chinese config by default)
python train.py --configs configs/config_zh.yml

# Evaluate trained model
python eval.py --configs configs/config_zh.yml

# Export model for inference
python export_model.py --configs configs/config_zh.yml

# Inference on audio file
python infer_path.py --wav_path ./dataset/test.wav

# Long audio inference with VAD segmentation
python infer_path.py --wav_path ./dataset/test.wav --is_long_audio=True

# Launch web server (Flask REST API + WebSocket streaming)
python infer_server.py

# Launch GUI interface for real-time recording & recognition
python infer_gui.py

# Prepare dataset manifest and vocabulary
python create_data.py
```

## Architecture

```
masr/
├── trainer.py              # MASRTrainer class: training orchestration, distributed training
├── predict.py              # Predictor class: inference with streaming/non-streaming modes
├── data_utils/
│   ├── reader.py           # MASRDataset - manifest-based dataset loading
│   ├── audio.py            # AudioSegment - audio loading & VAD processing
│   ├── collate_fn.py       # padding, stateless collate functions
│   ├── featurizer/
│   │   ├── audio_featurizer.py  # Fbank/MFCC/linear feature extraction
│   │   └── text_featurizer.py   # Vocabulary mapping, text normalization
│   ├── augmentor/          # AugmentationPipeline: noise, speed, volume, shift, resample, spec_augment
│   └── normalizer.py       # Mean/std normalization for features
├── decoders/
│   ├── ctc_greedy_decoder.py    # Fast, real-time, no LM
│   └── beam_search_decoder.py   # KenLM integration, higher accuracy, no Windows support
├── model_utils/
│   ├── deepspeech2/             # Streaming model (ConvStack + RNNStack)
│   ├── deepspeech2_no_stream/   # Non-streaming variant
│   └── utils.py                 # Model export utilities
└── utils/
    ├── utils.py                 # Argument parsing, manifest creation, audio utilities
    ├── metrics.py               # CER/WER calculation
    ├── text_utils.py            # Punctuation restoration (WeTextProcessing)
    └── audio_vad.py             # WebRTC VAD-based audio cropping
```

## Supported Models

| Model | Streaming | Parameters | Use Case |
|-------|-----------|------------|----------|
| `deepspeech2` | Yes | 35M | Standard streaming recognition |
| `deepspeech2_big` | Yes | 167M | Large datasets (WenetSpeech) |
| `deepspeech2_no_stream` | No | 98M | Full audio batch recognition |
| `deepspeech2_big_no_stream` | No | Large | High-accuracy non-streaming |

## Configuration

YAML configs in `configs/`:
- `config_zh.yml` - Chinese recognition (default)
- `config_en.yml` - English recognition
- `augmentation.json` - Data augmentation pipeline

Key config sections:
- `dataset`: batch_size, workers, manifest paths, duration filters
- `preprocess`: feature_method (fbank/mfcc/linear), sample_rate (16000), normalization
- `optimizer`: learning_rate, gamma, weight_decay, gradient_clip_norm
- `decoder`: `ctc_greedy` or `ctc_beam_search`
- `ctc_beam_search_decoder`: beam_size (300 default), alpha (LM weight), beta (word count)

## Data Format

Dataset structure:
```
dataset/
├── annotation/           # JSON annotation files (audio_path: transcript)
├── manifest.train        # Training manifest
├── manifest.test         # Test manifest
├── vocabulary.txt        # Character vocabulary (<blank>, <unk> included)
├── mean_std.json         # Feature normalization stats
├── manifest.noise        # Noise samples for augmentation
└── test.wav             # Test audio
```

Manifest format: `audio_path\ttranscript` (one per line)

## Key Patterns

**Training:** `MASRTrainer` handles data creation, feature normalization, augmentation, distributed training via `DSElasticDistributedSampler`, checkpointing (best_model, last_model), and VisualDL logging.

**Inference:** `Predictor` handles feature extraction, CTC decoding, stream state management (output_state_h, output_state_c for streaming), optional punctuation restoration (WeTextProcessing), and inverse text normalization (cn2an).

**Decoding:** Greedy decoder is fast for real-time; beam search uses KenLM language model and is more accurate but ~10x slower and unsupported on Windows.

**Augmentation:** JSON config enables SpecAugment, noise perturbation (SNR-based), speed/volume/shift perturbations, and resample augmentation.

## Audio Processing

- Resamples all audio to 16kHz mono
- Feature extraction: Fbank (80 mel bands), MFCC (40 coefficients), or linear spectrogram
- VAD-based segmentation for long audio (>20s)
- dB normalization (default -20dB)

## Entry Points

| File | Purpose |
|------|---------|
| `train.py` | Training entry point (31 lines) |
| `eval.py` | Model evaluation |
| `export_model.py` | Export to inference.pt |
| `infer_path.py` | Audio file recognition |
| `infer_server.py` | Flask + WebSocket server |
| `infer_gui.py` | PyAudio GUI recorder |
| `create_data.py` | Dataset preparation |

## Dependencies

Core: torch, torchaudio, librosa, soundfile, scipy, numpy
Web: flask, flask-cors, websockets
ASR: webrtcvad, python-Levenshtein, WeTextProcessing, zhconv, cn2an
Training: visualdl, tqdm, numba