"""Flask application for TensorFlow Model Analysis service."""

import os
from flask import Flask, jsonify

app = Flask(__name__)

# Get port from environment or default to 8080
PORT = int(os.environ.get('PORT', 8080))


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'tensorflow-model-analysis'})


@app.route('/', methods=['GET'])
def index():
    """Root endpoint with service information."""
    return jsonify({
        'service': 'TensorFlow Model Analysis',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'api': '/api/v1'
        }
    })


@app.route('/api/v1', methods=['GET'])
def api_info():
    """API information endpoint."""
    return jsonify({
        'name': 'TensorFlow Model Analysis API',
        'version': 'v1',
        'description': 'Library for analyzing and evaluating TensorFlow models'
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)