import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'status': 'running',
        'service': 'Parsl Web Service',
        'message': 'Parsl container is running successfully'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("Parsl container started successfully", flush=True)
    app.run(host='0.0.0.0', port=42012)