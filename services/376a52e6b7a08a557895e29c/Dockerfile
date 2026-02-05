FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY client/python/tests/integration/test_server/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY client/python/tests/integration/test_server/ ./test_server/

EXPOSE 8080

HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["uvicorn", "test_server.test_server:app", "--host", "0.0.0.0", "--port", "8080"]