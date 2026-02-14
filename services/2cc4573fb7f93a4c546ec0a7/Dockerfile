FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# Install ffmpeg for audio processing (librosa, pydub)
# Install curl for healthcheck
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/2cc4573fb7f93a4c546ec0a7

# Install build dependencies first
RUN pip install --no-cache-dir wheel setuptools

# Copy pyproject.toml and install package in editable mode
COPY pyproject.toml .
COPY vibevoice/ ./vibevoice/
COPY vllm_plugin/ ./vllm_plugin/
RUN pip install --no-cache-dir -e .

# Copy remaining files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY demo/ ./demo/

EXPOSE 8000

CMD ["uvicorn", "demo.web.app:app", "--host", "0.0.0.0", "--port", "8000"]