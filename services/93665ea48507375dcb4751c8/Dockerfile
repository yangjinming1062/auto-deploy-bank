FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/93665ea48507375dcb4751c8

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add Flask to requirements
RUN echo "flask" >> requirements.txt && pip install --no-cache-dir flask

# Copy application code
COPY . .

EXPOSE 40434

CMD ["python", "app.py"]