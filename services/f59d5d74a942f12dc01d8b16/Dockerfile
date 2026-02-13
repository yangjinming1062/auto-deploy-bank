FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl git build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY hugginggpt/server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY hugginggpt/server/ .

EXPOSE 8004

CMD ["python", "awesome_chat.py", "--config", "configs/config.default.yaml", "--mode", "server"]