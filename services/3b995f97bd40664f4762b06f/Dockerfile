FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl make default-jdk-headless && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .

RUN pip install --no-cache-dir -e .

COPY pyproject.toml .

COPY web.py .

COPY . .

RUN python tools/sort_definitions.py bricksrc/definitions.csv && \
    sed -i 's/offline=True/offline=False/' bricksrc/env.py

CMD ["sh", "-c", "make && python web.py"]