"""
Simple Flask web service for MWPBench (Math Word Problem Benchmark)
Provides a health check endpoint for container validation.
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for container orchestration."""
    return jsonify({
        'status': 'healthy',
        'service': 'mwpbench',
        'message': 'MWPBench service is running'
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint."""
    return jsonify({
        'service': 'MWPBench',
        'description': 'Math Word Problem Benchmark Evaluation Service',
        'endpoints': {
            '/health': 'Health check',
            '/': 'This info'
        }
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)