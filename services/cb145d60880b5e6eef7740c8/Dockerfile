FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/cb145d60880b5e6eef7740c8

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir aiohttp

COPY examples ./examples

EXPOSE 8080

CMD ["python", "examples/web_srv.py"]