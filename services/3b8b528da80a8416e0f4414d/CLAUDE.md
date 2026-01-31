# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MegaTTS3 is a zero-shot text-to-speech (TTS) synthesis system by ByteDance. It uses a latent diffusion transformer architecture with voice cloning capabilities from short reference audio clips.

## Build Commands

```bash
# Python 3.10 required
conda create -n megatts3-env python=3.10
conda activate megatts3-env

# Install dependencies
pip install -r requirements.txt

# Set root directory for Python imports
export PYTHONPATH="/path/to/MegaTTS3:$PYTHONPATH"

# Optional: Set GPU device
export CUDA_VISIBLE_DEVICES=0

# Required for multiprocessing
export TOKENIZERS_PARALLELISM=false
```

**Note:** If you encounter pydantic version conflicts with gradio, check version compatibility.

## Run Commands

**Command-line inference:**
```bash
python tts/infer_cli.py --input_wav 'path/to/prompt.wav' --input_text "Text to synthesize" --output_dir ./gen
```

Key parameters:
- `--time_step`: Inference steps (default 32, more steps = higher quality but slower)
- `--p_w`: Intelligibility weight (default 1.6, higher = clearer pronunciation)
- `--t_w`: Similarity weight (default 2.5, higher = more similar to reference voice)

**Accent control:**
- `p_w=1.0` with `t_w=3.0`: Retain original accent
- `p_w=2.5` with `t_w=2.5`: Shift toward standard pronunciation

**Language support:** Auto-detected (Chinese/English). Text is normalized before synthesis.

**Web UI:**
```bash
python tts/gradio_api.py
# Visit http://127.0.0.1:7860/ for gradio interface
```

## Architecture

The TTS pipeline consists of 5 stages:

1. **Prompt Preprocessing** (`infer_cli.py:preprocess()`)
   - Loads reference audio via librosa (24kHz)
   - Extracts voice latents using WaveVAE encoder (25 Hz latents)
   - Gets phoneme alignments from Whisper aligner
   - Creates duration prompt for context

2. **Text Normalization** (`infer_cli.py`)
   - Language detection via `langdetect`
   - Chinese: uses `tn.chinese.normalizer`
   - English: uses `tn.english.normalizer`
   - Text chunking: Chinese (~60 chars), English (~130 chars)

3. **Speech-Text Alignment** (`frontend_function.py:align()`)
   - Whisper Small encoder extracts audio features (16kHz)
   - Autoregressive phoneme prediction with EOS token
   - Outputs: ph_ref, tone_ref, mel2ph_ref

4. **Duration Prediction** (`frontend_function.py:dur_pred()`)
   - AR duration model predicts phoneme durations for target text
   - Uses KV cache from prompt for context (efficiency)
   - Supports duration disturbance (`dur_disturb`) and scaling (`dur_alpha`)

5. **Diffusion Transformer** (`modules/llm_dit/dit.py`)
   - Main speech synthesis model (0.45B parameters, 24 layers, 1024 dim)
   - Uses Conditional Flow Matching (CFM) with AMO sampling
   - Classifier-free guidance (CFG) with phone/similarity weights
   - Generates acoustic latents at 25 Hz

6. **WaveVAE Decoder** (`modules/wavvae/decoder/wavvae_v3.py`)
   - Reconstructs 24kHz audio from latents
   - V3 model includes encoder for latent extraction
   - Post-processing: loudness normalization to match prompt

## Key Modules

| Module | Location | Purpose |
|--------|----------|---------|
| Diffusion | `tts/modules/llm_dit/dit.py` | Latent diffusion transformer with CFM |
| AR Duration | `tts/modules/ar_dur/ar_dur_predictor.py` | Autoregressive duration prediction |
| WaveVAE | `tts/modules/wavvae/` | Audio codec encoder/decoder |
| Aligner | `tts/modules/aligner/whisper_small.py` | Whisper-based speech aligner |
| G2P Model | HuggingFace Qwen2.5-0.5B | Grapheme-to-phoneme conversion |
| Frontend | `tts/frontend_function.py` | G2P, alignment, duration pipeline |
| HParams | `tts/utils/commons/hparams.py` | YAML config loader with inheritance |

## Key Data Structures

- **Phone/tone tokens**: Phoneme sequences encoded as integers (phone_vocab ~302, tone_vocab ~32)
- **mel2ph**: Tensor mapping phonemes to time frames (compression ratio: 4:1 from audio to tokens)
- **vae_latent**: WaveVAE latents at 25 Hz (24kHz audio / 960)
- **resource_context**: Dict containing prompt embeddings and KV cache for inference

## Checkpoints

Models loaded from `./checkpoints/` directory:
- `diffusion_transformer/`: Main DiT model + config.yaml
- `aligner_lm/`: Whisper aligner + config.yaml
- `wavvae/`: WaveVAE decoder (+ encoder.ckpt if available)
- `duration_lm/`: Duration predictor + config.yaml
- `g2p/`: HuggingFace Qwen2.5-0.5B model

**Note:** WaveVAE encoder params not included. Use pre-extracted `.npy` latents (from Drive link in README).

## Docker

```bash
docker build . -t megatts3:latest
docker run -it -p 127.0.0.1:7929:7929 --gpus all -e CUDA_VISIBLE_DEVICES=0 megatts3:latest
```

## Configuration

Hyperparameters are defined in YAML config files within checkpoint directories. The `set_hparams()` function in `tts/utils/commons/hparams.py`:
- Loads and merges configs with support for inheritance via `base_config`
- Supports config overrides via `--hparams="key.subkey=value"`
- Stores final config in global `hparams` dict

Key hparams used:
- `win_size`: Audio window size for processing
- `frames_multiple`: Multiple for frame alignment
- `dur_code_size`: Duration token vocabulary size (128)
- `vae_stride`, `hop_size`: WaveVAE compression parameters

## Key Design Patterns

- **Global `hparams` dict**: Loaded configurations stored in `tts.utils.commons.hparams.hparams`
- **Checkpoint loading**: `load_ckpt()` in `ckpt_utils.py` handles distributed checkpoint loading with module stripping
- **KV caching**: Duration model uses incremental states for efficient autoregressive inference
- **Mixed precision**: Inference uses bfloat16/float16 with `torch.cuda.amp.autocast`
- **Segment processing**: Long texts are chunked, processed separately, then concatenated

## Limitations

- Reference audio must be < 24 seconds and in .wav format
- WaveVAE encoder parameters not included (use pre-extracted `.npy` latents)
- CPU inference ~30s for 32 steps (GPU recommended)
- `no_proxy` env var with `::` pattern causes httpx issues
- Windows: requires `pynini==2.1.5` via conda-forge, WeTextProcessing==1.0.3