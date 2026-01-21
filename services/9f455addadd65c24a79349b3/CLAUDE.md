# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ML-ProjectKart is a collection of 225+ machine learning, deep learning, computer vision, and NLP projects. Each project is a self-contained ML experiment, not a monolithic application. There is no shared framework or central entry point.

## Common Commands

Each project runs independently. To work on a specific project:

```bash
cd "Project Name/"                        # Navigate to project folder
pip install -r requirements.txt           # Install dependencies
jupyter notebook                          # Run Jupyter notebook (from project or Model folder)
python *.py                               # Run Python script
```

## Project Structure

Projects have varying structures depending on complexity:

**Standard ML/Analysis Project:**
```
Project_Name/
├── Dataset/              # CSV/data files
├── Model/
│   ├── *.ipynb          # Main notebook or *.py script
│   ├── requirements.txt
│   └── README.md
└── Images/              # Visualizations, screenshots
```

**Web App Project (Flask/Django):**
```
Project_Name/
├── Dataset/
├── Model/
├── Images/
├── app.py               # Web application entry point
├── static/              # CSS, JS, assets
├── templates/           # HTML templates
└── *.pkl               # Trained model file
```

**Full-Stack Project:**
```
Project_Name/
├── Back End/            # Flask/Django backend
├── Dataset/
├── Images/
├── Model/               # Jupyter notebooks
└── models/              # Saved model files
```

Note: Some legacy projects have code files at root level instead of in `Model/` folder.

## Contribution Guidelines

### Issue Workflow
1. Check `.github/ISSUE_TEMPLATE/` for feature request or bug report templates
2. Comment on issue to be assigned (first-come, first-served)
3. Maximum 1 issue assigned at a time
4. Complete before deadline or issue may be reassigned

### File Naming Conventions
- **Files**: Use **snake_case** only (e.g., `titanic_survival_prediction.ipynb`)
- **Folders**: Use Title Case (e.g., `Titanic Survival Prediction`)

### Required Files for Each Project
- `.ipynb` or `.py` - main code file
- `requirements.txt` - Python dependencies
- `README.md` - project documentation using `.github/readme_template.md`
- `Dataset/` - data files

### Code Standards
- Follow **PEP 8** style guide
- Comment code where necessary
- All work must be **original** - no plagiarism
- Use NumPy for basic algorithms; external libraries for complex ones

### Git Workflow
```bash
git remote add upstream https://github.com/prathimacode-hub/ML-ProjectKart.git
git checkout -b feature-name
git commit -m "Meaningful commit message"
git push origin feature-name
```

### Pull Request Requirements
- Fill out `.github/PULL_REQUEST_TEMPLATE.md` completely
- Reference issue: `Closes: #123` or `Fixes: #123`
- Explain your approach in the description
- Ensure code works before submitting
- For CodePeak 2025, check the contributor checkbox in PR template

### README Template (`.github/readme_template.md`)
Required sections:
- **GOAL**: Project purpose
- **DATASET**: Link and source
- **WHAT I HAD DONE**: Step-by-step procedure
- **MODELS USED**: Algorithms with rationale
- **LIBRARIES NEEDED**: Dependencies
- **ACCURACIES**: Performance metrics
- **CONCLUSION**: Key findings

## Project Categories

- **Classification**: Titanic, Breast Cancer, Spam Detection, Heart Disease
- **Regression/Prediction**: House Prices, Stock Prices, Flight Fares, Wine Quality
- **Computer Vision**: Face Mask Detection, Dog Breed ID, ASL Recognition, Object Detection
- **NLP**: Sentiment Analysis, Fake News Detection, Text Summarization, Sarcasm Detection
- **Recommendation Systems**: Movies, Books, Restaurants, Anime
- **Deep Learning**: CNNs, RNNs, GANs, Transfer Learning models

## Tech Stack

- **ML Libraries**: scikit-learn, XGBoost, LightGBM
- **Deep Learning**: TensorFlow, Keras, PyTorch
- **Computer Vision**: OpenCV, PIL
- **NLP**: NLTK, spaCy, Transformers
- **Data**: Pandas, NumPy, SciPy
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Web Frameworks**: Flask, Streamlit
- **Data Formats**: CSV, JSON, images (JPG, PNG)