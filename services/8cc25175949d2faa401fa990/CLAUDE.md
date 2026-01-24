# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DiffSinger is a Singing Voice Synthesis (SVS) and Text-to-Speech (TTS) system implementing the Shallow Diffusion Mechanism. The codebase uses PyTorch and PyTorch Lightning for training and inference.

## Common Commands

### Environment Setup
```sh
# GPU 2080Ti (CUDA 10.2)
pip install -r requirements_2080.txt

# GPU 3090 (CUDA 11.4)
pip install -r requirements_3090.txt

# Or use requirements.txt for custom setup
pip install -r requirements.txt
```

### Data Preparation & Binarization
```sh
export PYTHONPATH=.
# Binarize LJ Speech dataset for TTS
python data_gen/tts/bin/binarize.py --config configs/tts/lj/fs2.yaml

# Binarize PopCS/OpenCpop for SVS
python data_gen/singing/bin/binarize.py --config configs/singing/opencpop.yaml
```

### Training
```sh
# FastSpeech2 baseline (prerequisite for DiffSpeech)
python tasks/run.py --config configs/tts/lj/fs2.yaml --exp_name fs2_lj_1 --reset

# DiffSpeech (TTS)
python tasks/run.py --config usr/configs/lj_ds_beta6.yaml --exp_name lj_ds_beta6_1213 --reset

# DiffSinger (SVS)
python tasks/run.py --config configs/singing/opencpop.yaml --exp_name opencppop --reset
```

### Inference
Add `--infer` flag to training commands:
```sh
python tasks/run.py --config usr/configs/lj_ds_beta6.yaml --exp_name lj_ds_beta6_1213 --infer
```

### Monitoring
```sh
tensorboard --logdir_spec exp_name
```

## Architecture

### Core Components

- **`tasks/`** - Task implementations containing training/inference logic
  - `base_task.py` - BaseTask class defining training loop, validation, checkpointing
  - `tts/tts.py` - TtsTask base class for TTS/SVS
  - `tts/fs2.py` - FastSpeech2Task for FastSpeech2 model training

- **`modules/`** - Neural network model definitions
  - `fastspeech/` - FastSpeech2 encoder/decoder, duration/pitch/energy predictors
  - `hifigan/` - HiFiGAN vocoder
  - `parallel_wavegan/` - Parallel WaveGAN vocoder
  - `commons/` - Shared layers (positional embeddings, common modules)

- **`utils/`** - Utility functions
  - `hparams.py` - Configuration management (YAML loading with inheritance)
  - `pl_utils.py` - PyTorch Lightning utilities and data loaders
  - `text_encoder.py` - Phoneme encoding
  - `audio.py` - Audio processing (mel-spectrogram, waveform)
  - `pitch_utils.py` - F0 processing

- **`data_gen/`** - Data preprocessing
  - `tts/` - TTS binarization (phoneme alignment, pitch extraction)
  - `singing/` - SVS binarization with MIDI support

- **`configs/`** - Configuration YAML files (inherited via `base_config`)
  - `config_base.yaml` - Base training/validation settings
  - `tts/` - TTS configurations (LJ Speech, etc.)
  - `singing/` - SVS configurations (PopCS, OpenCpop)

- **`usr/`** - User implementations of specific models
  - `diffsinger_task.py` - DiffSingerTask (diffusion-based SVS)
  - `diffspeech_task.py` - DiffSpeechTask (diffusion-based TTS)

- **`inference/`** - Inference utilities and Gradio demos

### Configuration System

Configs use YAML with `base_config` for inheritance chains. The `set_hparams()` function in `utils/hparams.py` handles:
- Loading config from `args.config`
- Resolving base_config chains
- Overriding with CLI `--hparams` arguments
- Auto-creating `checkpoints/<exp_name>/` directories

Example config:
```yaml
base_config:
  - configs/tts/lj/fs2.yaml
  - ./base.yaml
task_cls: usr.diffspeech_task.DiffSpeechTask
vocoder: vocoders.hifigan.HifiGAN
fs2_ckpt: checkpoints/fs2_lj_1/model_ckpt_steps_150000.ckpt
```

### Model Architecture

**DiffSpeech/DiffSinger Pipeline:**
1. Text/MIDI -> Linguistic representation (Encoder)
2. Linguistic + F0 -> Mel-spectrogram (Decoder with Shallow Diffusion)
3. Mel + F0 -> Waveform (Vocoder: HiFiGAN/NSF-HiFiGAN)

**FastSpeech2:**
- FFT-based encoder with phoneme embeddings
- Duration, pitch, and energy predictors
- Length regulator for alignment
- Mel-spectrogram output layer

### Data Flow

Raw audio/text -> Binarizer (`data_gen/`) -> Binary dataset (`data/binary/`) ->
Dataset class (`tasks/tts/fs2_utils.py`) -> Training loop (`tasks/tts/fs2.py`)