FROM python:3.11-slim

WORKDIR /usr/src/app

ARG RERANKER_MODEL

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install "huggingface_hub>=0.20.0"
RUN python -c "from huggingface_hub import HfApi; HfApi().snapshot_download(repo_id='$RERANKER_MODEL', repo_type='model')"
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV PORT 8000
ENV CURRENT_HOST 0.0.0.0
ENV WORKERS 1

CMD ["sh", "-c", "uvicorn app:app --loop asyncio --reload --workers ${WORKERS} --host $CURRENT_HOST --port $PORT --proxy-headers"]