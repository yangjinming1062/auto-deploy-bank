# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build, Lint, and Test Commands

```bash
# Install for development
make install  # Installs package in editable mode
make install-dev  # Installs test requirements

# Linting
make lint  # Run mypy, pylint, and black checks
make black  # Auto-format code with black (line length 120)

# Testing
make test  # Run all unit tests
make test TEST_ARGS="tests/test_subsamplers.py::test_audio_rate_subsampler"  # Run specific test
```

## Architecture Overview

video2dataset is a tool for downloading and processing large video datasets. The architecture follows a pipeline pattern with configurable components:

### Core Pipeline

1. **Input Sharding** (`input_sharder.py`, `output_sharder.py`): Reads input data (CSV, parquet, JSON, TXT, webdataset) and shards it into batches for processing.

2. **Distribution** (`distributor.py`): Parallelizes work across compute resources:
   - `multiprocessing_distributor`: Spawns process pool for single-machine parallelism
   - `pyspark_distributor`: Distributes across Spark cluster nodes
   - `SlurmDistributor`: Distributes across SLURM cluster nodes

3. **Workers** (`workers/`): Process one shard at a time:
   - `DownloadWorker`: Downloads videos from URLs using yt-dlp
   - `SubsetWorker`: Re-processes existing webdataset tar files
   - `OpticalFlowWorker`: Computes optical flow for videos
   - `CaptionWorker`: Generates captions using BLIP-2
   - `WhisperWorker`: Transcribes audio using Whisper

4. **Subsamplers** (`subsamplers/`): Transform video/audio streams (inherit from `Subsampler` base class):
   - `ResolutionSubsampler`: Resize/scale/crop/pad videos
   - `FrameSubsampler`: Extract frames at specified FPS
   - `CutDetectionSubsampler`: Detect scene cuts using scenedetect
   - `ClippingSubsampler`: Split videos into clips based on cuts or timestamps
   - `FFProbeSubsampler`: Extract video metadata via ffprobe
   - `AudioRateSubsampler`: Resample audio
   - `OpticalFlowSubsampler`: Compute optical flow
   - `WhisperSubsampler`: Transcribe audio with Whisper
   - `CaptionSubsampler`: Generate captions with BLIP-2

5. **Data Writers** (`data_writer.py`): Store processed samples:
   - `WebDatasetSampleWriter`: TAR files with .mp4, .txt, .json for each sample
   - `FilesSampleWriter`: Individual files per sample
   - `ParquetSampleWriter`: Columnar parquet format
   - `TFRecordSampleWriter`: TensorFlow protobuf format

### Configuration System

Configs are defined in `video2dataset/configs/` and contain four sections:
- **subsampling**: Chain of subsamplers and their args
- **reading**: Download parameters (yt_args, timeout) and dataloader options
- **storage**: Shard size, output format options
- **distribution**: Process/thread counts, distributor type

### Key Data Structures

- **Streams dict**: Passed between subsamplers, contains video/audio streams as bytes
- **Metadata dict**: Contains captions, URLs, cut timestamps, status, etc.
- **Sample**: Written to output as (video_file, caption_file, metadata_json)

### Filesystem Abstraction

All file I/O uses `fsspec` for protocol-agnostic access:
- `s3://`, `hdfs://`, `gcs://` for cloud storage
- Local filesystem for development

### Entry Point

The main `video2dataset()` function in `main.py` orchestrates the entire pipeline. The CLI entry point uses `fire`:
```bash
video2dataset --url_list="videos.csv" --output_folder="dataset"
```

### Key Dependencies

- `yt-dlp`: Video downloading (supports 1700+ sites)
- `decord`: Fast video decoding
- `scenedetect`: Scene cut detection
- `webdataset`: TAR-based dataset format
- `torch`/`torchdata`: Video/audio loading and processing
- `transformers`: BLIP-2 for captioning, Whisper for transcription
- `omegaconf`: YAML config parsing
- `wandb`: Metrics and progress logging