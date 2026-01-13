FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /chroma

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir chroma-hnswlib

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "chromadb.app:app", "--workers", "1", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--timeout-keep-alive", "30"]