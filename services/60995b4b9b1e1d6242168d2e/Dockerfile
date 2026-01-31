FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl git wget && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/60995b4b9b1e1d6242168d2e

COPY requirements.txt .
RUN pip install --no-cache-dir 'numpy<2' pillow --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir tensorboard huggingface_hub pytz transformers typed-argument-parser flask

COPY . .

RUN git init && git config user.email "train@example.com" && git config user.name "Training" && git add -A && git commit -m "init" 2>/dev/null || true

CMD ["python", "train.py"]