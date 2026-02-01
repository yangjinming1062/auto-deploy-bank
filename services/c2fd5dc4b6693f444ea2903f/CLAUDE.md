# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Video Depth Anything is a video depth estimation model based on Depth Anything V2. It performs consistent depth estimation for arbitrarily long videos using DINOv2 encoder + temporal DPT heads with motion modules. Supports both relative depth and metric depth modes.

## Common Commands

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Download pretrained checkpoints:**
```bash
bash get_weights.sh
```

**Run inference (standard mode):**
```bash
python3 run.py --input_video ./assets/example_videos/davis_rollercoaster.mp4 --output_dir ./outputs --encoder vitl
python3 run.py --input_video ./path/to/video.mp4 --output_dir ./outputs --encoder vits|vitb|vitl --metric
```

**Run inference (streaming mode - experimental, lower memory):**
```bash
python3 run_streaming.py --input_video ./assets/example_videos/davis_rollercoaster.mp4 --output_dir ./outputs_streaming --encoder vitl
```

**Gradio demo:**
```bash
python3 app.py
```

**Benchmark evaluation:**
```bash
# Inference on benchmark datasets
python3 benchmark/infer/infer.py --infer_path ${out_path} --json_file ${json_path} --datasets ${dataset}

# Evaluation scripts
bash benchmark/eval/eval_tae.sh ${out_path} benchmark/dataset_extract/dataset
bash benchmark/eval/eval.sh ${out_path} benchmark/dataset_extract/dataset
bash benchmark/eval/eval_500.sh ${out_path} benchmark/dataset_extract/dataset
```

## Architecture

```
VideoDepthAnything (main model)
├── DINOv2 encoder (pretrained vision transformer)
│   ├── vits: 28.4M params (intermediate layers: [2, 5, 8, 11])
│   ├── vitb: 113.1M params (intermediate layers: [2, 5, 8, 11])
│   └── vitl: 381.8M params (intermediate layers: [4, 11, 17, 23])
└── DPTHeadTemporal (depth decoder with temporal modeling)
    ├── MotionModule at layer_3 (out_channels[2])
    ├── MotionModule at layer_4 (out_channels[3])
    ├── MotionModule at features (first fusion)
    └── MotionModule at features (second fusion)
```

**Key Inference Parameters (run.py):**
- `INFER_LEN = 32`: Frames processed per batch
- `OVERLAP = 10`: Overlap between consecutive batches
- `KEYFRAMES = [0,12,24,25,26,27,28,29,30,31]`: Keyframe indices used for overlap alignment

**Processing Pipeline:**
1. Video frames extracted via `read_video_frames()` in `utils/dc_utils.py`
2. Frames processed in sliding window of 32 frames with 10-frame overlap
3. Overlapping regions aligned using `compute_scale_and_shift()` for photometric consistency
4. Interpolated frames blended using `get_interpolate_frames()`

## Key Files

- `run.py`: Standard inference entry point
- `run_streaming.py`: Streaming mode for long videos (caches temporal hidden states)
- `video_depth_anything/video_depth.py`: Main model class with `infer_video_depth()` method
- `video_depth_anything/dpt_temporal.py`: Temporal DPT head extending `DPTHead` with motion modules
- `video_depth_anything/dinov2.py`: DINOv2 encoder wrapper
- `utils/util.py`: Scale/shift alignment and frame interpolation utilities
- `utils/dc_utils.py`: Video I/O using decord (preferred) or opencv fallback

## Model Variants

| Encoder | Parameters | Checkpoint Pattern |
|---------|------------|-------------------|
| vits | 28.4M | `video_depth_anything_vits.pth` / `metric_video_depth_anything_vits.pth` |
| vitb | 113.1M | `video_depth_anything_vitb.pth` / `metric_video_depth_anything_vitb.pth` |
| vitl | 381.8M | `video_depth_anything_vitl.pth` / `metric_video_depth_anything_vitl.pth` |

## Output Formats

- **Video**: `_vis.mp4` (colorized depth) or `_src.mp4` (input video)
- **Raw depth**: `.npz` format (enabled with `--save_npz`)
- **EXR format**: Per-frame `.exr` files (enabled with `--save_exr`)
- **Point clouds**: `.ply` files for metric depth mode (requires open3d)
