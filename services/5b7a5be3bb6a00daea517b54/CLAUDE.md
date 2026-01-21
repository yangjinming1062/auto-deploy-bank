# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Lip2Wav** is a deep learning lip-to-speech synthesis system that generates speech audio from lip movements in video frames. Based on the CVPR 2020 paper "Learning Individual Speaking Styles for Accurate Lip to Speech Synthesis."

## Dataset Setup

```bash
# Download videos for a speaker (requires youtube-dl)
sh download_speaker.sh Dataset/chem

# Output structure after download:
# Dataset/chem/
#   ├── videos/ (full downloaded videos)
#   ├── intervals/ (cropped 30s segments)
#   ├── preprocessed/ (after running preprocess.py)
#   ├── train.txt, val.txt, test.txt (video IDs)
```

**Installation:**
```bash
pip install -r requirements.txt
sudo apt-get install ffmpeg
# Download face detection model from: https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth
# Save to: face_detection/detection/sfd/s3fd.pth
```

**Preprocessing:**
```bash
python preprocess.py --speaker_root Dataset/chem --speaker chem
# Options: --ngpu N, --batch_size, --resize_factor
```

**Training:**
```bash
python train.py <run_name> --data_root Dataset/chem --preset synthesizer/presets/chem.json
# Options: --models_dir, --restore (bool), --checkpoint_interval, --eval_interval
# Checkpoints: synthesizer/saved_models/logs-<name>/taco_pretrained/tacotron_model.ckpt
```

**Inference/Generation:**
```bash
python complete_test_generate.py -d Dataset/chem -r Dataset/chem/test_results \
--preset synthesizer/presets/chem.json --checkpoint <path_to_checkpoint>
```

**Evaluation:**
```bash
python score.py -r Dataset/chem/test_results
```

## Architecture

```
Input Video Frames
    ↓
Face Detection (S3FD) → face_detection/
    ↓
Encoder (Conv3 + LSTM) → synthesizer/models/tacotron.py
    ↓
Tacotron-2 Decoder (LSTM + Attention) → synthesizer/tacotron2.py
    ↓
Mel Spectrogram Output (80-dim)
    ↓
Griffin-Lim Reconstruction
    ↓
Audio Waveform
```

### Key Components
- **`synthesizer/tacotron2.py`**: Core Tacotron2 model class (TensorFlow)
- **`synthesizer/models/tacotron.py`**: Encoder-CBHG, attention, decoder, postnet definition
- **`synthesizer/train.py`**: Training loop with scheduled teacher forcing
- **`synthesizer/feeder.py`**: Data loading with speaker embeddings and batching
- **`synthesizer/inference.py`**: `Synthesizer` class for face→spectrogram inference
- **`preprocess.py`**: Multi-GPU face detection and audio preprocessing pipeline
- **`face_detection/`**: S3FD face detector wrapper (PyTorch)

### Data Flow
```
Raw Video → intervals/30s clips → preprocess.py → preprocessed/<vid_id>/
                                                ├── *.jpg (face frames)
                                                ├── audio.wav
                                                └── mels.npz (mel/linear specs)

Training: feeder.py loads preprocessed → model.train() → checkpoint

Inference: faces → Synthesizer.synthesize_spectrograms() → mel → griffin_lim() → audio
```

### Speaker Presets
`synthesizer/presets/<speaker>.json` configures T (frames window), overlap, crops, batch sizes. Crop coordinates vary by video source (chem, chess, dl, hs, eh).

## Dependencies
- Python 3.7.4, TensorFlow 1.13.1 (GPU), PyTorch 1.1.0
- Audio: librosa, pystoi, pesq, sounddevice
- Video: opencv-python 4.1.1, youtube-dl

## License
MIT. If using this code, cite: Prajwal et al., CVPR 2020.