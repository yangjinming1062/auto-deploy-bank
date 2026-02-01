# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bytesep is a PyTorch-based music source separation library. It separates audio recordings into individual sources (vocals, accompaniment, etc.) using deep neural networks. The project uses PyTorch Lightning for training and supports both fullband and subband model architectures.

## Common Commands

### Installation
```bash
pip install -e .
```

### Download Pretrained Checkpoints
```bash
python3 -m bytesep download-checkpoints
```

### Separate Audio
```bash
python3 -m bytesep separate \
    --source_type="vocals" \
    --audio_path="./audio.mp3" \
    --output_path="output.mp3"
```

### Train a Model
```bash
# Using shell script
./scripts/4_train/musdb18/train.sh /path/to/workspace

# Or directly with Python
python3 bytesep/train.py train \
    --workspace=$WORKSPACE \
    --gpus=1 \
    --config_yaml=./scripts/4_train/musdb18/configs/vocals-accompaniment,resunet_subbandtime.yaml
```

### Apply Code Formatting
```bash
./scripts/apply-black.sh
```

## Architecture

### Core Components

**Models (`bytesep/models/`)**
- `lightning_modules.py` - Contains `LitSourceSeparation` (PyTorch Lightning wrapper) and `get_model_class()` factory
- Models follow a U-Net style encoder-decoder architecture with skip connections
- Subband models use PQMF filter banks to process audio in subbands
- Supported model types: ResUNet143, UNet, MobileNet_Subbandtime, and others (see `get_model_class()`)

**Training Pipeline (`bytesep/train.py`)**
1. Reads YAML config defining data, model, loss, optimizer
2. Creates `DataModule` with HDF5-based dataset loading
3. Wraps model in `LitSourceSeparation` with `LitSourceSeparation.training_step()`
4. Trains with PyTorch Lightning Trainer using DDPPlugin for multi-GPU

**Data Flow**
```
Audio Files → HDF5 Packing → Index Creation → SegmentSampler → Dataset
    → collate_fn → BatchDataPreprocessor → Model → Loss
```

**Key Data Classes**
- `Dataset` (`bytesep/data/data_modules.py`) - Loads audio segments from HDF5 with mix-augmentation
- `SegmentSampler` (`bytesep/data/samplers.py`) - Samples segment indices for training batches
- `BatchDataPreprocessor` (`bytesep/data/batch_data_preprocessors.py`) - Formats batch data into `input_dict`/`target_dict`

**Separation (`bytesep/separator.py`)**
- `Separator` class handles inference on long audio
- Chunks audio into overlapping segments with 50% overlap
- Uses windowing to reconstruct full audio from segments

### YAML Config Structure

Training configs follow this structure:
```yaml
task_name: musdb18
train:
    input_source_types: ['vocals', 'accompaniment']
    target_source_types: ['vocals']
    sample_rate: 44100
    segment_seconds: 3.0
    model_type: ResUNet143_DecouplePlusInplaceABN_ISMIR2021
    loss_type: l1_wav
    batch_size: 16
    learning_rate: 1e-3
```

### Key Design Patterns

- **Model factory pattern**: `get_model_class(model_type)` dynamically imports model classes
- **Dict-based I/O**: Models accept and return `{'waveform': tensor}` dictionaries
- **Subband processing**: Subband models use `pqmf.analysis()` and `pqmf.synthesis()` with STFT for magnitude/phase estimation
- **Loss composition**: Losses combine time-domain and frequency-domain objectives
- **Mixed-precision support**: Training configs specify `precision: 32` (or 16)

### Output Directories

When training, outputs are saved to:
- Checkpoints: `$WORKSPACE/checkpoints/<task>//config=...`
- Logs: `$WORKSPACE/logs/<task>//config=...`
- TensorBoard: `$WORKSPACE/tensorboard_logs/<task>//`
- Statistics: `$WORKSPACE/statistics/<task>//config=.../statistics.pkl`