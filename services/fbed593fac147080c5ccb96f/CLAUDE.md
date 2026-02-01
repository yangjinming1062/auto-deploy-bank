# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

M3-Agent is a multimodal agent framework with long-term memory for video understanding. It processes video and audio streams to build entity-centric multimodal memory graphs, then answers questions through iterative reasoning and memory retrieval.

## Build & Development Commands

```bash
# Install dependencies
bash setup.sh
pip install git+https://github.com/huggingface/transformers@f742a644ca32e65758c3adb36225aef1731bd2a8
pip install qwen-omni-utils==0.0.4

# Control pipeline dependencies (alternative)
pip install transformers==4.51.0
pip install vllm==0.8.4
pip install numpy==1.26.4

# Run memorization pipeline (generate memory graphs from videos)
python m3_agent/memorization_memory_graphs.py --data_file data/data.jsonl

# Run control pipeline (question answering with memory retrieval)
python m3_agent/control.py --data_file data/annotations/robot.json

# Visualize memory graph for a specific clip
python visualization.py --mem_path data/memory_graphs/robot/bedroom_01.pkl --clip_id 1
```

## Architecture

M3-Agent operates through two parallel processes:

### Memorization Process (`m3_agent/`)
Processes video/audio into structured memory graphs:
1. **Intermediate Outputs** (`memorization_intermediate_outputs.py`): Face detection and speaker diarization
2. **Memory Graphs** (`memorization_memory_graphs.py`): Generates episodic and semantic memories using M3-Agent-Memorization model

Key outputs stored in `data/memory_graphs/`: pickle files containing VideoGraph objects.

### Control Process (`m3_agent/control.py`)
Question answering through iterative reasoning:
1. Loads pre-built memory graphs
2. Generates search queries using M3-Agent-Control model
3. Retrieves relevant memories via vector similarity search
4. Synthesizes final answers from retrieved context

## Key Modules

### VideoGraph (`mmagent/videograph.py`)
Central data structure storing multimodal memory:
- **Node types**: `img` (faces), `voice` (speakers), `episodic` (event descriptions), `semantic` (high-level conclusions)
- **Character resolution**: Groups face/voice nodes into `character_N` entities via equivalence relationships
- **Memory retrieval**: Cosine similarity search over text node embeddings

### Memory Retrieval (`mmagent/retrieve.py`)
- `search()`: Vector similarity search over text memories
- `back_translate()`: Expands queries using character ID mappings
- `translate()`: Converts character IDs to names in retrieved memories

### Processing Modules
- `face_processing.py`: Face detection and embedding
- `voice_processing.py`: Speaker diarization and voice embedding
- `memory_processing.py`: Memory parsing and entity extraction
- `memory_processing_qwen.py`: Qwen2.5-Omni based memory generation

## Configuration

All configs are JSON files in `configs/`:
- `processing_config.json`: Processing parameters (fps, thresholds, batch sizes)
- `memory_config.json`: Graph parameters (max embeddings, similarity thresholds)
- `api_config.json`: API keys for GPT-4o, Gemini, and embedding models

## Data Formats

**Input (data.jsonl)**:
```json
{"id": "bedroom_01", "video_path": "...", "clip_path": "...", "mem_path": "...", "intermediate_path": "..."}
```

**Memory Graph**: Pickled VideoGraph with nodes and edges for faces, voices, and text memories organized by clip ID.

## Important Patterns

- Character references use IDs like `<face_1>`, `<voice_2>`, `<character_0>` which must be translated to names during retrieval
- Search queries support `CLIP_x` syntax for temporal filtering
- Memory truncation via `truncate_memory_by_clip()` enables time-limited reasoning
- `refresh_equivalences()` re-computes character mappings after graph modifications