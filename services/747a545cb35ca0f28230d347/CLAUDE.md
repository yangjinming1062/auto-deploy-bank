# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ByteTrack is a multi-object tracking (MOT) library built on top of YOLOX. It associates every detection box (including low-score ones) to track objects across video frames.

**Tech Stack**: Python 3.6+, PyTorch 1.7+, YOLOX detection framework

## Development Commands

### Demo
```bash
# Video demo
python3 tools/demo_track.py video -f exps/example/mot/yolox_x_mix_det.py -c pretrained/bytetrack_x_mot17.pth.tar --fp16 --fuse --save_result
```

### Installation
```bash
pip3 install -r requirements.txt
python3 setup.py develop

# Additional dependencies
pip3 install cython
pip3 install 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
pip3 install cython_bbox
```

### Training
```bash
# Ablation model (CrowdHuman + MOT17 half train)
python3 tools/train.py -f exps/example/mot/yolox_x_ablation.py -d 8 -b 48 --fp16 -o -c pretrained/yolox_x.pth

# Full MOT17 model
python3 tools/train.py -f exps/example/mot/yolox_x_mix_det.py -d 8 -b 48 --fp16 -o -c pretrained/yolox_x.pth

# MOT20 model (requires clipping bounding boxes in data_augment.py, mosaicdetection.py, boxes.py)
python3 tools/train.py -f exps/example/mot/yolox_x_mix_mot20_ch.py -d 8 -b 48 --fp16 -o -c pretrained/yolox_x.pth

# Custom dataset - first convert data to COCO format, create Exp file, then:
python3 tools/train.py -f exps/example/mot/your_exp_file.py -d 8 -b 48 --fp16 -o -c pretrained/yolox_x.pth
```

### Tracking & Evaluation
```bash
# Track on MOT17 half val
python3 tools/track.py -f exps/example/mot/yolox_x_ablation.py -c pretrained/bytetrack_ablation.pth.tar -b 1 -d 1 --fp16 --fuse

# Track on MOT17 test set (run interpolation afterward for final results)
python3 tools/track.py -f exps/example/mot/yolox_x_mix_det.py -c pretrained/bytetrack_x_mot17.pth.tar -b 1 -d 1 --fp16 --fuse
python3 tools/interpolation.py

# Track on MOT20 (uses different input sizes per sequence)
python3 tools/track.py -f exps/example/mot/yolox_x_mix_mot20_ch.py -c pretrained/bytetrack_x_mot20.pth.tar -b 1 -d 1 --fp16 --fuse --match_thresh 0.7 --mot20
python3 tools/interpolation.py

# MOT20 requires special handling: clip bounding boxes inside image boundaries
# (add clip operations in data_augment.py, mosaicdetection.py, boxes.py - see README)
```

### Data Conversion
```bash
python3 tools/convert_mot17_to_coco.py
python3 tools/convert_mot20_to_coco.py
python3 tools/convert_crowdhuman_to_coco.py
python3 tools/convert_cityperson_to_coco.py
python3 tools/convert_ethz_to_coco.py
python3 tools/mix_data_ablation.py      # Mix CrowdHuman + MOT17 half
python3 tools/mix_data_test_mot17.py     # Mix CrowdHuman + MOT17 + Cityperson + ETHZ
python3 tools/mix_data_test_mot20.py     # Mix CrowdHuman + MOT20
```

### Code Quality
```bash
flake8 .  # Uses setup.cfg settings (max-line-length=100, max-complexity=18)
isort .   # Uses setup.cfg import ordering
```

## Architecture

### BYTETrack Algorithm
The core innovation is **two-stage association**:
1. **First association**: Match high-score detections (above `track_thresh`) to existing tracks using IoU distance + Kalman filter prediction
2. **Second association**: Match remaining low-score detections to remaining tracks to recover occluded objects

Key classes in `yolox/tracker/byte_tracker.py`:
- `BYTETracker`: Main tracker class initialized with args (frame_rate, track_thresh, track_buffer)
- `STrack`: Single tracklet with Kalman filter state (mean, covariance) and prediction/update methods
- `KalmanFilter`: Motion prediction using constant velocity model
- `matching.py`: IoU distance calculation and linear assignment (Hungarian algorithm)

### Exp File System
Experiments are configured via Python classes inheriting from `yolox.exp.Exp` (or `BaseExp`). All hyperparameters, model definitions, and data loaders are defined here:

Key methods to override:
- `get_data_loader(batch_size, is_distributed, no_aug)`: Returns training DataLoader with MosaicDetection
- `get_eval_loader(batch_size, is_distributed, testdev)`: Returns evaluation DataLoader
- `get_evaluator(batch_size, is_distributed, testdev)`: Returns COCO/MOT evaluator

Key attributes to set:
- `self.num_classes`: Number of detection classes (1 for MOT)
- `self.depth`, `self.width`: Model scaling factors
- `self.input_size`, `self.test_size`: Image dimensions
- `self.max_epoch`: Training epochs
- `self.basic_lr_per_img`: Learning rate per image
- `self.train_ann`, `self.val_ann`: COCO annotation files

### Directory Structure

| Directory | Purpose |
|-----------|---------|
| `yolox/` | Core library code |
| `yolox/models/` | YOLOX network architectures (backbone, neck, head) |
| `yolox/tracker/` | BYTETracker implementation (`byte_tracker.py`) |
| `yolox/data/` | Dataset handling, data loading, augmentations |
| `yolox/core/` | Training and inference engines |
| `yolox/evaluators/` | MOT evaluation logic |
| `yolox/layers/` | Custom CUDA/C++ layers |
| `exps/` | Experiment configuration files |
| `tools/` | CLI tools (train.py, track.py, demo_track.py, etc.) |
| `deploy/` | Deployment configs (ONNX, TensorRT, ncnn, DeepStream) |
| `datasets/` | User-provided datasets in COCO format |

### Key Components

**BYTETracker** (`yolox/tracker/byte_tracker.py`): Core tracking algorithm that associates detection boxes with tracklets. Uses both high and low score detections to recover true objects and filter background.

**Data Pipeline**: Raw datasets → COCO format conversion → `mix_data_*.py` scripts to merge datasets → `MOTDataset` class for loading → `MosaicDetection` for augmentation → training loop

## Coding Standards

Linting and import sorting are configured in `setup.cfg`:
- **flake8**: max-line-length=100, max-complexity=18
- **isort**: line_length=100, custom category order (see setup.cfg for full list)

## Dataset Organization

Datasets must be placed in `datasets/` and converted to COCO format:
```
datasets/
  ├── mot/
  │    ├── train/
  │    └── test/
  ├── MOT20/
  ├── crowdhuman/
  │    ├── Crowdhuman_train/
  │    ├── Crowdhuman_val/
  │    ├── annotation_train.odgt
  │    └── annotation_val.odgt
  └── ...
```

Run conversion scripts, then `mix_data_*.py` scripts to create combined training sets in `datasets/mix_*` directories.

## Using BYTETracker with Other Detectors

```python
from yolox.tracker.byte_tracker import BYTETracker

tracker = BYTETracker(args)
for image in images:
    dets = detector(image)  # Format: x1, y1, x2, y2, score
    online_targets = tracker.update(dets, info_imgs, img_size)
```