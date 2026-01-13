FROM python:3.10-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir "skypilot[all]" fastapi "uvicorn[standard]"

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/app"

ENV PYTHONUNBUFFERED=1
ENV SKYPILOT_DEV=False
ENV SKYPILOT_DEBUG=False
ENV SKYPILOT_DISABLE_USAGE_COLLECTION=False
ENV SKYPILOT_MINIMIZE_LOGGING=True
ENV SKYPILOT_SKIP_CLOUD_IDENTITY_CHECK=False

CMD ["python", "examples/serve/http_server/server.py", "--port", "8000"]
