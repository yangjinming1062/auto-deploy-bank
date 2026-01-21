FROM python:3.12-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/c7675a71bf1feb8ece64da97

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install local agentforge package in editable mode
RUN pip install --no-cache-dir -e .

# Download spacy model
RUN python -m spacy download en_core_web_sm

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]