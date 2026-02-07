FROM python:3.11-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV PORT 8000
ENV CURRENT_HOST 0.0.0.0
ENV WORKERS=1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]