# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
DiffSinger is a PyTorch implementation of singing voice synthesis (SVS) and text-to-speech (TTS) using a shallow diffusion mechanism. The project supports multiple model variants:
- **DiffSpeech** (TTS): Text → Mel → Waveform
- **DiffSinger** (SVS): Lyrics + F0/MIDI → Mel → Waveform with various configurations (PopCS, OpenCpop)

## Architecture
The codebase is organized as a PyTorch Lightning-based training framework with modular components:

### Core Directories
- **`modules/`** - Neural network model implementations
  - `commons/` - Shared utilities and base classes
  - `diffsinger_midi/` - MIDI processing components
  - `fastspeech/` - FFT-based TTS models
  - `hifigan/` & `parallel_wavegan/` - Vocoder implementations
- **`tasks/`** - Task definitions and entry points
  - `base_task.py` - PyTorch Lightning training loop and orchestration
  - `run.py` - Main entry point that loads configs and runs tasks
- **`configs/`** - YAML configuration files
  - `tts/` - DiffSpeech configurations
  - `singing/` - DiffSinger configurations (base.yaml, fs2.yaml)
  - `config_base.yaml` - Base configuration template
- **`data_gen/`** - Data preprocessing and binarization
- **`usr/`** - Additional task-specific configurations
- **`inference/`** - Inference scripts for raw input synthesis

### Configuration System
The project uses hierarchical YAML configurations:
1. Base config (`configs/config_base.yaml`) defines global training parameters
2. Task-specific configs inherit from base and override/add parameters
3. Configs specify: model architecture, dataset paths, hyperparameters, training settings

Configuration parameters are loaded via `utils/hparams.py` and accessed globally through `hparams` dictionary.

## Common Commands

### Environment Setup
```bash
# Option 1: Conda (recommended)
conda create -n diffsinger python=3.8
conda activate diffsinger
pip install -r requirements_2080.txt  # for GPU 2080Ti, CUDA 10.2
# or
pip install -r requirements_3090.txt  # for GPU 3090, CUDA 11.4

# Option 2: Python venv
python -m venv venv
source venv/bin/activate
pip install -U pip
pip install Cython numpy==1.19.1
pip install torch==1.9.0
pip install -r requirements.txt
```

### Data Preparation
```bash
# Binarize dataset for training
export PYTHONPATH=.
python data_gen/tts/bin/binarize.py --config <config_path>
# Example:
python data_gen/tts/bin/binarize.py --config usr/configs/midi/cascade/opencs/aux_rel.yaml
```

### Training
```bash
# Train a model (training mode)
python tasks/run.py --config <config_path> --exp_name <experiment_name> --reset

# Example - Train FFT-Singer:
python tasks/run.py --config usr/configs/midi/cascade/opencs/aux_rel.yaml --exp_name 0302_opencpop_fs_midi --reset

# Example - Train DiffSinger:
python tasks/run.py --config usr/configs/midi/cascade/opencs/ds60_rel.yaml --exp_name 0303_opencpop_ds58_midi --reset
```

### Inference
```bash
# Infer from packed test set
python tasks/run.py --config <config_path> --exp_name <experiment_name> --infer

# Example:
python tasks/run.py --config usr/configs/midi/cascade/opencs/ds60_rel.yaml --exp_name 0303_opencpop_ds58_midi --infer
# Results saved in: ./checkpoints/<exp_name>/generated_*

# Infer from raw inputs (interactive)
python inference/svs/ds_cascade.py --config <config_path> --exp_name <experiment_name>
# Results saved in: ./infer_out
```

### Monitoring
```bash
# Start TensorBoard
tensorboard --logdir_spec exp_name
# View at http://localhost:6006
```

## Key Configuration Details

### Base Training Parameters (`configs/config_base.yaml`)
- `work_dir` - Experiment directory (default: checkpoints/)
- `infer` - Set to `false` for training, `true` for inference
- `load_ckpt` - Path to checkpoint for resuming/finetuning
- `save_ckpt` - Whether to save checkpoints
- `max_epochs` / `max_updates` - Training termination criteria
- `num_sanity_val_steps` - Validation steps at training start

### Dataset Configuration
Each task config specifies:
- `binarizer_cls` - Data preprocessing class (e.g., `data_gen.singing.binarize.SingingBinarizer`)
- `pre_align_cls` - Alignment preprocessing class
- `hop_size`, `fft_size`, `win_size` - Audio processing parameters
- Dataset paths and preprocessing options

## Model Variants

### SVS Models (docs/README-SVS.md)
1. **PopCS version** (Ground-truth F0 required)
   - `docs/README-SVS-popcs.md`
   - Pipeline: Lyrics → Linguistic → Mel (with GT F0) → Waveform

2. **OpenCpop Cascade** (MIDI → F0 prediction)
   - `docs/README-SVS-opencpop-cascade.md`
   - Pipeline: Lyrics + MIDI → F0 + Duration → Mel → Waveform

3. **OpenCpop E2E** (End-to-end, no explicit F0 prediction)
   - `docs/README-SVS-opencpop-e2e.md`
   - Pipeline: Lyrics + MIDI → Duration → Mel → (Pitch Extractor) → Waveform

4. **PNDM Acceleration**
   - `docs/README-SVS-opencpop-pndm.md`
   - Uses PNDM solver for faster sampling

### TTS Models (docs/README-TTS.md)
- **DiffSpeech** - Text → Mel → Waveform using shallow diffusion
- **DiffSpeech + PNDM** - Accelerated version

## Vocoders
The project uses separate vocoder models trained independently:
- **HiFiGAN** - For TTS (DiffSpeech)
- **NSF-HiFiGAN** - For SVS (DiffSinger), includes NSF mechanism for pitch conditioning

Pretrained vocoders must be placed in `checkpoints/` directory before training/inference. See `docs/README-SVS-opencpop-cascade.md` for download links.

## Data Flow
1. **Preprocessing**: Raw audio/text/MIDI → Binarized HDF5 files
2. **Training**: Binarized data → PyTorch Lightning training loop
3. **Inference**: Trained model → Mel spectrograms → Waveform (via vocoder)

## Important Notes
- GPU memory requirements: Varies by model size and batch size; check GPU compatibility via requirements files
- Dataset licensing: OpenCpop requires separate download following their instructions
- Multi-GPU: Controlled via `CUDA_VISIBLE_DEVICES` environment variable
- Checkpoints: Saved in `checkpoints/<exp_name>/` with automatic versioning
- Pre-trained models: Available in releases; place in `checkpoints/` before use