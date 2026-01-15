# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**CoNR (Collaborative Neural Rendering using Anime Character Sheets)** - Official implementation of a research paper (IJCAI2023) that generates vivid dancing videos from hand-drawn anime character sheets (ACS). The model takes character sheets and pose sequences as input and outputs rendered animation frames.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Web UI (Streamlit)
streamlit run streamlit.py --server.port=8501

# Terminal inference
python -m torch.distributed.launch \
  --nproc_per_node=1 train.py --mode=test \
  --world_size=1 --dataloaders=2 \
  --test_input_poses_images=./poses/ \
  --test_input_person_images=./character_sheet/ \
  --test_output_dir=./results/ \
  --test_checkpoint_dir=./weights/

# Or use the provided script
sh infer.sh
```

## Architecture

The model consists of four main neural network components orchestrated in `conr.py`:

1. **UDP Parser Net** (`ResEncUnet`, backbone='resnet50_danbo') - Segmenter that extracts parsing masks and features from character sheets
2. **Target Pose Encoder** (`ResEncUnet`, backbone='resnet18_danbo-4') - Encodes Ultra-Dense Pose (UDP) of target animation frames
3. **CINN Shader** (`model/shader.py`) - Conditional Image Neural Network performing flow-based warping of character features to target pose
4. **RGBA Decoder Net** (`model/decoder_small.py`) - Final decoder that converts shader features to RGBA output

### Data Flow
```
Character Sheet → UDP Parser Net → Parser Features
                                      ↓
Pose Sequence → Target Pose Encoder → Pose Features
                                      ↓
                    CINN Shader (with attention/warping) → RGBA Decoder → Output Frame
```

### Key Model Files

- `model/backbone.py`: ResNet-based U-Net encoder-decoder with danbo-pretrained weights (resnet18/50 variants)
- `model/shader.py`: Multi-scale flow-based rendering network (CINN) with attention across reference views
- `model/warplayer.py`: Feature warping utilities using optical flow
- `data_loader.py`: Custom dataset with `RandomResizedCropWithAutoCenteringAndZeroPadding` for character sheet augmentation

## Input Requirements

- **Character sheets**: PNG images with transparent backgrounds (RGBA) in `character_sheet/`
- **Pose sequences**: Ultra-Dense Pose (UDP) files or pose images in `poses/`
- **Model weights**: Download from Google Drive to `weights/` directory (4 files: udpparsernet, target_pose_encoder, shader, rgbadecodernet)

## Key Arguments

- `--test_pose_use_parser_udp`: Use parser to generate UDP from pose images (default: False)
- `--dataloader_imgsize`: Input image size (default: 256)
- `--test_output_video`: Output final RGBA frames as PNG sequence
- `--test_output_udp`: Output parser-generated UDP sequences