# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **AI Engineer Headquarters**, an educational repository containing hands-on projects and tutorials for learning AI/ML engineering. It's organized into numbered modules covering foundational topics through advanced concepts in AI engineering.

## Repository Structure

The repository is organized into the following main directories:

- **0_Prep**: Python fundamentals (Jupyter notebooks)
- **1_Foundations of AI Engineering**: Python hands-on, ML/DL fundamentals, and project labs
  - Notable projects:
    - `012_MLops end-to-end project/insurance-claim-prediction-mlops`: Complete MLOps pipeline with data ingestion, validation, transformation, model training, and deployment
    - `013_Project Lab/resume_analyzer`: Flask-based resume parsing application using spaCy
- **2_Mastering Large Language Models**: LLM training, inference, and applications
- **3_Retrieval-Augmented Generation (RAG)**: Vector databases, embeddings, and production RAG systems
  - `29_RAG Production/rag_financial`: Production-ready RAG system with LangChain, ChromaDB, and FastAPI
- **4_Fine-Tuning**: Domain-specific model customization
- **6_Agentic Workflows**: Autonomous AI agents and tool calling
- **workshop-webinar**: Workshop materials
- **youtube-code**: Supplementary code from YouTube tutorials

## Common Development Commands

Each project is independent and may have different dependencies. Follow these general patterns:

### Setup and Dependencies

```bash
# Navigate to any project directory (examples)
cd "1_Foundations of AI Engineering/012_MLops end-to-end project/insurance -claim-prediction-mlops"
cd "1_Foundations of AI Engineering/013_Project Lab/resume_analyzer"
cd "3_Retrieval-Augmented Generation (RAG)/29_RAG Production/rag_financial"
cd "2_Mastering Large Language Models/19_20_Cloud vs On-Prem and HQ query bot/hr_query_bot/frontend"

# Create virtual environment (if not using global Python)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -e .  # For projects with setup.py (e.g., MLOps insurance project)

# For spaCy projects (resume_analyzer)
python -m spacy download en_core_web_sm
```

### Running Projects

```bash
# Flask applications
python app.py  # or python main.py (varies by project)

# Jupyter notebooks
jupyter notebook
# or
jupyter lab

# Direct Python execution
python main.py
python script_name.py

# FastAPI applications
uvicorn main:app --reload  # For API-based projects
```

### Testing Individual Files

```bash
# Run specific Python scripts
python filename.py

# Test Jupyter notebooks interactively
jupyter notebook  # Then open and run cells manually
```

## Code Architecture Patterns

### MLOps Project Pattern (insurance-claim-prediction-mlops)

Follows structured ML pipeline architecture:

```
claim/
├── components/          # ML pipeline stages
│   ├── data_ingestion.py
│   ├── data_validation.py
│   ├── data_transformation.py
│   └── model_trainer.py
├── entity/              # Configuration & artifacts
│   ├── *_config.py
│   └── *_artifact.py
├── pipeline/            # End-to-end orchestration
│   └── training_pipeline.py
├── constants/           # Hardcoded values
├── utils/               # Helper functions
├── exception/           # Custom exceptions
├── logging/             # Logging setup
└── config/
    └── params.yaml      # Hyperparameters
```

Run the complete pipeline:
```bash
cd "1_Foundations of AI Engineering/012_MLops end-to-end project/insurance -claim-prediction-mlops"
python claim/pipeline/run_pipeline.py
```

### Flask Web App Pattern (resume_analyzer)

Simple Flask application structure:

```
resume_analyzer/
├── app.py              # Flask app entry point
├── resume_parser.py    # Core parsing logic
├── utils.py            # Helper functions
├── templates/          # HTML templates
├── static/             # CSS/JS files
└── requirements.txt
```

Run the web app:
```bash
cd "1_Foundations of AI Engineering/013_Project Lab/resume_analyzer"
python app.py
# Visit http://localhost:5000
```

### RAG Production Pattern

Production-ready RAG system using:
- **LangChain** for pipeline orchestration
- **ChromaDB** for vector storage
- **FastAPI** for API layer
- **LlamaIndex** for advanced indexing

Dependencies include extensive ML libraries (transformers, torch, openai, etc.). Installation may take several minutes.

### Frontend Projects

Some projects include React/Vite frontend:

```bash
cd "2_Mastering Large Language Models/19_20_Cloud vs On-Prem and HQ query bot/hr_query_bot/frontend"
npm install
npm run dev
```

## Key Technologies by Project Type

- **Classical ML**: pandas, numpy, scikit-learn, imblearn
- **Deep Learning**: torch, transformers
- **NLP**: spaCy, NLTK
- **RAG**: LangChain, LlamaIndex, ChromaDB, OpenAI
- **Web Frameworks**: Flask, FastAPI
- **MLOps**: MLflow, MySQL, SQLAlchemy
- **Agentic AI**: LangChain agents, tool calling
- **Frontend**: React/Vite (some projects)

## Important Notes

1. **Independent Projects**: Each numbered directory and sub-project is self-contained with its own dependencies
2. **Educational Purpose**: These are learning examples, not production systems
3. **Jupyter Notebooks**: Found throughout for experimentation (68+ notebooks total)
4. **Variable Structure**: Project organization varies - check README.md in each project folder
5. **Environment Setup**: Some projects may require specific Python versions or system dependencies
6. **Large Dependencies**: Some projects (especially RAG/LLM) have extensive dependencies requiring significant installation time

## Getting Started

1. Start with `0_Prep` for Python fundamentals (Jupyter notebooks)
2. Move to `1_Foundations of AI Engineering` for core concepts
3. Progress to specialized topics (LLMs, RAG, Fine-tuning, Agents)
4. Check individual project README.md files for specific instructions

Each project directory contains its own README with setup and usage instructions.
