"""
Flask service wrapper for PyTorch SNAKE object detection demo.
"""
import sys
import os
sys.path.insert(0, '/home/ubuntu/deploy-projects/b921526a8e06ad21a48433ff')

# Patch sys.argv before importing lib.config
# This ensures the config module parses the correct arguments
sys.argv = ['service.py', '--cfg_file', 'configs/coco_snake.yaml', '--type', 'demo']

from flask import Flask, request, jsonify, send_file
import os
import cv2
import numpy as np
import torch
from werkzeug.utils import secure_filename
import tempfile
import traceback

from lib.config import cfg, args as lib_args
from lib.networks import make_network
from lib.utils.net_utils import load_network
from lib.visualizers import make_visualizer
from lib.utils.snake import snake_config
from lib.utils import data_utils

app = Flask(__name__)

# Global variables for model
network = None
visualizer = None
model_loaded = False


def normalize_image(inp):
    inp = (inp.astype(np.float32) / 255.)
    inp = (inp - snake_config.mean) / snake_config.std
    inp = inp.transpose(2, 0, 1)
    return inp


def init_model():
    global network, visualizer, model_loaded

    if model_loaded:
        return True

    try:
        network = make_network(cfg).cuda()
        load_network(network, cfg.model_dir, resume=cfg.resume, epoch=cfg.test.epoch)
        network.eval()
        visualizer = make_visualizer(cfg)
        model_loaded = True
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        traceback.print_exc()
        return False


@app.route('/', methods=['GET'])
def index():
    """Root endpoint - returns service info and health status."""
    return jsonify({
        "service": "PyTorch SNAKE Object Detection",
        "version": "1.0.0",
        "endpoints": {
            "/": "GET - This info",
            "/health": "GET - Health check",
            "/predict": "POST - Image detection (multipart form with 'image' field)"
        },
        "status": "healthy",
        "model_loaded": model_loaded
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    if model_loaded:
        return jsonify({"status": "healthy", "model": "loaded"})
    return jsonify({"status": "healthy", "model": "not_loaded"}), 200


@app.route('/predict', methods=['POST'])
def predict():
    """
    Accept an image and return detection results.
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No image selected"}), 400

    try:
        # Save uploaded image to temp file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            tmp_path = tmp.name
            file.save(tmp_path)

        # Read and process image
        img = cv2.imread(tmp_path)
        if img is None:
            os.unlink(tmp_path)
            return jsonify({"error": "Failed to read image"}), 400

        # Initialize model if needed
        if not model_loaded:
            if not init_model():
                os.unlink(tmp_path)
                return jsonify({"error": "Model not loaded"}), 500

        # Preprocess
        width, height = img.shape[1], img.shape[0]
        center = np.array([width // 2, height // 2])
        scale = np.array([width, height])
        x = 32
        input_w = (int(width / 1.) | (x - 1)) + 1
        input_h = (int(height / 1.) | (x - 1)) + 1

        trans_input = data_utils.get_affine_transform(center, scale, 0, [input_w, input_h])
        inp = cv2.warpAffine(img, trans_input, (input_w, input_h), flags=cv2.INTER_LINEAR)
        inp = normalize_image(inp)

        # Prepare batch
        batch = {
            'inp': torch.FloatTensor(inp)[None].cuda(),
            'meta': {'center': center, 'scale': scale, 'test': '', 'ann': ''}
        }

        # Run inference
        with torch.no_grad():
            output = network(batch['inp'], batch)

        # Get visualization
        result_path = tmp_path.replace('.jpg', '_result.jpg')
        # Create a list batch for compatibility with visualize method
        batch_list = [batch]
        visualizer.visualize(output, batch_list)
        # Rename the output file if visualize saves it
        import glob
        result_files = glob.glob(tmp_path.replace('.jpg', '_*.jpg'))
        if result_files:
            import shutil
            shutil.move(result_files[0], result_path)

        # Return result image
        if os.path.exists(result_path):
            response = send_file(result_path, mimetype='image/jpeg')
            # Clean up temp files
            os.unlink(tmp_path)
            return response
        else:
            os.unlink(tmp_path)
            return jsonify({"error": "Processing failed"}), 500

    except Exception as e:
        print(f"Error during prediction: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("Starting PyTorch SNAKE service...")
    app.run(host='0.0.0.0', port=40209, debug=False)