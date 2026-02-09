"""
Simple Flask web server for LLM Finetune service.
Provides basic endpoints for model training and inference.
"""
from flask import Flask, jsonify, request
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Home page with service information."""
    return jsonify({
        "service": "LLM Finetune Service",
        "status": "running",
        "endpoints": {
            "/": "Service info",
            "/health": "Health check",
            "/train/qwen2": "Train Qwen2 model",
            "/train/glm4": "Train GLM4 model",
            "/predict/qwen2": "Run Qwen2 prediction",
            "/predict/glm4": "Run GLM4 prediction"
        }
    })

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})

@app.route('/train/qwen2', methods=['POST'])
def train_qwen2():
    """Train Qwen2 model."""
    try:
        # Run training in background
        subprocess.Popen(["python", "train_qwen2.py"],
                        cwd="/home/ubuntu/deploy-projects/443a5abcbfc6de916990347c",
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        return jsonify({"status": "training started", "model": "qwen2"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/train/glm4', methods=['POST'])
def train_glm4():
    """Train GLM4 model."""
    try:
        subprocess.Popen(["python", "train_glm4.py"],
                        cwd="/home/ubuntu/deploy-projects/443a5abcbfc6de916990347c",
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        return jsonify({"status": "training started", "model": "glm4"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict/qwen2', methods=['POST'])
def predict_qwen2():
    """Run Qwen2 prediction."""
    try:
        result = subprocess.run(
            ["python", "predict_qwen2.py"],
            cwd="/home/ubuntu/deploy-projects/443a5abcbfc6de916990347c",
            capture_output=True,
            text=True,
            timeout=300
        )
        return jsonify({
            "status": "completed",
            "output": result.stdout[-2000:] if result.stdout else "",
            "error": result.stderr[-500:] if result.stderr else ""
        })
    except subprocess.TimeoutExpired:
        return jsonify({"error": "prediction timed out"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict/glm4', methods=['POST'])
def predict_glm4():
    """Run GLM4 prediction."""
    try:
        result = subprocess.run(
            ["python", "predict_glm4.py"],
            cwd="/home/ubuntu/deploy-projects/443a5abcbfc6de916990347c",
            capture_output=True,
            text=True,
            timeout=300
        )
        return jsonify({
            "status": "completed",
            "output": result.stdout[-2000:] if result.stdout else "",
            "error": result.stderr[-500:] if result.stderr else ""
        })
    except subprocess.TimeoutExpired:
        return jsonify({"error": "prediction timed out"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=41295)