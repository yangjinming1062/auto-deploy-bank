#!/usr/bin/env python3
"""Flask web server for SkyAR sky replacement service."""

import os
import threading
import time
from flask import Flask, render_template_string, request, redirect, url_for, send_file, jsonify

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max upload

# Template for the main page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SkyAR - Sky Replacement Service</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #fff;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .subtitle {
            text-align: center;
            color: #8892b0;
            margin-bottom: 30px;
        }
        .card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .status-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .status-healthy { background: #10b981; color: #fff; }
        .status-warning { background: #f59e0b; color: #fff; }
        .status-error { background: #ef4444; color: #fff; }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .info-item {
            background: rgba(0, 0, 0, 0.2);
            padding: 15px;
            border-radius: 8px;
        }
        .info-label { color: #8892b0; font-size: 0.85rem; margin-bottom: 5px; }
        .info-value { font-size: 1.1rem; font-weight: 500; }
        .upload-area {
            border: 2px dashed rgba(0, 212, 255, 0.5);
            border-radius: 12px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 15px;
        }
        .upload-area:hover {
            border-color: #00d4ff;
            background: rgba(0, 212, 255, 0.1);
        }
        .upload-icon { font-size: 3rem; margin-bottom: 15px; }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .feature {
            text-align: center;
            padding: 20px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 8px;
        }
        .feature-icon { font-size: 2rem; margin-bottom: 10px; }
        footer {
            text-align: center;
            margin-top: 30px;
            color: #8892b0;
            font-size: 0.85rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>SkyAR</h1>
        <p class="subtitle">AI-Powered Sky Replacement Service</p>

        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h2>Service Status</h2>
                <span class="status-badge {{ 'status-healthy' if model_available else 'status-warning' }}">
                    {{ 'Ready' if model_available else 'Awaiting Model' }}
                </span>
            </div>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Model Checkpoint</div>
                    <div class="info-value">{{ 'Loaded' if model_available else 'Not Found' }}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">SkyBox Image</div>
                    <div class="info-value">{{ skybox }}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Input Mode</div>
                    <div class="info-value">{{ input_mode|capitalize }}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Output Resolution</div>
                    <div class="info-value">{{ out_width }}x{{ out_height }}</div>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>Features</h2>
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">☁️</div>
                    <div>Sky Replacement</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">✨</div>
                    <div>Auto Light Match</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">🌈</div>
                    <div>Relighting</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">💫</div>
                    <div>Halo Effect</div>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>Upload Video</h2>
            <p style="color: #8892b0; margin-bottom: 15px;">
                Upload a video to apply sky replacement effect
            </p>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <div class="upload-area" onclick="document.getElementById('video_file').click()">
                    <div class="upload-icon">📹</div>
                    <div>Click or drag to upload video</div>
                    <div style="font-size: 0.85rem; color: #8892b0; margin-top: 10px;">
                        Supported formats: MP4, AVI, MOV
                    </div>
                </div>
                <input type="file" id="video_file" name="video" accept=".mp4,.avi,.mov" style="display: none;" onchange="this.form.submit()">
            </form>
            {% if not model_available %}
            <div style="margin-top: 15px; padding: 15px; background: rgba(245, 158, 11, 0.2); border-radius: 8px; border-left: 4px solid #f59e0b;">
                <strong>⚠️ Model Required</strong>
                <p style="margin-top: 5px; font-size: 0.9rem; color: #8892b0;">
                    Please place the model checkpoint at:
                    <code style="background: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 4px;">{{ checkpoint_path }}</code>
                </p>
            </div>
            {% endif %}
        </div>

        <footer>
            SkyAR - Neural Network-based Sky Replacement<br>
            Powered by PyTorch & OpenCV
        </footer>
    </div>
</body>
</html>
'''

# Global state
processing_lock = threading.Lock()
is_processing = False

def check_model_available():
    """Check if the model checkpoint exists."""
    checkpoint_path = os.environ.get('CHECKPOINT_PATH', '/home/ubuntu/deploy-projects/45a553c4a3d29b92ade41628/checkpoints_G_coord_resnet50/best_ckpt.pt')
    return os.path.exists(checkpoint_path)

def get_skybox_from_config():
    """Extract skybox image from config."""
    config_path = os.environ.get('CONFIG_PATH', '/home/ubuntu/deploy-projects/45a553c4a3d29b92ade41628/config/config-canyon-district9ship.json')
    try:
        import json
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config.get('skybox', 'Unknown')
    except:
        return 'Unknown'

@app.route('/')
def index():
    """Main page showing service status."""
    return render_template_string(
        HTML_TEMPLATE,
        model_available=check_model_available(),
        checkpoint_path=os.environ.get('CHECKPOINT_PATH', '/home/ubuntu/deploy-projects/45a553c4a3d29b92ade41628/checkpoints_G_coord_resnet50/best_ckpt.pt'),
        skybox=get_skybox_from_config(),
        input_mode='video',
        out_width=845,
        out_height=480
    )

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_available': check_model_available(),
        'service': 'SkyAR',
        'version': '1.0.0'
    })

@app.route('/upload', methods=['POST'])
def upload():
    """Handle video upload for processing."""
    global is_processing

    if not check_model_available():
        return jsonify({
            'error': 'Model checkpoint not found. Please upload the model file first.',
            'checkpoint_path': os.environ.get('CHECKPOINT_PATH', '/home/ubuntu/deploy-projects/45a553c4a3d29b92ade41628/checkpoints_G_coord_resnet50/best_ckpt.pt')
        }), 400

    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save uploaded file
    upload_dir = '/home/ubuntu/deploy-projects/45a553c4a3d29b92ade41628/uploads'
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, file.filename)
    file.save(filepath)

    return jsonify({
        'message': 'Video uploaded successfully',
        'filename': file.filename,
        'status': 'processing'
    })

@app.route('/status')
def status():
    """Get processing status."""
    return jsonify({
        'is_processing': is_processing,
        'model_available': check_model_available()
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 43950))
    host = os.environ.get('HOST', '0.0.0.0')

    print(f"Starting SkyAR Web Server on {host}:{port}")
    print(f"Model available: {check_model_available()}")

    app.run(host=host, port=port, debug=False, threaded=True)