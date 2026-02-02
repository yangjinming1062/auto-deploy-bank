FROM python:3.12-slim

LABEL maintainer=["Muhammad Ahmad <ahmadshaukat_4@outlook.com>"]

WORKDIR /code

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY agent-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agent-service/ .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
