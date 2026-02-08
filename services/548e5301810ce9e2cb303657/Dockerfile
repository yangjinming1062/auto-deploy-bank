FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=. \
    HF_HOME=/root/.cache/huggingface

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/548e5301810ce9e2cb303657

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5050

CMD ["python", "vis_androidworld/vis_androidworld_trace.py", "--path", "/data", "--port", "5050"]