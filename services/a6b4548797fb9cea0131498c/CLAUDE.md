# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DragGAN is an unofficial PyTorch implementation of "Drag Your GAN: Interactive Point-based Manipulation on the Generative Image Manifold." It provides an interactive web interface for manipulating generated images by dragging handle points to target locations, with automatic point tracking and feature matching.

## Architecture

The codebase follows a modular structure:

- **`draggan/draggan.py`** - Core DragGAN algorithm implementation:
  - `load_model()` - Loads StyleGAN2-ADA models from pickle files with hooks for feature extraction
  - `generate_W()` - Generates latent codes in W+ space from random seeds
  - `drag_gan()` - Main optimization loop implementing point-based manipulation:
    - Optimizes first 6 layers of latent code W using Adam optimizer
    - Motion supervision: enforces feature consistency between handle points and shifted handle points
    - Point tracking: locates new handle positions by finding matching features in feature maps
    - Early termination when handle points reach targets (within tolerance d=2)
  - `motion_supervison()` - Computes L1 loss between feature patches and shifted patches
  - `forward_G()` - Generator forward pass with registered hooks for feature extraction
  - `point_tracking()` - Finds new handle point locations by feature matching

- **`draggan/web.py`** and **`gradio_app.py`** - Gradio-based interactive web interface:
  - Point selection (handle and target) with visual feedback
  - Real-time iteration display during dragging
  - Image generation from seeds
  - Model selection dropdown (supports FFHQ, cats, dogs, horses, etc.)
  - Save functionality for images and videos
  - Custom image upload with GAN inversion support

- **`draggan/utils.py`** - Utility functions:
  - Automatic checkpoint downloading from HuggingFace to `~/draggan/checkpoints-pkl/`
  - `draw_handle_target_points()` - Visualizes handle (red) and target (blue) points with arrows
  - Mask creation helpers (`create_circular_mask`, `create_square_mask`)
  - Tensor-to-PIL image conversion

- **`draggan/stylegan2/`** - Forked StyleGAN2 implementation from NVIDIA:
  - Custom CUDA operations in `torch_utils/ops/` for performance (bias_act, upfirdn2d)
  - Legacy pickle file loading support
  - Feature extraction hooks registered at synthesis layer 7 (256x256 resolution)

## Common Commands

### Installation

**PyPI (recommended):**
```bash
conda create -n draggan python=3.7
conda activate draggan
pip install torch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
pip install draggan
```

**Manual installation:**
```bash
git clone <repo>
cd DragGAN
conda create -n draggan python=3.7
conda activate draggan
pip install -r requirements.txt
```

**Docker:**
```bash
# Pre-built image (GPU)
docker run -t -p 7860:7860 --gpus all baydarov/draggan

# Build locally
docker build -t draggan .
docker run -t -p 7860:7860 --gpus all draggan
```

### Running the Application

**With PyPI package:**
```bash
python -m draggan.web  # GPU
python -m draggan.web --device mps  # Apple Silicon
python -m draggan.web --device cpu  # CPU
```

**With manual installation:**
```bash
python gradio_app.py --device cuda  # GPU
python gradio_app.py --device mps   # Apple Silicon
python gradio_app.py --device cpu   # CPU
```

**Additional options:**
```bash
python gradio_app.py --share  # Create public link
python gradio_app.py -p 8080 --ip 0.0.0.0  # Custom port
```

### Development

**Dependencies:** Listed in `requirements.txt` and `setup.py`:
- PyTorch, torchvision (deep learning framework)
- Gradio 3.34.0 (web UI)
- Ninja (fast C++ compilation for custom ops)
- imageio, imageio-ffmpeg (video generation)
- scikit-image (image processing)
- tqdm (progress bars)
- fire (CLI argument parsing)

**Model checkpoints:** Automatically downloaded on first use from:
- URL: `https://huggingface.co/aaronb/StyleGAN2-pkl/resolve/main/{base_path}`
- Stored in: `~/draggan/checkpoints-pkl/`
- Override with: `export DRAGGAN_HOME=/path/to/checkpoints`

**Available models** (defined in `CKPT_SIZE` dict):
- `ada/afhqcat.pkl` (512px) - Default model
- `ada/afhqdog.pkl` (512px)
- `ada/ffhq.pkl` (1024px)
- `stylegan2/stylegan2-ffhq-config-f.pkl` (1024px)
- `human/stylegan_human_v2_512.pkl` (512px)
- `human/stylegan_human_v2_1024.pkl` (1024px)
- And many more...

## Usage Workflow

1. **Launch** the Gradio interface
2. **Select model** from dropdown (or use default)
3. **Generate image** using a seed number
4. **Draw mask** (optional) to constrain movable region
5. **Place handle points** (red dots) - points to drag
6. **Place target points** (blue dots) - desired destinations
7. **Adjust parameters**:
   - Learning rate (default: 2e-3)
   - Max iterations (default: 20)
8. **Click "Drag it"** to start manipulation
9. **Save results** - Images and videos saved to `draggan_tmp/` directory

## Key Implementation Details

- **Device handling:** Explicit `device` variable set to 'cuda' by default, passed to all tensor operations
- **Latent code optimization:** Only optimizes first 6 layers of W to preserve global structure
- **Feature resolution:** Hook registered at layer 7 (256x256), features upsampled to target resolution
- **Point tracking radius:** r1=3 for motion supervision, r2=12 for point tracking
- **Tolerance:** d=2 pixels for early termination when handle reaches target
- **Batch size:** All operations use batch_size=1

## Known Issues & Limitations

- **GAN inversion:** Custom image upload uses GAN inversion, results may be distorted or fail completely
- **Model dependency:** Must choose model closest to image type (e.g., FFHQ for faces, cat model for cats)
- **Performance:** 8GB VRAM recommended for 1024px models, 6GB for 512px models
- **PyTorch custom ops:** StyleGAN2 CUDA ops require Ninja compiler; Windows users may encounter issues

## CI/CD

- **Docker Hub integration:** `.github/workflows/docker-hub.yml` builds and pushes image on push to main
- **Registry:** `docker.io/baydarov/draggan`
- **Build context:** Root directory with Docker daemon

## References

- [Colab Demo](https://colab.research.google.com/github/Zeqiang-Lai/DragGAN/blob/master/colab.ipynb)
- [Tutorial](https://zeqiang-lai.github.io/blog/en/posts/drag_gan/)
- [Original Paper](https://vcai.mpi-inf.mpg.de/projects/DragGAN/)
- [Official Implementation](https://github.com/XingangPan/DragGAN)