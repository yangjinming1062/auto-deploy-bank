# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Audio classification pipeline using TensorFlow 2.3 and Keras for prototyping audio classification algorithms. Uses [Kapre](https://github.com/keunwoochoi/kapre) library for on-the-fly mel spectrogram computation from raw audio waveforms.

## Setup

```bash
conda create -n audio python=3.7
activate audio
pip install -r requirements.txt
```

For Jupyter notebooks: `ipython kernel install --user --name=audio`

## Common Commands

**Preprocess audio data:** `python clean.py`
- Converts multi-channel audio to mono
- Downsamples to specified sample rate (default 16000 Hz)
- Removes low-magnitude audio segments using envelope detection
- Splits audio into fixed-duration segments (default 1.0s)
- Outputs to `clean/` directory

**Train a model:** `python train.py`
- Supports three model architectures: `conv1d`, `conv2d`, `lstm`
- Uses `clean/` directory as source by default
- Key arguments: `--model_type`, `--batch_size`, `--delta_time`, `--sample_rate`
- Saves checkpoints to `models/` and training history to `logs/`

**Run inference:** `python predict.py`
- Loads trained model from `models/`
- Predicts on audio files in `wavfiles/` by default
- Outputs predictions to `logs/`

## Architecture

### Data Pipeline
- `DataGenerator` class (train.py): Keras Sequence-based batch generator that loads WAV files on-demand
- Audio is loaded as raw waveform and fed to Kapre's mel spectrogram layer during model execution

### Models (models.py)
All three models share this structure:
1. Input: Raw audio waveform (SR × 1)
2. Kapre mel spectrogram layer: Converts waveform to mel spectrogram (time × mel_freq × 1)
3. Model-specific feature extraction layers
4. Dense classification head with softmax activation

Key models:
- **Conv1D**: TimeDistributed 1D convolutions → GlobalMaxPooling
- **Conv2D**: 2D convolutions → Flatten
- **LSTM**: Bidirectional LSTM with skip connections → Dense

### Audio Utilities (clean.py)
- `envelope()`: Computes signal envelope with rolling max, creates boolean mask for segments above threshold
- `downsample_mono()`: Converts stereo to mono using librosa, resamples to target rate
- `split_wavs()`: Steps through audio and saves fixed-duration segments

## Configuration

Key parameters that must be consistent across preprocessing, training, and inference:
- `--sample_rate` (default: 16000): Target sample rate
- `--delta_time` (default: 1.0): Duration of audio samples in seconds
- `--threshold` (default: 20): Envelope detection threshold for clean.py

## File Structure

- `train.py`: Training script with DataGenerator and model instantiation
- `models.py`: Model definitions (Conv1D, Conv2D, LSTM functions)
- `clean.py`: Audio preprocessing utilities
- `predict.py`: Inference script
- `wavfiles/`: Source audio files organized in class subdirectories
- `clean/`: Preprocessed audio segments (output of clean.py)
- `models/`: Saved model checkpoints (.h5 files)
- `logs/`: Training history CSVs and prediction arrays