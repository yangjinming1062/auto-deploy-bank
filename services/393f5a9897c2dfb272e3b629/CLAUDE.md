# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LLMVoX is a lightweight 30M-parameter, LLM-agnostic autoregressive streaming Text-to-Speech system. It converts LLM text outputs into high-fidelity streaming speech with low latency (~300ms). The architecture uses a multi-queue approach with two TTS model replicas for continuous low-latency speech generation.

## Setup and Installation

```bash
# Create conda environment
conda create -n llmvox python=3.9
conda activate llmvox

# Install PyTorch with CUDA 11.8
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install Flash Attention
pip install flash-attn --no-build-isolation

# Install dependencies
pip install -r requirements.txt

# Required: Add WavTokenizer to PYTHONPATH (contains audio tokenizer models)
export PYTHONPATH=./WavTokenizer/:$PYTHONPATH

# Download checkpoints to CHECKPOINTS/ directory:
# - wavtokenizer_large_speech_320_24k.ckpt
# - ckpt_english_tiny.pt
#
# Update paths in configs/inference_config.py before running:
# - wav_model_path: Path to WavTokenizer checkpoint
# - llmvox_checkpoint_path: Path to LLMVoX model checkpoint
```

## Common Commands

### Training

```bash
# Single GPU training
python train.py --batch_size=8 --learning_rate=5e-5 --n_layer=6

# Distributed training (4 GPUs)
torchrun --standalone --nproc_per_node=4 train.py --batch_size=16

# Custom training with all parameters
python train.py \
  --n_layer=4 --n_head=8 --n_embd=768 \
  --data_path="/path/to/dataset.json" \
  --speech_data_folder="/path/to/audio_files" \
  --wav_config_path="WavTokenizer/configs/wavtokenizer_smalldata_frame75_3s_nq1_code4096_dim512_kmeans200_attn.yaml" \
  --wav_model_path="/path/to/wavtokenizer_large_speech_320_24k.ckpt" \
  --out_dir="my_llmvox_model" \
  --compile=True --wandb_log=True
```

### Running the Streaming Server

```bash
# Voice chat (ASR speech input → LLM → TTS streaming audio)
python streaming_server.py --chat_type voice --llm_checkpoint "meta-llama/Llama-3.1-8B-Instruct" --eos_token "<|eot_id|>"

# Text chat only (text input → LLM → TTS)
python streaming_server.py --chat_type text --llm_checkpoint "meta-llama/Llama-3.1-8B-Instruct"

# Visual speech (voice + image → VLM → TTS)
python streaming_server.py --chat_type visual_speech --llm_checkpoint "Qwen/Qwen2.5-VL-7B-Instruct"

# Multimodal chat (voice + images for native multimodal LLMs)
python streaming_server.py --chat_type multimodal --llm_checkpoint "microsoft/Phi-4-multimodal-instruct"
```

**chat_type options**: `text`, `voice`, `visual_speech`, `multimodal`

### GPU Resource Allocation

```bash
# Run TTS models on separate GPUs
python streaming_server.py --chat_type voice --llm_checkpoint "meta-llama/Llama-3.1-8B-Instruct" --tts_device_1 1 --tts_device_2 2

# Specify LLM device separately
python streaming_server.py --chat_type voice --llm_checkpoint "meta-llama/Llama-3.1-8B-Instruct" --llm_device "cuda:0" --tts_device_1 1 --tts_device_2 2
```

### Streaming Quality/Latency Tuning

```bash
# Lower latency (faster first response, ~300ms): smaller initial chunks
python streaming_server.py --chat_type voice --llm_checkpoint "meta-llama/Llama-3.1-8B-Instruct" --initial_dump_size_1 5 --initial_dump_size_2 40 --max_dump_size 320

# Higher quality (better speech): larger chunks
python streaming_server.py --chat_type voice --llm_checkpoint "meta-llama/Llama-3.1-8B-Instruct" --initial_dump_size_1 20 --initial_dump_size_2 320 --max_dump_size 2560
```

- `initial_dump_size_1`: First audio chunk tokens (smaller = faster initial response)
- `initial_dump_size_2`: Second model initial chunk (larger, runs in parallel)
- `max_dump_size`: Maximum chunk size for quality vs latency tradeoff

### Running Demo UI

```bash
# First start the streaming server
python streaming_server.py --chat_type voice --llm_checkpoint "meta-llama/Llama-3.1-8B-Instruct" --api_port 5003

# Then start the UI
python run_ui.py --ip STREAMING_SERVER_IP --port PORT
```

## Architecture

### Multi-Queue Streaming (Core Innovation)

LLMVoX uses **two TTS model replicas** that alternate processing text chunks at sentence boundaries. This enables:
- Continuous audio playback (no gaps)
- End-to-end latency as low as 300ms
- Infinite-length dialogue support

The producer-consumer pattern:
1. LLM runs in a separate thread, streaming tokens
2. Tokens are accumulated until sentence boundary (`.`)
3. Chunks alternate between two TTS model queues
4. Audio plays while next chunk generates

### Core Model Components (`src/model.py`)

- **GPT**: GPT-2 style transformer based on NanoGPT with causal self-attention
- **CausalSelfAttention**: Supports Flash Attention (PyTorch 2.0+) and traditional attention; includes KV cache for inference
- **Block**: Transformer block with layer norm, attention, and MLP
- **KV Cache**: Used during inference for efficient autoregressive generation

### Data Processing (`src/data.py`)

- **SpeechDataset**: Loads audio/text pairs, tokenizes speech using WavTokenizer, processes text with ByT5 tokenizer
- **SpeechDataCollator**: Pads sequences for batching
- Audio is encoded to discrete tokens via WavTokenizer (~40-75 tokens/sec)
- Special tokens: PAD_TOKEN_ID=384, EOA_TOKEN_ID=453 (End of Audio)

### Inference System (`inference/`)

- **model_handler.py**: Initializes WavTokenizer, ByT5 encoder embeddings, and GPT speech decoder on specified devices
- **llm_streaming.py**: Wraps LLMs with TextIteratorStreamer for token-by-token output; customize for new LLMs
- **asr.py**: Whisper-based ASR for converting speech input to text
- **vlm_streaming.py**: Vision-language model streaming for `visual_speech` mode
- **multimodal_streaming.py**: Multimodal streaming for models like Phi-4-multimodal-instruct

To add support for a new LLM, create a custom streamer in `inference/` following the pattern in `llm_streaming.py`.

### Streaming Server (`streaming_server.py`)

FastAPI-based server with multi-queue architecture:
- **text_streamer_producer**: Runs LLM in thread, routes tokens to alternating TTS queues
- **audio_generator_sync**: Two instances generate audio chunks in parallel
- **Model alternation**: Queues switch at sentence boundaries (`.` token) for latency/quality balance
- **API endpoints**: `/tts`, `/voicechat`, `/multimodalchat`, `/vlmschat`

### Key Configuration Files

- `configs/train_config.py`: Training hyperparameters, model architecture, paths
- `configs/inference_config.py`: Runtime settings, chat_type, device assignments, tokens

## Token Flow (Autoregressive)

```
Input Text → ByT5 Embeddings → [Text + Previous Audio Tokens] → GPT Decoder
                                                                   ↓
                                                            Logits → Argmax
                                                                   ↓
                                                            Audio Token IDs
                                                                   ↓
                                                            WavTokenizer Decode → Audio Waveform
```

The model generates audio tokens one at a time, autoregressively. Each audio token represents ~25ms of speech (40-75 tokens/second at 24kHz).

## Dataset Format

JSON file with entries:
```json
[
  {
    "speech_folder": "/path/to/audio/files",
    "speech_file": "audio1.wav",
    "answer_text": "Text transcript",
    "id": "unique_id"
  }
]
```

## Special Tokens

- **Text EOS**: Model-specific end-of-sequence token:
  - LLaMA: `<|eot_id|>`
  - Mistral: `<|im_end|>`
  - Phi-4: `<|end|>`
- **EOA (End of Audio)**: 453 - signals audio generation complete
- **PAD**: 384 - padding token for batching

## ASR Configuration (Whisper)

```bash
# Use larger model for better transcription
python streaming_server.py --chat_type voice --llm_checkpoint "meta-llama/Llama-3.1-8B-Instruct" --asr_model "medium"

# Smaller model for speed
python streaming_server.py --chat_type voice --llm_checkpoint "meta-llama/Llama-3.1-8B-Instruct" --asr_model "tiny" --asr_device "cuda:0"
```