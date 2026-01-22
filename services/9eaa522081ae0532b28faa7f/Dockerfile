FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY root-requirements.txt .
RUN pip install --no-cache-dir -r root-requirements.txt

COPY . .

CMD ["python", "app.py"]