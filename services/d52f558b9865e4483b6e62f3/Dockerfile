FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies for PyTorch and healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/d52f558b9865e4483b6e62f3

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create startup script
RUN echo '#!/bin/bash\n\
export PYTHONPATH="${PYTHONPATH:-/home/ubuntu/deploy-projects/d52f558b9865e4483b6e62f3}"\n\
# Use demo app if no model provided, otherwise use the full gradio webserver\n\
if [ -z "${MODEL_NAME_OR_PATH}" ]; then\n\
    echo "Starting in demo mode. Set MODEL_NAME_OR_PATH for full functionality."\n\
    python /home/ubuntu/deploy-projects/d52f558b9865e4483b6e62f3/demo_app.py\n\
else\n\
    echo "Starting with model: ${MODEL_NAME_OR_PATH}"\n\
    python server/gradio_webserver.py --model_name_or_path "${MODEL_NAME_OR_PATH}" --load_8bit --no_cuda\n\
fi\n' > /start.sh && chmod +x /start.sh

EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

CMD ["/start.sh"]