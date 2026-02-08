#!/usr/bin/env python3
"""Simple web server for Lackey automation service."""

from flask import Flask, jsonify

app = Flask(__name__)

SERVICE_VERSION = "0.7.4"


@app.route('/')
def index():
    return jsonify({
        "service": "Lackey Automation Service",
        "version": SERVICE_VERSION,
        "status": "running",
        "message": "GUI automation library is ready for use"
    })


@app.route('/health')
def health():
    return jsonify({"status": "healthy"})


if __name__ == '__main__':
    print(f"Starting Lackey Web Service v{SERVICE_VERSION}")
    app.run(host='0.0.0.0', port=5000)