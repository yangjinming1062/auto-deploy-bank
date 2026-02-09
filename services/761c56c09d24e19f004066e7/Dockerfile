FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY login.html .
COPY test_auth.py .
COPY server.py .
COPY app/ ./app/

EXPOSE 5006

CMD ["python", "server.py"]