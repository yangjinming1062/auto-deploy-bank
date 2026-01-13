FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install the mapproxy application from source
RUN pip install .

EXPOSE 8080

CMD ["mapproxy-util", "serve-develop", "docker/mapproxy-example.yaml", "--bind", "0.0.0.0:8080"]