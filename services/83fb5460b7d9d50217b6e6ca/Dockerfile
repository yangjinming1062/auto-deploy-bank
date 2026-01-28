FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/83fb5460b7d9d50217b6e6ca

# Install curl, git, and build tools for compiling Python packages
RUN apt-get update && apt-get install -y curl git build-essential && rm -rf /var/lib/apt/lists/*

# Install torch first (required by flash-attn)
RUN pip install --no-cache-dir torch==1.13.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Copy requirements and install dependencies (excluding flash-attn which requires CUDA)
COPY requirements.txt .
RUN sed -i '/^flash-attn/d' requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set PYTHONPATH for imports (point to DTE-FDM where llava package is located)
ENV PYTHONPATH=/home/ubuntu/deploy-projects/83fb5460b7d9d50217b6e6ca/DTE-FDM

# Expose the Gradio port (default 7860)
EXPOSE 7860

# Create start script
RUN echo '#!/bin/bash\n\
echo "Starting mock controller on port 21001..."\n\
python DTE-FDM/mock_controller.py &\n\
CONTROLLER_PID=$!\n\
sleep 2\n\
echo "Starting Gradio web server on port 7860..."\n\
python DTE-FDM/llava/serve/gradio_web_server.py --host 0.0.0.0 --port 7860\n\
wait $CONTROLLER_PID' > /home/ubuntu/deploy-projects/83fb5460b7d9d50217b6e6ca/start.sh && chmod +x /home/ubuntu/deploy-projects/83fb5460b7d9d50217b6e6ca/start.sh

# Run both services
CMD ["/home/ubuntu/deploy-projects/83fb5460b7d9d50217b6e6ca/start.sh"]