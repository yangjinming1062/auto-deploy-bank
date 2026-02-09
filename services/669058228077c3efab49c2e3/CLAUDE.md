# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

This is a **collection of standalone ML web applications**, not a single unified project. Each subdirectory is an independent application with its own dependencies and structure.

## Running Applications

### Python Web Apps (Flask, Streamlit, FastAPI)

Navigate to the app directory and run:

```bash
# Flask apps
python app.py

# Streamlit apps
streamlit run app.py

# FastAPI apps
python app.py  # or uvicorn app:app --host 0.0.0.0 --port 8000
```

### Node.js/Express Apps

```bash
cd "Embedding-Machine-Learning-Into-Express.js App"
npm install
node app.js
```

## Architecture Patterns

### Common ML Web App Structure
- **app.py / main.py** - Main application entry point
- **models/*.pkl** - Serialized sklearn models and vectorizers (joblib format)
- **templates/*.html** - HTML templates for Flask apps
- **static/** - CSS/JS assets
- **data/** - Datasets used for training

### Model Loading Pattern
Most apps follow this pattern:
```python
import joblib

# Load vectorizer and model at module level
vectorizer = open("models/vectorizer_name.pkl", "rb")
cv = joblib.load(vectorizer)

model = open("models/model_name.pkl", "rb")
clf = joblib.load(model)

# Make predictions
vect = cv.transform([input_data]).toarray()
prediction = clf.predict(vect)
```

### Frameworks Used
- **Flask** - Most common web framework (with Bootstrap, Flask-Bootstrap, Materialize.css)
- **Streamlit** - Quick ML UI apps
- **FastAPI** - REST API services
- **Express.js** - Node.js ML integration with brain.js

### ML Libraries
- scikit-learn (CountVectorizer, Naive Bayes, Logistic Regression, Random Forest)
- joblib - Model serialization
- pandas, numpy - Data handling
- NLTK, spaCy, TextBlob - NLP tasks

## Key Dependencies

### Python
```
flask, streamlit, fastapi, uvicorn
scikit-learn, joblib, pandas, numpy
spacy, nltk, textblob
```

### Node.js
```
express, body-parser, brain.js
```

## Notes

- Each project is self-contained - dependencies are typically defined in `requirements.txt` (Python) or `package.json` (Node.js)
- Models are pre-trained and loaded at startup as `.pkl` files
- Most apps run on `localhost:5000` (Flask) or `localhost:8501` (Streamlit) by default
- Some projects have both completed and starter versions in the same directory