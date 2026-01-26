# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a TensorFlow 2.0 implementation of the **Music Transformer** (ICLR 2019) for generating music with long-term structure. The key innovation is using **Relative Global Attention** to reduce space complexity from O(N²D) to O(ND), allowing it to scale to musical sequences on the order of minutes.

**Paper:** [Music Transformer: Generating Music with Long-Term Structure](https://arxiv.org/abs/1809.04281)

## Commands

### Environment Setup
```bash
# Clone required midi-neural-processor dependency
git clone https://github.com/jason9693/midi-neural-processor.git
mv midi-neural-processor midi_processor

# Install dependencies
pip install -r requirements.txt
```

### Dataset Preprocessing
```bash
python preprocess.py {midi_load_dir} {dataset_save_dir}
```

### Training
```bash
python train.py --epochs={NUM_EPOCHS} --load_path={NONE_OR_LOADING_DIR} \
  --save_path={SAVING_DIR} --max_seq={SEQ_LENGTH} \
  --pickle_dir={DATA_PATH} --batch_size={BATCH_SIZE} --l_r={LEARNING_RATE}
```

**Default training command:**
```bash
python train.py --epochs=100 --save_path=result/dec0722 --pickle_dir=dataset/processed \
  --batch_size=10 --max_seq=2048 --num_layers=6
```

### Generating Music
```bash
python generate.py --load_path={CKPT_CONFIG_PATH} --length={GENERATE_SEQ_LENGTH} \
  --beam={NONE_OR_BEAM_SIZE} --save_path={OUTPUT_MIDI_PATH}
```

## Hyperparameters (from params.py)
- Sequence length: 2048
- Embedding dimension: 256
- Number of attention layers: 6
- Number of heads: 4 (d_model / 64)
- Learning rate: CustomSchedule with warmup (default) or specified value
- Batch size: 10 (overrides paper's batch size of 2)
- Dropout: 0.2

## Architecture

### Core Components

**Model Hierarchy (`model.py`):**
- `MusicTransformer` - Full encoder-decoder transformer (not recommended for music generation)
- `MusicTransformerDecoder` - **Primary model used** - Decoder-only with self-attention for AR music generation

**Attention Mechanism (`custom/layers.py`):**
- `RelativeGlobalAttention` - Key innovation implementing relative positional attention from the paper
- `DynamicPositionEmbedding` - Sinusoidal position embeddings added to token embeddings
- `EncoderLayer` / `DecoderLayer` - Transformer layers using RelativeGlobalAttention

**Data Pipeline (`data.py`):**
- `Data` class loads `.pickle` files from processed dataset directory
- Train/eval/test split: 80%/10%/10%
- Batching methods: `slide_seq2seq_batch()` is used for training (sliding window approach)

### Training Loop (`train.py`)
- Uses manual training loop with `train_on_batch()` and `evaluate()`
- TensorBoard logging with attention weight visualization
- Checkpoints saved every 100 batches with config.json and ckpt files

### Tokenization (midi_processor dependency)
- Converts MIDI files to event sequences
- Vocab size = RANGE_NOTE_ON + RANGE_NOTE_OFF + RANGE_TIME_SHIFT + RANGE_VEL + 3 (special tokens)
- Special tokens: SOS (start), EOS (end), PAD

## Key Files
- `model.py` - MusicTransformer and MusicTransformerDecoder classes
- `custom/layers.py` - Transformer layers including RelativeGlobalAttention
- `custom/callback.py` - CustomSchedule learning rate, loss functions
- `data.py` - Data loading and batching
- `utils.py` - Masking utilities, attention visualization, MIDI conversion
- `params.py` - Hyperparameters and vocab configuration
- `generate.py` - Music generation script with beam search support