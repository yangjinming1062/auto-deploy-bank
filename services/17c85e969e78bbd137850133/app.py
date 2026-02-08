#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Flask web service for nlpia library."""

from flask import Flask, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nlpia

app = Flask(__name__)

# Initialize sentiment analyzer
sa = SentimentIntensityAnalyzer()


@app.route("/")
def index():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "message": "nlpia service is running",
        "version": nlpia.__version__
    })


@app.route("/sentiment", methods=["POST"])
def sentiment():
    """Simple sentiment analysis endpoint using VADER."""
    text = request.json.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    scores = sa.polarity_scores(text=text)
    return jsonify({
        "text": text,
        "sentiment": scores
    })


@app.route("/tokenize", methods=["POST"])
def tokenize():
    """Tokenize text using NLTK."""
    import nltk
    text = request.json.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    try:
        tokens = nltk.word_tokenize(text)
        return jsonify({"text": text, "tokens": tokens})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)