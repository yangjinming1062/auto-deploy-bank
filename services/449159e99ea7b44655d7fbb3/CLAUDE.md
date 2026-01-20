# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

YOLOU is a unified YOLO (You Only Look Once) object detection framework that aggregates multiple YOLO variants for learning and deployment purposes. The name "U" stands for United - it consolidates various YOLO algorithms into a single codebase.

### Supported Model Architectures (--mode flag)

- **Anchor-base**: YOLOv3, YOLOv4, YOLOv5, YOLOv5-Lite, YOLOv7
- **Anchor-free**: YOLOv6, YOLOX, YOLOX-Lite
- **Face detection**: YOLOFaceV2
- **Lightweight models**: YOLO-FastestV2, FastestDet

## Commands

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Training
```bash
python train.py --mode yolov6 --data coco.yaml --cfg yolov6.yaml --weights yolov6.pt --batch-size 32
```

Default mode is `yolofacev2`. Key training arguments:
- `--mode` - Model architecture (yolo, yolov7, yolox, yolov6, yolo-fasterV2, FastestDet, yolofacev2)
- `--data` - Dataset YAML path
- `--cfg` - Model config YAML path
- `--weights` - Pretrained weights path
- `--epochs` - Training epochs (default: 100)
- `--batch-size` - Batch size (default: 16)
- `--device` - CUDA device (0 or cpu)
- `--resume` - Resume training from last checkpoint

### Detection/Inference
```bash
python detect.py --source 0  # webcam
python detect.py --source file.jpg  # image
python detect.py --source file.mp4  # video
python detect.py --source path/  # directory
python detect.py --source 'https://youtu.be/NUsoVlDFqZg'  # YouTube URL
```

Key detection arguments:
- `--weights` - Model path
- `--conf-thres` - Confidence threshold (default: 0.55)
- `--iou-thres` - NMS IoU threshold (default: 0.65)
- `--view-img` - Display results window
- `--save-txt` - Save results to TXT files

### Validation
```bash
python val.py --weights yolov5s.pt --data coco.yaml --img 640
```

### Export Models
```bash
python export.py --weights ./weights/yolov6s.pt
```

Supports export to: PyTorch (.pt), TorchScript, ONNX, OpenVINO, TensorRT, CoreML, TensorFlow SavedModel, TFLite.

## Architecture

### Directory Structure
- `models/` - Model architecture definitions (yolo.py is the main Model class)
- `utils/` - Core utilities
  - `loss.py` - Loss functions for different YOLO variants
  - `metrics.py` - mAP, IoU, confusion matrix calculations
  - `dataloaders.py` - Data loading and augmentation
  - `general.py` - NMS, image scaling, coordinate conversion utilities
  - `plots.py` - Visualization and annotation
  - `torch_utils.py` - Training utilities (EMA, AMP, model fusion)
- `data/` - Dataset configurations and hyperparameters
  - `hyps/` - Hyperparameter files (hyp.scratch.yaml, hyp.scratch-facev2.yaml, etc.)

### Model Loading Pattern
All models inherit from `nn.Module` and use a YAML configuration file. The main entry point is `models/yolo.py::Model` which:
1. Parses YAML config to build the network architecture
2. Supports multiple detection heads (Detect, DetectX, Detectv6, DetectFaceV2, etc.)
3. Handles both anchor-based and anchor-free detection

### Loss Computation
Different modes use different loss functions defined in `utils/loss.py`:
- `ComputeLoss` - Standard YOLO loss
- `ComputeLossOTA` - Optimal Transport Assignment (YOLOv7)
- `ComputeXLoss` - YOLOX loss
- `Computev6Loss` - YOLOv6 loss
- `ComputeFaceV2Loss` - YOLOFaceV2 with Repulsion Loss

### Data Format
Standard YOLO format:
```
data/
  images/
    train2017/
    val2017/
  labels/
    train2017/
    val2017/
```
Labels are TXT files with format: `class_id center_x center_y width height` (normalized 0-1).

## Key Implementation Details

- **DetectMultiBackend** (`models/common.py`) - Unified inference interface supporting PyTorch, TorchScript, ONNX, TensorRT, OpenVINO, and OpenCV DNN
- **Mixed Precision Training** - Automatic AMP support via `torch.cuda.amp.GradScaler`
- **Distributed Training** - DDP support with `torch.distributed`
- **Early Stopping** - Configurable patience via `--patience` argument