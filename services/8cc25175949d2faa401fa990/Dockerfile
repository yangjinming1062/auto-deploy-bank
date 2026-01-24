FROM python:3.9-slim

# Install curl for healthcheck and build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/8cc25175949d2faa401fa990

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    TORCH_SHARE_STRATEGY=file_system \
    OMP_NUM_THREADS=1 \
    MASTER_ADDR=127.0.0.1 \
    PYTHONPATH=/home/ubuntu/deploy-projects/8cc25175949d2faa401fa990

# Copy requirements and install Python dependencies
COPY requirements.txt .

# Install core dependencies with compatible versions
RUN pip install --no-cache-dir \
    "numpy>=1.19.0,<1.24.0" \
    "PyYAML>=5.3.1" \
    "tqdm" \
    "jieba" \
    "einops" \
    "chardet" \
    "setuptools>=41.0.0" \
    "numba>=0.48.0" \
    "pandas>=1.2.0" \
    "librosa>=0.8.0" \
    "pytorch-lightning==0.7.1" \
    "h5py>=3.1.0" \
    "pypinyin>=0.39.0" \
    "g2pM>=0.1.2.5" \
    "gradio>=3.0.0,<4.0.0" \
    "huggingface_hub>=0.14.0,<0.20.0" \
    "scikit-learn>=0.24.0" \
    "tensorboardX" \
    "pyloudnorm" \
    "torch==1.9.0" \
    "torchaudio==0.9.0"

# Install remaining optional dependencies
RUN pip install --no-cache-dir \
    "matplotlib" \
    "scikit-image>=0.19.0,<0.22.0" \
    "pretty-midi>=0.2.9" \
    "textgrid" \
    "jiwer" \
    "praat-parselmouth>=0.3.3" \
    "pycwt" \
    "miditoolkit" \
    "resemblyzer" \
    "webrtcvad"

# Copy application code
COPY . .

# Reinstall scipy with correct version after all other packages
RUN pip install --no-cache-dir --force-reinstall "scipy>=1.5.0,<1.10.0"

# Create checkpoint directory for the model
RUN mkdir -p /home/ubuntu/deploy-projects/8cc25175949d2faa401fa990/checkpoints/0228_opencpop_ds100_rel && \
    echo "# Placeholder config - replace with actual model checkpoint" > /home/ubuntu/deploy-projects/8cc25175949d2faa401fa990/checkpoints/0228_opencpop_ds100_rel/config.yaml

# Expose Gradio default port
EXPOSE 7860

# Run the Gradio app with config
CMD ["python", "inference/svs/gradio/infer.py", "--config", "usr/configs/midi/e2e/opencpop/ds100_adj_rel.yaml", "--exp_name", "0228_opencpop_ds100_rel"]