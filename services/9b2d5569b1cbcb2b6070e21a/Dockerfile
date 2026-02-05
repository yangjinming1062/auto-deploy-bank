FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl libgomp1 && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/9b2d5569b1cbcb2b6070e21a

COPY requirements.txt .
COPY setup.py .

RUN pip install --no-cache-dir -r requirements.txt

COPY feature_selector ./feature_selector

RUN pip install --no-cache-dir -e .

COPY app.py .
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:40115/ || exit 1

CMD ["/entrypoint.sh"]