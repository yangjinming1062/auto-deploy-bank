#!/bin/bash
set -e

echo "Testing FeatureSelector installation..."
python -c "
from feature_selector import FeatureSelector
import numpy as np
import pandas as pd

# Create sample data for testing
np.random.seed(42)
n_samples = 100
n_features = 10
data = pd.DataFrame(np.random.randn(n_samples, n_features), columns=[f'feature_{i}' for i in range(n_features)])
labels = np.random.randint(0, 2, n_samples)

# Test FeatureSelector initialization
fs = FeatureSelector(data=data, labels=labels)
print('FeatureSelector initialized successfully!')

# Run a simple missing value check
fs.identify_missing(missing_threshold=0.5)
print(f'Features with >50% missing: {len(fs.ops.get(\"missing\", []))}')

# Run single unique value check
fs.identify_single_unique()
print(f'Features with single unique value: {len(fs.ops.get(\"single_unique\", []))}')

print('FeatureSelector library is working correctly!')
"

echo "Starting FeatureSelector API server..."
exec python /home/ubuntu/deploy-projects/9b2d5569b1cbcb2b6070e21a/app.py