# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a collection of **independent computer vision and machine learning projects** organized into three main directories:

- **`codes/`** - Archive of 30+ CV/ML projects (projects 5-34 and some numbered projects)
- **`2024_projects/`** - Recent 2024 projects
- **`cpp_projs/`** - C++ projects using TensorRT/CUDA

Each project is **standalone and self-contained** with its own README.md, dependencies, and running instructions. There is **no centralized build system** or test suite.

## Common Development Commands

### Python Projects
Most Python projects follow these patterns:

```bash
# Install dependencies (if requirements.txt exists)
pip install -r requirements.txt

# Run a demo script (varies by project, check README.md)
python demo.py
python demo_windows.py
python demo_mac.py

# Alternative patterns
python demo.py --video_path media/video.mp4 --snap_path media/snap.png --output_path result.mp4

# For Jupyter notebook projects
jupyter notebook  # or jupyter lab
```

### C++ Projects (TensorRT/CUDA)
Projects in `cpp_projs/` use CMake:

```bash
# Build the project
cmake . -B build && cmake --build build

# Alternative build pattern
cmake -S . -B build
cmake --build build

# Run the executable
./build/runtime_thread ./weights/yolov5.engine {video_file} 2 50 0 2000000
./build/HelloWorld <video_file> <reference_image>
```

### Dependencies
Common Python packages across projects:
- `opencv-python`, `numpy`, `Pillow` - Core image processing
- `torch`, `torchvision` - PyTorch deep learning
- `tensorflow` (some projects) - TensorFlow
- `mediapipe` - Hand tracking/gesture recognition
- `tensorboard` - Visualization
- `PyQt5`, `autopy` - GUI/automation

Typical Python environment: **Python 3.8**

## Project Structure

Each project has a similar structure:
```
project_name/
├── README.md           # Project description and usage
├── requirements.txt    # Dependencies (if needed)
├── demo.py            # Main demo script
├── *.py               # Python source files
├── media/ or videos/  # Sample data (optional)
└── models/            # Model weights (optional)
```

## Code Architecture

**Each project is completely independent** - there are no shared libraries or modules between projects. Projects typically follow this pattern:

1. **Input**: Video file, camera stream, or images
2. **Processing**: CV/ML algorithms (YOLO, MediaPipe, GANs, transformers, etc.)
3. **Output**: Annotated video, predictions, or real-time control

**Key project types**:
- **Detection/Tracking**: YOLO-based object detection and DeepSort tracking
- **Classification**: Image/video classification with CNNs, transformers
- **Pose/Hand Recognition**: MediaPipe-based gesture control
- **GANs/StyleGAN**: Image generation and editing
- **Hardware Integration**: Robotic arm control, drone control
- **C++ High-performance**: TensorRT deployment for real-time inference

## Finding the Right Project

Check the main **README.md** in the repository root - it contains a comprehensive table with all 30+ projects, their descriptions, and screenshots.

Project naming convention:
- **codes/**: `number.name` format (e.g., `10.virtual_mouse`, `18.deepsort 道路车辆分析`)
- **2024_projects/**: Sequential numbering (e.g., `1.vision_tachometer`, `2.k210_vision`)
- **cpp_projs/**: Sequential numbering (e.g., `1.people_cross_gather`, `2.deepstream_detect_track`)

## Important Notes

- **No unified testing framework** - test individual projects by running their demo scripts
- **Media files** often need to be downloaded from external releases (check README.md in each project)
- **Model weights** may need manual downloading (typically stored in `models/` or `weights/` directories)
- **GPU requirements** vary - some projects need CUDA-enabled GPU (CUDA 11.1+), others work on CPU
- **Cross-platform** - most projects work on both Windows and macOS, some with platform-specific scripts
- **Chinese documentation** - Many README files are in Chinese with WeChat QR codes for support

## Working with This Repository

When helping with a specific project:
1. First check the project's README.md for exact setup and running instructions
2. Look for requirements.txt for dependencies
3. Each project is a standalone demo/tutorial - modify as needed for experimentation
4. No package installation at repository root needed - install per-project