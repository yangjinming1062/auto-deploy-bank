from flask import Flask, jsonify
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)


@app.route('/')
def index():
    """Health check and service info endpoint."""
    return jsonify({
        'service': 'Generative AI Python Service',
        'status': 'healthy',
        'version': '1.0.0',
        'endpoints': {
            '/': 'Health check',
            '/health': 'Detailed health status'
        }
    })


@app.route('/health')
def health():
    """Detailed health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'environment': {
            'OPENAI_API_KEY': 'configured' if os.getenv('OPENAI_API_KEY') else 'not configured',
            'AZURE_OPENAI_ENDPOINT': 'configured' if os.getenv('AZURE_OPENAI_ENDPOINT') else 'not configured',
            'HUGGING_FACE_API_KEY': 'configured' if os.getenv('HUGGING_FACE_API_KEY') else 'not configured',
            'GITHUB_TOKEN': 'configured' if os.getenv('GITHUB_TOKEN') else 'not configured',
            'GOOGLE_DEVELOPER_API_KEY': 'configured' if os.getenv('GOOGLE_DEVELOPER_API_KEY') else 'not configured'
        }
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)