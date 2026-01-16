FROM python:3.11-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set Python environment variables
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /home/ubuntu/deploy-projects/0da75108a9d80495a5f2a7ef

# Install torch first (required by flash-attn)
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# Set CUDA_HOME for flash-attn
ENV CUDA_HOME=/usr/local/cuda

# Install flash-attn pre-built wheel if GPU is available, otherwise skip (it's optional)
RUN pip install --no-cache-dir flash-attn==2.7.0.post2 || echo "flash-attn skipped (no GPU or CUDA toolkit)"

# Copy requirements.txt and install remaining dependencies
COPY requirements.txt .

# Remove incompatible packages from requirements.txt (not required for core functionality)
RUN sed -i '/^flash-attn$/d' requirements.txt
RUN sed -i '/^pyext$/d' requirements.txt

# Install remaining dependencies (excluding flash-attn and pyext)
RUN pip install --no-cache-dir -r requirements.txt

# Copy project and install in editable mode
COPY . .

# Install the package without dependencies (pyext is incompatible with Python 3.11)
# The package will still work without pyext
RUN pip install -e . --no-deps

# Patch NaiveRewardManager to accept extra parameters (workaround for code bug)
RUN sed -i 's/is_long_penalty=config.reward_model.get("is_long_penalty", False),is_binary_reward=config.reward_model.get("is_binary_reward", True), is_power4_reward=config.reward_model.get("is_power4_reward", False)//' /home/ubuntu/deploy-projects/0da75108a9d80495a5f2a7ef/verl/trainer/main_ppo.py

# Default command - will be overridden by docker-compose or command line
CMD ["python", "-m", "verl.trainer.main_ppo", "--help"]