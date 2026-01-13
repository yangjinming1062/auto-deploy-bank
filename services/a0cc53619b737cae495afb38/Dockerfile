FROM python:3.10-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]