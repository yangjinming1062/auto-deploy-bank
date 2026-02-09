# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of machine learning web applications built with Flask, Streamlit, and FastAPI. Each subdirectory contains an independent ML web app demonstrating different ML integration patterns.

## Common Commands

### Running Apps

**Flask Apps:**
```bash
python app.py
# App runs on http://127.0.0.1:5000 with debug=True
```

**Streamlit Apps:**
```bash
streamlit run app.py
# App opens in browser automatically
```

**FastAPI Apps:**
```bash
uvicorn app:app --reload
# API runs on http://127.0.0.1:8000
# Or: python app.py (includes uvicorn.run)
```

**Installing Dependencies:**
```bash
pip install -r requirements.txt
```

### Common Dependencies Across Apps
- `flask` - Web framework for Flask apps
- `streamlit` - Web framework for Streamlit apps
- `fastapi` + `uvicorn` - API framework
- `scikit-learn` - ML algorithms
- `pandas`, `numpy` - Data manipulation
- `joblib` or `pickle` - Model serialization
- `spacy` - NLP processing
- `textblob` - Sentiment analysis
- `nltk` - NLP tasks
- `matplotlib`, `wordcloud` - Visualization

## Architecture

### Flask App Structure
```
app.py           # Main application with routes
templates/       # HTML Jinja2 templates
static/          # CSS, JS, images
data/            # CSV datasets, serialized models
models/          # Trained ML models (.pkl files)
```

### Streamlit App Structure
```
app.py           # Single-file Streamlit app
models/          # Trained ML models
images/          # Static images
```

### FastAPI App Structure
```
app.py           # Main FastAPI application with endpoints
models/          # Trained ML models
```

### Common ML Patterns

1. **Model Loading**: Models are loaded at module level using `joblib.load("models/model_name.pkl")`
2. **Vectorization**: Text inputs use `CountVectorizer` or similar from sklearn
3. **Prediction**: `model.predict()` with reshaped input data
4. **API Endpoints**: FastAPI uses `@app.get('/predict/')` or `@app.post('/predict/{name}')`

### Note on sklearn.externals
Older apps use `from sklearn.externals import joblib`. This is deprecated - use `import joblib` directly.

## App List

Key apps in this repository:
- `Bible-Verse-Prediction-ML-App/` - Text classification with TextBlob sentiment
- `Youtube-Spam-Detector-ML-Flask-App/` - Spam classification
- `Serving_ML_Models_as_API_with_FastAPI/` - FastAPI gender prediction API
- `gender_classifier_mlapp_with_streamlit/` - Streamlit gender classifier
- `NLPIffy_NLP_Based_SpaCy_Flask_App&_API/` - NLP with SpaCy + REST API
- `Iris-Species-Predictor-ML-Flask-App-With-Materialize.css/` - Multi-model iris prediction
- `DisplaCify_App-Using-Displacy-in-Flask/` - Named entity visualization