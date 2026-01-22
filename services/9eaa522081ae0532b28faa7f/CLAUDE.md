# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ML-Capsule** is a comprehensive educational repository containing 200+ machine learning projects ranging from beginner to advanced levels. Projects cover NLP, computer vision, deep learning, chatbots (RASA), recommendation systems, and more.

- **Primary Language**: Python 3.7+
- **Frameworks**: TensorFlow, Keras, PyTorch, scikit-learn, OpenCV, NLTK, Beautiful Soup
- **Format**: Mix of Python scripts and Jupyter notebooks (.ipynb)

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests (pytest configured with tests directory)
pytest
pytest tests/           # specific test directory

# Type checking
mypy src/

# Build specific PyPI packages (in PyPI Package/ subdirectory)
cd PyPI\ Package/ && python setup.py build

# Update README from GitHub repo structure (CI/CD automation)
python build_readme.py
```

## Repository Structure

```
├── requirements.txt          # Root dependencies (requests, bs4)
├── build_readme.py           # GitHub Actions workflow script for README updates
├── Training.py               # CNN emotion detection training example
├── random_forest.py          # Custom random forest implementation
├── .github/workflows/        # 10 GitHub Actions workflows
│   ├── build.yml            # README auto-update (push, hourly cron, manual)
│   └── codeql.yml           # Security scanning
├── [200+ project directories]/
│   └── Project_Name/
│       ├── README.md        # Project-specific documentation
│       ├── *.ipynb          # Jupyter notebooks
│       ├── *.py             # Python scripts
│       ├── requirements.txt # Project-specific dependencies
│       └── Dockerfile       # Containerized projects
└── PyPI Package/            # Distribution packages (setup.py, pyproject.toml)
```

## Contribution Guidelines

**Workflow**: Fork → Clone → Create feature branch → Commit → Push → PR

**Key Rules**:
- Follow PEP8 coding standards
- Do not edit/delete existing code—only add new files/folders
- Use descriptive names (snake_case for functions/variables, UPPERCASE for constants, CamelCase for classes)
- Write meaningful commit messages
- Each project must include a README with: Goal, Models Used, Libraries Needed, Steps, Conclusion, Screenshots

**Upstream sync**:
```bash
git remote add upstream https://github.com/Niketkumardheeryan/ML-CaPsule.git
git pull upstream main
```

## Architecture Patterns

- **CNN architectures** for image classification tasks
- **Keras/TensorFlow Sequential models** for deep learning
- **Scikit-learn** for traditional ML algorithms
- **Flask/Streamlit** for web deployments
- **RASA** for conversational AI/chatbots
- **DVC** for data version control on selected projects
- **Data splits**: 70-80% training, 20-30% testing in most projects

## Key Files

- `CONTRIBUTING.md`: Detailed contribution guidelines
- `.github/pullrequest_template.md`: PR template
- `.github/readme_template.md`: Standardized project README template
- `.github/auto-label.json`: File labeling by type (Frontend, Backend, Python, etc.)