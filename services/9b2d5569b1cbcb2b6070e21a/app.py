from flask import Flask, jsonify
from feature_selector import FeatureSelector
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'service': 'FeatureSelector API',
        'status': 'running',
        'endpoints': {
            '/': 'This info',
            '/health': 'Health check',
            '/features': 'List available features'
        }
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/features', methods=['GET', 'POST'])
def features():
    """Example endpoint using FeatureSelector with sample data"""
    # Create sample data for demonstration
    np.random.seed(42)
    n_samples = 100
    n_features = 10
    data = pd.DataFrame(np.random.randn(n_samples, n_features), columns=[f'feature_{i}' for i in range(n_features)])
    labels = np.random.randint(0, 2, n_samples)

    # Use FeatureSelector
    fs = FeatureSelector(data=data, labels=labels)
    fs.identify_missing(missing_threshold=0.5)
    fs.identify_single_unique()

    return jsonify({
        'features': list(data.columns),
        'missing_features': fs.ops.get('missing', []),
        'single_unique_features': fs.ops.get('single_unique', [])
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 40115))
    app.run(host='0.0.0.0', port=port)