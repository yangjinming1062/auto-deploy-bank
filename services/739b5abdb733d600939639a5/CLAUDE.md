# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository contains video preprocessing tools for the First Order Motion Model for Image Animation (NeurIPS 2019). It processes three datasets: **TaiChi**, **VoxCeleb**, and **UvaNemo** to produce cropped video sequences suitable for training image animation models.

## Dependencies

```bash
pip install -r requirements.txt
```

Additional requirements for specific scripts:
- **crop_vox.py** / **crop_nemo.py**: Requires [face-alignment](https://github.com/1adrianb/face-alignment) library
- **crop_taichi.py**: Requires [maskrcnn-benchmark](https://github.com/facebookresearch/maskrcnn-benchmark)
- **youtube-dl**: Required for downloading videos from YouTube
- **ffmpeg**: Required for video processing

## Common Commands

### Install Additional Dependencies

```bash
# Face alignment for face detection
git clone https://github.com/1adrianb/face-alignment
cd face-alignment && pip install -r requirements.txt && python setup.py install

# MaskRCNN for person detection (TaiChi)
# Follow install guide: https://github.com/facebookresearch/maskrcnn-benchmark/blob/master/INSTALL.md

# Download youtube-dl
wget https://yt-dl.org/downloads/latest/youtube-dl -O youtube-dl
chmod a+rx youtube-dl

# Install ffmpeg
sudo apt-get install ffmpeg
```

### Load Videos (All Datasets)

```bash
# TaiChi
python load_videos.py --metadata taichi-metadata.csv --format .mp4 --out_folder taichi --workers 8

# VoxCeleb
python load_videos.py --metadata vox-metadata.csv --format .mp4 --out_folder vox --workers 8
```

### Preprocessing

```bash
# VoxCeleb preprocessing (face detection + cropping)
python crop_vox.py --workers 40 --device_ids 0,1,2,3,4,5,6,7 --format .mp4 --dataset_version 2

# TaiChi preprocessing (person detection + keypoints + cropping)
python crop_taichi.py --workers 40 --device_ids 0,1,2,3,4,5,6,7 --format .mp4

# Nemo preprocessing (face detection + cropping)
python crop_nemo.py --in_folder /path/to/videos --out_folder nemo --device_ids 0,1 --workers 8 --format .mp4
```

## Architecture

### Dataset Processing Pipeline

Each dataset has a dedicated preprocessing script following a similar pattern:

1. **load_videos.py** - Downloads raw videos from YouTube and applies initial cropping using pre-annotated bounding boxes from CSV metadata
2. **crop_[dataset].py** - Refines crop using ML-based detection (face-alignment or MaskRCNN), splits into segments, and saves processed output

### Shared Utilities (util.py)

- `crop_bbox_from_frames()` - Crops video frames using bounding box with aspect ratio preservation
- `bb_intersection_over_union()` - IoU calculation for tracking
- `join()` - Merges bounding boxes across frames into a "tube"
- `compute_aspect_preserved_bbox()` - Expands bounding box while maintaining aspect ratio
- `scheduler()` - Parallel execution wrapper using multiprocessing.Pool
- `save()` - Saves frames as .mp4 or sequence of .png files

### Model Wrappers

- **maskrcnn.py** - Wrapper around maskrcnn-benchmark for person detection with keypoint support (used by crop_taichi.py)
- Face alignment is called directly from the `face_alignment` library in crop_vox.py and crop_nemo.py

### Data Flow

```
Metadata CSV → load_videos.py → Raw Videos → crop_[dataset]..py → Cropped Dataset (train/test)
                                                                 ↓
                                                        metadata CSV output
```

### Key Configurations

- **Reference FPS**: 25 (Vox, TaiChi), 50 (Nemo)
- **Reference frame size**: 360p (Vox), variable (TaiChi), 360x640 (Nemo)
- **Image shape**: Default (256, 256) for output crops
- **Output formats**: .mp4 (lossy, smaller) or .png (lossless, larger I/O)