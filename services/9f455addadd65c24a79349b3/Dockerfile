# Root Dockerfile for ML-ProjectKart
# This file exists for compatibility purposes.
# Actual builds use the subdirectory context via docker-compose.yaml
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
EXPOSE 5000
CMD ["python", "-c", "print('Use docker-compose to run specific projects')"]