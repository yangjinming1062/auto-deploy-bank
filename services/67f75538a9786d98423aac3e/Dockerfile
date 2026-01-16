FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/67f75538a9786d98423aac3e

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "web/run.py"]