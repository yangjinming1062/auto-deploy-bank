FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/8fe856d4bed85f031b5ffe1a

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml .
COPY composeml ./composeml
RUN pip install --no-cache-dir -e .

COPY app.py .

EXPOSE 41164

CMD ["python", "app.py"]