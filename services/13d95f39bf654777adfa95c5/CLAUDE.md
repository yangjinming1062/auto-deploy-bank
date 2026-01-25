# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CoNR (Collaborative Neural Rendering using Anime Character Sheets) generates vivid dancing videos from hand-drawn anime character sheets (ACS). It takes a character sheet (collection of pose images) and UDP (Ultra-Dense Pose) sequences to synthesize animated character poses.

## Development Commands

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run with web UI (Streamlit):**
```bash
streamlit run streamlit.py --server.port=8501
```

**Run inference via terminal:**
```bash
./infer.sh
# Or manually:
python3 -m torch.distributed.launch \
--nproc_per_node=1 train.py --mode=test \
--world_size=1 --dataloaders=2 \
--test_input_poses_images=./poses/ \
--test_input_person_images=./character_sheet/ \
--test_output_dir=./results/ \
--test_checkpoint_dir=./weights/

# Generate video from frames
ffmpeg -r 30 -y -i ./results/%d.png -r 30 -c:v libx264 output.mp4 -r 30
```

**Data preparation:**
- Download pre-trained weights from Google Drive (4 model files: udpparsernet.pth, target_pose_encoder.pth, shader.pth, rgbadecodernet.pth) to `./weights/`
- Download pose sequences (UDP format) to `./poses/`
- Download character sheets to `./character_sheet/` - PNG with transparent background (use waifucutout.com to cut out foreground)

## Architecture

### Core Components

**Model Pipeline (in `conr.py`):** CoNR class orchestrates the rendering pipeline with four main stages:
1. `character_parser_forward` - Parses character sheets via U-Net backbone, extracts features
2. `pose_parser_sc_forward` - Parses pose images to UDP format
3. `shader_pose_encoder_forward` - Encodes target pose features
4. `shader_forward` - Renders character to target pose using CINN

**Model Architecture (`model/`):**
- `backbone.py`: ResEncUnet - U-Net with ResNet backbones (resnet18_danbo-4, resnet50_danbo). Danbo pretrained models from https://github.com/RF5/danbooru-pretrained
- `shader.py`: CINN - Collaborative Intermediate Neural Network with flow-based warping and attention across reference images
- `decoder_small.py`: RGBADecoderNet - Final output decoder for RGBA rendering
- `warplayer.py`: Feature warping utilities

**Data Pipeline (`data_loader.py`):**
- `FileDataset`: Loads character sheets and pose images
- `RandomResizedCropWithAutoCenteringAndZeroPadding`: Smart cropping based on alpha mask, handles padding for off-center subjects

### Key Data Formats

**Character Sheets:** PNG images with RGBA (4 channels), transparent background required. Each reference pose is NCHW format with values 0-255 uint8.

**UDP Format:** 4-channel float32 (XYZ + visibility), stored in .npz or 16-bit PNG with BGRA2RGBA colorspace.

**Input Structure:** `FileDataset` expects `[target_pose_image, *character_sheet_images]` tuples.

### Distributed Training Support

Uses `torch.distributed.launch` with `DistributedDataParallel` for multi-GPU training. The `--local_rank` argument is managed automatically by PyTorch's launcher.

## Code Patterns

- **Device handling:** Use module-level `device = torch.device("cuda" if torch.cuda.is_available() else "cpu")`
- **Normalization:** Input images normalized with `(x - 0.6) / 0.2970`
- **Sigmoid applied after decoder:** Final outputs use `torch.clamp(x, min=0, max=1)` for clipping
- **Caching:** Character parser outputs are cached (`self.parser_ckpt`) to avoid redundant computation across frames
- **Image format conversion:** CV2 uses BGRA internally, requires `cv2.COLOR_RGBA2BGRA` and `cv2.COLOR_BGRA2RGBA` for compatibility