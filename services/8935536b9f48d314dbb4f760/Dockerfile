FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    CUDA_GRAPHS=0 \
    PAYLOAD_LIMIT=8000000 \
    HF_TOKEN=${HF_TOKEN}

WORKDIR /home/ubuntu/deploy-projects/8935536b9f48d314dbb4f760

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy entire project first
COPY codes/ ./codes/

# Install project dependencies and package
RUN pip install --no-cache-dir \
    matplotlib>=3.10.3 \
    pillow>=11.2.1 \
    pyautogui>=0.9.54 \
    flask>=3.0.0 \
    && pip install --no-cache-dir ./codes

# Run tests and keep container alive
COPY test_runner.sh /usr/local/bin/test_runner.sh
COPY web_server.py /home/ubuntu/deploy-projects/8935536b9f48d314dbb4f760/web_server.py
RUN chmod +x /usr/local/bin/test_runner.sh

CMD ["/usr/local/bin/test_runner.sh"]