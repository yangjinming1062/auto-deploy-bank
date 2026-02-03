# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI-Practices is a systematic AI/ML learning platform with 14 core modules covering foundations to advanced topics: machine learning, neural networks, computer vision, sequence models, generative models, reinforcement learning, LLMs, multimodal learning, deployment, distributed training, and agents.

## Common Commands

```bash
# Setup and installation
conda create -n ai-practices python=3.10 -y
conda activate ai-practices
pip install -r requirements.txt

# Development dependencies
pip install -e ".[dev]"        # Testing/formatting tools
pip install -e ".[llm]"        # LLM dependencies
pip install -e ".[multimodal]" # Multimodal dependencies
pip install -e ".[full]"       # All dependencies

# Code quality
black . --line-length=100                          # Format code
ruff check . --fix                                 # Lint with auto-fix
mypy .                                             # Type checking
pre-commit install && pre-commit run --all-files   # Git hooks

# Testing
pytest -v --tb=short                               # All tests
pytest <path> -v                                   # Specific test file
pytest <path>::TestClassName::test_method -v       # Specific test

# Documentation
npm run docs:dev                                   # VitePress dev server
npm run docs:build                                 # Build docs
```

## Architecture

### Module Structure
Each module follows this pattern:
```
XX-module-name/
├── README.md                    # Module overview
├── YY-submodule/
│   ├── README.md
│   ├── 知识点.md                 # Topic notes (Chinese)
│   ├── src/                     # Implementation
│   │   ├── __init__.py
│   │   ├── core/                # Core algorithms
│   │   ├── models/              # Model definitions
│   │   ├── utils/               # Utilities
│   │   └── environments/        # RL environments
│   ├── tests/                   # Unit tests (test_*.py)
│   ├── notebooks/               # Jupyter tutorials (NN_tutorial.ipynb)
│   └── examples/                # Usage examples
```

### Core Modules
- **01-foundations/**: ML basics (linear models, SVM, decision trees, ensemble, clustering)
- **02-neural-networks/**: Neural network fundamentals, Keras/TensorFlow
- **03-computer-vision/**: CNNs, transfer learning, object detection
- **04-sequence-models/**: RNN/LSTM, Transformer, Attention
- **06-generative-models/**: VAE, GAN, Diffusion Models
- **07-reinforcement-learning/**: DQN, PPO, SAC, Actor-Critic (comprehensive tests)
- **10-large-language-models/**: GPT, LLaMA, LoRA, RAG, Agents
- **11-multimodal-learning/**: CLIP, Stable Diffusion, Whisper, TTS
- **12-deployment-optimization/**: Quantization, TensorRT, FastAPI, MLOps
- **13-distributed-training/**: DDP, FSDP, ZeRO, mixed precision
- **14-agents-reasoning/**: Tool use, CoT, ReAct, multi-agent systems

### Shared Utilities
- **utils/**: Common visualization, metrics, path utilities
- **scripts/**: Setup scripts, MCP server implementation

## Code Conventions

### Naming
| Type | Convention | Example |
|------|-----------|---------|
| Files | snake_case.py | transformer_architecture.py |
| Classes | PascalCase | TransformerEncoder, CLIPModel |
| Functions/variables | snake_case | compute_loss, forward_pass |
| Constants | UPPER_SNAKE_CASE | MAX_LENGTH, DEFAULT_LR |
| Private | _leading_underscore | _init_weights |

### Style Requirements
- Python: PEP 8, Black formatted (100 char line width)
- All public functions require type annotations
- All public functions require Google-style docstrings
- Use `pathlib` instead of `os.path`
- Prefer f-strings over .format()

### PyTorch Patterns
```python
# Model definition
class MyModel(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.layer = nn.Linear(...)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layer(x)

# Training loop
for epoch in range(num_epochs):
    model.train()
    for batch in train_loader:
        optimizer.zero_grad()
        loss = criterion(model(batch), targets)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        # validation
```

### Test Structure
```python
import pytest
import torch

class TestModel:
    @pytest.fixture
    def model(self):
        return Model(config)

    def test_forward_shape(self, model):
        x = torch.randn(2, 10, 64)
        output = model(x)
        assert output.shape == (2, 10, 64)
```

## Git Workflow

- Branch naming: `feature/<slug>` or `fix/<slug>`
- Commit format: `<type>(<scope>): <description>`
  - Types: feat, fix, docs, style, refactor, test, chore
- Run lint + tests before committing

## Key Dependencies

- **Core**: torch>=2.5.0, tensorflow>=2.18.0, keras>=3.8.0
- **ML**: scikit-learn>=1.5.0, xgboost>=2.1.0, lightgbm>=4.5.0
- **NLP/LLM**: transformers>=4.47.0, peft>=0.14.0, accelerate>=1.2.0
- **Multimodal**: diffusers>=0.32.0, timm>=1.0.0
- **Data**: numpy>=1.26.0, pandas>=2.2.0, matplotlib>=3.9.0

## Performance Notes

- Use `torch.compile()` for PyTorch 2.0+ optimization
- Enable mixed precision with `torch.cuda.amp`
- Set DataLoader `num_workers` and `pin_memory`
- Always call `model.eval()` and use `torch.no_grad()` during inference

## Configuration

Test paths are configured in `pyproject.toml`:
```toml
[tool.pytest.ini_options]
testpaths = [
    "07-reinforcement-learning",
    "09-practical-projects",
    "10-large-language-models",
    "11-multimodal-learning",
    "12-deployment-optimization",
    "13-distributed-training",
    "14-agents-reasoning",
]
```