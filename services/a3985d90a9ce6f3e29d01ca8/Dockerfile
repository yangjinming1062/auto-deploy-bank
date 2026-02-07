FROM python:3.11-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY indexer/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY indexer/ ./indexer/

WORKDIR /usr/src/app/indexer

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/src/app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]