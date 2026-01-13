# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is **"Papers in 100 Lines of Code"** - a collection of 56 deep learning research papers, each implemented concisely in Python. The repository contains self-contained, educational implementations of foundational ML/DL papers spanning:

- Generative models (GANs, VAEs, Diffusion Models, Normalizing Flows)
- Reinforcement Learning (DQN, PPO, DDPG variants)
- Neural Radiance Fields (NeRF and variants)
- Meta-Learning (MAML, Reptile)
- Activation Functions (ReLU, GELU, ELU, SELU)
- Optimizers (Adam, RAdam)
- And more...

## Repository Structure

```
/home/ubuntu/deploy-projects/36185e6195d5e38175ff6026/
├── README.md                          # Master list of all 56 papers
├── CODE_OF_CONDUCT.md
├── LICENSE
└── [Paper_Name]/                      # One directory per paper
    ├── *.py                          # Main implementation (~100 lines)
    ├── README.md                     # Paper explanation and details
    ├── requirements.txt              # Dependencies
    └── Data/                         # Optional: dataset files (when needed)
```

Each paper's directory is named using underscores (e.g., `Generative_Adversarial_Networks` instead of `Generative Adversarial Networks`).

## Common Commands

### Working with Individual Papers

Each paper is completely independent and can be run separately:

```bash
# Navigate to a paper's directory
cd Generative_Adversarial_Networks

# Install dependencies
pip install -r requirements.txt

# Run the implementation
python GANs.py

# Output will be generated in the Imgs/ directory within the paper's folder
```

### Development Workflow

Since each paper is self-contained:

1. **Edit and test per-paper**: Modify the `.py` file in a specific paper directory
2. **Install dependencies**: Run `pip install -r requirements.txt` in the paper's directory
3. **Execute**: Run `python <paper_name>.py` to train and generate visualizations
4. **View results**: Check the `Imgs/` directory for generated plots/images

## Code Architecture

### Common Patterns

Every implementation follows a similar structure:

1. **Imports**: PyTorch, NumPy, Matplotlib, Tqdm (standard stack)
2. **Data Loading**: Often embedded directly in the file (e.g., MNIST via Keras)
3. **Model Class**: nn.Module subclass defining the network architecture
4. **Training Function**: Separate function handling the training loop
5. **Main Block**: `if __name__ == "__main__":` that:
   - Sets device (`device = 'cuda:0'`)
   - Instantiates model, optimizer(s)
   - Calls training function
   - Generates and saves visualizations

### Typical File Structure

```python
import torch
import torch.nn as nn
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

# Data loading utilities (often inline)

class ModelName(nn.Module):
    def __init__(self, ...):
        super().__init__()
        # Network definition using nn.Sequential or manual layers

    def forward(self, x):
        # Forward pass

def train_function(model, optimizer, epochs, ...):
    # Training loop with loss computation and backprop
    for epoch in tqdm(range(epochs)):
        # ... training code ...
    return losses

if __name__ == "__main__":
    device = 'cuda:0'

    # Initialize model and optimizer
    model = ModelName(...).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # Train
    losses = train_function(model, optimizer, epochs)

    # Generate and save visualizations
    # plt.figure(figsize=...); plt.plot(...); plt.savefig('Imgs/...')
```

### Key Conventions

- **Device**: CUDA is used if available (`device = 'cuda:0'`), otherwise falls back to CPU
- **Batch Size**: Typically 100 for efficiency
- **Epochs**: Varies widely (100 to 500,000+ depending on the paper)
- **Visualizations**: All plots saved to `Imgs/` directory with descriptive names
- **Dependencies**: Each paper has its own `requirements.txt` (slight variations exist)

### Dependencies (Common)

Most papers use these core packages:
- `torch` (1.7.1 to 2.8.0 depending on paper)
- `numpy` (~1.19-1.24)
- `matplotlib` (~3.3-3.5)
- `tqdm` (~4.48-4.64)
- Paper-specific: `scipy`, `keras`, etc.

## Important Notes

1. **No Build System**: There's no `setup.py`, `pyproject.toml`, or unified build process. Each paper is completely independent.

2. **Data Requirements**: Some papers require external datasets:
   - Papers using MNIST: Load automatically via Keras
   - Frey Face dataset: Requires `Data/frey_rawface.mat` file
   - NeRF papers: Require preprocessed ray data files
   - Check each paper's README.md for data requirements

3. **CUDA Dependency**: Most implementations assume CUDA is available. If running on CPU-only, modify the `device` variable in the main block.

4. **No Tests**: This repository doesn't include unit tests or integration tests. Each paper is meant to be run as a standalone script.

5. **Educational Purpose**: These are concise, readable implementations (≈100 lines each) designed for learning, not production use.

## Adding New Papers

When implementing a new paper:

1. Create a new directory named with underscores (matching the paper title)
2. Create `<technique_name>.py` with the implementation
3. Add `requirements.txt` with necessary dependencies
4. Add `README.md` explaining the paper and implementation
5. Update the root `README.md` to include the new paper entry

## Examples

### To run a simple GAN on MNIST:
```bash
cd Generative_Adversarial_Networks
pip install -r requirements.txt
python GANs.py
# Generates Imgs/regenerated_MNIST_data.png
```

### To run a VAE:
```bash
cd Auto_Encoding_Variational_Bayes
pip install -r requirements.txt
python VAEs.py
# Requires Data/frey_rawface.mat
# Generates Imgs/Training_loss.png and Imgs/Learned_data_manifold.png
```

### To run NeRF:
```bash
cd NeRF_Representing_Scenes_as_Neural_Radiance_Fields_for_View_Synthesis
pip install -r requirements.txt
python nerf.py
# Requires preprocessed dataset in Data/
# Generates novel_views/img_*.png files
```